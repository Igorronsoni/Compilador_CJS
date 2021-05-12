# Futuramento o compilador sera refatorado e isso será util
# class Token:

#     def __init__(self,type = None, text = None):
#         self.TK_IDENTIFICADOR    = 0
#         self.TK_NUMERO           = 1
#         self.TK_OPERADOR         = 2
#         self.TK_PONTUACAO        = 3
#         self.TK_ATRIBUICAO       = 4
#         self.TK_RESERVED_WORD    = 5
#         self.TK_LOGICAL_OPERATOR = 6
        
#         self.TK_TEXT = ["IDENTIFIER", "NUMBER", "OPERATOR", "PONCTUACTION", "ASSIGNMENT"]
        
#         self.type = type
#         self.text = text
#         self.linha = 0

#     def getType(self):
#         return self.type

#     def setType(self,type):
#         self.type = type
    
#     def getText(self):
#         return self.text
    
#     def setText(self,text):
#         self.text = text
    
#     def setLinha(self,linha):
#         self.linha = linha

#     def getLinha(self):
#         return self.linha

#     def toString(self):
#         return f"Token [type={self.type} text={self.text}]"