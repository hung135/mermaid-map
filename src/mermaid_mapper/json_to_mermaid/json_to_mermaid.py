import json
import random
from typing import Tuple, Union

from jsonpath_ng import jsonpath, parse

MermTuple = Tuple[str, str]

IGNORE = [
    "end_col_offset",
    "end_lineno",
    "lineno",
    "col_offset",
    "end_col_offset",
    "ctx",
    "id","type_comment"
]
NOT_IGNORE = [("_type","Name"),
("_type","Module")]

class JSONToMermaid:
    """
    TODO: Doc String
    """

    json: dict
    mermaid: list = []
    file_id: int
    JSONPath=set()
    def __init__(self, json_file_loc: str):
        self.file_id = str(random.randint(0, 10000))
        self.json_file_loc = json_file_loc
        self.load_json()
        self._setup_mermaid()

    def _setup_mermaid(self) -> None:
        """Sets mermaid output up"""
        self.mermaid.append("graph TD\n")
        self.mermaid.append(f'{self.file_id}["{self.json_file_loc}"]\n')

    def pipeline(self) -> None:
        self.traverse(self.json, (self.json_file_loc, self.file_id))
        self.mermaid_output()
        print(self.JSONPath)

    def load_json(self) -> None:
        """Loads the json file"""
        with open(self.json_file_loc, "r") as _file:
            self.json = json.load(_file)

    def describe_json_path(self) -> None:
        """Describes the JSON path"""
        jsonpath_expression = parse("$.body[0].names")
        _match = jsonpath_expression.find(json_data)
        if _match:
            return _match[0].value
        return None

    def mermaid_output(self) -> None:
        """Ouputs the mermaid representation of the JSON file"""
        with open("output.md", "w") as _out:
            _out.writelines("```mermaid\n")
            _out.writelines(map(str, self.mermaid))
            _out.writelines("\n```\n")

    def _mermaid_add(self, box: MermTuple, arrow: MermTuple) -> None:
        """Adds a new box and arrow to the mermaid output

        :param MermTuple box: Mermaid box values
        :param MermTuple arrow: Mermaid arrow values
        """
        self.mermaid.append(f'{box[0]}["{box[1]}"]\n')
        self.mermaid.append(f"{arrow[0]}-->{arrow[1]}\n")

    def traverse(self, data: Union[dict, list], parent_node: Tuple[str, str],depth='') -> None:
        """Traverse the JSON file, parsing the ast into a mermaid format

        :param Union[dict, list] data: Data to recursively parse
        :param Tuple[str,str] parent_node: Parent node to review
        """ 
        if isinstance(data, dict):
            for key, val in data.items():
                curr_path=depth+'.'+key
                self.JSONPath.add(curr_path)
                
                if key not in IGNORE:
                    
                    key_id = str(random.randint(0, 10000))
                    self._mermaid_add((key_id, key), (key_id, parent_node[1]))

                    if isinstance(val, dict) or isinstance(val, list):
                        self.traverse(val, (key, key_id),curr_path)
                    else:
                        val_id = str(random.randint(0, 10000))
                        self._mermaid_add((val_id, val), (val_id, key_id))

        else:

            for i, element in enumerate(data):
                
                _id = str(random.randint(0, 10000))
                self._mermaid_add((_id, i), (_id, parent_node[1]))

                if isinstance(element, dict) or isinstance(element, list):
                    curr_path=depth
                    self.JSONPath.add(curr_path)
                    self.traverse(element, (i, _id),curr_path)
                else:
                    val_id = str(random.randint(0, 10000))
                    
                    self._mermaid_add((val_id, element), (val_id, _id))


if __name__ == "__main__":
    import sys

    test = JSONToMermaid(sys.argv[1])
    test.pipeline()
    
