import sys
import operator
from pyparsing import nums, oneOf, Word, Literal, Suppress
from pyparsing import ParseException, Forward, Group

op_map = { '*' : operator.mul, \
           '+' : operator.add, \
           '/' : operator.div, \
           '-' : operator.sub}

exp = Forward()

number = Word(nums).setParseAction(lambda s, l, t: int(t[0]))
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()
op = oneOf('+ - * /').setResultsName('op').setParseAction(lambda s, l, t: op_map[t[0]])

exp << Group(lparen + op + (number | exp) + (number | exp) + rparen)

def processArg(arg):
    if isinstance(arg, int):
        return arg
    else:
        return processList(arg)

def processList(lst):
    args = [processArg(x) for x in lst[1:]]
    return lst.op(args[0], args[1])


def handleLine(line):
    result = exp.parseString(line)
    return processList(result[0])

while True:
    try:
        print handleLine(raw_input('> '))
    except ParseException, e:
        print >>sys.stderr, \
            "Syntax error at position %d: %s" % (e.col, e.line)
    except ZeroDivisionError:
        print >>sys.stderr, \
            "Division by zero error"



