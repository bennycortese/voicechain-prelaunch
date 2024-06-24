import sys
import os
from dotenv import load_dotenv

def run_script(script_name):
    # Add the parent directory to the sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
    # Load environment variables
    load_dotenv()
    
    # Construct the full path to the script
    script_path = os.path.join(current_dir, '', script_name)
    
    # Execute the script
    with open(script_path, 'rb') as file:
        exec(compile(file.read(), script_path, 'exec'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_misc_script.py <script_name>")
        sys.exit(1)
    
    # Get the script name from the command line arguments
    script_to_run = sys.argv[1]
    run_script(script_to_run)
