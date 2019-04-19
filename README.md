# SQL测试数据生成工具

### 1. 环境依赖

+ Python3
+ Pandas
+ openpyxl

### 2. 运行方式

#### 2.1 在`generator.py`中定义表结构

**表结构定义方式:**

 	1. 直接在代码中定义表结构dict, 示例`generator.py: line 69-89` 
 	2. 使用excel文件定义表结构, 示例`input_example.xlsx`

**每个字段需要定义以下内容:**

+ 字段名(name)
+ 字段类型(Type):
  + INT - 整形数
  + FLOAT - 浮点数
  + CHAR - 字符串
  + DATE - 日期
  + DTTM - 日期+时间
  + CUST - 自定义
+ 取值范围(Range):
  + 区间(中括号, 小括号) - 例如`(100, 200], [1994/01/01, 2020/05/01]`
  + 集合(大括号) - 例如`{张三, 李四}`
  + 若未定义, 默认各字段能取到的最大, 最小值
+ 逻辑(Logic):
  + ASC - 自增, 起始点为取值范围最小值
  + DESC - 自减, 起始点为取值范围最大值
  + RAND - 在取值范围中随机抽取
  + DISTINCT - 表示该列中不含重复值
+ 规则(Rules):
  + 支持加,减,乘,除等常规运算, 若需要括号使用小括号`()`
  + 支持常用统计运算(函数名后使用中括号):
    + MAX[c1, c2, c3]: 取c1, c2, c3最大值
    + MIN[c1, c2, c3]: 取c1, c2, c3最小值
    + AVG[c1, c2, c3]: 取c1, c2, c3平均值
    + SUM[c1, c2, c3]: 取c1, c2, c3和
  + 支持常规与统计混合运算
  + CHAR类型支持加法运算, 表示字符串拼接
+ 模板(Patterns):
  + 浮点数模板, 例如`%.2f`表示保留二位小数
  + 字符串模板, 例如:`\d\dCMB\d\d\d\s\s `
    + `\d`: 1位整数, 0-9
    + `\s`: 1个小写字符
    + `\S`: 1个大写字符
  + 日期类模板, 例如: `%Y/%m/%d` 可对应 `1994/01/01`
    + `%Y`: 4位年份
    + `%m`: 月份
    + `%d`: 日期
    + 更多详情查看[官网](https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior)
  + 时间类模板, 例如: `%H:%M:%S` 可对应 `14:28:40`
    + `%H`: 小时
    + `%M`: 分钟
    + `%S`: 秒
    + 更多详情查看[官网](https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior)
+ 输出顺序序号
  + 所有列将根据序号升序排序输出

#### 2.2 运行函数 -- 带参数

运行方式如下, 可通过`python3 generator.py -h` 获得:

```bash
python3 generator.py -i <input_file> -o <output_file> -n <generate_num>
```

例如:

```bash
python3 generator.py -i input_example.xlsx -o output_example.xlsx -n 200
```



#### 2.3 运行函数 -- 不带参数

```bash
python3 generator.py
```

可更改不同参数

```python
# 输入表结构目录
g = generator('input_example.xlsx')
# 生成100个数据
g.gen(100)
# 支持增量生成, 自增,自减,查重会接着已生成数据
g.gen(300)
# 将数据存为csv或excel
g.to_csv('output_example.csv')
g.to_excel('output_example.xlsx')
```



### 3. 各字段逻辑说明

| 数据类型 |      取值范围(a,b)       | 自增(ASC) | 自减(DESC) |       随机(RAND)       |
| :------: | :----------------------: | :-------: | :--------: | :--------------------: |
|   INT    |      取a至b中的整数      |  步长=1   |   步长=1   |      随机抽取整数      |
|  FLOAT   |     取a至b中的浮点数     |    NA     |     NA     |     随机抽取浮点数     |
|   CHAR   |  取长度为a至b间的字符串  |    NA     |     NA     |     随机生成字符串     |
|   DATE   | a为最早日期, b为最晚日期 | 步长=1天  |  步长=1天  | 随机生成取值范围内日期 |
|   DTTM   | a为最早时间, b为最晚时间 | 步长=1秒  |  步长=1秒  | 随机生成取值范围内时间 |

 

### 4. 自定义字段类型实现

**可在`DataNode.py`末尾处定义`dnode_CUS`, 以下为一种自定义字段类型示例:**

假设要生成CHAR类型数据满足以下模式`CMBxxxx`, 其中`xxxx`为自增数字, 例如CMB0001, CMB0002, CMB0003……, `dnode_CUS`实现方式如下:

```python
class dnode_CUS(dnode):
    def __init__(self):
        self.idx = 0

    def generate(self, d):
        self.idx += 1
        return 'CMB%04d'%(self.idx)
```

