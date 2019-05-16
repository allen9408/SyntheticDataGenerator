from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
from generator import *
import pdb
from utils import get_rules_from_db

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.g = generator({})
        self.init_ui()
        self.init_top()
        self.init_left()
        self.init_right()
        # self.beauty_main()
        self.beauty_top()
        self.beauty_left()
        self.beauty_right()
        self.data_columns = [
            [1,2,3,4,5,6],
            [7,8,9,10,11,12]]
        # self.init_generator()
        # self.show_table()

    def init_generator(self):
        self.g = generator(self.input_file)

    def show_table(self):
        # column = self.g.get_columns()
        # print(column)
        # row_idx = 0
        # for n in self.g.get_in_order():
        #     r = column[n]
        #     self.right_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(n))
        #     self.right_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(r['Type']))
        #     self.right_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(r['Range']))
        #     self.right_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(r['Logic'])))
        #     self.right_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(r['Rules']))
        #     self.right_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(r['Pattern']))
        #     self.right_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(r['OutIdx'])))
        #     row_idx += 1
        self.timer = QtCore.QTimer()
        self.change_flag = True
        # self.timer.timeout.connect(self.show_table)
        self.timer.timeout.connect(self.show_table_content)
        self.timer.start(500)

    def show_table_content(self):
        column = self.g.get_columns()
        row_idx = 0
        for n in self.g.get_out_order():
            r = column[n]
            self.right_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(n))
            self.right_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(r['Type']))
            self.right_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(r['Range']))
            self.right_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(r['Logic'])))
            self.right_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(r['Rules']))
            self.right_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(r['Pattern']))
            self.right_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(r['OutIdx'])))
            row_idx += 1



    @QtCore.pyqtSlot()
    def update_table(self, col_name):
        cols = self.g.get_columns()
        row_idx = len(cols) - 1
        n, r = col_name, cols[col_name]
        self.right_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(n))
        self.right_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(r['Type']))
        self.right_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(r['Range']))
        self.right_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(r['Logic'])))
        self.right_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(r['Rules']))
        self.right_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(r['Pattern']))
        self.right_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(r['OutIdx'])))



    def init_ui(self):
        self.setFixedSize(1024,700)
        self.setWindowTitle('SQL DATA GENERATOR')
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.top_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.top_widget.setLayout(self.top_layout) # 设置左侧部件布局为网格

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.top_widget, 0,0,3,10)
        self.main_layout.addWidget(self.left_widget,3,0,12,4) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,3,4,12,6) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件


    def left_add_op(self):
        # print('add_button trig')
        try:
            input_d = {}
            col_name = self.name_input.text()
            input_d['Type'] = self._get_type()
            input_d['Range'] = self.range_input.text()
            input_d['Logic'] = self._get_logic()
            input_d['Rules'] = self.rule_input.text()
            input_d['Pattern'] = self.pattern_input.text()
            input_d['OutIdx'] = int(self.outidx_input.text())
            # print(input_d)
            self.g.add_column(col_name, input_d)
            self.show_table()
            self.msg_content.setText('Add Complete')
        except Exception as e:
            self.msg_content.setText('Error:' + str(e))
        # print(self.left_add.isEnabled())

    def left_browse_op(self):
        try:
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose input excel file", "","All Files (*);;Excel Files (*.xlsx)", options=options)
            print('browse:', file_name)
            self.input_file = file_name
            self.init_generator()
            self.show_table()
        except Exception as e:
            self.msg_content.setText('Error: ' + str(e))

    def generate_op(self):
        try:
            gen_num = int(self.gennum_input.text())
            for i in range(gen_num):
                self.g.gen(1)
                self.process_bar.setValue(int((i+1)/gen_num*100))
            self.g.to_csv('output_ui.csv')
        except Exception as e:
            self.msg_content.setText('Error: ' + str(e))

    def upload_op(self):
        try:
            self.msg_content.setText('Uploading ... ')
            host = self.db_ip_input.text().strip()
            user = self.db_user_input.text().strip()
            password = self.db_pswd_input.text()
            database = self.db_db_input.text().strip()
            schema = self.tb_sc_input.text().strip()
            table_name = self.tb_na_input.text().strip()
            upload_to_db(host, user, password, database, schema, table_name)
            self.msg_content.setText('Upload successful!')
        except Exception as e:
            self.msg_content.setText('Error: ' + str(e))


    def _get_type(self):
        type_ckbox_d = {
            'INT': self.type_int,
            'FLOAT': self.type_flt,
            'CHAR':self.type_str,
            'DATE':self.type_dat,
            'DTTM':self.type_dtm
        }
        for k, v in type_ckbox_d.items():
            if v.isChecked():
                return k
    def _get_logic(self):
        res = set()
        logic_ckbox_d = {
            'ASC': self.logic_asc,
            'DESC': self.logic_desc,
            'RAND': self.logic_rand,
            'DISTINCT': self.logic_set
        }
        for k, v in logic_ckbox_d.items():
            if v.isChecked():
                res.add(k)
        return res

    def int_click(self, state):
        type_boxes = [self.type_flt, self.type_str, self.type_dat, self.type_dtm]
        for cb in type_boxes:
            cb.setCheckState(QtCore.Qt.Unchecked)
    def flt_click(self, state):
        type_boxes = [self.type_int, self.type_str, self.type_dat, self.type_dtm]
        for cb in type_boxes:
            cb.setCheckState(QtCore.Qt.Unchecked)
    def str_click(self, state):
        type_boxes = [self.type_int, self.type_flt, self.type_dat, self.type_dtm]
        for cb in type_boxes:
            cb.setCheckState(QtCore.Qt.Unchecked)
    def dat_click(self, state):
        type_boxes = [self.type_int, self.type_flt, self.type_str, self.type_dtm]
        for cb in type_boxes:
            cb.setCheckState(QtCore.Qt.Unchecked)
    def dtm_click(self, state):
        type_boxes = [self.type_int, self.type_flt, self.type_str, self.type_dat]
        for cb in type_boxes:
            cb.setCheckState(QtCore.Qt.Unchecked)

    def asc_click(self, state):
        if self.logic_asc.isChecked():
            self.logic_desc.setCheckState(QtCore.Qt.Unchecked)
            self.logic_rand.setCheckState(QtCore.Qt.Unchecked)
            self.logic_set.setCheckState(QtCore.Qt.Checked)
    def desc_click(self, state):
        if self.logic_desc.isChecked():
            self.logic_asc.setCheckState(QtCore.Qt.Unchecked)
            self.logic_rand.setCheckState(QtCore.Qt.Unchecked)
            self.logic_set.setCheckState(QtCore.Qt.Checked)
    def rand_click(self, state):
        if self.logic_rand.isChecked():
            self.logic_desc.setCheckState(QtCore.Qt.Unchecked)
            self.logic_asc.setCheckState(QtCore.Qt.Unchecked)
    def set_click(self, state):
        pass

    def table_click_op(self):
        try:
            r = self.right_table.currentRow()
            if not self.right_table.item(r, 0):
                return
            name = self.right_table.item(r, 0).text()
            typ = self.right_table.item(r, 1).text()
            rang = self.right_table.item(r, 2).text()
            logic = self.right_table.item(r, 3).text()
            rule = self.right_table.item(r, 4).text()
            pattern = self.right_table.item(r, 5).text()
            outidx = self.right_table.item(r, 6).text()

            # set name
            self.name_input.setText(name)
            # set type
            if typ == 'INT':
                self.type_int.setCheckState(QtCore.Qt.Checked)
                type_boxes = [self.type_flt, self.type_str, self.type_dat, self.type_dtm]
            elif typ == 'FLOAT':
                self.type_flt.setCheckState(QtCore.Qt.Checked)
                type_boxes = [self.type_int, self.type_str, self.type_dat, self.type_dtm]
            elif typ == 'CHAR':
                self.type_str.setCheckState(QtCore.Qt.Checked)
                type_boxes = [self.type_flt, self.type_int, self.type_dat, self.type_dtm]
            elif typ == 'DATE':
                self.type_dat.setCheckState(QtCore.Qt.Checked)
                type_boxes = [self.type_flt, self.type_str, self.type_int, self.type_dtm]
            elif typ == 'DTTM':
                self.type_dtm.setCheckState(QtCore.Qt.Checked)
                type_boxes = [self.type_flt, self.type_str, self.type_int, self.type_int]
            for cb in type_boxes:
                cb.setCheckState(QtCore.Qt.Unchecked)
            # set range
            self.range_input.setText(rang)
            # set logic
            if 'ASC' in logic:
                self.logic_asc.setCheckState(QtCore.Qt.Checked)
            if 'DESC' in logic:
                self.logic_desc.setCheckState(QtCore.Qt.Checked)
            if 'RAND' in logic:
                self.logic_rand.setCheckState(QtCore.Qt.Checked)
            if 'DISTINCT' in logic:
                self.logic_set.setCheckState(QtCore.Qt.Checked)
            # set rules
            self.rule_input.setText(rule)
            self.pattern_input.setText(pattern)
            self.outidx_input.setText(outidx)
        except Exception as e:
            self.msg_content.setText('Error: ' + str(e))

    def pull_db_op(self):
        try:
            host = self.db_ip_input.text()
            user = self.db_user_input.text()
            password = self.db_pswd_input.text()
            database = self.db_db_input.text()
            schema = self.tb_sc_input.text()
            table_name = self.tb_na_input.text()
            self.msg_content.setText('Connecting database ... ')
            rule_d = get_rules_from_db(host, user, password, database, schema, table_name)
            self.msg_content.setText('Initializing table ...')
            self.g = generator(rule_d)
            self.show_table()
            self.msg_content.setText('Complete pulling')
        except Exception as e:
            self.msg_content.setText('Error: ' + str(e))

    def init_top(self):
        self.db_widget = QtWidgets.QWidget()
        self.db_layout = QtWidgets.QGridLayout()

        self.db_ip_label = QtWidgets.QLabel('Server: ')
        self.db_ip_label.setFont(qtawesome.font('fa', 12))
        self.db_ip_input = QtWidgets.QLineEdit()

        self.db_user_label = QtWidgets.QLabel('User: ')
        self.db_user_label.setFont(qtawesome.font('fa', 12))
        self.db_user_input = QtWidgets.QLineEdit()

        self.db_pswd_label = QtWidgets.QLabel('Password: ')
        self.db_pswd_label.setFont(qtawesome.font('fa', 12))
        self.db_pswd_input = QtWidgets.QLineEdit()
        self.db_pswd_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.db_db_label = QtWidgets.QLabel('Database: ')
        self.db_db_label.setFont(qtawesome.font('fa', 12))
        self.db_db_input = QtWidgets.QLineEdit()

        self.db_layout.addWidget(self.db_ip_label, 0, 0)
        self.db_layout.addWidget(self.db_ip_input, 0, 1)
        self.db_layout.addWidget(self.db_user_label, 0, 3)
        self.db_layout.addWidget(self.db_user_input, 0, 4)
        self.db_layout.addWidget(self.db_pswd_label, 0, 5)
        self.db_layout.addWidget(self.db_pswd_input, 0, 6)

        self.db_widget.setLayout(self.db_layout)
        self.top_layout.addWidget(self.db_widget, 0, 0, 1, 10)

        self.tb_widget = QtWidgets.QWidget()
        self.tb_layout = QtWidgets.QGridLayout()

        self.tb_sc_label = QtWidgets.QLabel('Schema: ')
        self.tb_sc_label.setFont(qtawesome.font('fa', 12))
        self.tb_sc_input = QtWidgets.QLineEdit()

        self.tb_na_label = QtWidgets.QLabel('Table: ')
        self.tb_na_label.setFont(qtawesome.font('fa', 12))
        self.tb_na_input = QtWidgets.QLineEdit()

        self.db_pull_btn = QtWidgets.QPushButton("Pull")
        self.db_pull_btn.clicked[bool].connect(self.pull_db_op)

        self.tb_layout.addWidget(self.db_db_label, 0, 0)
        self.tb_layout.addWidget(self.db_db_input, 0, 1)
        self.tb_layout.addWidget(self.tb_sc_label, 0, 2)
        self.tb_layout.addWidget(self.tb_sc_input, 0, 3)
        self.tb_layout.addWidget(self.tb_na_label, 0, 4)
        self.tb_layout.addWidget(self.tb_na_input, 0, 5)
        self.tb_layout.addWidget(self.db_pull_btn, 0, 6)

        self.tb_widget.setLayout(self.tb_layout)
        self.top_layout.addWidget(self.tb_widget, 1, 0, 1, 10)

    def init_left(self):
        self.left_add = QtWidgets.QPushButton("Add") # 关闭按钮
        self.left_reset = QtWidgets.QPushButton("Reset") # 空白按钮
        self.left_browse = QtWidgets.QPushButton("Browse")  # 最小化按钮
        self.left_add.clicked[bool].connect(self.left_add_op)
        self.left_browse.clicked[bool].connect(self.left_browse_op)
        # self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_browse, 16, 0,1,1)
        self.left_layout.addWidget(self.left_add, 16, 2,1,1)
        self.left_layout.addWidget(self.left_reset, 16, 1, 1, 1)

        self.name_label = QtWidgets.QLabel('Column Name: ')
        self.name_label.setFont(qtawesome.font('fa', 14))
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Please input the column name")
        self.left_layout.addWidget(self.name_label,1,0,1,5)
        self.left_layout.addWidget(self.name_input,2,0,1,5)

        self.type_label = QtWidgets.QLabel('Type: ')
        self.type_label.setFont(qtawesome.font('fa', 14))
        self.left_layout.addWidget(self.type_label,3,0,1,5)
        self.type_widget = QtWidgets.QWidget()
        self.type_layout = QtWidgets.QGridLayout()
        self.type_widget.setLayout(self.type_layout)
        self.type_int = QtWidgets.QCheckBox('INT')
        self.type_flt = QtWidgets.QCheckBox('FLOAT')
        self.type_str = QtWidgets.QCheckBox('CHAR')
        self.type_dat = QtWidgets.QCheckBox('DATE')
        self.type_dtm = QtWidgets.QCheckBox('DTTM')

        self.type_int.clicked.connect(self.int_click)
        self.type_flt.clicked.connect(self.flt_click)
        self.type_str.clicked.connect(self.str_click)
        self.type_dat.clicked.connect(self.dat_click)
        self.type_dtm.clicked.connect(self.dtm_click)

        self.type_layout.addWidget(self.type_int, 0,0)
        self.type_layout.addWidget(self.type_flt, 0,1)
        self.type_layout.addWidget(self.type_str, 0,2)
        self.type_layout.addWidget(self.type_dat, 0,3)
        self.type_layout.addWidget(self.type_dtm, 0,4)
        self.left_layout.addWidget(self.type_widget, 4,0,1,5)

        self.range_label = QtWidgets.QLabel('Range: ')
        self.range_label.setFont(qtawesome.font('fa', 14))
        self.range_input = QtWidgets.QLineEdit()
        self.range_input.setPlaceholderText('[]/()/[)/(] for range, {} for set')
        self.left_layout.addWidget(self.range_label, 5,0,1,1)
        self.left_layout.addWidget(self.range_input, 6,0,1,3)

        self.logic_label = QtWidgets.QLabel('Logic: ')
        self.logic_label.setFont(qtawesome.font('fa', 14))
        self.left_layout.addWidget(self.logic_label, 7,0,1,5)
        self.logic_widget = QtWidgets.QWidget()
        self.logic_layout = QtWidgets.QGridLayout()
        self.logic_widget.setLayout(self.logic_layout)
        self.logic_asc = QtWidgets.QCheckBox('ASC')
        self.logic_desc = QtWidgets.QCheckBox('DESC')
        self.logic_rand = QtWidgets.QCheckBox('RAND')
        self.logic_set = QtWidgets.QCheckBox('DISTINCT')
        self.logic_layout.addWidget(self.logic_asc, 0,0,1,1)
        self.logic_layout.addWidget(self.logic_desc, 0,1,1,1)
        self.logic_layout.addWidget(self.logic_rand, 0,2,1,1)
        self.logic_layout.addWidget(self.logic_set, 0,3,1,1)
        self.left_layout.addWidget(self.logic_widget, 8,0,1,5)

        self.logic_asc.clicked.connect(self.asc_click)
        self.logic_desc.clicked.connect(self.desc_click)
        self.logic_rand.clicked.connect(self.rand_click)
        self.logic_set.clicked.connect(self.set_click)

        self.rule_label = QtWidgets.QLabel('Rules: ')
        self.rule_label.setFont(qtawesome.font('fa', 14))
        self.rule_input = QtWidgets.QLineEdit()
        self.rule_input.setPlaceholderText('+ - * / MAX[] MIN[] SUM[] AVG[]')
        self.left_layout.addWidget(self.rule_label, 9,0,1,1)
        self.left_layout.addWidget(self.rule_input, 10,0,1,5)

        self.pattern_label = QtWidgets.QLabel('Patterns: ')
        self.pattern_label.setFont(qtawesome.font('fa', 14))
        self.pattern_input = QtWidgets.QLineEdit()
        self.pattern_input.setPlaceholderText('')
        self.left_layout.addWidget(self.pattern_label, 11,0,1,2)
        self.left_layout.addWidget(self.pattern_input, 12,0,1,5)

        self.outidx_label = QtWidgets.QLabel('OutIdx: ')
        self.outidx_label.setFont(qtawesome.font('fa', 14))
        self.outidx_input = QtWidgets.QLineEdit()
        self.outidx_input.setPlaceholderText('')
        self.left_layout.addWidget(self.outidx_label, 13,0,1,1)
        self.left_layout.addWidget(self.outidx_input, 14,0,1,5)

    def init_right(self):
        self.right_table = QtWidgets.QTableWidget()
        self.right_table.setColumnCount(7)
        self.right_table.setRowCount(500)
        for i in range(500):
            self.right_table.setRowHeight(i, 50)
        self.right_table.setColumnWidth(1, 60)
        self.right_table.setColumnWidth(2, 200)
        self.right_table.setColumnWidth(3, 200)
        self.right_table.setColumnWidth(4, 200)
        self.right_table.setColumnWidth(6, 60)


        self.right_table.setHorizontalHeaderLabels(['Name','Type','Range','Logic','Rule','pattern','OutIdx'])
        self.right_table.doubleClicked.connect(self.table_click_op)
        self.right_layout.addWidget(self.right_table, 0,0,9,5)

        self.gennum_label = QtWidgets.QLabel('Number of data:')
        self.gennum_label.setFont(qtawesome.font('fa', 14))
        self.gennum_input = QtWidgets.QLineEdit()
        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.clicked[bool].connect(self.generate_op)
        self.upload_button = QtWidgets.QPushButton("Upload")
        self.upload_button.clicked[bool].connect(self.upload_op)


        self.process_bar = QtWidgets.QProgressBar()
        self.process_bar.setValue(0)
        self.process_bar.setFixedHeight(5)
        self.process_bar.setTextVisible(False)


        self.right_layout.addWidget(self.gennum_label, 10,0,1,2)
        self.right_layout.addWidget(self.gennum_input, 10,2,1,1)
        self.right_layout.addWidget(self.generate_button, 10,3,1,1)
        self.right_layout.addWidget(self.upload_button, 10,4,1,1)

        self.right_layout.addWidget(self.process_bar, 11,0,1,5)

        self.msg_label = QtWidgets.QLabel('Message:')
        self.msg_label.setFont(qtawesome.font('fa', 14))
        self.msg_content = QtWidgets.QLabel('welcome')
        # self.msg_label.setFont(qtawesome.font('fa', 8))

        self.right_layout.addWidget(self.msg_label, 12,0,1,1)
        self.right_layout.addWidget(self.msg_content, 12,2,1,4)

    def beauty_main(self):
        self.main_widget.setStyleSheet('''
            QWidget#main_widget{
                color:#455A64;
                background:#455A64;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
            }
        ''')

    def beauty_top(self):
        self.db_ip_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')

        self.db_user_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.db_pswd_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.tb_sc_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.tb_na_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.db_db_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')

        self.top_widget.setStyleSheet('''
            QWidget#top_widget{
                color:#1976D2;
                background:#627E8F;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                color:white;
                font-size:14px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
    def beauty_left(self):
        self.name_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.range_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.rule_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.pattern_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.outidx_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{
                color:#1976D2;
                background:#627E8F;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                color:white;
                font-size:14px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QCheckBox{
                color:white;
                font-size:14px;
                font-weight:400;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
    def beauty_right(self):
        self.gennum_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#1976D2;
                background:#627E8F;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                color:white;
                font-size:14px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.msg_content.setStyleSheet('''
            QLabel{
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
                color:black;
                background:white;
                font-size:12px;
                font-weight:300;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }

            ''')
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
