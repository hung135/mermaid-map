import pandas
import ast
from pandas import DataFrame
FILE='test.txt'
File2='test2.txt'
 
with open(FILE,'r',encoding='utf-8') as f:
    print(f)
    import numpy
xx=pandas.read_csv(FILE)
 

with open(File2,'w',encoding='utf-8') as f:
    print(f) 

with open('file_abc.txt','w',encoding='utf-8') as f:
    print(f) 