import argparse, textwrap, os

from .extra import *
debug = False

def main() :
    #parse arguments
    
    args = "projeto/gramatica.txt"
    output = 'Analisadores/AnalisadorLexico/dfageneratormaster/output'
    if not os.path.exists(output):
        os.makedirs(output)

    input_file = open(args,'r')
    lines = input_file.read().splitlines()
    input_file.close()

    #Parse input file
    ndfa, terminals, final = parseNDFA(lines)

    #Export NDFA as csv
    if debug: print("Exporting nondeterministic finite automaton...",end='')
    ndfa_file = open(os.path.join(output,'ndfa.csv'),'w+')
    writeNDFA(ndfa_file, ndfa, terminals, final)
    ndfa_file.close()
    if debug: print(" Done!")

    #Minify NDFA
    ndfa = minifyFA(ndfa,final,False)

    #Export NDFA-minified as csv
    if debug: print("\nExporting nondeterministic finite automaton (minified)...",end='')
    ndfa_file = open(os.path.join(output,'ndfa-min.csv'),'w+')
    writeNDFA(ndfa_file, ndfa, terminals, final)
    ndfa_file.close()
    if debug: print(" Done!")

    #Determinize NDFA
    dfa, terminals, final = determinizeNDFA(ndfa, final)

    #Export DFA as csv
    if debug: print("\nExporting deterministic finite automaton...",end='')
    dfa_file = open(os.path.join(output,'dfa.csv'),'w+')
    writeDFA(dfa_file, dfa, terminals, final)
    dfa_file.close()
    if debug: print(" Done!")

    #Add error state to DFA
    dfa, final = addErrorStateDFA(dfa, terminals, final)

    #Export DFA-errorstate as csv
    if debug: print("\nExporting deterministic finite automaton (with error state)...",end='')
    dfa_file = open(os.path.join(output,'dfa-err.csv'),'w+')
    writeDFA(dfa_file, dfa, terminals, final)
    dfa_file.close()
    if debug: print(" Done!")

if __name__=="__main__" :
    main()
