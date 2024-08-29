import random

def generate():
  operators = ["+", "-", "*", "/"]
  operator = operators[random.randint(0, len(operators) - 1)]
  
  num1 = random.randint(0, 10)
  num2 = random.randint(0, 10)
  
  operation = f"{num1} {operator} {num2}"
  
  if operator == "/":
    answer = num1 / num2
  elif operator == "+":
    answer = num1 + num2
  elif operator == "-":
    answer = num1 - num2
  elif operator == "*":
    answer = num1 * num2
  
  return {
    "operation": operation,
    "answer": answer
  }