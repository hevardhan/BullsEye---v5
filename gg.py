import json
import os
import psutil

def get_jupyter_runtime_dir():
    # Default path for Jupyter runtime on Windows
    return os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "jupyter", "runtime")

def list_active_kernels():
    """List currently active kernels."""
    connection_file_dir = get_jupyter_runtime_dir()
    if not os.path.exists(connection_file_dir):
        print(f"Runtime directory does not exist: {connection_file_dir}")
        return []

    kernels = []
    connection_files = [f for f in os.listdir(connection_file_dir) if f.endswith('.json')]
    
    for connection_file in connection_files:
        with open(os.path.join(connection_file_dir, connection_file)) as f:
            try:
                connection_info = json.load(f)
                if 'kernel' in connection_info and 'id' in connection_info['kernel']:
                    kernels.append({
                        'kernel_id': connection_info['kernel']['id'],
                        'name': connection_info['kernel']['name'],
                        'connection_file': connection_file
                    })
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {connection_file}. Skipping.")
    
    return kernels

def is_notebook_running(notebook_path):
    """Check if the specified notebook is currently running."""
    active_kernels = list_active_kernels()

    # Check the notebook's metadata to get the kernel spec
    try:
        with open(notebook_path) as nb_file:
            notebook_content = json.load(nb_file)
            notebook_kernel_name = notebook_content.get('metadata', {}).get('kernelspec', {}).get('name', None)
            if notebook_kernel_name is None:
                print("No kernel name found in the notebook metadata.")
                return False
            
            # Check active kernels to see if the notebook's kernel is running
            for kernel in active_kernels:
                if kernel['name'] == notebook_kernel_name:
                    return True
    except Exception as e:
        print(f"Error reading notebook {notebook_path}: {e}")
    
    return False

# Example usage
notebook_file = "mew.ipynb"  # Specify your notebook file path
if is_notebook_running(notebook_file):
    print(f"{notebook_file} is currently running.")
else:
    print(f"{notebook_file} is not running.")
