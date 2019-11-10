import math


def top(a):
    return a[len(a) - 1]           # посмотреть последний элемент списка


def bin_operation(x, y, op):       # выполнение бинарных операций
    x = float(x)
    y = float(y)
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y
    elif op == '^':
        return x ** y


def un_operation(y, op):           # выполнение унарных операций
    y = float(y)
    if op == 'exp':
        return math.exp(y)
    elif op == 'ln':
        return math.log(y)
    elif op == 'sin':
        return math.sin(y)
    elif op == 'cos':
        return math.cos(y)
    elif op == 'sqrt':
        return math.sqrt(y)


def symbols(a):                # разбить всю строку на отдельные элементы: вещ. числа, скобки и все возможные операции
    a = str(a)
    a = a.replace(' ', '')         # на случай, если где-то стоят ненужные пробелы
    a = a.replace('(', ' ( ')      # добавляем нужные пробелы, чтобы потом по ним расплитить
    a = a.replace(')', ' ) ')
    i = 1
    if a[0] == '-':               # минус, как бинарную операцию, нужно разнести пробелами,
        a = ' -1 *' + a[1:]       # а при отрицательном числе его нужно оставить без пробела.
        i += 4                    # если минус перед числом, то он либо в начале строки, либо после открывающейся скобки
    while i < len(a):
        if a[i] == '-':
            if a[i - 2] != '(':
                a = a[:i] + ' - ' + a[i + 1:]
                i += 2
            else:
                a = a[:i] + ' -1 *' + a[i + 1:]
                i += 4
        i += 1
    bin_op = {'+', '*', '/', '^'}
    un_op = {'exp', 'ln', 'sin', 'cos', 'sqrt'}
    for operation in bin_op:                      # добавляем пробелы между остальными операциями
        a = a.replace(operation, ' ' + operation + ' ')
    for operation in un_op:
        a = a.replace(operation, operation + ' ')
    a = a.replace('pi', str(math.pi))             # заменяем pi и e на числовые значения
    a = a.replace(' e ', ' ' + str(math.e) + ' ')
    a = a.split()
    return a


def is_number(str):     # проверка, является ли элемент строки числом
    try:
        float(str)
        return True
    except ValueError:
        return False


numb = []     # стек для чисел
oper = []     # стек для операций и скобок
check = 1
bin_op = {'+', '-', '*', '/', '^'}
un_op = {'exp', 'ln', 'sin', 'cos', 'sqrt'}
order = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'exp': 3, 'ln': 3, 'sin': 3, 'cos': 3, 'sqrt': 3}  # порядок выполнения
a = input()
a = symbols(a)
for i in range(len(a) - 1):
    if a[i] in bin_op and a[i + 1] in bin_op:  # проверка на две идущие подряд операции
        print('Incorrect expression')
        check = 0
        break
    elif a[i] == '(' and a[i + 1] == ')':   # проверка на пустые скобки
        print('Incorrect expression')
        check = 0
        break
    elif is_number(a[i]) and is_number(a[i + 1]): # проверка на два идущих подряд числа
        print('Incorrect expression')
        check = 0
        break
if check:
    if a.count('(') != a.count(')'):    # проверка на равное количество открывающихся и закрывающихся скобок
        print('Incorrect expression')
    else:
        try:
            i = 0
            while i < len(a):
                if is_number(a[i]):
                    numb.append(a[i])       # добавление числа в стек чисел
                    i += 1
                elif a[i] in order:      # для всех операций
                    if (not oper) or (top(oper) == '(') or (order[top(oper)] < order[a[i]]):
                        oper.append(a[i])   # добавление операции в стек операций, если он был пуст,
                        i += 1     # или последний элемент был открывающейся скобкой либо операцией меньшего приоритета
                    else:          # в ином случае нужно сделать последнюю операцию из стека с последним(и) числом(ами)
                        if a[i] in bin_op:
                            y = numb.pop()
                            x = numb.pop()
                            op = oper.pop()
                            numb.append(bin_operation(x, y, op))
                        elif a[i] in un_op:
                            y = numb.pop()
                            op = oper.pop()
                            numb.append(un_operation(y, op))
                elif a[i] == '(':
                    oper.append(a[i])    # добавление открывающейся скобки в стек операций
                    i += 1
                elif a[i] == ')':         # нужно выполнить все операции с конца стека операций,
                    while top(oper) != '(':   # пока не дойдем до открывающейся скобки
                        y = numb.pop()
                        x = numb.pop()
                        op = oper.pop()
                        numb.append(bin_operation(x, y, op))
                    oper.pop()
                    if oper and top(oper) in un_op:
                        y = numb.pop()
                        op = oper.pop()
                        numb.append(un_operation(y, op))
                    i += 1
                else:                          # если элемент строки не число, не операция и не скобка
                    print('Incorrect expression')
                    check = 0
                    break
            if check:
                while oper:                   # выполняем все операции, пока стек операций не пуст
                    y = numb.pop()
                    x = numb.pop()
                    op = oper.pop()
                    numb.append(bin_operation(x, y, op))
                print('{0:.6f}'.format(*numb))  # оставшееся число в стеке чисел - ответ
        except ZeroDivisionError:
            print('Incorrect expression: division by 0')
