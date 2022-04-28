import yaml
import json
import random
from json_to_mermaid import JSONToMermaid

class K8SParser:
    def __init__(self, yaml_file_paths: list):
        self.yaml_file_paths = yaml_file_paths
        self.pod_list = {}
        self.service_parser = None
        self.deployment_parser = None
        self.load_yaml()
    
    def load_yaml(self) -> None:
        """Loads the yaml files and makes a parser for each particular K8S component (i.e. deployment)"""
        for path in self.yaml_file_paths:
            with open(path, 'r') as yaml_file, open("output.json", 'w') as json_file:
                yaml_contents = yaml.safe_load(yaml_file)
                json.dump(yaml_contents, json_file, indent=4)

            parsed_json = JSONToMermaid("output.json")
            if parsed_json.json["kind"] == "Deployment":
                self.deployment_parser = parsed_json
            elif parsed_json.json["kind"] == "Service":
                self.service_parser = parsed_json
    
    def setup_deployment_visualization(self) -> None:
        """Generate mermaid code for the deployment section of the diagram based on the parsed deployment yaml"""
        pod_count = int(self.deployment_parser.json["spec"]["replicas"])
        pod_container_image = self.deployment_parser.json["spec"]["template"]["spec"]["containers"][0]["image"]
        container_list = self.deployment_parser.json["spec"]["template"]["spec"]["containers"]

        for i in range(pod_count):
            pod_id = str(random.randint(0, 10000))
            self.deployment_parser.mermaid.append(f'{pod_id}["Pod {i}"]\n')

            for container in container_list:
                container_id = str(random.randint(0, 10000))
                self.deployment_parser.mermaid.append(f'{container_id}["container image: {pod_container_image}"]\n')
                self.deployment_parser.mermaid.append(f'{container_id}-->|"port list: {container["ports"]}"|{pod_id}\n')
            
            self.pod_list[pod_id] = (self.deployment_parser.json["spec"]["selector"]["matchLabels"],)

    def setup_service_visualization(self) -> None:
        """Generate mermaid code for the service section of the diagram based on the parsed service yaml"""
        service_name = self.service_parser.json["metadata"]["name"]
        selector_label = self.service_parser.json["spec"]["selector"]
        service_target_port = self.service_parser.json["spec"]["ports"][0]["targetPort"]
        service_id = str(random.randint(0, 10000))
        self.service_parser.mermaid.append(f'{service_id}["{service_name}"]\n')

        for key, val in self.pod_list.items():
            if val[0] == selector_label:
                self.service_parser.mermaid.append(f'{key}-->|"target port: {service_target_port}"|{service_id}\n')

    def create_mermaid(self) -> None:
        """Output the generated mermaid code into a mermaid file"""
        with open('output.md', 'w') as mermaid_output:
            mermaid_output.write('```mermaid\ngraph TD\nsubgraph Node\n')
            self.cleanup_parsers_mermaid()

            if self.service_parser != None:
                mermaid_output.writelines(self.service_parser.mermaid)
            elif self.deployment_parser != None:
                mermaid_output.writelines(self.deployment_parser.mermaid)

            mermaid_output.write('end\n```')

    def cleanup_parsers_mermaid(self) -> None:
        """Remove the unnecessary filename box from the mermaid output"""
        if self.service_parser != None:
            self.service_parser.mermaid.pop(0)
            self.service_parser.mermaid.pop(0)
        if self.deployment_parser != None:
            self.deployment_parser.mermaid.pop(0)
            self.deployment_parser.mermaid.pop(0)


if __name__ == "__main__":
    import sys
    test = K8SParser(sys.argv[1::])
    test.setup_deployment_visualization()
    test.setup_service_visualization()
    test.create_mermaid()

