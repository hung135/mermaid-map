import ast

code = ast.parse("print('Hello world!')")
print(ast.dump(code))

PY_FILE='/workspaces/mermaid-map/test/helloworld.py'
with open(PY_FILE, 'r',encoding='utf8') as file:
    code = file.read().rstrip()
parsed_code=ast.parse(code)

code_tree=ast.dump(parsed_code)

print(type(code_tree))
for aa in code_tree:
    pass 

top_imported = set()
id=set()
file_open = set()
fopen=False

prev_Name = None
variable_dict ={}

def is_variable(node,prev_Name):

    if prev_Name and isinstance(node,ast.Constant):
        id.add(f"{node.value}")
        print("xxxxxxxxxxx------",node.value)
        if not variable_dict.get(prev_Name,None):
            variable_dict[prev_Name]=node.value
        
    elif isinstance(node,ast.Name):
       return node.id
    return None

for node in ast.walk(parsed_code):
    print("\n\t",node,"\n\t\t",node.__dict__)
    prev_Name=is_variable(node,prev_Name)
    if isinstance(node, ast.Import):
        for name in node.names:
            top_imported.add(name.name.split('.')[0])
    elif isinstance(node, ast.ImportFrom):
        if node.level > 0:
            # Relative imports always refer to the current package.
            continue
        assert node.module
        top_imported.add(node.module.split('.')[0])
    if isinstance(node,ast.With):
         
        print("----",node.__dict__)
        for a in node.body:
            print("------>",a)

    if fopen and isinstance(node,ast.Name):
        

        file_open.add(node.id)
        fopen=False
    
   
    if isinstance(node,ast.Name):
        #id.add(node.id)
        print("-----",node.__dict__)
        if hasattr(node, 'ctx'):
            print("-----------",type(node.ctx))
        if node.id=='open':
            
            fopen=True


with open('test_flow.md','w',encoding='utf8') as f:
    f.writelines("```mermaid\ngraph TD\n")
    for a in top_imported:
        f.writelines(f"{a}-->|imports|{__file__}\n")
        print()
    # for a,v in variable_dict.items():
    #     f.writelines(f"{a}-->|{v}|{__file__}\n")
    #     print(f"{a}-->{__file__}")
    for a in file_open:
        f.writelines(f"{a}-->{__file__}\n")
        print(f"{a}-->{__file__}")
    f.writelines("```\n")
