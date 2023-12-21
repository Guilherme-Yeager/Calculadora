from customtkinter import CTkButton, CTkLabel
from tkinter import Frame, Tk

def posicionarJanela(janela):
    x = str(janela.winfo_screenwidth() // 2 - 150)
    y = str(janela.winfo_screenheight() // 6)
    janela.geometry(f'325x515+{x}+{y}')

def atualizarFrame(frame):
    frame.destroy()
    novoFrame = Frame(janela, border = 2, bg = '#dcdcde')
    novoFrame.place(x = 5, y = 5, width = 315, height = 80)
    return novoFrame

def atualizarOperador(frameExpressao, op):
    operador = CTkLabel(frameExpressao, text = op, font = ('Arial', 20, 'bold'), fg_color = '#dcdcde', text_color = '#000000')
    operador.place(x = 275, y = 65, anchor = 'center')

def atualizarExpressao(frameExpressao, operando):
    expressao = CTkLabel(frameExpressao, text = operando, font = ('Arial', 25, 'bold'), fg_color = '#dcdcde', text_color = '#000000')
    expressao.place(x = 275 - ((len(valorOperando[0]) - 1) * 7), y = 28, anchor = 'center')

class Calculo:

    def __init__(self):
        self.primeiroTermo = ''
        self.segundoTermo = ''
        self.operador = ''
        self.resultado = 0
        self.controle = True
        self.calculado = False
    
    def limpar(self, valorOperando, frameExpressao):
        self.primeiroTermo = ''
        self.segundoTermo = ''
        self.operador = ''
        self.resultado = 0
        valorOperando[0] = ''
        valorOperando[1] = '0'
        frameExpressao = atualizarFrame(frameExpressao)
        self.calculado = False

    def operando(self, num, valorOperando, frameExpressao):
        if self.calculado == True:
            self.limpar(valorOperando, frameExpressao)
            return
        elif len(valorOperando[0]) > 18:
            return
        elif self.operador == '':
            self.primeiroTermo += num
        else:
            self.segundoTermo += num
        valorOperando[0] += num
        valorOperando[1] = str(int(valorOperando[1]) + 1)
        # Frame
        frameExpressao = atualizarFrame(frameExpressao)
        # Label
        atualizarExpressao(frameExpressao, valorOperando[0])
        # Operador
        atualizarOperador(frameExpressao, self.operador)

    def addOperador(self, op, valorOperando, frameExpressao):
        if self.calculado == True:
            self.limpar(valorOperando, frameExpressao)
        elif valorOperando[0] == '' and op == '-':
            valorOperando[0] += '-'
            valorOperando[1] = '1'
            if not self.primeiroTermo == '':
                self.segundoTermo = '-'
            else:
                self.primeiroTermo = '-'
            # Frame
            frameExpressao = atualizarFrame(frameExpressao)
            # Label
            atualizarExpressao(frameExpressao, valorOperando[0])
        elif not self.primeiroTermo == '':
            self.operador = op
            self.controle = True
            valorOperando[0] = ''
            valorOperando[1] = '0'
            # Frame
            frameExpressao = atualizarFrame(frameExpressao)
            # Label
            expressao = CTkLabel(frameExpressao, text = '0.00', font = ('Arial', 25, 'bold'), fg_color = '#dcdcde', text_color = '#000000')
            expressao.place(x = 275, y = 28, anchor='center')
            atualizarOperador(frameExpressao, self.operador)
            
    def calcular(self, valorOperando, frameExpressao):
        try:
            if self.calculado == True:
                self.limpar(valorOperando, frameExpressao)
            elif not self.segundoTermo == '':
                if self.operador == 'Raiz':
                    if int(self.primeiroTermo) < 0:
                        raise ValueError 
                    self.resultado = float(self.primeiroTermo) ** (1 / float(self.segundoTermo))
                else:
                    self.resultado = eval(self.primeiroTermo + self.operador + self.segundoTermo)
                # Frame
                frameExpressao = atualizarFrame(frameExpressao)
                # Label
                resultado = ''
                if len(str(self.resultado)) >= 18:
                    resultado = f'{self.resultado:.0e}'
                else:
                    resultado = f'{self.resultado:.2f}'
                expressao = CTkLabel(frameExpressao, text = resultado, font = ('Arial', 25, 'bold'), fg_color = '#dcdcde', text_color = '#000000')
                expressao.place(x = 275 - ((len(resultado) - 3) * 7), y = 28, anchor = 'center')
                self.controle = True
                self.calculado = True
        except ZeroDivisionError:
            print('Error: Divisão por 0')
        except ValueError:
            print('Raiz negativa')

    def addPonto(self, valorOperando, frameExpressao):
        if not self.primeiroTermo == '' and self.segundoTermo == '' and self.controle == True:
            self.primeiroTermo += '.'
            self.controle = False
            valorOperando[0] += '.'
        elif not self.segundoTermo == '' and self.controle == True:
            self.segundoTermo += '.'
            self.controle = False
            valorOperando[0] += '.'
        if not valorOperando[0] == '':
            # Frame
            frameExpressao = atualizarFrame(frameExpressao)
            # Label
            atualizarExpressao(frameExpressao, valorOperando[0])
            atualizarOperador(frameExpressao, self.operador)

    def limparUmDigito(self, valorOperando, frameExpressao):
        if self.calculado == True:
            self.limpar(valorOperando, frameExpressao)
        elif self.primeiroTermo == '':
            return
        elif not valorOperando[0] == '':
            valorOperando[0] = valorOperando[0][:-1]
        # Frame
        frameExpressao = atualizarFrame(frameExpressao)
        # Label
        atualizarExpressao(frameExpressao, valorOperando[0])
        if not self.operador == '':
            atualizarOperador(frameExpressao, self.operador)

        

if __name__ == '__main__':
    # Janela
    janela = Tk()
    janela.title('Calculadora')
    janela.iconbitmap('img/icon.ico')
    posicionarJanela(janela)
    janela.resizable(False, False)
    janela.configure(bg = '#0c043d')
    
    # Cores
    corAzul = '#1117cf'
    corBranco = '#ffffff'

    # Objeto para calcular as contas
    calculo = Calculo()
    
    # Componentes
    valorOperando = ['', '0']

    # Frame
    frameExpressao = Frame(janela, border = 2, bg = '#dcdcde')
    frameExpressao.place(x = 5, y = 5, width = 315, height = 80)

    # Label
    expressao = CTkLabel(frameExpressao, text = '0.00', font = ('Arial', 25, 'bold'), fg_color = '#dcdcde', text_color = '#000000')
    expressao.place(x = 275, y = 28, anchor = 'center')

    # Botões
    botaoZero = CTkButton(janela, text = '0', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('0', valorOperando, frameExpressao))
    botaoZero.place(x = 85, y = 430)
    
    botaoUm = CTkButton(janela, text = '1', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('1', valorOperando, frameExpressao))
    botaoUm.place(x = 5, y = 345)

    botaoDois = CTkButton(janela, text = '2', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('2', valorOperando, frameExpressao))
    botaoDois.place(x = 85, y = 345)

    botaoTres = CTkButton(janela, text = '3', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('3', valorOperando, frameExpressao))
    botaoTres.place(x = 165, y = 345)

    botaoQuatro = CTkButton(janela, text = '4', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('4', valorOperando, frameExpressao))
    botaoQuatro.place(x = 5, y = 260)
    
    botaoCinco = CTkButton(janela, text = '5', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('5', valorOperando, frameExpressao))
    botaoCinco.place(x = 85, y = 260)
    
    botaoSeis = CTkButton(janela, text = '6', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('6', valorOperando, frameExpressao))
    botaoSeis.place(x = 165, y = 260)
    
    botaoSete = CTkButton(janela, text = '7', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('7', valorOperando, frameExpressao))
    botaoSete.place(x = 5, y = 175)
    
    botaoOito = CTkButton(janela, text = '8', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('8', valorOperando, frameExpressao))
    botaoOito.place(x = 85, y = 175)
    
    botaoNove = CTkButton(janela, text = '9', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.operando('9', valorOperando, frameExpressao))
    botaoNove.place(x = 165, y = 175)
  
    botaoDivide = CTkButton(janela, text = '/', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('/', valorOperando, frameExpressao))
    botaoDivide.place(x = 245, y = 175)

    botaoMultiplica = CTkButton(janela, text = 'X', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 18, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('*', valorOperando, frameExpressao))
    botaoMultiplica.place(x = 245, y = 260)

    botaoSoma = CTkButton(janela, text = '+', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 23, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('+', valorOperando, frameExpressao))
    botaoSoma.place(x = 245, y = 345)

    botaoSubtrai = CTkButton(janela, text = '-', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 27, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('-', valorOperando, frameExpressao))
    botaoSubtrai.place(x = 165, y = 430)

    botaoCalcular = CTkButton(janela, text = '=', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.calcular(valorOperando, frameExpressao))
    botaoCalcular.place(x = 245, y = 430)

    botaoLimpar = CTkButton(janela, text = 'DEL', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 18, 'bold'), text_color = corBranco, command = lambda: calculo.limpar(valorOperando, frameExpressao))
    botaoLimpar.place(x = 245, y = 90)

    botaoPonto = CTkButton(janela, text = '.', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.addPonto(valorOperando, frameExpressao))
    botaoPonto.place(x = 5, y = 430)
    
    botaoC = CTkButton(janela, text = 'C', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.limparUmDigito(valorOperando, frameExpressao))
    botaoC.place(x = 165, y = 90)

    botaoRaiz = CTkButton(janela, text = '√', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('Raiz', valorOperando, frameExpressao))
    botaoRaiz.place(x = 85, y = 90)

    botaoExpoente = CTkButton(janela, text = '^', width = 75, height = 80, corner_radius = 6, fg_color = corAzul, font = ('Arial', 25, 'bold'), text_color = corBranco, command = lambda: calculo.addOperador('**', valorOperando, frameExpressao))
    botaoExpoente.place(x = 5, y = 90)

    janela.mainloop()


