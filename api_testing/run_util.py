import importlib.util
import sys
import os

def run_script_from_utils(script_name):
    # Construct the full path to the script
    script_path = os.path.join("utils", script_name)
    
    # Check if the script exists
    if not os.path.isfile(script_path):
        print(f"Script {script_name} not found in the utils folder.")
        return

    # Dynamically load the script as a module
    spec = importlib.util.spec_from_file_location(script_name[:-3], script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_util.py <script_name.py>")
    else:
        script_name = sys.argv[1]
        run_script_from_utils(script_name)
