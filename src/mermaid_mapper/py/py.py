import json
from ast import parse
from ast2json import ast2json
        

class PyToJson:
    '''
    Doc string
    '''
    json = None
    def __init__(self, python_file,encoding='utf8'):
        print(python_file)
 
        ast = ast2json(parse(open(python_file,encoding=encoding).read()))
        self.json=json.dumps(ast, indent=4)
    def print(self):
        '''
        Print to Screen
        '''
        print(self.json)

    def write_to_file(self,json_file,encoding='utf8'):
        '''
        Write to file

        '''
        with open(json_file,'w',encoding=encoding) as F:
            F.write(self.json)

if __name__ == '__main__':
    print("hello")
    print(PyToJson('/workspaces/mermaid-map/test/helloworld.py').json)
    PyToJson('/workspaces/mermaid-map/test/helloworld.py').write_to_file('test.json')