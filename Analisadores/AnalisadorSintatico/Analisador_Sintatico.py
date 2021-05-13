class Analisador_Sintatico:

    def __init__(self):
        self.scanner = []
        self.estados = dict()
        self.producoes = dict()
        self.pilha = ['0']
        
        self.debug = False

    def read(self):
        arquivo = open('output/output.lex.txt','r')
        self.scanner = arquivo.readlines()

        for i in range(len(self.scanner)):
            self.scanner[i] = self.scanner[i].replace('\n','')
         
        # Carrega tabela LALR
        lr = open('LALR.txt','r')
        lr = lr.readlines()
        lr[0] = lr[0][3:] # Retira dado estranho do arquivo LALR
        linhaDosEstados = 0
        # Adiciona ao dicionario de produções
        for i in range(len(lr)):
            if lr[i][0] != 'S' and lr[i][0] != '\n':
                estado = lr[i][: lr[i].index(' ') ]
                prod = lr[i][ lr[i].index('<') : lr[i].index('>') +1 ]
                qt = len((lr[i][ lr[i].index('=') +2 :]).split(' '))
                self.producoes.update({estado: {}})
                self.producoes[estado].update({qt: prod})
            else:
                linhaDosEstados = i + 1 # Verifica onde começa a identificação dos estados
                break

        lr = lr[linhaDosEstados:]
        estado = ''
        for i in range(len(lr)):
            if 'State' in lr[i]:
                lr[i] = lr[i].replace('State ','')
                estado = lr[i].replace('\n','')
                self.estados.update({estado: {}})
                continue
            
            prod = lr[i][ 8 :lr[i].index(' ',9)]                
            acao = (lr[i][ lr[i].index(' ',9)+1:].replace('\n','')).split(' ')
            if '' in acao:
                acao.remove('')
            acao = ''.join(acao)
            self.estados[estado].update({prod: acao})

    def write(self):
        cabecote = 0
        readState = self.pilha[-1]
        transition = self.getEstadoFita(cabecote)
        while True:

            if transition in self.estados[readState]:
                acao = self.estados[readState][transition]
            else:
                termo = self.scanner[cabecote].split(' ')
                if termo[0] == '$':
                    return
                raise SyntaxError(f"Unrecognized Expression. The expression '{termo[3]}' was not recognized at line {termo[1]} and at the column {termo[2]}")

            if self.debug:
                print('Acao:',self.getAcao(acao),'Cabecote:',cabecote,'readState:',readState,'Pilha',self.pilha,'Transition:',transition)

            if self.getAcao(acao) == 's':
                self.pilha.append(self.getTransicaoEstado(acao))
                cabecote += 1
                readState = ''

            elif self.getAcao(acao) == 'r':
                size = self.producoes[self.getTransicaoEstado(acao)]
                for i in size.keys(): key = i
                readState = self.removeItens(int(key))
                transition = size[key]
                self.pilha.append(self.getTransicaoEstado(self.estados[readState][transition]))
            
            elif self.getAcao(acao) == 'g':
                self.pilha.append(self.getTransicaoEstado(acao))

            elif self.getAcao(acao) == 'a':
                return

            readState = self.pilha[-1]
            transition = self.getEstadoFita(cabecote)

    # Uteis
    def getEstadoFita(self,index):
        tmp = self.scanner[index]
        if len(tmp) != 1:
            return tmp[: tmp.index(' ') or tmp.index('\n')]
        return tmp

    def getAcao(self,acao):
        return acao[:1]
    
    def getTransicaoEstado(self,acao):
        return acao[1:].replace('\n','')

    def removeItens(self,quantidade = 1):
        for i in range(quantidade):
            self.pilha.pop()
        return self.pilha[-1]