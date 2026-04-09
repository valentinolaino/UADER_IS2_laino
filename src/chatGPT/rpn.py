#!/usr/bin/env python3
import sys, math

class RPNError(Exception):
    pass

def is_num(x):
    try:
        float(x)
        return True
    except:
        return False

def deg(x): return math.radians(x)
def rad(x): return math.degrees(x)

def eval_rpn(expr):
    stack = []
    mem = [0.0]*10

    def need(n):
        if len(stack) < n:
            raise RPNError("Pila insuficiente")

    tokens = expr.split()
    i = 0

    while i < len(tokens):
        t = tokens[i]

        if is_num(t):
            stack.append(float(t))

        elif t in "+-*/":
            need(2)
            b, a = stack.pop(), stack.pop()
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)
            elif t == "*": stack.append(a * b)
            elif t == "/":
                if b == 0: raise RPNError("División por cero")
                stack.append(a / b)

        elif t == "dup":
            need(1); stack.append(stack[-1])

        elif t == "swap":
            need(2); stack[-1], stack[-2] = stack[-2], stack[-1]

        elif t == "drop":
            need(1); stack.pop()

        elif t == "clear":
            stack.clear()

        elif t in ("p", "pi"):
            stack.append(math.pi)
        elif t == "e":
            stack.append(math.e)
        elif t == "j":
            stack.append((1 + 5**0.5)/2)

        elif t == "chs":
            need(1); stack[-1] = -stack[-1]

        elif t == "sqrt":
            need(1); stack.append(math.sqrt(stack.pop()))

        elif t == "log":
            need(1); stack.append(math.log10(stack.pop()))

        elif t == "ln":
            need(1); stack.append(math.log(stack.pop()))

        elif t == "ex":
            need(1); stack.append(math.exp(stack.pop()))

        elif t == "10x":
            need(1); stack.append(10**stack.pop())

        elif t == "yx":
            need(2)
            b, a = stack.pop(), stack.pop()
            stack.append(a**b)

        elif t == "1/x":
            need(1)
            x = stack.pop()
            if x == 0: raise RPNError("División por cero")
            stack.append(1/x)

        elif t in ("sin","cos","tg","asin","acos","atg"):
            need(1)
            x = stack.pop()
            if t == "sin": stack.append(math.sin(deg(x)))
            elif t == "cos": stack.append(math.cos(deg(x)))
            elif t == "tg": stack.append(math.tan(deg(x)))
            elif t == "asin": stack.append(rad(math.asin(x)))
            elif t == "acos": stack.append(rad(math.acos(x)))
            elif t == "atg": stack.append(rad(math.atan(x)))

        elif t in ("sto","rcl"):
            if i+1 >= len(tokens):
                raise RPNError("Falta índice de memoria")

            idx = tokens[i+1]
            if not (idx.isdigit() and 0 <= int(idx) <= 9):
                raise RPNError("Memoria inválida")
            idx = int(idx)

            if t == "sto":
                need(1)
                mem[idx] = stack.pop()   # 🔥 FIX
            else:
                stack.append(mem[idx])

            i += 1

        else:
            raise RPNError(f"Token inválido: {t}")

        i += 1

    if len(stack) != 1:
        raise RPNError("La pila no terminó con un solo valor")

    return stack[0]

def main():
    try:
        expr = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("RPN> ")
        print(eval_rpn(expr))
    except RPNError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()