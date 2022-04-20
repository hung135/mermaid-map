import yaml
import json
import random
from json_to_mermaid import JSONToMermaid

class K8SParser:
    def __init__(self, yaml_file_path: str):
        self.yaml_file_path = yaml_file_path
        self.pod_list = {}
        self.load_yaml()
    
    def load_yaml(self):
        with open(self.yaml_file_path, 'r') as yaml_file, open("output.json", 'w') as json_file:
            yaml_contents = yaml.safe_load(yaml_file)
            json.dump(yaml_contents, json_file, indent=4)
            
        self.json_parser = JSONToMermaid("output.json", True)
    
    def setup_deployment_visualization(self):
        pod_count = int(self.json_parser.json["spec"]["replicas"])
        pod_container_image = self.json_parser.json["spec"]["template"]["spec"]["containers"][0]["image"]
        container_list = self.json_parser.json["spec"]["template"]["spec"]["containers"]

        for i in range(pod_count):
            pod_id = str(random.randint(0, 10000))
            self.json_parser.mermaid.append(f'{pod_id}["Pod {i}"]\n')

            for container in container_list:
                container_id = str(random.randint(0, 10000))
                self.json_parser.mermaid.append(f'{container_id}["container image: {pod_container_image}"]\n')
                self.json_parser.mermaid.append(f'{container_id}-->|"port list: {container["ports"]}"|{pod_id}\n')
            
            self.pod_list[pod_id] = (self.json_parser.json["spec"]["selector"]["matchLabels"])

    def setup_service_visualization(self):
        return

    def create_mermaid(self):
        self.json_parser.mermaid_output(parsing_k8s=True)



if __name__ == "__main__":
    import sys

    test = K8SParser(sys.argv[1])
    test.setup_deployment_visualization()
    test.create_mermaid()

