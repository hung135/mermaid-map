import sys
import json
import random

def traverseJson(data, mermaidOutput, parent):
    if isinstance(data, dict):
        for key, val in data.items():
            #print(key)
            keyId = str(random.randint(0, 10000))
            mermaidOutput.append("{0}[{1}]\n".format(keyId, key))
            mermaidOutput.append("{0}-->{1}\n".format(keyId, parent[1]))

            if isinstance(val, dict):
                traverseJson(val, mermaidOutput, (key, keyId))
            elif isinstance(val, list):
                traverseJson(val, mermaidOutput, (key, keyId))
            else:
                valId = str(random.randint(0, 10000))
                mermaidOutput.append("{0}[{1}]\n".format(valId, val))
                mermaidOutput.append("{0}-->{1}\n".format(valId, keyId))
    else:
        for i in range(len(data)):
            id = str(random.randint(0, 10000))
            mermaidOutput.append("{0}[{1}]\n".format(id, i))
            mermaidOutput.append("{0}-->{1}\n".format(id, parent[1]))

            if isinstance(data[i], dict):
                traverseJson(data[i], mermaidOutput, (i, id))
            elif isinstance(data[i], list):
                traverseJson(data[i], mermaidOutput, (i, id))
            else:
                valId = str(random.randint(0, 10000))
                mermaidOutput.append("{0}[{1}]\n".format(valId, data[i]))
                mermaidOutput.append("{0}-->{1}\n".format(valId, id))
    return 0

def main(filename):
    mermaidOutput = ['graph TD\n']

    with open(filename) as jsonInput:
        data = json.load(jsonInput)
        fileId = str(random.randint(0, 10000))
        mermaidOutput.append("{0}[{1}]\n".format(fileId, filename))
        traverseJson(data, mermaidOutput, (filename, fileId))

    with open("output.md", "w") as jsonOutput:
        jsonOutput.writelines(mermaidOutput)
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1])