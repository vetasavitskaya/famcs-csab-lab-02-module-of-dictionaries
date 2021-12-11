import decimal
import sys
from decimal import Decimal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QHBoxLayout, QComboBox, QPlainTextEdit


class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.signs_headers = ['+', '-', '*', '/']
        self.round_types_headers = ['математическое', 'бухгалтерское', 'усечение']

        self.is_calculated = False
        self.calculation_result = Decimal(0)

        self.setFixedSize(600, 280)

        self.formalization_nonsense = QHBoxLayout()
        self.calculation_layout = QHBoxLayout()  # layout для вычислений
        self.calculation_results_layout = QHBoxLayout()  # layout для выбора типа округления
        self.round_type_choice_layout = QHBoxLayout()  # layout для результатов вычислений
        self.entry_form_layout = QHBoxLayout()  # layout для кнопок и ошибок

        # выбор знака операции
        self.choice_of_the_first_sign = QComboBox(self)
        self.choice_of_the_first_sign.addItems(self.signs_headers)
        self.choice_of_the_first_sign.setFixedSize(48, 28)

        self.choice_of_the_second_sign = QComboBox(self)
        self.choice_of_the_second_sign.addItems(self.signs_headers)
        self.choice_of_the_second_sign.setFixedSize(48, 28)

        self.choice_of_the_third_sign = QComboBox(self)
        self.choice_of_the_third_sign.addItems(self.signs_headers)
        self.choice_of_the_third_sign.setFixedSize(48, 28)

        self.enter_error = QLineEdit()  # вывод ошибок
        self.enter_error.setStyleSheet("color: grey;")
        self.enter_error.setFixedSize(280, 28)
        self.enter_error.setText("No errors yet !")
        self.enter_error.setEnabled(False)

        # ввод чисел
        self.first_number_input = QLineEdit('0')
        self.first_number_input.setFixedSize(100, 28)

        self.second_number_input = QLineEdit('0')
        self.second_number_input.setFixedSize(100, 28)

        self.third_number_input = QLineEdit('0')
        self.third_number_input.setFixedSize(100, 28)

        self.fourth_number_input = QLineEdit('0')
        self.fourth_number_input.setFixedSize(100, 28)

        self.choice_of_the_round_type = QComboBox(self)
        self.choice_of_the_round_type.addItems(self.round_types_headers)
        self.choice_of_the_round_type.setFixedSize(200, 28)

        # вывод результатов
        self.calculation_results = QPlainTextEdit()
        self.calculation_results.setFixedSize(580, 100)

        # кнопки
        self.button_calculate = QPushButton('calculate') 
        self.button_calculate.setFixedSize(90, 28)

        self.button_add_round = QPushButton('add round')
        self.button_add_round.setFixedSize(90, 28)

        self.button_clear = QPushButton('clear')
        self.button_clear.setFixedSize(90, 28)

        self.button_quit = QPushButton('exit')  # выход
        self.button_quit.setFixedSize(90, 28)

        self.formalization_nonsense.addWidget(QLabel("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа"))

        self.calculation_layout.setSpacing(2)
        self.calculation_layout.addWidget(self.first_number_input)
        self.calculation_layout.addWidget(self.choice_of_the_first_sign)
        self.calculation_layout.addWidget(QLabel('('))
        self.calculation_layout.addWidget(self.second_number_input)
        self.calculation_layout.addWidget(self.choice_of_the_second_sign)
        self.calculation_layout.addWidget(self.third_number_input)
        self.calculation_layout.addWidget(QLabel(')'))
        self.calculation_layout.addWidget(self.choice_of_the_third_sign)
        self.calculation_layout.addWidget(self.fourth_number_input)
        self.calculation_layout.addWidget(QLabel('='))

        self.round_type_choice_layout.addWidget(self.choice_of_the_round_type)
        self.round_type_choice_layout.addWidget(self.button_add_round)

        self.calculation_results_layout.addWidget(self.calculation_results)

        self.entry_form_layout.setSpacing(10)
        self.entry_form_layout.addWidget(self.button_calculate)
        self.entry_form_layout.addWidget(self.button_clear)
        self.entry_form_layout.addWidget(self.button_quit)
        self.entry_form_layout.addWidget(self.enter_error)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.formalization_nonsense)
        self.layout.setAlignment(self.formalization_nonsense, Qt.AlignTop)

        self.layout.addLayout(self.calculation_layout)
        self.layout.setAlignment(self.calculation_layout, Qt.AlignHCenter)

        self.layout.addLayout(self.calculation_results_layout)
        self.layout.setAlignment(self.calculation_results_layout, Qt.AlignHCenter)

        self.layout.addLayout(self.round_type_choice_layout)
        self.layout.setAlignment(self.round_type_choice_layout, Qt.AlignHCenter)

        self.layout.addLayout(self.entry_form_layout)
        self.layout.setAlignment(self.entry_form_layout, Qt.AlignBottom)

        self.setLayout(self.layout)

        self.button_calculate.clicked.connect(self.calculation)
        self.button_clear.clicked.connect(self.clear)
        self.button_add_round.clicked.connect(self.add_round)
        self.button_quit.clicked.connect(lambda: application_window.quit())

    def mathematical_round(self, value):  # математическое округление
        return int(value + (Decimal(0.5) if value > Decimal(0.0) else Decimal(-0.5)))

    def accounting_round(self, value):  # бухгалтерское округление
        return round(value)

    def truncation_round(self, value):  # усечение
        return int(value)

    def addition_of_numbers(self, first_value, second_value):
        return Decimal(first_value + second_value)

    def difference_of_numbers(self, first_value, second_value):
        return Decimal(first_value - second_value)

    # Дополнить выбор операций «умножением» и «делением».
    def multiplication_of_numbers(self, first_value, second_value):
        return Decimal(first_value * second_value)

    # При делении округлять результат по правилам математики до 6 знаков после запятой.
    def division_of_numbers(self, first_value, second_value):
        division_result = Decimal(first_value / second_value)
        division_result = division_result.quantize(Decimal("1.0000000"))
        if str(division_result)[-1:] == '5':
            division_result += Decimal(0.0000005 if division_result > 0 else -0.0000005)
        return division_result.quantize(Decimal("1.000000"))

    # Все промежуточные вычисления всегда округлять до 10 знаков после запятой по правилам математического округления.
    def rounding_of_intermediate_operations(self, value):
        value = value.quantize(Decimal("1.00000000000"))
        if str(value)[-1:] == '5':
            value += Decimal(0.00000000005 if value > 0 else -0.00000000005)
        return value.quantize(Decimal("1.0000000000"))

    def operation_switch(self, sign, first_value, second_value):
        if sign == '+':
            return self.addition_of_numbers(first_value, second_value)
        elif sign == '-':
            return self.difference_of_numbers(first_value, second_value)
        elif sign == '*':
            return self.multiplication_of_numbers(first_value, second_value)
        elif sign == '/':
            return self.division_of_numbers(first_value, second_value)

    def convert_text_to_numbers(self, first_number_string_, second_number_string_, third_number_string_,
                                fourth_number_string_):
        first_number, second_number, third_number, fourth_number = 0, 0, 0, 0
        validity_of_all_numbers = True
        try:
            first_number, second_number, third_number, fourth_number = Decimal(first_number_string_), \
                Decimal(second_number_string_), Decimal(third_number_string_), Decimal(fourth_number_string_)
        except decimal.InvalidOperation:
            validity_of_all_numbers = False
            self.enter_error.setText("Invalid number !")
            self.enter_error.setStyleSheet("color: red;")
            self.clear()
        return validity_of_all_numbers, first_number, second_number, third_number, fourth_number

    def check_validity_of_number_format(self, number_string):
        if number_string[0] == '-':
            number_string = number_string[1:]
        if number_string.find('.') != -1:
            number_string = number_string[:number_string.find('.')]
        if number_string[0] == '0' and len(number_string) > 1 or number_string.find('e') != -1 \
                or number_string.find('E') != -1:
            return False
        if number_string.find(' ') == -1:
            return True
        else:
            number_string_parts = number_string.split(' ')
            if '' not in number_string_parts:
                if len(number_string_parts[0]) <= 3 and \
                        sum([len(number_string_parts[part_index]) for part_index in
                             range(1, len(number_string_parts))]) % 3 == 0:
                    return True
        return False

    def add_round(self):
        if self.is_calculated:
            previous_result = self.calculation_results.toPlainText() +'\n'
            if previous_result != '':
                selected_round_type = str(self.choice_of_the_round_type.currentText())
                if selected_round_type == 'математическое':
                    previous_result += 'математическое округление: ' + \
                        str(self.formatted_number_output(self.mathematical_round(self.calculation_result)))
                elif selected_round_type == 'бухгалтерское':
                    previous_result += 'бухгалтерское округление: ' + \
                        str(self.formatted_number_output(self.accounting_round(self.calculation_result)))
                elif selected_round_type == 'усечение':
                    previous_result += 'усечение: ' + \
                        str(self.formatted_number_output(self.truncation_round(self.calculation_result)))
                self.calculation_results.clear()
                self.calculation_results.insertPlainText(previous_result)

    def formatted_number_output(self, calculation_result_):
        # Целую часть числа обязательно отображать всегда в разбивке пробелами по тысячам, миллионам, миллиардам
        # в результате вычислений
        calculation_result_string_ = "{:,}".format(calculation_result_)
        if calculation_result_string_.find(".") != -1 and calculation_result_string_[-1] == '0':
            while calculation_result_string_[-1] == '0':
                calculation_result_string_ = calculation_result_string_[:-1]

        if calculation_result_string_[-1] == '.':
            calculation_result_string_ = calculation_result_string_[:-1]
        calculation_result_string_ = calculation_result_string_.replace(',', ' ')
        return calculation_result_string_

    def calculation(self):

        self.calculation_results.clear()
        self.is_calculated = False

        first_number_string, second_number_string, third_number_string, fourth_number_string = \
            self.first_number_input.text().replace(',', '.'), self.second_number_input.text().replace(',', '.'), \
            self.third_number_input.text().replace(',', '.'), self.fourth_number_input.text().replace(',', '.')

        if self.check_validity_of_number_format(first_number_string) and \
            self.check_validity_of_number_format(second_number_string) and \
            self.check_validity_of_number_format(third_number_string) and \
            self.check_validity_of_number_format(fourth_number_string):

            first_number_string, second_number_string, third_number_string, fourth_number_string = \
            first_number_string.replace(' ', ''), second_number_string.replace(' ', ''), \
            third_number_string.replace(' ', ''), fourth_number_string.replace(' ', '')

            validity_of_all_numbers, first_number, second_number, third_number, fourth_number = \
                self.convert_text_to_numbers(first_number_string, second_number_string, third_number_string,
                                             fourth_number_string)

            if validity_of_all_numbers:
                first_sign, second_sign, third_sign = str(self.choice_of_the_first_sign.currentText()), \
                                                      str(self.choice_of_the_second_sign.currentText()), str(
                    self.choice_of_the_third_sign.currentText())

                try:
                    value_in_brackets_result = self.operation_switch(second_sign, second_number, third_number)
                    value_in_brackets_result = self.rounding_of_intermediate_operations(value_in_brackets_result)

                    if first_sign == '*' or first_sign == '/':
                        first_operation_result = self.operation_switch(first_sign, first_number, value_in_brackets_result)
                        first_operation_result = self.rounding_of_intermediate_operations(first_operation_result)
                        third_operation_result = self.operation_switch(third_sign, first_operation_result,
                                                                       fourth_number)
                    else:
                        third_operation_result = self.operation_switch(third_sign, value_in_brackets_result,
                                                                       fourth_number)
                        third_operation_result = self.rounding_of_intermediate_operations(third_operation_result)
                        third_operation_result = self.operation_switch(first_sign, first_number,
                                                                       third_operation_result)
                    # В результате вычислений отображать в результате расчетов только шесть знаков после запятой.
                    # Незначащие нули не отображать.
                    self.calculation_result = third_operation_result.quantize(Decimal("1.0000000"))
                    if str(self.calculation_result)[-1:] == '5':
                        self.calculation_result += Decimal(0.0000005 if self.calculation_result > 0 else -0.0000005)
                    self.calculation_result = self.calculation_result.quantize(Decimal("1.000000"))

                    # В результате вычислений разделителем целой и дробной части в результате всегда отображать «точку».
                    self.calculation_results.insertPlainText(self.formatted_number_output(self.calculation_result))

                    self.is_calculated = True
                    self.enter_error.setText("No errors yet !")
                    self.enter_error.setStyleSheet("color: grey;")
                except:
                    self.enter_error.setText("Division by zero !")
                    self.enter_error.setStyleSheet("color: red;")
                    self.clear()
        else:
            self.enter_error.setText("Invalid number format !")
            self.enter_error.setStyleSheet("color: red;")
            self.clear()

    def clear(self):
        self.calculation_results.clear()
        self.first_number_input.setText('0')
        self.choice_of_the_first_sign.setCurrentText('+')
        self.second_number_input.setText('0')
        self.choice_of_the_second_sign.setCurrentText('+')
        self.third_number_input.setText('0')
        self.choice_of_the_third_sign.setCurrentText('+')
        self.fourth_number_input.setText('0')


class MainWindow(QMainWindow):  # создали окошко приложения
    def __init__(self, window_content):
        super().__init__()
        self.setWindowTitle("Савицкая Елизавета Дмитриевна, 2021 год, 4 курс, 4 группа")
        self.setFixedSize(600, 280)
        self.setCentralWidget(window_content)


if __name__ == '__main__':
    application_window = QApplication(sys.argv)
    content = ContentWindow()
    reporting_module_application_window = MainWindow(content)
    reporting_module_application_window.show()
    sys.exit(application_window.exec_())
