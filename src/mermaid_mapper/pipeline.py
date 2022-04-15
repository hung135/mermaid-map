from json_to_mermaid.json_to_mermaid import JSONToMermaid
from python_mapper.python_mapper import PyToJson


def python_pipeline(python_file: str, python_json_output: str) -> None:
    py_obj = PyToJson(python_file, python_json_output)
    py_obj.write_to_file()

    to_mermaid = JSONToMermaid(python_json_output)
    to_mermaid.pipeline()


if __name__ == "__main__":
    import sys

    python_pipeline(sys.argv[1], sys.argv[2])
