import sys
import json
import random

ignore_list=[ 
            "end_col_offset",
            "end_lineno", 
            "lineno","col_offset","end_col_offset","ctx","id"
                        ]
def get_paths(d, root="obj"):
    def recur(d):
        if isinstance(d, dict):
            for key, value in d.items():
                yield f'.{key}'
                yield from (f'.{key}{p}' for p in get_paths(value))

        elif isinstance(d, list):
            for i, value in enumerate(d):
                yield f'[{i}]'
                yield from (f'[{i}]{p}' for p in get_paths(value))

    return (root + p for p in recur(d))
def get_json_path(json_string):
    import json

    from jsonpath_ng import jsonpath, parse
 
    json_data = json.loads(json_string)

    jsonpath_expression = parse('$.body[0].names')

    match = jsonpath_expression.find(json_data)

    #print(match)
    print("value is", match[0].value)

def traverseJson(data, mermaidOutput, parent):
    if isinstance(data, dict):
        for key, val in data.items():
            if key not in ignore_list:
                #print(key)
                keyId = str(random.randint(0, 10000))
                
                mermaidOutput.append("{0}[\"{1}\"]\n".format(keyId, key))
                mermaidOutput.append("{0}-->{1}\n".format(keyId, parent[1]))

                if isinstance(val, dict):
                    traverseJson(val, mermaidOutput, (key, keyId))
                elif isinstance(val, list):
                    traverseJson(val, mermaidOutput, (key, keyId))
                else:
                    valId = str(random.randint(0, 10000))
                    mermaidOutput.append("{0}[\"{1}\"]\n".format(valId, val))
                    mermaidOutput.append("{0}-->{1}\n".format(valId, keyId))
    else:
        for i in range(len(data)):
            id = str(random.randint(0, 10000))
            
            mermaidOutput.append("{0}[\"{1}\"]\n".format(id, i))
            mermaidOutput.append("{0}-->{1}\n".format(id, parent[1]))

            if isinstance(data[i], dict):
                traverseJson(data[i], mermaidOutput, (i, id))
            elif isinstance(data[i], list):
                traverseJson(data[i], mermaidOutput, (i, id))
            else:
                valId = str(random.randint(0, 10000))
                mermaidOutput.append("{0}[\"{1}\"]\n".format(valId, data[i]))
                mermaidOutput.append("{0}-->{1}\n".format(valId, id))
    return 0

def main(filename): 
    mermaidOutput = ['graph TD\n']
    data=None
    with open(filename) as jsonInput:
        data = json.load(jsonInput)
        fileId = str(random.randint(0, 10000))
        mermaidOutput.append("{0}[\"{1}\"]\n".format(fileId, filename))
        traverseJson(data, mermaidOutput, (filename, fileId))
        get_json_path(json.dumps(data)) 

    with open("output.md", "w") as jsonOutput:
        jsonOutput.writelines("```mermaid\n")
        
        jsonOutput.writelines(mermaidOutput)
        jsonOutput.writelines("\n```\n")
 
        
     
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1])