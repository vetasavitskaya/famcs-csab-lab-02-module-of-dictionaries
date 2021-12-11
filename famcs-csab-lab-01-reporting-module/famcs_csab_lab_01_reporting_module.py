import os
import random as rnd
import subprocess
import sys
from datetime import date
from operator import itemgetter
import docx
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QHBoxLayout, QFileDialog, QTableWidgetItem, QCheckBox
from docx.shared import Inches
from mailmerge import MailMerge


def sort_dates(date_item):
    date_item_parts = date_item[2].split('.')[::-1]
    return date(int(date_item_parts[0]), int(date_item_parts[1]), int(date_item_parts[2]))


class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.random_product_names = ["IdeaPad Slim 3i Chromebook", "IdeaPad Slim 3i", "IdeaPad Slim 5i", "Tab K10",
                                     "IdeaCentre 3 (AMD)", "Yoga Smart Tab", "Tab M10 FHD Plus", "Tab M10 HD",
                                     "Tab M10 FHD", "ThinkVision FHD Monitor", "ThinkPad E14 AMD",
                                     "Thinkbook 15 G2 ITL",
                                     "IdeaPad Gaming"]
        self.random_produced_by = ["Lenovo (Beijing) Limited", "Lenovo (Asia Pacific) Limited", "Lenovo (Belgium) BVBA",
                                   "Lenovo HK Services Limited", "Medion AG", "Motorola Mobility LLC",
                                   "NEC Personal Computers",
                                   "Stoneware, Inc."]
        #  Даты везде отображать только в формате ДД.ММ.ГГГГ.
        self.random_date_of_manufacture = ['01.01.2018', '01.02.2018', '01.03.2018', '01.04.2018', '01.05.2018',
                                           '01.06.2018', '01.07.2018', '01.08.2018', '01.09.2018', '01.10.2018',
                                           '01.11.2018', '01.12.2018', '01.01.2019', '01.02.2019', '01.03.2019',
                                           '01.04.2019', '01.05.2019', '01.06.2019', '01.07.2019', '01.08.2019',
                                           '01.09.2019', '01.10.2019', '01.11.2019', '01.12.2019', '01.01.2020',
                                           '01.02.2020', '01.03.2020', '01.04.2020', '01.05.2020', '01.06.2020',
                                           '01.07.2020', '01.08.2020', '01.09.2020', '01.10.2020', '01.11.2020',
                                           '01.12.2020', '01.01.2021', '01.02.2021', '01.03.2021', '01.04.2021',
                                           '01.05.2021', '01.06.2021', '01.07.2021', '01.08.2021', '01.09.2021',
                                           '01.10.2021', '01.11.2021', '01.12.2020']
        self.random_product_names_size = len(self.random_product_names)
        self.random_produced_by_size = len(self.random_produced_by)
        self.random_date_of_manufacture_size = len(self.random_date_of_manufacture)
        self.data_limit = min(self.random_product_names_size, self.random_produced_by_size,
                              self.random_date_of_manufacture_size)
        self.data = []
        self.current_template_name = "no template is selected"
        self.is_any_template_selected = False
        self._is_sorted_in_ascending_order = False
        self._is_sorted_in_descending_order = False
        self.number_of_rows_in_table_int = 0
        self.items = 0
        self.setFixedSize(900, 800)
        #  Создать на форме таблицу с таким же количеством, порядком, названиями колонок, как и в шаблоне документа
        #  Word. Шрифт, цвет и начертание – на ваше усмотрение.
        self.amazon_invoice_layout = QTableWidget()  # создаём таблицу для оттображения данных из файла
        self.amazon_invoice_layout.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.amazon_invoice_layout.setColumnCount(4)  # количество колонок в таблице
        self.set_table_header()

        self.amazon_invoice_layout.show()
        self.amazon_invoice_layout.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.amazon_invoice_layout.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.amazon_invoice_layout.setFixedSize(600, 758)

        self.form_layout = QVBoxLayout()  # форма для ввода новых данных
        self.number_of_rows_in_table = QLineEdit()  # количество записей в таблице
        self.number_of_rows_in_table.setFixedSize(200, 28)

        #  Создать поля для ввода информации, которые потом будут переноситься в «места для заполнения»
        #  шаблона-документа Word.
        self.invoice_number = QLineEdit()
        self.invoice_number.setFixedSize(200, 28)
        self.payment_reference = QLineEdit()
        self.payment_reference.setFixedSize(200, 28)
        self.account_number = QLineEdit()
        self.account_number.setFixedSize(200, 28)
        self.bank_code = QLineEdit()
        self.bank_code.setFixedSize(200, 28)

        self.enter_error = QLineEdit()  # вывод ошибок
        self.enter_error.setFixedSize(200, 28)
        self.enter_error.setText("No errors yet !")
        self.enter_error.setEnabled(False)

        # кнопки
        self.button_open_template = QPushButton('open template')  # загрузить шаблон
        self.button_open_template.setFixedSize(200, 28)
        self.button_generate_table = QPushButton('generate')
        # выбрать колонку по которой будем сортировать
        self.checkbox_by_product_name = QCheckBox('Sort by Product Name', self)
        self.checkbox_produced_by = QCheckBox('Sort by Produced By', self)
        self.checkbox_manufacture_date = QCheckBox('Sort by Manufacture Date', self)
        self.checkbox_cost = QCheckBox('Sort by Cost', self)

        self.button_sort_in_ascending_order = QPushButton('sort in ascending order')
        self.button_sort_in_ascending_order.setFixedSize(200, 28)
        self.button_sort_in_descending_order = QPushButton('sort in descending order')
        self.button_sort_in_descending_order.setFixedSize(200, 28)
        self.button_save_to_word = QPushButton('save file')  # сохранить результат в word
        self.button_save_to_word.setFixedSize(200, 28)
        self.button_quit = QPushButton('exit')  # выход
        self.button_quit.setFixedSize(200, 28)

        self.button_save_to_word.setEnabled(False)  # не отображать сохранение пока всё не заполнено

        self.template_label = QLineEdit()  # название шаблона

        self.template_label.setFixedSize(200, 28)
        self.template_label.setText(self.current_template_name)
        self.template_label.setEnabled(False)
        self.form_layout.addWidget(self.template_label)
        self.form_layout.addWidget(self.button_open_template)

        self.form_layout.addWidget(QLabel('Set number of rows in table :'))
        self.form_layout.addWidget(self.number_of_rows_in_table)
        self.form_layout.addWidget(self.button_generate_table)

        self.form_layout.addWidget(self.checkbox_by_product_name)
        self.form_layout.addWidget(self.checkbox_produced_by)
        self.form_layout.addWidget(self.checkbox_manufacture_date)
        self.form_layout.addWidget(self.checkbox_cost)

        self.form_layout.addWidget(self.button_sort_in_ascending_order)
        self.form_layout.addWidget(self.button_sort_in_descending_order)

        self.form_layout.setSpacing(9)
        self.form_layout.addWidget(QLabel('Invoice number : '))
        self.form_layout.addWidget(self.invoice_number)

        self.form_layout.addWidget(QLabel('Payment Reference :'))
        self.form_layout.addWidget(self.payment_reference)

        self.form_layout.addWidget(QLabel('Account Number :'))
        self.form_layout.addWidget(self.account_number)

        self.form_layout.addWidget(QLabel('Bank/Sort Code :'))
        self.form_layout.addWidget(self.bank_code)

        self.form_layout.addWidget(QLabel('Error :'))
        self.form_layout.addWidget(self.enter_error)

        self.form_layout.addWidget(self.button_save_to_word)
        self.form_layout.addWidget(self.button_quit)

        self.layout = QHBoxLayout()  # собираем все элементы интерфейса вместе
        self.layout.addWidget(self.amazon_invoice_layout)
        self.layout.setAlignment(self.amazon_invoice_layout, Qt.AlignTop)
        self.layout.addLayout(self.form_layout)
        self.layout.setAlignment(self.form_layout, Qt.AlignTop)
        self.setLayout(self.layout)

        self.button_open_template.clicked.connect(self.open_template)
        self.button_generate_table.clicked.connect(self.generate_data)
        self.button_sort_in_ascending_order.clicked.connect(self.sort_table_in_ascending_order)
        self.button_sort_in_descending_order.clicked.connect(self.sort_table_in_descending_order)
        self.button_save_to_word.clicked.connect(self.save_to_word)
        self.button_quit.clicked.connect(lambda: application_window.quit())

        self.invoice_number.textChanged[str].connect(self.check_disable)
        self.payment_reference.textChanged[str].connect(self.check_disable)
        self.account_number.textChanged[str].connect(self.check_disable)
        self.bank_code.textChanged[str].connect(self.check_disable)

    #  Выравнивание в столбцах повторить как в шаблоне документа, т.е. текст по левому краю или ширине, даты –
    #  посередине, числа – по правому краю.
    def set_table_header(self):
        product_name_header = QTableWidgetItem('Product Name')
        product_name_header.setTextAlignment(Qt.AlignLeft)
        self.amazon_invoice_layout.setHorizontalHeaderItem(0, product_name_header)

        produced_by_header = QTableWidgetItem('Produced By')
        produced_by_header.setTextAlignment(Qt.AlignLeft)
        self.amazon_invoice_layout.setHorizontalHeaderItem(1, produced_by_header)

        manufacture_date_header = QTableWidgetItem('Manufacture Date')
        manufacture_date_header.setTextAlignment(Qt.AlignCenter)
        self.amazon_invoice_layout.setHorizontalHeaderItem(2, manufacture_date_header)

        Cost = QTableWidgetItem('Cost')
        Cost.setTextAlignment(Qt.AlignRight)
        self.amazon_invoice_layout.setHorizontalHeaderItem(3, Cost)

    def open_template(self):  # выбор шаблона word
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #  (требование для десктопных приложений) при открытии окна для выбора шаблона по умолчанию обязательно
        #  предлагать текущую папку откуда запущено приложение или где лежит шаблон
        #  Создать возможность вызова диалогового окна для выбора на диске созданного файла шаблона Word. Обеспечить
        #  фильтрацию выбора только файлов (.dotx и .docx).
        file_name, _ = QFileDialog.getOpenFileName(self.window(), "Open Word Template File", os.path.abspath(os.curdir),
                                                   "(*.docx *.dotx)", options=options)
        if file_name and file_name.endswith('docx'):
            self.current_template_name = str(file_name)
            self.template_label.setText(self.current_template_name[self.current_template_name.rfind('/') + 1:])
            self.is_any_template_selected = True
            self.enter_error.setText("No errors yet !")
        else:
            self.is_any_template_selected = False
            self.current_template_name = "no template is selected"
            self.template_label.setText(self.current_template_name)

    def generate_date_row_item(self):  # генерируем данные для заполнения одной строки таблицы
        return [rnd.choice(self.random_product_names), rnd.choice(self.random_produced_by),
                #  Числовые данные генерировать разной длины (т.е. чтобы можно было протестировать сортировку
                #  “как числа” в пункте 8 ниже).
                rnd.choice(self.random_date_of_manufacture), round(rnd.uniform(100.00, 1000.00, ), 2)]

    #  Обеспечить сортировку данных в колонках таблицы по возрастанию и убыванию, при этом текст должен сортировать как
    #  текст, даты – как даты, а числа – как числа.
    def sort_table_in_ascending_order(self):
        if self.is_any_template_selected:
            if self.items >= 1:
                if self.checkbox_by_product_name.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(0))
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_produced_by.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(1))
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_manufacture_date.checkState() == 2:
                    self.data = sorted(self.data, key=sort_dates)
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_cost.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(3))
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_by_product_name.checkState() == 0 and self.checkbox_produced_by.checkState() == 0 \
                        and self.checkbox_manufacture_date.checkState() == 0 and self.checkbox_cost.checkState() == 0:
                    self.enter_error.setText("Choose variant of sort !")
                self.fill_table()
            else:
                self.enter_error.setText("Table is empty !")
        else:
            self.enter_error.setText("No template is selected !")

    def sort_table_in_descending_order(self):
        if self.is_any_template_selected:
            if self.items >= 1:
                if self.checkbox_by_product_name.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(0), reverse=True)
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_produced_by.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(1), reverse=True)
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_manufacture_date.checkState() == 2:
                    self.data = sorted(self.data, key=sort_dates, reverse=True)
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_cost.checkState() == 2:
                    self.data = sorted(self.data, key=itemgetter(3), reverse=True)
                    self.enter_error.setText("No errors yet !")
                if self.checkbox_by_product_name.checkState() == 0 and self.checkbox_produced_by.checkState() == 0 \
                        and self.checkbox_manufacture_date.checkState() == 0 and self.checkbox_cost.checkState() == 0:
                    self.enter_error.setText("Choose variant of sort !")
                self.fill_table()
            else:
                self.enter_error.setText("Table is empty !")
        else:
            self.enter_error.setText("No template is selected !")

    def generate_data(self):  # генерируем данные для заполнения таблицы
        self.data = []  # удаляем старые данные из таблицы
        self.items = 0  # сбрасываем количество строк в таблице
        if self.is_any_template_selected:  # если выбран шаблон
            try:
                if int(self.number_of_rows_in_table.text()) >= 1:  # и если число строк таблицы валидное
                    self.number_of_rows_in_table_int = int(self.number_of_rows_in_table.text())
                    for _ in range(self.number_of_rows_in_table_int):
                        self.data.append(self.generate_date_row_item())
                        self.items += 1
                    self.fill_table()
                    self.enter_error.setText("No errors yet !")
                else:
                    self.enter_error.setText("Wrong number of rows!")
            except ValueError:
                self.enter_error.setText("Wrong number of rows type!")
        else:
            self.enter_error.setText("No template is selected !")

    #  Создать действие (кнопку, ссылку, …) для заполнения (перезаполнения) на экране задаваемого пользователем
    #  количества строк таблицы. Данные в таблице генерировать любые случайные, но все строки должны быть разными.
    #  Создать действие (кнопку, ссылку, …) для заполнения (перезаполнения) на экране задаваемого пользователем
    #  количества строк таблицы. Данные в таблице генерировать любые случайные, но все строки должны быть разными.
    def fill_table(self):
        self.amazon_invoice_layout.clear()
        self.amazon_invoice_layout.setRowCount(self.items)
        self.amazon_invoice_layout.setColumnCount(4)
        self.set_table_header()
        self.amazon_invoice_layout.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.amazon_invoice_layout.setAlternatingRowColors(True)
        for row in range(self.items):
            #  Выравнивание в столбцах повторить как в шаблоне документа, т.е. текст по левому краю или ширине, даты –
            #  посередине, числа – по правому краю.
            product_name_item = QTableWidgetItem(self.data[row][0])
            self.amazon_invoice_layout.setItem(row, 0, product_name_item)

            produced_by_item = QTableWidgetItem(self.data[row][1])
            self.amazon_invoice_layout.setItem(row, 1, produced_by_item)

            date_of_manufacture_item = QTableWidgetItem(self.data[row][2])
            date_of_manufacture_item.setTextAlignment(Qt.AlignHCenter)
            self.amazon_invoice_layout.setItem(row, 2, date_of_manufacture_item)

            cost_item = QTableWidgetItem(str(self.data[row][3]))
            cost_item.setTextAlignment(Qt.AlignRight)
            self.amazon_invoice_layout.setItem(row, 3, cost_item)

    def check_disable(self):
        if self.invoice_number.text() and self.payment_reference.text() and self.account_number.text() \
                and self.bank_code.text() and self.is_any_template_selected and self.items > 0:
            self.button_save_to_word.setEnabled(True)
        else:
            self.button_save_to_word.setEnabled(False)

    #  Создать кнопку (ссылку) «Создать документ». По нажатию должен открыться документ Word на основе выбранного
    #  шаблона. На данном шаге его заполнение не требуется.
    #  Автоматизировать экспорт данных с экранной формы в «места для заполнения» документа Microsoft Word.
    #  Автоматизировать заполнение таблицы в документе сгенерированными на экране данными.
    def save_to_word(self):
        try:
            #  17 Увеличить во всем документе абзацный отступ
            template_doc = MailMerge(self.current_template_name)
            template_doc.merge(
                invoice_number=self.invoice_number.text(),
                payment_reference=self.payment_reference.text(),
                account_number=self.account_number.text(),
                bank_code=self.bank_code.text()
            )
            data_to_write_in_word_table = []
            for row in self.data:
                data_to_write_in_word_table.append({'product_name': row[0], 'produced': row[1],
                                                    'date_of_manufacture': row[2], 'cost': str(row[3])})
            template_doc.merge_rows('product_name', data_to_write_in_word_table)
            result_file_name = self.current_template_name[:self.current_template_name.rfind('/') + 1] + 'result.docx'
            template_doc.write(result_file_name)
            template_doc.close()
            result_document = docx.Document(result_file_name)
            for paragraph in result_document.paragraphs:
                paragraph.paragraph_format.left_indent = Inches(0.6)
            result_document.save('result.docx')
            # Заполненный документ достаточно оставлять открытым на экране, т.е. его сохранение не требуется.
            #os.system('start ' + result_file_name)
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, result_file_name])
        except:
            self.enter_error.setText("Error while writing file !")


class MainWindow(QMainWindow):  # создали окошко приложения
    def __init__(self, window_content):
        super().__init__()
        #  Добавить на форму ваши данные: ФИО, год, курс, группа.
        self.setWindowTitle("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа")
        self.setFixedSize(900, 800)
        self.setCentralWidget(window_content)


if __name__ == '__main__':
    application_window = QApplication(sys.argv)
    content = ContentWindow()
    reporting_module_application_window = MainWindow(content)
    reporting_module_application_window.show()
    sys.exit(application_window.exec_())