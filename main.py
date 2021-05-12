from Analisadores.AnalisadorLexico.Analisador_Lexico import *
from Analisadores.AnalisadorSintatico.Analisador_Sintatico import *
from Analisadores.AnalisadorLexico.dfageneratormaster.main import *

import argparse, textwrap, os

def readArgs() :
    helpEpilog = ""
    parser = argparse.ArgumentParser(description="Compiladores 2020/2", add_help=True)
    parser.add_argument("-i","--input",help="input txt file", required=True, type=str, dest="input")
    parser.add_argument("-o","--output",help="output folder", default="output", type=str, dest="output")
    return parser.parse_args()

def compilador() :
    main()
    
    lexico = Analisador_Lexico()
    sintatico = Analisador_Sintatico()

    args = readArgs()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    arquivo = open(args.input,'r')
    entrada = arquivo.read()
    try:
        lexico.read(entrada.strip())  
        lexico.write()
        sintatico.read()
        sintatico.write()

        print("Compilation Sucesseful")
    except ValueError as err:
        print("ValueError:", err)
    except SyntaxError as err:
        print("SyntaxError:", err)   

if __name__=="__main__" :
    compilador()
