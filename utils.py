import re
from collections import defaultdict
import pdb

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
    rules = re.split('(\]|MAX\[|MIN\[|AVG\[|SUM\[|\,|\+|\-|\*|\/|\(|\))', rules)
    rules_fil = []
    for e in rules:
        if e in d:
            rules_fil.append(str(d[e]))
        else:
            rules_fil.append(e)
    rules_p = ''.join(rules_fil)
    try:
        result = eval(rules_p)
        return result
    except:
        rules_l = re.split('(\]|MAX\[|MIN\[|AVG\[|SUM\[|\,)', rules_p)
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

def get_graph(rules):
    # nodes = set(rules.keys())
    graph = defaultdict(set)
    # pdb.set_trace()
    for n, v in rules.items():
        depend_str = v['Rules']
        depends = re.split('\[|\]|\(|\)|\,|\+|\-|\*|\/', depend_str)
        depends = [d.strip() for d in depends if d.strip()]
        for d in depends:
            if d in rules:
                graph[d].add(n)
    for n in rules:
        if not n in graph:
            graph[n] = set()
    return graph

def t_sort(graph):
    visited = set()
    post_order = []
    
    def dfs(graph, node):
        if node in visited:
            return
        visited.add(node)
        for n in graph[node]:
            dfs(graph, n)
        post_order.append(node)
    
    for n in graph:
        dfs(graph, n)
    return post_order[::-1]

def topological_sort(rules):
    graph = get_graph(rules)
    sort_res = t_sort(graph)
    return sort_res