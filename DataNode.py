'''Class for synthetic data generator node

Author: Allen Ni

'''
import datetime
import random
import re
import sys

from utils import parse_rules

digits = '0123456789'
lower_letters = 'abcdefghijklmnopqrstuvwxyz'
upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MAX_RETRY = 10

class dnode():
    def __init__(self, name, attrs):
        self.name = name
        self.Type = attrs['Type'].strip()
        self.Range = attrs['Range'].strip()
        self.Logic = attrs['Logic']
        self.Rules = attrs['Rules'].strip()
        self.Pattern = attrs['Pattern'].strip()
        self.generated_value = set()
        self.collection_set = set()
        self.mode = self._get_mode()
        self.min, self.max = None, None
        if self.mode == 'sel':
            self._get_set()
        else:
            self._get_range()

    def _get_mode(self):
        '''Get mode for generating data
        
        sel - select from collection set
        gen - generate by logic or rule
        '''
        if self.Range and self.Range[0] == '{':
            return 'sel'
        else:
            return 'gen'

    def _get_set(self):
        '''Get collection set
        '''
        range_list = re.split('\{|\}|\,', self.Range)
        range_list = [r for r in range_list if r]
        for s in range_list:
            self.collection_set.add(float(s))

    def generate(self, d):
        if self.Rules:
            return self._generate_by_rule(d)

        ret_val = self._generate_by_logic()
        if 'SET' in self.Logic:
            attemp = 0
            while attemp < MAX_RETRY and ret_val in self.generated_value:
                ret_val = self._generate_by_logic()
                attemp += 1
                if attemp == MAX_RETRY:
                    print('Warning: Column - ', self.name, ' already tried for ', MAX_RETRY, 'times, the column contains duplicate values')
        self.generated_value.add(ret_val)
        return ret_val

    def _generate_by_rule(self, d):
        return parse_rules(self.Rules, d)

    def _generate_by_logic(self):
        pass

    def _get_set(self):
        self.collection_set = self.Range[1:-1].split(',')

    def _get_range(self):
        pass

class dnode_DAT(dnode):
    def __init__(self, name, attrs):
        super(dnode_DAT, self).__init__(name, attrs)

    def _get_range(self):
        if not self.Range:
            self.min = datetime.datetime.min
            self.max = datetime.datetime.max
            return
        range_list = re.split('(\[|\]|\(|\)|\,)', self.Range)
        range_list = [r.strip() for r in range_list if r.strip()]
        if range_list[1] == 'inf':
            self.min = datetime.datetime.min
        else:
            self.min = datetime.datetime.strptime(range_list[1], self.Pattern)
            if range_list[0] == '(':
                self.min += datetime.timedelta(days=1)
        if range_list[-2] == 'inf':
            self.max = datetime.datetime.max
        else:
            self.max = datetime.datetime.strptime(range_list[-2], self.Pattern)
            if range_list[-1] == ')':
                self.max -= datetime.timedelta(days=1)

    def _generate_by_logic(self):
        if self.mode == 'sel':
            return random.choice(self.collection_set)
        if 'RAND' in self.Logic:
            delta = (self.max - self.min).days
            sft = random.randint(1, delta)
            new_date = self.min + datetime.timedelta(days=sft)
            return datetime.datetime.strftime(new_date, self.Pattern)
        if 'ASC' in self.Logic:
            ret_date = datetime.datetime.strftime(self.min, self.Pattern)
            self.min += datetime.timedelta(days=1)
            return ret_date
        if 'DESC' in self.Logic:
            ret_date = datetime.datetime.strftime(self.max, self.Pattern)
            self.max -= datetime.timedelta(days=1)
            return ret_date

class dnode_DTM(dnode_DAT):
    def _get_range(self):
        if not self.Range:
            self.min = datetime.datetime.min
            self.max = datetime.datetime.max
            return
        range_list = re.split('(\[|\]|\(|\)|\,)', self.Range)
        range_list = [r.strip() for r in range_list if r.strip()]
        if range_list[1] == 'inf':
            self.min = datetime.datetime.min
        else:
            self.min = datetime.datetime.strptime(range_list[1], self.Pattern)
            if range_list[0] == '(':
                self.min += datetime.timedelta(seconds=1)
        if range_list[-2] == 'inf':
            self.max = datetime.datetime.max
        else:
            self.max = datetime.datetime.strptime(range_list[-2], self.Pattern)
            if range_list[-1] == ')':
                self.max -= datetime.timedelta(seconds=1)
    def _generate_by_logic(self):
        if self.mode == 'sel':
            return random.choice(self.collection_set)
        if 'RAND' in self.Logic:
            delta = (self.max - self.min).seconds
            sft = random.randint(1, delta)
            new_date = self.min + datetime.timedelta(seconds=sft)
            return datetime.datetime.strftime(new_date, self.Pattern)
        if 'ASC' in self.Logic:
            ret_date = datetime.datetime.strftime(self.min, self.Pattern)
            self.min += datetime.timedelta(seconds=1)
            return ret_date
        if 'DESC' in self.Logic:
            ret_date = datetime.datetime.strftime(self.max, self.Pattern)
            # print(ret_date)
            self.max -= datetime.timedelta(seconds=1)
            return ret_date


class dnode_STR(dnode):
    def __init__(self, name, attrs):
        super(dnode_STR, self).__init__(name, attrs)

    def _get_range(self):
        if not self.Range:
            self.min, self.max = 0, sys.maxsize
            return
        range_list = re.split('(\[|\]|\(|\)|\,)', self.Range)
        range_list = [r.strip() for r in range_list if r.strip()]
        if range_list[1] == 'inf':
            self.min = -sys.maxsize + 1
        else:
            if range_list[0] == '(':
                self.min = float(range_list[1] + 1)
            else:
                self.min = float(range_list[1])
        if range_list[-2] == 'inf':
            self.max = sys.maxsize
        else:
            if range_list[-1] == ')':
                self.max = float(range_list[-2] - 1)
            else:
                self.max = float(range_list[-2])

    def _generate_by_logic(self):
        if self.mode == 'sel':
            return random.choice(self.collection_set)
        generate_str = ''
        if self.Pattern:
            patterns = re.split(r'(\\d|\\s|\\S)', self.Pattern)
            # print(patterns)
            for p in patterns:
                if p == r'\s':
                    generate_str += random.choice(lower_letters)
                elif p == r'\S':
                    generate_str += random.choice(upper_letters)
                elif p == r'\d':
                    generate_str += random.choice(digits)
                else:
                    generate_str += p
            return generate_str
        if 'RAND' in self.Logic:
            str_len = random.randint(self.min, self.max)
            for _ in range(str_len):
                generate_str += random.choice(digits + lower_letters + upper_letters)
            return generate_str

class dnode_FLT(dnode):
    def __init__(self, name, attrs):
        super(dnode_FLT, self).__init__(name, attrs)
            
    def _get_range(self):
        if not self.Range:
            self.min, self.max = -sys.maxsize + 1, sys.maxsize
            return
        range_list = re.split('(\[|\]|\(|\)|\,)', self.Range)
        range_list = [r.strip() for r in range_list if r.strip()]
        if range_list[1] == 'inf':
            self.min = -sys.maxsize + 1
        else:
            if range_list[0] == '(':
                self.min = float(range_list[1] + 1e-10)
            else:
                self.min = float(range_list[1])
        if range_list[-2] == 'inf':
            self.max = sys.maxsize
        else:
            if range_list[-1] == ')':
                self.max = float(range_list[-2] - 1e-10)
            else:
                self.max = float(range_list[-2])
    def _generate_by_logic(self):
        if self.mode == 'sel':
            return float(random.choice(self.collection_set))
        if 'ASC' in self.Logic:
            self.min += 1
            return self.min - 1
        if 'DESC' in self.Logic:
            self.max -= 1
            return self.max + 1
        if 'RAND' in self.Logic:
            num = random.uniform(self.min, self.max)
            return num

class dnode_INT(dnode):
    def __init__(self, name, attrs):
        super(dnode_INT, self).__init__(name, attrs)
            
    def _get_range(self):
        if not self.Range:
            self.min, self.max = -sys.maxsize + 1, sys.maxsize
            return

        range_list = re.split('(\[|\]|\(|\)|\,)', self.Range)
        range_list = [r.strip() for r in range_list if r.strip()]
        # print(range_list)
        if range_list[1] == 'inf':
            self.min = -sys.maxsize + 1
        else:
            if range_list[0] == '(':
                self.min = int(range_list[1] + 1)
            else:
                self.min = int(range_list[1])
        if range_list[-2] == 'inf':
            self.max = sys.maxsize
        else:
            if range_list[-1] == ')':
                self.max = int(range_list[-2] - 1)
            else:
                self.max = int(range_list[-2])
    def _generate_by_logic(self):
        if self.mode == 'sel':
            return int(random.choice(self.collection_set))
        if 'ASC' in self.Logic:
            self.min += 1
            return self.min - 1
        if 'DESC' in self.Logic:
            self.max -= 1
            return self.max + 1
        if 'RAND' in self.Logic:
            num = random.randint(self.min, self.max)
            return num

class dnode_CUS(dnode):
    def __init__(self):
        pass

    def generate(self, d):
        pass
