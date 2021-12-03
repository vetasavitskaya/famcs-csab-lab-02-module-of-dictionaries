'''
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_new_record_window = AnotherWindow()
        self.edit_record_window = AnotherWindow()

        form_layout = QVBoxLayout()

        button_add_new_record = QPushButton("add new record")
        button_edit_record = QPushButton("edit record")

        button_add_new_record.clicked.connect(lambda checked: self.toggle_window(self.add_new_record_window))
        button_edit_record.clicked.connect(lambda checked: self.toggle_window(self.edit_record_window))

        form_layout.addWidget(button_edit_record)
        form_layout.addWidget(button_add_new_record)
        w = QWidget()
        w.setLayout(form_layout)
        self.setCentralWidget(w)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            window.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()'''
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QHBoxLayout, QFileDialog, QTableWidgetItem, QCheckBox, QComboBox


class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []

        self.setFixedSize(1000, 620)

        self.dictionary_names = ['renters', 'rent contracts']
        self.renters_table_headers = ['name', 'surname', 'patronymic', 'address', 'passport id', "driver's license"]
        self.rent_contracts_table_headers = ['car number', 'rent starting date', 'rent ending date', 'cost']

        self.dictionary_content_layout = QTableWidget()

        self.dictionary_content_layout.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dictionary_content_layout.setColumnCount(4)

        self.dictionary_content_layout.show()
        self.dictionary_content_layout.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.dictionary_content_layout.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dictionary_content_layout.setFixedSize(700, 580)

        self.form_layout = QVBoxLayout()

        self.choice_of_the_dictionary = QComboBox(self)
        self.choice_of_the_dictionary.addItems(self.dictionary_names)
        self.choice_of_the_dictionary.setFixedSize(200, 28)
        self.choice_of_the_dictionary.currentIndexChanged.connect(self.set_table_layout)

        self.enter_error = QLineEdit()  # вывод ошибок
        self.enter_error.setFixedSize(200, 28)
        self.enter_error.setText("No errors yet !")
        self.enter_error.setEnabled(False)

        # кнопки
        self.button_quit = QPushButton('exit')  # выход
        self.button_quit.setFixedSize(200, 28)

        self.form_layout.addWidget(self.choice_of_the_dictionary)

        self.form_layout.setSpacing(9)
        self.form_layout.addWidget(QLabel('Error :'))
        self.form_layout.addWidget(self.enter_error)

        self.form_layout.addWidget(self.button_quit)
        self.set_table_layout()

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.dictionary_content_layout)
        self.layout.setAlignment(self.dictionary_content_layout, Qt.AlignTop)

        self.layout.addLayout(self.form_layout)
        self.layout.setAlignment(self.form_layout, Qt.AlignTop)

        self.setLayout(self.layout)

        self.button_quit.clicked.connect(lambda: application_window.quit())

    def set_table_layout(self):
        if self.choice_of_the_dictionary.currentText() == 'renters':
            self.dictionary_content_layout.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.dictionary_content_layout.setColumnCount(len(self.renters_table_headers))

            for counter in range(len(self.renters_table_headers)):
                header = QTableWidgetItem(self.renters_table_headers[counter])
                header.setTextAlignment(Qt.AlignCenter)

                self.dictionary_content_layout.setHorizontalHeaderItem(counter, header)

        if self.choice_of_the_dictionary.currentText() == 'rent contracts':
            self.dictionary_content_layout.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.dictionary_content_layout.setColumnCount(len(self.rent_contracts_table_headers))

            for counter in range(len(self.rent_contracts_table_headers)):
                header = QTableWidgetItem(self.rent_contracts_table_headers[counter])
                header.setTextAlignment(Qt.AlignCenter)

                self.dictionary_content_layout.setHorizontalHeaderItem(counter, header)


class MainWindow(QMainWindow):  # создали окошко приложения
    def __init__(self, window_content):
        super().__init__()
        #  Добавить на форму ваши данные: ФИО, год, курс, группа.
        self.setWindowTitle("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа")
        self.setFixedSize(1000, 620)
        self.setCentralWidget(window_content)


if __name__ == '__main__':
    application_window = QApplication(sys.argv)
    content = ContentWindow()
    reporting_module_application_window = MainWindow(content)
    reporting_module_application_window.show()
    sys.exit(application_window.exec_())