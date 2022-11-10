import os
import math
import re

tokens = []
token_info = []

numbers = []
operator = []
specials = []
results = []
var_names = []
variables = {}
lexemes = []
calculations = ''


def matcher(contas):
	for s in contas:
		tokens.clear()
		while (s != ''):
			matched = False
			s = s.strip()
			for token in token_info:
				equals = re.match(token[0], s)
				if equals != None and equals.group() != '':
					matched = True
					s = re.sub(token[0], '', s, 1)
					tokens.append((token[1], equals.group(0)))
					lexemes.append(equals.group(0))
					break
			if not matched:
				print(
				 f"\nLinha {calculations.index(calculus)+1}: lexemas {[s[0]]} inválidos")
				raise Exception(f"\nLinha {calculations.index(calculus)+1}: Erro léxico")
				break
		validate()


def validate():
	for token in tokens:
		if token[0] == "NUMERO":
			numbers.append(token[1])
		if token[0] == "OPERADORES":
			operator.append(token[1])
		if token[0] == "ESPECIAIS":
			specials.append(token[1])
		if token[0] == "RESULTADO":
			results.append(token[1])
		if token[0] == "VARIAVEL":
			var_names.append(token[1])
			if token[1] in variables:
				numbers.append(variables[token[1]])
				results.remove(variables[token[1]])
	calculate()


def calculate():
	if (len(operator) == 0):
		results.append(numbers[0])
		numbers.pop(0)
		saveVar()

	for op in operator[::-1]:
		if op == "+":
			calculations = float(numbers[0]) + float(numbers[1])
			remove(2)
		elif op == "-":
			calculations = float(numbers[0]) - float(numbers[1])
			remove(2)
		elif op == "*":
			calculations = float(numbers[0]) * float(numbers[1])
			remove(2)
		elif op == "/":
			calculations = float(numbers[0]) / float(numbers[1])
			remove(2)
		elif op == "exp":
			calculations = float(numbers[0])**float(numbers[1])
			remove(2)
		elif op == "rot":
			calculations = float(numbers[0])**(1 / float(numbers[1]))
			remove(2)
		elif op == "sin":
			calculations = math.sin(float(math.radians(float(numbers[0]))))
			remove(1)
		elif op == "cos":
			calculations = math.cos(float(math.radians(float(numbers[0]))))
			remove(1)

		numbers.append(calculations)
		results.append(calculations)

		if "?" in specials:
			redo()
		if len(var_names) != 0:
			saveVar()


def redo():
	for especial in specials:
		if especial == "?":
			numbers.append(results[-1])


def remove(n):
	for i in range(n):
		numbers.pop(0)
	operator.pop(0)


def saveVar():
	for nome in var_names:
		if nome not in variables.keys():
			variables[nome] = results[-1]


def clean():
	numbers.clear()
	tokens.clear()
	specials.clear()


def readFile(archive):
	arch = open(archive, 'r')
	lines = arch.readlines()
	arch.close()
	return lines


# um jeito mais eficiente de executar os casos de teste agrupados em diretorio
if __name__ == '__main__':
	calculations = []
	dir = "/home/runner/Interpretador/tests/"

	for archive in os.listdir(dir):
		with open(dir + archive, 'r') as arch:
			quantity = arch.readline()
			for i in range(int(quantity)):
				line = arch.readline()
				line = re.split(r'\).\(', line)
				calculations.append(line)
			arch.close()

	token_info.append(('[\?|\(|\)|\|;]', "ESPECIAIS"))
	token_info.append(("\+|\-|\/|\*|sin|cos|rot|exp", "OPERADORES"))
	token_info.append(("[0.-9.]*", "NUMERO"))
	token_info.append(('[A-Za-z0-9]*', "VARIAVEL"))

	for calculus in calculations:
		try:
			matcher(calculus)
			str_calculo = ""
			print(
			 f"\nLinha {calculations.index(calculus)+1}: lexemas {lexemes} todos válidos"
			)
			print(f"\nLinha {calculations.index(calculus)+1}: sintaxe: correta")
			print(f"\nLinha {calculations.index(calculus)+1}: resposta: %.3f" %
			      float(results[-1]))
			numbers = []
			operator = []
			specials = []
			results = []
			var_names = []
			variables = {}
			lexemes = []
		except Exception:
			print(f"\nLinha {calculations.index(calculus)+1}: sintaxe: incorreta")
