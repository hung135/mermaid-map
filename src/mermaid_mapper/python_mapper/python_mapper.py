import json
from ast import parse
from ast2json import ast2json


class PyToJson:
    """
    TODO: Doc String
    """

    json: dict
    json_output_loc: str

    def __init__(
        self, python_file_loc: str, json_output_loc: str, encoding: str = "utf8"
    ):
        """Init"""
        self.read_python(python_file_loc, encoding)
        self.json_output_loc = json_output_loc

    def read_python(self, python_file_loc, encoding):
        with open(python_file_loc, "r", encoding=encoding) as _file:
            ast = ast2json(parse(_file.read()))
        self.json = json.dumps(ast, indent=4)

    def write_to_file(self, encoding: str = "utf8") -> None:
        """Writes python file to JSON

        :param str json_file: location of the python file
        :param str encoding: Encodning type
        """
        with open(self.json_output_loc, "w", encoding=encoding) as _file:
            _file.write(self.json)

    def __str__(self):
        """String representation of object"""
        return self.json


if __name__ == "__main__":
    import sys

    _file = sys.argv[1]
    python_json = PyToJson(_file, "helloworld_output.json")
    python_json.write_to_file()
