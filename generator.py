import pandas as pd
import sys, pdb, getopt

from DataNode import *
from utils import topological_sort

class generator():
    def __init__(self, rules):
        if type(rules) == dict:
            self.rules = rules
        else:
            self.rules = self._init_dict(rules)
        self.nodes = {}
        self.columns = []
        self._init_nodes()
        self.result = []
        # pdb.set_trace()
        self.gen_order = self._get_gen_order()
        self.out_order = self._get_out_order()

    def get_columns(self):
        return self.rules

    def add_column(self, name, d):
        self.rules[name] = d

    def _get_out_order(self):
        orders = [(v['OutIdx'], k) for k,v in self.rules.items()]
        orders.sort()
        return [o[1] for o in orders]

    def _get_gen_order(self):
        return topological_sort(self.rules)


    def _init_dict(self, rules):
        df = pd.read_excel(rules, index_col=0)
        rules_d = {}
        for n in df.columns:
            d_tmp = {}
            d_type    = str(df[n]['Type'])
            d_range   = str(df[n]['Range'])
            d_logic   = str(df[n]['Logic'])
            d_rules   = str(df[n]['Rules'])
            d_pattern = str(df[n]['Pattern'])
            d_tmp['Type']    = d_type if d_type != 'nan' else ''
            d_tmp['Range']   = d_range if d_range != 'nan' else ''
            d_tmp['Logic']   = set(d_logic.split(',')) if d_logic != 'nan' else {'RAND'}
            d_tmp['Rules']   = d_rules if d_rules != 'nan' else ''
            d_tmp['Pattern'] = d_pattern if d_pattern != 'nan' else ''
            d_tmp['OutIdx'] = int(df[n]['OutIdx'])
            rules_d[n] = d_tmp
        return rules_d
    def _init_nodes(self):
        nodes_dict = {
            'INT': dnode_INT,
            'FLOAT': dnode_FLT,
            'CHAR': dnode_STR,
            'DATE': dnode_DAT,
            'DTTM': dnode_DTM,
            'CUST': dnode_CUS
        }
        for name, attrs in self.rules.items():
            self.columns.append(name)
            # self.nodes.append(nodes_dict[attrs['Type']](name, attrs))
            self.nodes[name] = nodes_dict[attrs['Type']](name, attrs)

    def gen(self, num):
        # result = []
        for i in range(num):
            res = []
            d = {}
            for name in self.gen_order:
                # print(name)
            # for name, n in zip(self.columns, self.nodes):
                n = self.nodes[name]
                val = n.generate(d)
                d[name] = val
            for name in self.out_order:
                res.append(d[name])
            self.result.append(res)
        # return result

    def to_csv(self, file_dir):
        df = pd.DataFrame(self.result, columns=self.out_order)
        df.to_csv(file_dir, index=False)

    def to_excel(self, file_dir):
        df = pd.DataFrame(self.result, columns=self.out_order)
        df.to_excel(file_dir, index=False)


if __name__ == '__main__':
    Columns = {
        'ID'       :{'Type': 'INT', 'Range': '[0, inf]', 'Logic': {'ASC'}, 'Rules':'', 'Pattern':''},
        'DATE_ASC' :{'Type': 'DATE', 'Range': '[1994/01/01, 2019/04/11]', 'Logic': {'ASC'}, 'Rules':'', 'Pattern':'%Y/%m/%d'},
        'DATE_DESC':{'Type': 'DATE', 'Range': '[1994/01/01, 2019/04/11]', 'Logic': {'DESC'}, 'Rules':'', 'Pattern':'%Y/%m/%d'},
        'DATE_RAND':{'Type': 'DATE', 'Range': '[1994/01/01, 2019/04/11]', 'Logic': {'RAND'}, 'Rules':'', 'Pattern':'%Y/%m/%d'},
        'TIME_ASC' :{'Type': 'DTTM', 'Range': '[00:00:00, 23:59:59]', 'Logic':{'ASC'}, 'Rules':'', 'Pattern':'%H:%M:%S'},
        'TIME_DESC':{'Type': 'DTTM', 'Range': '[00:00:00, 23:59:59]', 'Logic':{'DESC'}, 'Rules':'', 'Pattern':'%H:%M:%S'},
        'TIME_RAND':{'Type': 'DTTM', 'Range': '[00:00:00, 23:59:59]', 'Logic':{'RAND', 'SET'}, 'Rules':'', 'Pattern':'%H:%M:%S'},
        'STR_RAND' :{'Type': 'CHAR', 'Range': '[8,20]', 'Logic': {'RAND'}, 'Rules':'', 'Pattern':''},
        'STR_SEL'  :{'Type': 'CHAR', 'Range': '{good,moderate,bad}', 'Logic': {'RAND'}, 'Rules':'', 'Pattern':''},
        'STR_PATT' :{'Type': 'CHAR', 'Range': '', 'Logic': {'RAND'}, 'Rules':'', 'Pattern':'\d\dCMB\d\d\d\s\s'},
        'num'      :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_1'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_2'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_3'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_4'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_5'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_6'    :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {'RAND','SET'}, 'Rules':'', 'Pattern':''},    
        'num_MAX'  :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {}, 'Rules':'MAX[num, num_1, num_2, num_3, num_4, num_5, num_6]', 'Pattern':''},
        'num_CAL'  :{'Type': 'FLOAT', 'Range': '[-2.0, 2.0]', 'Logic': {}, 'Rules':'MAX[num_1, MIN[num_2, num_3, num_5], num_6, AVG[num_1, num_2, 1/(0.6)*SUM[num_5, num_6, num_1, (2+5)*8]*0.6, num_3], num_2]', 'Pattern':''},
    }
    
    input_file = 'input_example.xlsx'
    output_file = 'output_example.xlsx'
    num_gen = 100
    
    if len(sys.argv) > 1:
        # pdb.set_trace()
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:n:",["ifile=","ofile=","gen_num="])
        for opt, arg in opts:
            if opt == '-h':
                print('python3 generator.py -i <input_file> -o <output_file> -n <generate_num>')
                sys.exit()
            elif opt == '-i':
                input_file = arg
            elif opt == '-o':
                output_file = arg
            elif opt == '-n':
                num_gen = int(arg)

    # Define table structure by code
    # g = generator(Columns)
    # Define table structure by input file
    g = generator(input_file)
    # generate 100 synthetic data
    g.gen(num_gen)
    # save result to excel
    g.to_excel(output_file)


