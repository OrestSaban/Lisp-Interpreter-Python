# tinylisp-compiler: A simple Lisp-to-Python compiler
import sys

def tokenize(code: str) -> list:
    "Convert a string of characters into a list of tokens."
    return code.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Expr:
    "Parse a program into an Expr."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list) -> Expr:
    if(len(tokens) == 0):
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)

    if(token == '('):
        List = []
        while(tokens[0] != ')'):
            List.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return List
        
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)



