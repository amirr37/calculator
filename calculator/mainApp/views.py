from django.shortcuts import render

# Create your views here.
import parser
from copy import copy

Operators = {'+', '-', '*', '/', '(', ')', '^'}  # collection of Operators
Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities of Operators
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def fixNegatives(expression):
    if expression.__contains__('(-'):
        expression = [char for char in expression]

        for index in range(len(expression)):
            if expression[index] == '(' and expression[index + 1] == '-':
                expression.insert(index + 1, '0')
    return "".join(expression)


def fixNumbers(mystr):
    operations = ['+', '-', '*', '/', '(', ')', '^']
    mystr = [char for char in mystr]

    while ' ' in mystr: mystr.remove(' ')
    mystrcopy = []

    for char in mystr:
        if char not in operations:
            if len(mystrcopy) == 0:
                mystrcopy.append(char)
            else:
                if mystrcopy[-1] not in operations:
                    mystrcopy[-1] = mystrcopy[-1] + char
                else:
                    mystrcopy.append(char)
        else:
            mystrcopy.append(char)
    return mystrcopy


def infixToPostfix(expression):
    stack = []  # initialization of empty stack
    expression = fixNumbers(expression)
    output = []

    for character in expression:

        if character not in Operators:  # if an operand append in postfix expression

            output.append(character)

        elif character == '(':  # else Operators push onto stack

            stack.append('(')

        elif character == ')':

            while stack and stack[-1] != '(':
                output.append(stack.pop())

            stack.pop()

        else:

            while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:
                output.append(stack.pop())

            stack.append(character)

    while stack:
        output.append(stack.pop())

    return output


def computer(inputs):
    main_inp = []
    result = 0
    for item in inputs:
        try:
            main_inp.append((int(item)))
            continue

        except:
            main_inp.append(item)

    while True:
        thelen = copy(len(main_inp))
        new_item = None
        index = None
        for index in range(2, len(main_inp)):
            if main_inp[index] == '/' or main_inp[index] == '*' or main_inp[index] == '+' or main_inp[index] == '-' or \
                    main_inp[index] == '^':
                if main_inp[index] == '^':
                    new_item = main_inp[index - 2] ** main_inp[index - 1]
                elif main_inp[index] == '/':
                    new_item = main_inp[index - 2] / main_inp[index - 1]
                elif main_inp[index] == '*':
                    new_item = main_inp[index - 2] * main_inp[index - 1]
                elif main_inp[index] == '+':
                    new_item = main_inp[index - 2] + main_inp[index - 1]
                elif main_inp[index] == '-':
                    new_item = main_inp[index - 2] - main_inp[index - 1]

                main_inp.remove(main_inp[index])
                main_inp.remove(main_inp[index - 1])
                main_inp[index - 2] = new_item
                break
        if thelen == len(main_inp):
            break
    print("after computer : " + str(main_inp))
    return main_inp[-1]


def get_result(string=None):
    return computer(infixToPostfix(fixNegatives(string)))


def main(request):
    context = {}
    if request.method == 'POST':
        context = {'result': get_result(request.POST['my_string'])}
    else:
        context = {'result': None}
    return render(request, 'mainApp/index.html', context)
