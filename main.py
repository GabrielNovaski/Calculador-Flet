import flet as ft
from util import isNumOrDot, isValidNumber
from math import pow
class calculadora:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.op = None
        self.result = None

    def main(self, pagina):
        self.pagina = pagina
        self.pagina.window.width = 500
        self.pagina.window.height = 560
        self.pagina.window.resizable = False
        self.info = ft.Text('Sua Conta', text_align=ft.TextAlign.RIGHT)
        self.display = ft.TextField('', width=400, text_align=ft.TextAlign.RIGHT, text_size=30, read_only=True, bgcolor='#2F4F4F')
        self.display.border_radius = ft.border_radius.all(10)
        central = ft.Row([ft.Column([self.info, self.display], 
                        horizontal_alignment=ft.CrossAxisAlignment.END)], 
                        alignment=ft.MainAxisAlignment.CENTER,)

        self.pagina.add(central)
        self.botoesNaTela()
        self.pagina.update()

    def numberToDisplay(self, e):
        self.newDisplayValue = self.display.value + e.control.text
        if not isValidNumber(self.newDisplayValue):
            return
        self.display.value = self.newDisplayValue
        self.pagina.update()

    def clearDisplay(self):
            self.display.value = ''
            self.left = None
            self.right = None
            self.op = None
            self.info.value = 'Sua Conta'

    def operatorClicked(self, e):
        if e.control.text == 'C':
            self.clearDisplay()
        
        if e.control.text == 'D':
            self.displayBackSpace()

        if e.control.text == '=':
            self.eq()
        
        if e.control.text in '+-*/^':
            self.confgLeft(e.control.text)
        
        if e.control.text == 'N':
            self.invertNumber()
        
        self.pagina.update()

    def invertNumber(self):
        displayValue = self.display.value
        try:
            displayValue = int(displayValue) * -1
            self.display.value = displayValue
        except:
            self.makeShowError('DIGITE UM NUMERO VALIDO.')
            return


    def displayBackSpace(self):
        displayText = self.display.value
        if displayText == '':
            return
        displayText = displayText[:-1]
        self.display.value = displayText
        
    
    def confgLeft(self, texto):
        if not isValidNumber(self.display.value) and self.left is None:
            self.makeShowError('DISPLAY VAZIO')
            return
            
        if self.left is None:
            self.left = self.display.value
            self.display.value = ''

        self.op = texto
        self.info.value = f'{self.left} {self.op} ??'


    def eq(self): # Quando o sinal de = for clicado
        if self.left is None or self.display.value == '':
            self.makeShowError('CONTA INCOMPLETA')
            return
        
        self.right = self.display.value
        self.equation = f'{self.left} {self.op} {self.right}'
        
        try:
            if self.op == '^':
                self.result = pow(float(self.left), float(self.right))
            else:
                self.result = eval(self.equation)
        except ZeroDivisionError:
            self.clearDisplay()
            self.makeShowError('ZeroDivisionError: Divisao Por Zero')
            return
        except OverflowError:
            self.clearDisplay()
            self.makeShowError('OverFlowErrror: Excedido o maximo de caracteres')
            return
 
        self.result = int(self.result)
        self.info.value = f'{self.equation} = {self.result}'
        self.left = self.result
        self.display.value = ''

            
    def botoesNaTela(self):
        teclas = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '=']
            ]
        for i in range (0, 5):
            linha = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            for j in range(0, 4):
                if isNumOrDot(teclas[i][j]):
                    botao = ft.ElevatedButton(teclas[i][j],width=60, height=60, on_click=self.numberToDisplay)
                else:
                    botao = ft.ElevatedButton(teclas[i][j], width=60, height=60, on_click=self.operatorClicked)
                linha.controls.append(botao)
            self.pagina.add(linha)

    def makeShowError(self, message):
        botao_ok = ft.ElevatedButton(text='OK', on_click=self.close_popup)
        self.janela = ft.AlertDialog(title=ft.Text(message, size=23), actions=[botao_ok])
        
        self.pagina.add(self.janela)
        self.janela.open = True
        self.pagina.update()

    def close_popup(self, e):
        self.janela.open = False
        self.pagina.update()

if __name__ == '__main__':
    app = calculadora()
    ft.app(app.main)
