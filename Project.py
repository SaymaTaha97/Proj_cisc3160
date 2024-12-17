import re

class Interpreter:
    def __init__(my):
        my.variables = {}
        my.errors = []

    def parse_identifier(my, token):
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token)

    def parse_literal(my, token):
        return re.match(r'^(0|[1-9][0-9]*)$', token)

    def evaluate_expression(my, expr):
        try:
            for var in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr):
                if var not in my.variables:
                    my.errors.append(f"Uninitialized variable: {var}")
                    return None
                expr = expr.replace(var, str(my.variables[var]))

            value = eval(expr, {}, {})
            if not isinstance(value, int):
                raise ValueError("Expression did not evaluate to an integer.")
            return value
        except Exception as e:
            my.errors.append(f"Error in expression '{expr}': {e}")
            return None

    def parse_assignment(my, line):
        if not line.endswith(';'):
            my.errors.append("Syntax error: Missing semicolon.")
            return

        line = line[:-1].strip()
        if '=' not in line:
            my.errors.append("Syntax error: Missing '=' in assignment.")
            return

        identifier, expr = map(str.strip, line.split('=', 1))

        if not my.parse_identifier(identifier):
            my.errors.append(f"Syntax error: Invalid identifier '{identifier}'.")
            return

        if re.match(r'^[0][0-9]+$', expr):
            my.errors.append("Syntax error: Leading zeros in literal.")
            return

        value = my.evaluate_expression(expr)
        if value is not None:
            my.variables[identifier] = value

    def interpret(my, program):
        my.variables.clear()
        my.errors.clear()

        for line in program.strip().splitlines():
            line = line.strip()
            if line:
                my.parse_assignment(line)

        if my.errors:
            print("error")
            for error in my.errors:
                print(error)
        else:
            for var, value in my.variables.items():
                print(f"{var} = {value}")

interpreter = Interpreter()

# Input 1
print("Input 1")
interpreter.interpret("x = 001;")
print()

# Input 2
print("Input 2")
interpreter.interpret("x_2 = 0;")
print()

# Input 3
print("Input 3")
interpreter.interpret("""
x = 0
y = x;
z = ---(x+y);
""")
print()

# Input 4
print("Input 4")
interpreter.interpret("""
x = 1;
y = 2;
z = ---(x+y)*(x+-y);
""")


