# tinylisp-compiler: A simple Lisp-to-Python compiler
import sys
import math
import operator as op
from functools import reduce

# 1. Define basic data structures
class Expr:
    pass

class Atom(Expr):
    def __init__(self, value):
        self.value = value

class Symbol(Atom):
    pass

class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class Symbol:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

class List:
    def __init__(self, elements):
        # Convert Python lists to our List type if needed
        self.elements = [
            x if isinstance(x, (Number, Symbol, List)) else Number(x) 
            for x in elements
        ]

    def __repr__(self):
        if len(self.elements) > 0 and isinstance(self.elements[0], Symbol) and self.elements[0].value == 'quote':
            return "'" + str(self.elements[1])
        return f"({' '.join(map(str, self.elements))})"
    
    def __add__(self, other):
        # Handle list concatenation
        if isinstance(other, list):
            other = List(other)
        if isinstance(other, List):
            return List(self.elements + other.elements)
        raise TypeError(f"Cannot concatenate List with {type(other)}")

    def __getitem__(self, index):
        return self.elements[index]
    
    def __len__(self):
        return len(self.elements)

# 2. Define the tokenizer 

def tokenize(code: str) -> list:
    "Convert a string of characters into a list of tokens."
    # Remove comments (anything after ;)
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        comment_idx = line.find(';')
        if comment_idx != -1:
            line = line[:comment_idx]
        cleaned_lines.append(line)
    code = ' '.join(cleaned_lines)
    return code.replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ").split()

# 3. Define parser

def parse(program: str):
    "Parse a program string into a list of expressions"
    tokens = tokenize(program)
    expressions = []
    while tokens:  # Process all tokens
        expressions.append(read_from_tokens(tokens))
    return expressions

def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)

    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(read_from_tokens(tokens))
        tokens.pop(0)
        return List(lst)
    elif token == "'":  # Handle quote
        quoted = read_from_tokens(tokens)
        return List([Symbol('quote'), quoted])
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try: 
        return Number(int(token))  # Wrap the number in the Number class
    except ValueError:
        try: 
            return Number(float(token))  # Handle floats as well
        except ValueError:
            return Symbol(token)  # If not a number, it's a symbol


def raise_error(msg):
    raise Exception(msg)

# 4. Define the environment
class Env(dict):
    def __init__(self, outer=None):
        super().__init__()
        self.outer = outer

    def lookup(self, var):
        if var in self:
            return self[var]
        elif self.outer:
            return self.outer.lookup(var)
        else:
            raise NameError(f"Unbound symbol: {var}")

    def set(self, var, value):
        self[var] = value

    

# 5. define the evaluator
def eval(expr, env):
    # If it's a number, return its value
    if isinstance(expr, Number):
        return expr.value
    
    # If it's a symbol, lookup its value in the environment
    if isinstance(expr, Symbol):
        return env.lookup(expr.value)
    
    # If it's a list, process it
    if isinstance(expr, List):
        if not expr.elements:  # Handle empty list
            return List([])
            
        first = expr.elements[0]
        if isinstance(first, Symbol):
            # Handle special forms
            if first.value == 'quote':
                return expr.elements[1]
                
            if first.value == 'define':
                var = expr.elements[1]
                value = eval(expr.elements[2], env)
                env.set(var.value, value)
                return value
                
            elif first.value == 'lambda':
                params = expr.elements[1].elements  # Get parameter list
                body = expr.elements[2]  # Get function body
                return LambdaFunction(params, body, env)
                
            elif first.value == 'if':
                condition = eval(expr.elements[1], env)
                if condition:
                    return eval(expr.elements[2], env)
                else:
                    return eval(expr.elements[3], env) if len(expr.elements) > 3 else None
                    
            elif first.value == 'list':
                # Return a List of evaluated arguments
                return List([eval(arg, env) for arg in expr.elements[1:]])
        
        # Function application
        proc = eval(expr.elements[0], env)
        args = [eval(arg, env) for arg in expr.elements[1:]]
        if isinstance(proc, LambdaFunction):
            return proc(*args)
        return proc(*args)

    return None




# 6. define lambda function
class LambdaFunction:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
        
    def __call__(self, *args):
        # Create new environment with parent as the creation environment
        new_env = Env(self.env)
        # Bind parameters to arguments
        for param, arg in zip(self.params, args):
            new_env.set(param.value, arg)
        return eval(self.body, new_env)

    def __repr__(self):
        return f"<lambda function with params: {self.params}>"


# 7. Define standard environment

def standard_env() -> dict:
    env = Env()
    env.update(vars(math))
    env.update({
        # Fix arithmetic operations to handle Number objects
        '+': lambda *args: sum(x.value if isinstance(x, Number) else x for x in args),
        '-': lambda x, *args: (x.value if isinstance(x, Number) else x) - sum(y.value if isinstance(y, Number) else y for y in args) if args else -(x.value if isinstance(x, Number) else x),
        '*': lambda *args: reduce(op.mul, (x.value if isinstance(x, Number) else x for x in args)),
        '/': lambda x, *args: (x.value if isinstance(x, Number) else x) / reduce(op.mul, (y.value if isinstance(y, Number) else y for y in args)) if args else 1/(x.value if isinstance(x, Number) else x),
        '>': lambda x, y: (x.value if isinstance(x, Number) else x) > (y.value if isinstance(y, Number) else y),
        '<': lambda x, y: (x.value if isinstance(x, Number) else x) < (y.value if isinstance(y, Number) else y),
        '>=': lambda x, y: (x.value if isinstance(x, Number) else x) >= (y.value if isinstance(y, Number) else y),
        '<=': lambda x, y: (x.value if isinstance(x, Number) else x) <= (y.value if isinstance(y, Number) else y),
        '=': lambda x, y: (x.value if isinstance(x, Number) else x) == (y.value if isinstance(y, Number) else y),
        'abs': lambda x: abs(x.value if isinstance(x, Number) else x),
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *args: args[-1] if args else None,
        'car': lambda lst: lst.elements[0] if isinstance(lst, List) and lst.elements else None,
        'cdr': lambda lst: List(lst.elements[1:]) if isinstance(lst, List) and lst.elements else List([]),
        'cons': lambda x, lst: List([x] + (lst.elements if isinstance(lst, List) else [lst])),
        'eq?': op.eq,
        'equal?': op.eq,
        'length': len,
        'list': lambda *args: List(list(args)),
        'list?': lambda lst: isinstance(lst, List),
        'map': lambda proc, lst: List([proc(x) for x in (lst.elements if isinstance(lst, List) else lst)]),
        'max': lambda *args: max(x.value if isinstance(x, Number) else x for x in args),
        'min': lambda *args: min(x.value if isinstance(x, Number) else x for x in args),
        'not': op.not_,
        'null?': lambda lst: len(lst.elements) == 0 if isinstance(lst, List) else lst == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': lambda x: isinstance(x, LambdaFunction),
        'round': lambda x: round(x.value if isinstance(x, Number) else x),
        'symbol?': lambda x: isinstance(x, Symbol),
        'zero?': lambda x: (x.value if isinstance(x, Number) else x) == 0,
        'newline': lambda: '\n',
        'and': lambda *args: all(args),
        'or': lambda *args: any(args),
        'string?': lambda x: isinstance(x, str),
        'string-append': lambda *args: ''.join(args),
        'string-length': len,
        'substring': lambda s, start, end: s[start:end],
        'string->symbol': lambda s: Symbol(s),
        'floor': math.floor,
        'ceiling': math.ceil,
        'modulo': op.mod,
        'error': raise_error,
    })
    return env

global_env = standard_env()

def run(filename: str):
    with open(filename, 'r') as file:
        program = file.read()
    print(f"\nExecuting {filename}:")
    
    parsed_expressions = parse(program)
    
    result = None
    # Evaluate each expression in sequence
    for expr in parsed_expressions:
        result = eval(expr, global_env)
    
    print(f"Result: {result}")
    return result


# ... existing code ...

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 compiler.py <filename>")
    else:
        run(sys.argv[1])