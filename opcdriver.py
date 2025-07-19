from opcua import Client
import json
import argparse
import random
import shutil


def get_parser():
        parser = argparse.ArgumentParser(description='OPC Driver Server URL')
        parser.add_argument('--server_address', nargs='?',
                            help='The OPC server address (default: localhost)')
        parser.add_argument('--server_port', nargs='?', default=4870,
                            help='The OPC server port (default: 4870)')
        parser.add_argument('--protocol', nargs='?', default="opc.tcp",
                            help='The OPC protocol (default: opc.tcp)')
        parser.add_argument('--objects_node_name', nargs='?', default="WinCC Panel RT",
                            help='The OPC objects node name (default: WinCC Panel RT)')
        return parser

def random_values():
    # Copy the original JSON file to a new file
    shutil.copy("variables.json", "variables_copy.json")

    # Load the copied variables
    with open("variables_copy.json", "r") as f:
        variables = json.load(f)

    excluded_variables = ["@DiagnosticsIndicatorTag", "Tag_ScreenNumber"]
    # Randomly change the values of the variables
    for variable in variables:
        if variable["name"] not in excluded_variables:
            if isinstance(variable["value"], bool):
                variable["value"] = random.choice([True, False])
            elif isinstance(variable["value"], (int, float)):
                variable["value"] += random.uniform(-10, 10)  # Randomly adjust numeric values

    with open("variables_copy.json", "w") as f:
        json.dump(variables, f, indent=4)
        

class OCUDriver:
    def __init__(self, server_url, objects_node_name='WinCC Panel RT'):
        try:
            self.server_url = server_url
            self.objects_node_name = objects_node_name
            self.client = Client(server_url)
            self.client.connect()
            self.root_node = self.client.get_root_node()
            self.objects_node = self.client.get_objects_node()
            self.variables_node = self.objects_node.get_child([f"1:{objects_node_name}", "3:Tags"]) # TODO: This path is hardcoded for variables
            self.variables = self.variables_node.get_children()
        except Exception as e:
            raise Exception(f"Error connecting to the server: {e}")
    
    def disconnect(self):
        if hasattr(self, 'client'):
            self.client.disconnect()

    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures disconnect"""
        self.disconnect()

    def get_variables(self):
        variables = []
        for variable in self.variables:
            name = variable.get_display_name().Text
            variables.append({
                "name": name,
                "node_id": variable.nodeid.to_string(),
                "value": variable.get_value()
            })
        return variables

    def export_variables(self, path):
        variables = []
        for variable in self.variables:
            variables.append({
                "name": variable.get_display_name().Text,
                "value": variable.get_value()
            })
        with open(path, "w") as f:
            json.dump(variables, f, indent=4)
    
    def load_variables(self, path):
        try:
            with open(path, "r") as f:
                variables = json.load(f)
            for variable in variables:
                variable_node = self.variables_node.get_child([f'3:${variable["name"]}'])
                variable_type = variable_node.get_data_type()
                variable_node.set_value(self._convert_value(variable_type, variable["value"]))
        except Exception as e:
            import pdb; pdb.set_trace()
            print(f"Error loading variable {variable['name']}, with type {variable_type}: {e}")

    def _convert_value(self, variable_type, value):
        type_node = self.client.get_node(variable_type)
        type_node_browse_name = type_node.get_browse_name().to_string()
        if "Boolean" in type_node_browse_name:
            return bool(value)
        elif "Int" in type_node_browse_name or "SByte" in type_node_browse_name or "UInteger" in type_node_browse_name:
            return str(value)
        elif "Float" in type_node_browse_name:
            return value
        else:
            raise ValueError(f"Unsupported variable type: {variable_type}")


if __name__ == "__main__":

    ### Handle arguments
    parser = get_parser()
    args = parser.parse_args()

    if not args.server_address:
        print("Server address is required")
        parser.print_help()
        exit(1)

    server_url = f"{args.protocol}://{args.server_address}:{args.server_port}"
    
    ### Connect to the server and get variables using context manager
    try:
        with OCUDriver(server_url, args.objects_node_name) as driver:
            ### Get variables from the server
            variables = driver.get_variables()
            print(json.dumps(variables, indent=4))
            
            ### Export variables to json file
            driver.export_variables("variables.json")
            
            ### Randomly adjust numeric values
            random_values() 

            ### Load variables from json file
            driver.load_variables("variables_copy.json")
            print("Updated variables")
            variables = driver.get_variables()
            print(json.dumps(variables, indent=4))
    except Exception as e:
        print(f"Error: {e}")