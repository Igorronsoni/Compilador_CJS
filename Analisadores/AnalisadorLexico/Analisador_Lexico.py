class Analisador_Lexico:
    
    def __init__(self):
        self.content = []
        self.termo = ""

        self.tabela = dict()
        self.estado = "-><S>"
        
        self.linha = 1
        self.coluna = -1
        self.pos = 0

        self.FitaSaida = list()
        self.ids = ['*[<1A><if1>]','*[<1A><else1>]','*[<1A><var1>]','*[<1A><const1>]','*[<1A><true1>]','*[<1A><false1>]','*<1A>','*[<1A><else2>]','*[<1A><var2>]','*[<1A><const2>]','*[<1A><true2>]','*[<1A><false2>]','*[<1A><else3>]','*[<1A><const3>]','*[<1A><true3>]','*[<1A><false3>]','*[<1A><const4>]','*[<1A><false4>]']

        # Para fins de debug
        self.debug = False

    # Lê o arquivo de entrada e a tabela do automato, realiza o salvamento do automato em um dict
    def read(self, entrada):
        tabela = open('Analisadores/AnalisadorLexico/dfageneratormaster/output/dfa-err.csv','r').readlines()
        tokens = tabela[0].replace("\n","").split(',')

        linha = []
        for i in range(1,len(tabela)):
            linha = tabela[i].replace("\n","").split(',')
            
            self.tabela.update({linha[0]: {}})
            for ii in range(1,len(linha)):
                self.tabela[linha[0]].update({tokens[ii]: linha[ii]})
        self.content = entrada

    def write(self):
        self.limpaTermo()
        self.estado = "-><S>"
        
        erro = False

        if not self.isEOF():

            while True:

                if self.isEOF():
                    if not self.isSpace(currentChar): 
                        self.FitaSaida.append(self.saveData())
                    break

                currentChar = self.nextChar()
                
                #################################################################################################################################
                #                                                               Debugger                                                        #
                if self.debug: print("estado:",self.estado,"termo:",self.termo,"caracter:",currentChar,"linha:",self.linha,"coluna:",self.coluna)
                
                if not self.isSpace(currentChar):
                    self.adicionaTermo(currentChar)

                    if self.isError(currentChar):
                        self.estado = self.isTerminal(self.transition(currentChar))

                    elif self.isDelimiter(currentChar) or self.isOperator(currentChar) or self.isDelimiter(self.termo[-2]) or self.isOperator(self.termo[-2]):
                        self.removeUltimoChar()
                        self.FitaSaida.append(self.saveData())
                        self.back()
                    
                    else:
                        erro = True
            
                else:
                    if erro:
                        raise ValueError(f"Unrecognized Term. The term '{self.termo}' was not recognized at line {self.linha} and at the column {self.coluna - len(self.termo)}") 

                    tmp = self.isLineBreak(currentChar)
                    if tmp:
                        self.coluna -= 1
                    if self.termo != '':
                        self.FitaSaida.append(self.saveData())
                    if tmp:
                        self.coluna = 0

        self.FitaSaida.append('$')
        self.transformaVetor()
        outputlex = open('output/output.lex.txt','w+')
        outputlex.writelines(self.FitaSaida)

    def transformaVetor(self):
        for i in range(len(self.FitaSaida)):
            self.FitaSaida[i] = " ".join([str(_) for _ in self.FitaSaida[i]]) + '\n'
            
    # utils
    def adicionaTermo(self,arg):
        self.termo += arg

    def removeUltimoChar(self):
        self.termo = self.termo[:-1]

    def limpaTermo(self):
        self.termo = ""

    def isError(self, arg):
        return arg in self.tabela[self.estado] and self.transition(arg) != "<ErrorState>"

    def isTerminal(self,estado):
        if estado in self.tabela:
            return estado
        else:
            return "*" + estado

    def transition(self, arg):
        return self.tabela[self.estado][arg]

    def saveData(self):
        saida = []
        if self.estado in self.ids:
            self.estado = 'id'
        saida.append(self.estado)
        saida.append(self.linha)
        saida.append(self.coluna - len(self.termo))
        saida.append(self.termo)
        self.limpaTermo()
        self.estado = "-><S>"
        return saida

    def nextChar(self):
        tmp = self.content[self.pos]
        self.pos += 1
        self.coluna += 1
        return tmp

    def back(self):
        self.pos -= 1
        self.coluna -= 1

    def isDigit(self, arg):
        return arg >= '0' and arg <= '9'
    
    def isChar(self, arg):
        return arg >= 'a' and arg <= 'z' or arg >= 'A' or arg <= 'Z'

    def isDelimiter(self,arg):
        return arg == '{' or arg == '}' or arg == '(' or arg == ')' or arg == ';'
    
    def isSpace(self,arg):
        if self.isLineBreak(arg):
            self.linha += 1
        return arg == ' ' or arg == '\t' or self.isLineBreak(arg)

    def isLineBreak(self, arg):
        return arg == '\n' or arg == '\r'

    def isOperator(self,arg):
        return arg == '<' or arg == '>' or arg == '=' or arg == '!' or arg == '+' or arg == '-' or arg == '*' or arg == '/'

    def isEOF(self):
        return self.pos == len(self.content)