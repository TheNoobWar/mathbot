# Successfull burning attack: f = (x, h) -> if (h - 40, f(x * 2, h + 1) + f(x * 2 + 1, h + 1), 0)

import json
import asyncio
import traceback
import sys

import calculator.new_interpereter as calc
import calculator.attempt6 as parser
import calculator.bytecode as bytecode
from calculator.runtime import wrap_with_runtime

def run_with_timeout(future, timeout = None):
	loop = asyncio.get_event_loop()
	future = asyncio.wait_for(future, timeout = timeout)
	return loop.run_until_complete(future)


def print_token_parse_caret(to):
	print(' '.join(to.tokens))
	print((sum(map(len, to.tokens[:to.rightmost])) + to.rightmost) * ' ' + '^')

ERROR_TEMPLATE = '''\
{prev}
{cur}
{carat}
{next}
'''


def format_parse_error(message, string, position):
	lines = [' '] + string.split('\n') + [' ']
	line = 1
	while position > len(lines[line]):
		position -= len(lines[line]) + 1
		line += 1
	length = len(string)
	return ERROR_TEMPLATE.format(
		prev = lines[line - 1],
		cur = lines[line],
		next = lines[line + 1],
		carat = ' ' * (position - 1) + '^'
	)


if __name__ == '__main__':

	if len(sys.argv) == 1:

		show_tree = False
		show_parsepoint = False
		interpereter = calc.Interpereter(wrap_with_runtime(bytecode.CodeBuilder(), None))
		interpereter.run()

		while True:
			line = input('> ')
			if line == '':
				break
			elif line == ':tree':
				show_tree = not show_tree
			elif line == ':parsepoint':
				show_parsepoint = not show_parsepoint
			else:
				tokens, ast = parser.parse(line)
				# print(json.dumps(ast, indent = 4))
				interpereter.prepare_extra_code({
					'#': 'program',
					'items': [ast]
				})
				# for index, byte in enumerate(bytes):
				# 	print('{:3d} - {}'.format(index, byte))
				print(run_with_timeout(interpereter.run_async(), 5))


	elif len(sys.argv) == 2:

		filename = sys.argv[1]
		if filename[0] == '+':
			filename = './calculator/scripts/' + filename[1:] + '.c5'
		code = open(filename).read()
		try:
			print(c.calculate(code))
		except calculator.attempt6.ParseFailed as e:
			print(format_parse_error('error', code, e.position))

	else:

		print('???')