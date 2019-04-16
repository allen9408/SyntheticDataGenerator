import re

def calculate(l, op, d):
    elements = []
    l = l.split(',')
    for e in l:
        if type(e) in {int, float}:
            elements.append(e)
        elif e in d:
            elements.append(d[e])
        else:
            elements.append(eval(e))
    if op == 'MAX[':
        return max(elements)
    if op == 'MIN[':
        return min(elements)
    if op == 'AVG[':
        return sum(elements)/len(elements)
    if op == 'SUM[':
        return sum(elements)

def parse_rules(rules, d):
    stack = []
    rules = rules.replace(' ', '')
    rules_l = re.split('(\]|MAX\[|MIN\[|AVG\[|SUM\[|\,)', rules)
    rules_l = [r for r in rules_l if r]
    stack = []
    for s in rules_l:
        if s != ']':
            stack.append(s)
        else:
            tmp = []
            while stack and (type(stack[-1]) == int or type(stack[-1]) == float or '[' not in stack[-1]):
                tmp.append(str(stack.pop()))
            res = calculate(''.join(tmp[::-1]), stack.pop(), d)
            stack.append(res)
    if len(stack) != 1:
        print('Syntax error in rules, please check')
        print(stack)
        return

    return stack[0]