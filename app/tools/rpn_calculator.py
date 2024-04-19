import math
from collections.abc import Callable

OPERATORS: dict[str, tuple[Callable[..., float], int, str]] = {
    "+": (lambda a, b: a + b, 2, "Add"),
    "-": (lambda a, b: a - b, 2, "Subtract"),
    "*": (lambda a, b: a * b, 2, "Multiply"),
    "/": (lambda a, b: a / b, 2, "Divide"),
    "%": (lambda a, b: a % b, 2, "Modulus"),
    "^": (lambda a, b: pow(a, b), 2, "Power"),
    "exp": (lambda a: math.exp(a), 1, "Exponentiation"),
    "!": (lambda x: math.factorial(int(x)), 1, "Factorial"),
    "sqrt": (lambda x: math.sqrt(x), 1, "Square Root"),
    "ln": (lambda x: math.log(x), 1, "Natural Logarithm"),
    "log": (lambda x: math.log10(x), 1, "Logarithm"),
    "sin": (lambda x: math.sin(x), 1, "Sine"),
    "asin": (lambda x: math.asin(x), 1, "ASine"),
    "cos": (lambda x: math.cos(x), 1, "Cosine"),
    "acos": (lambda x: math.acos(x), 1, "ACosine"),
    "tan": (lambda x: math.tan(x), 1, "Tangent"),
    "atan": (lambda x: math.atan(x), 1, "ATangent"),
}

VARIABLES: dict[str, tuple[float, str]] = {
    "pi": (math.pi, "pi"),
    "e": (math.e, "Eular's number"),
}


class RPNCalculatorError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class RPNCalculator:
    def __init__(self, expression: str):
        self.stack: list[float] = []
        self.expression = expression

    def solve(self) -> float:
        for token in self.expression.split():
            try:
                if token.replace(".", "").isnumeric():
                    self.stack.append(float(token))
                elif token in VARIABLES:
                    self.stack.append(VARIABLES[token][0])
                else:
                    if len(self.stack) < OPERATORS[token][1]:
                        raise RPNCalculatorError("Insufficient operands for operator.")
                    func, _, operator = OPERATORS[token]
                    operand2 = self.stack.pop()
                    if operator == "Factorial" and not operand2.is_integer():
                        raise RPNCalculatorError("Factorial operator need a integer.")
                    if OPERATORS[token][1] == 2:
                        operand1 = self.stack.pop()
                        result = func(operand1, operand2)
                    else:
                        result = func(operand2)
                    self.stack.append(result)
            except KeyError as e:
                raise RPNCalculatorError(
                    f"{e.__class__.__name__}: Invalid expression. ({str(e)})"
                ) from e
            except ZeroDivisionError as e:
                raise RPNCalculatorError(f"{e.__class__.__name__}: {str(e)}.") from e
        if len(self.stack) != 1:
            raise RPNCalculatorError(
                "Multiple elements left on stack. Invalid expression."
            )
        return self.stack.pop()
