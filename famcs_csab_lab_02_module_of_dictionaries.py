import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QHBoxLayout, QFileDialog, QTableWidgetItem, QCheckBox, QComboBox


class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.dictionary_data = []
        self.current_dictionary_name = "no dictionary is selected"
        self.number_of_columns_in_table = 0

        self.dictionaries_headers = {'renters': ['name', 'address', 'passport id', "driver's license"],
                                     'rent contracts': ['renter name', 'car number', 'rent starting date',
                                                        'rent ending date', 'cost']}
        self.items = 0
        self.setFixedSize(1080, 800)

        self.combo = QComboBox(self)
        self.combo.addItems(self.dictionaries_headers)

        # layout 1 for showing table of dictionary
        self.dictionary_layout = QTableWidget()  # создаём таблицу для оттображения данных из файла
        self.dictionary_layout.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dictionary_layout.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dictionary_layout.setFixedSize(800, 758)

        self.entry_form_layout = QVBoxLayout()
        # кнопки
        self.button_delete_row = QPushButton('delete row')  # выход
        self.button_delete_row.setFixedSize(200, 28)

        self.button_add_row = QPushButton('add row')  # выход
        self.button_add_row.setFixedSize(200, 28)

        self.button_edit_row = QPushButton('edit row')  # выход
        self.button_edit_row.setFixedSize(200, 28)

        self.button_enter = QPushButton('enter')  # выход
        self.button_enter.setFixedSize(200, 28)

        self.button_quit = QPushButton('exit')  # выход
        self.button_quit.setFixedSize(200, 28)

        self.renter_name = QLineEdit()
        self.renter_name.setFixedSize(200, 28)

        self.renter_surname = QLineEdit()
        self.renter_surname.setFixedSize(200, 28)

        self.renter_patronymic = QLineEdit()
        self.renter_patronymic.setFixedSize(200, 28)

        self.renter_address = QLineEdit()
        self.renter_address.setFixedSize(200, 28)

        self.renter_passport_id = QLineEdit()
        self.renter_passport_id.setFixedSize(200, 28)

        self.renter_drivers_license_number = QLineEdit()
        self.renter_drivers_license_number.setFixedSize(200, 28)

        self.enter_error = QLineEdit()  # вывод ошибок
        self.set_base_input_form_layout()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dictionary_layout)
        self.layout.setAlignment(self.dictionary_layout, Qt.AlignTop)
        self.layout.addLayout(self.entry_form_layout)
        self.layout.setAlignment(self.entry_form_layout, Qt.AlignTop)
        self.setLayout(self.layout)
        self.combo.activated[str].connect(self.choose_dictionary)
        self.button_add_row.clicked.connect(self.add_row)
        self.button_quit.clicked.connect(lambda: application_window.quit())
        # self.bank_code.textChanged[str].connect(self.check_disable)

    def set_base_input_form_layout(self):
        self.enter_error.setFixedSize(200, 28)
        self.enter_error.setText("No errors yet !")
        self.enter_error.setEnabled(False)
        self.entry_form_layout.setSpacing(9)
        self.entry_form_layout.addWidget(self.combo)
        self.entry_form_layout.addWidget(self.button_delete_row)
        self.entry_form_layout.addWidget(self.button_add_row)
        self.entry_form_layout.addWidget(self.button_edit_row)
        self.entry_form_layout.addWidget(self.button_quit)

    def set_add_input_form_layout(self):
        self.set_base_input_form_layout()
        self.entry_form_layout.addWidget(QLabel('renter name :'))
        self.entry_form_layout.addWidget(self.renter_name)

        self.entry_form_layout.addWidget(QLabel('renter patronymic:'))
        self.entry_form_layout.addWidget(self.renter_patronymic)

        self.entry_form_layout.addWidget(QLabel('renter address :'))
        self.entry_form_layout.addWidget(self.renter_address)

        self.entry_form_layout.addWidget(QLabel('renter passport id :'))
        self.entry_form_layout.addWidget(self.renter_passport_id)

        self.entry_form_layout.addWidget(QLabel('renter drivers license_number :'))
        self.entry_form_layout.addWidget(self.renter_drivers_license_number)

        self.entry_form_layout.addWidget(self.button_enter)

    def choose_dictionary(self, dictionary_name):
        self.current_dictionary_name = dictionary_name
        self.set_base_table_view()

    def choose_row_in_dictionary(self):
        return self.dictionary_layout.selectionModel().currentIndex().row()

    def set_table_headers(self):
        headers = self.dictionaries_headers[self.current_dictionary_name]
        for header_index in range(len(headers)):
            header = QTableWidgetItem(headers[header_index])
            header.setTextAlignment(Qt.AlignCenter)
            self.dictionary_layout.setHorizontalHeaderItem(header_index, header)

    def set_base_table_view(self):
        self.dictionary_layout.clear()
        self.number_of_columns_in_table = len(self.dictionaries_headers[self.current_dictionary_name])
        self.dictionary_layout.setColumnCount(self.number_of_columns_in_table)
        self.dictionary_layout.show()
        self.set_table_headers()
        self.dictionary_layout.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dictionary_layout.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dictionary_layout.setAlternatingRowColors(True)

    def check_disable(self):
        if self.invoice_number.text() and self.payment_reference.text() and self.account_number.text() \
                and self.bank_code.text() and self.is_any_template_selected and self.items > 0:
            self.button_save_to_word.setEnabled(True)
        else:
            self.button_save_to_word.setEnabled(False)

    def add_row(self):
        self.set_add_input_form_layout()


class MainWindow(QMainWindow):  # создали окошко приложения
    def __init__(self, window_content):
        super().__init__()
        #  Добавить на форму ваши данные: ФИО, год, курс, группа.
        self.setWindowTitle("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа")
        self.setFixedSize(1080, 800)
        self.setCentralWidget(window_content)


if __name__ == '__main__':
    application_window = QApplication(sys.argv)
    content = ContentWindow()
    reporting_module_application_window = MainWindow(content)
    reporting_module_application_window.show()
    sys.exit(application_window.exec_())
