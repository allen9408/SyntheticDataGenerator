import re
from collections import defaultdict
import pdb
import datetime
from vertica_python import connect
import os

def get_rules_from_db(host, user, password, database, schema, table_name):
    conn_info = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
        }
    print(conn_info)
    connection = connect(**conn_info)
    cur = connection.cursor('dict')
    command = '''select * from v_catalog.columns
        where table_schema=\'''' + schema + '''\' and table_name=\'''' + table_name + '''\';'''
    print(command)
    # pdb.set_trace()
    cur.execute(command)
    columns_d = cur.fetchall()
    connection.close()
    return parse_rules_db(columns_d)

def upload_to_db(host, user, password, database, schema, table_name):
    conn_info = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
        }
    connection = connect(**conn_info)
    cur = connection.cursor('dict')
    # cwd = os.getcwd()
    # command =  '''COPY ''' + schema + '''.''' + table_name + ''' FROM LOCAL \'''' + cwd + '''\\output_ui.csv' DELIMITER ',' NULL '';'''     
    # print(command)
    # cur.copy(command)
    # print(cur.fetchall())
    command =  '''COPY ''' + schema + '''.''' + table_name + ''' FROM STDIN DELIMITER ',' NULL '';'''     
    with open('output_ui.csv', 'rb') as f:
        cur.copy(command, f)
    connection.close()
    print('Upload complete')

def parse_rules_db(columns_d):
    result_d = {}
    for column in columns_d:
        name = column['column_name']
        tmp_d = {}
        tmp_d['OutIdx'] = column['ordinal_position']
        if column['data_type'] == 'int':
            tmp_d['Type'] = 'INT'
            tmp_d['Range'] = '[1, 10000]'
            if 'nbr' in name.lower() or 'id' in name.lower():
                tmp_d['Logic'] = {'RAND', "DISTINCT"}
            else:
                tmp_d['Logic'] = {'RAND'}
            tmp_d['Rules'] = ''
            tmp_d['Pattern'] = ''
        elif column['data_type'] == 'float':
            tmp_d['Type'] = 'FLOAT'
            tmp_d['Range'] = '[1, 1000000]'
            tmp_d['Logic'] = {'RAND'}
            tmp_d["Rules"] = ''
            tmp_d['Pattern'] = '%.2f'
        elif column['data_type'] == 'date':
            tmp_d['Type'] = 'DATE'
            cur_date = datetime.datetime.strftime(datetime.datetime.now(),'%Y/%m/%d')
            prev_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=100) ,'%Y/%m/%d')
            tmp_d['Range'] = '[' + prev_date + ',' + cur_date + ']'
            tmp_d['Logic'] = {'RAND'}
            tmp_d['Rules'] = ''
            tmp_d['Pattern'] = '%Y/%m/%d'
        else:
            tmp_d['Type'] = 'CHAR'
            tmp_d['Range'] = '[8,20]'
            tmp_d['Logic'] = {'RAND'}
            tmp_d['Rules'] = ''
            tmp_d['Pattern'] = ''
        result_d[name] = tmp_d
    return result_d

def guess_rules_from_name(name, idx):
    tmp_d = {}
    if 'nbr' in name.lower() or 'cnt' in name.lower():
        tmp_d['Type'] = 'INT'
        tmp_d['Range'] = '[1, 10000]'
        tmp_d['Logic'] = {'RAND'}
        tmp_d["Rules"] = ''
        tmp_d['Pattern'] = ''
        tmp_d['OutIdx'] = idx
    elif 'amt' in name.lower() or 'fee' in name.lower():
        tmp_d['Type'] = 'FLOAT'
        tmp_d['Range'] = '[1, 1000000]'
        tmp_d['Logic'] = {'RAND'}
        tmp_d["Rules"] = ''
        tmp_d['Pattern'] = '%.2f'
        tmp_d['OutIdx'] = idx
    elif 'dat' in name.lower():
        tmp_d['Type'] = 'DATE'
        cur_date = datetime.datetime.strftime(datetime.datetime.now(),'%Y/%m/%d')
        prev_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=100) ,'%Y/%m/%d')
        tmp_d['Range'] = '[' + prev_date + ',' + cur_date + ']'
        tmp_d['Logic'] = {'RAND'}
        tmp_d['Rules'] = ''
        tmp_d['Pattern'] = '%Y/%m/%d'
        tmp_d['OutIdx'] = idx
    else:
        tmp_d['Type'] = 'CHAR'
        tmp_d['Range'] = '[8,20]'
        tmp_d['Logic'] = {'RAND'}
        tmp_d['Rules'] = ''
        tmp_d['Pattern'] = ''
        tmp_d['OutIdx'] = idx
    return tmp_d


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

def parse_rules_str(rules, d):
    rules = rules.replace(' ', '')
    rules = rules.split('+')
    result = [str(d.get(r, r)) for r in rules]
    return ''.join(result)

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