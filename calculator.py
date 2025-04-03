import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("공학용 계산기")
        self.window.geometry("400x600")
        self.window.resizable(False, False)

        # 계산 결과를 표시할 엔트리
        self.display = ttk.Entry(self.window, justify="right", font=("Arial", 20))
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # 버튼에 표시될 텍스트와 기능을 딕셔너리로 정의
        self.scientific_functions = {
            'sin': lambda x: math.sin(math.radians(float(x))),
            'cos': lambda x: math.cos(math.radians(float(x))),
            'tan': lambda x: math.tan(math.radians(float(x))),
            'log': lambda x: math.log10(float(x)),
            'ln': lambda x: math.log(float(x)),
            'sqrt': lambda x: math.sqrt(float(x)),
            'x²': lambda x: float(x) ** 2,
            'x³': lambda x: float(x) ** 3,
            '1/x': lambda x: 1 / float(x),
            'e^x': lambda x: math.exp(float(x)),
            'π': lambda x: math.pi,
        }

        # 버튼 배치
        button_layout = [
            ['sin', 'cos', 'tan', '(', ')', 'C'],
            ['log', 'ln', 'sqrt', 'x²', 'x³', '⌫'],
            ['1/x', 'e^x', 'π', '7', '8', '9'],
            ['±', '%', '/', '4', '5', '6'],
            ['rad', 'deg', '*', '1', '2', '3'],
            ['EXP', '×10^x', '-', '0', '.', '+'],
            ['=']
        ]

        # 버튼 생성
        for i, row in enumerate(button_layout):
            for j, text in enumerate(row):
                if text == '=':
                    button = ttk.Button(self.window, text=text,
                                     command=lambda t=text: self.button_click(t))
                    button.grid(row=i+1, column=0, columnspan=6, padx=2, pady=2, sticky="nsew")
                else:
                    button = ttk.Button(self.window, text=text,
                                     command=lambda t=text: self.button_click(t))
                    button.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")

        # 그리드 설정
        for i in range(8):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.window.grid_columnconfigure(i, weight=1)

        self.current_expression = ""
        self.angle_mode = "deg"  # 기본값은 도(degree) 모드

    def button_click(self, value):
        if value == '=':
            try:
                result = self.evaluate_expression()
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.current_expression = str(result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                self.current_expression = ""
        elif value == 'C':
            self.display.delete(0, tk.END)
            self.current_expression = ""
        elif value == '⌫':  # Backspace
            self.current_expression = self.current_expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_expression)
        elif value == 'rad':
            self.angle_mode = "rad"
        elif value == 'deg':
            self.angle_mode = "deg"
        elif value == '±':
            try:
                if self.current_expression and self.current_expression[0] == '-':
                    self.current_expression = self.current_expression[1:]
                else:
                    self.current_expression = '-' + self.current_expression
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_expression)
            except:
                pass
        elif value in self.scientific_functions:
            try:
                if self.current_expression:
                    current_value = float(self.evaluate_expression())
                    result = self.scientific_functions[value](current_value)
                    self.display.delete(0, tk.END)
                    self.display.insert(0, str(result))
                    self.current_expression = str(result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                self.current_expression = ""
        else:
            self.current_expression += value
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_expression)

    def evaluate_expression(self):
        # 수식에서 π를 math.pi로 변환
        expression = self.current_expression.replace('π', str(math.pi))
        
        try:
            # eval 함수를 사용하여 수식 계산
            result = eval(expression)
            return result
        except:
            raise ValueError("Invalid expression")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = ScientificCalculator()
    calc.run() 