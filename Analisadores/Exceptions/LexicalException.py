# Classe de excessões pai
class LexicalException(Exception()):

    def __init__(self,msg):
        self.__mensagem = msg
        self.__linha = None   

# Classes de excessão referente aos nomes dos identificadores
class NameException(LexicalException):

    def __init__(self, msg):
        super().__init__(self,msg)

    def setLinha(self, linha):
        self.__linha = linha

    def getMessage(self):
        return self.__mensagem

    def getLinha(self):
        return self.__linha

# Classes de excessão referente aos valores dos identificadores
class ValueException(LexicalException):

    def __init__(self, msg):
        super().__init__(self,msg)

    def setLinha(self, linha):
        self.__linha = linha

    def getMessage(self):
        return self.__mensagem

    def getLinha(self):
        return self.__linha
