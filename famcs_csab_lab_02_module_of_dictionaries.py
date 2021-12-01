import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QHBoxLayout, QTableWidgetItem, QComboBox, QPlainTextEdit


class AddEditWindow(QWidget):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.entry_form_layout = QVBoxLayout()
        self.setFixedSize(230, 400)
        self.setLayout(self.entry_form_layout)


class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.add_or_edit_renter_window = None
        self.add_or_edit_rent_contract_window = None

        self.dictionary_data = []
        self.current_dictionary_name = "no dictionary is selected"
        self.number_of_columns_in_table = 0
        self.new_row_to_insert = []

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

        self.button_quit = QPushButton('exit')  # выход
        self.button_quit.setFixedSize(200, 28)

        self.enter_error = QLineEdit()  # вывод ошибок

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dictionary_layout)
        self.layout.setAlignment(self.dictionary_layout, Qt.AlignTop)
        self.layout.addLayout(self.entry_form_layout)
        self.layout.setAlignment(self.entry_form_layout, Qt.AlignTop)
        self.setLayout(self.layout)
        self.combo.activated[str].connect(self.choose_dictionary)
        self.button_add_row.clicked.connect(self.show_add_or_edit_renter_window)
        self.button_quit.clicked.connect(lambda: application_window.quit())

        self.enter_error.setFixedSize(200, 28)
        self.enter_error.setText("No errors yet !")
        self.enter_error.setEnabled(False)
        self.entry_form_layout.setSpacing(9)
        self.entry_form_layout.addWidget(self.combo)
        self.entry_form_layout.addWidget(self.button_delete_row)
        self.entry_form_layout.addWidget(self.button_add_row)
        self.entry_form_layout.addWidget(self.button_edit_row)
        self.entry_form_layout.addWidget(self.button_quit)

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
        if self.add_or_edit_renter_window.renter_name.text() and self.add_or_edit_renter_window.renter_surname.text() \
                and self.add_or_edit_renter_window.renter_patronymic \
                and self.add_or_edit_renter_window.renter_address.text() \
                and self.add_or_edit_renter_window.renter_passport_id.text() \
                and self.add_or_edit_renter_window.renter_drivers_license_number.text():
            self.button_save_to_word.setEnabled(True)
        else:
            self.button_save_to_word.setEnabled(False)

    def add_row(self):
        self.dictionary_layout = self.entry_form_layout

    def show_add_or_edit_renter_window(self):
        self.dictionary_layout = self.entry_form_layout

    def show_add_or_edit_rent_contract_window(self):

        if self.add_or_edit_renter_window is None:
            self.add_or_edit_renter_window = AddEditWindow("Add New Renter")

            self.add_or_edit_renter_window.renter_name = QLineEdit()
            self.add_or_edit_renter_window.renter_name.setFixedSize(200, 28)

            self.add_or_edit_renter_window.renter_surname = QLineEdit()
            self.add_or_edit_renter_window.renter_surname.setFixedSize(200, 28)

            self.add_or_edit_renter_window.renter_patronymic = QLineEdit()
            self.add_or_edit_renter_window.renter_patronymic.setFixedSize(200, 28)

            self.add_or_edit_renter_window.renter_address = QPlainTextEdit()
            self.add_or_edit_renter_window.renter_address.setFixedSize(200, 48)

            self.add_or_edit_renter_window.renter_passport_id = QLineEdit()
            self.add_or_edit_renter_window.renter_passport_id.setFixedSize(200, 28)

            self.add_or_edit_renter_window.renter_drivers_license_number = QLineEdit()
            self.add_or_edit_renter_window.renter_drivers_license_number.setFixedSize(200, 28)

            self.add_or_edit_renter_window.entry_form_layout.setSpacing(9)
            self.add_or_edit_renter_window.entry_form_layout.addWidget(QLabel('name :'))
            self.add_or_edit_renter_window.entry_form_layout.addWidget(self.add_or_edit_renter_window.renter_name)

            self.add_or_edit_renter_window.entry_form_layout.addWidget(QLabel('patronymic:'))
            self.add_or_edit_renter_window.entry_form_layout.addWidget(self.add_or_edit_renter_window.renter_patronymic)

            self.add_or_edit_renter_window.entry_form_layout.addWidget(QLabel('address :'))
            self.add_or_edit_renter_window.entry_form_layout.addWidget(self.add_or_edit_renter_window.renter_address)

            self.add_or_edit_renter_window.entry_form_layout.addWidget(QLabel('passport id :'))
            self.add_or_edit_renter_window.entry_form_layout.addWidget(
                self.add_or_edit_renter_window.renter_passport_id)

            self.add_or_edit_renter_window.entry_form_layout.addWidget(QLabel('drivers license_number :'))
            self.add_or_edit_renter_window.entry_form_layout.addWidget(
                self.add_or_edit_renter_window.renter_drivers_license_number)

            self.add_or_edit_renter_window.button_enter = QPushButton('enter')
            self.add_or_edit_renter_window.button_enter.setFixedSize(200, 28)
            self.add_or_edit_renter_window.entry_form_layout.addWidget(self.add_or_edit_renter_window.button_enter)
            # self.bank_code.textChanged[str].connect(self.check_disable)
        self.add_or_edit_renter_window.show()


class MainWindow(QMainWindow):  # создали окошко приложения
    def __init__(self, window_content):
        super().__init__()
        self.setWindowTitle("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа")
        self.setFixedSize(1080, 800)
        self.setCentralWidget(window_content)


if __name__ == '__main__':
    application_window = QApplication(sys.argv)
    content = ContentWindow()
    reporting_module_application_window = MainWindow(content)
    reporting_module_application_window.show()
    sys.exit(application_window.exec_())
