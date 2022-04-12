import pandas
import ast
from pandas import DataFrame
FILE='test.txt'
open='test'
with open(FILE,'r',encoding='utf-8') as f:
    print(f)
    import numpy
x=pandas.read_csv(FILE)
print(x)

