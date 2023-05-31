import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import platform
import secrets

def generate_token(length = 16):
    return secrets.token_hex(length)

def get_operating_system(verbose=False):
    # Get the operating system name
    operating_system = platform.system()

    if operating_system == 'Windows':
        # Windows-specific code
        if verbose: print("Windows detected")
        return operating_system
    elif operating_system == 'Darwin':
        # macOS-specific code
        if verbose: print("macOS detected")
        return "macOS"
    elif operating_system == 'Linux':
        # Linux-specific code
        if verbose: print("Linux detected")
        return operating_system
    else:
        # Code for other operating systems
        print("Unsupported operating system")
        return "Unsupported"
        # TODO: Add functionality for what to do when unsupported.


#DO_WSL = False

PYENV = "~/.pyenv/bin/pyenv"

def make_wsl(command, DO_WSL):
    if DO_WSL:
        return f"wsl {command}"
    else:
        return [command]


# def activate_environment(environment):
#     command = f"source activate {environment}"
#     subprocess.run(make_wsl(command, DO_WSL))

def launch_jupyter(server_type, environment):
    if server_type == "Jupyter Lab":
        package = "jupyterlab"
        url = "http://localhost:8888/lab"
    else:
        package = "notebook"
        url = "http://localhost:8888/?token="

    check_command = f"bash -c pip show {package}"

    print(check_command)
    # result = subprocess.run(make_wsl(check_command, True), shell=True, capture_output=True, text=True)
    result = subprocess.run(["wsl", "bash", "-c", "~/.pyenv/shims/pip show notebook"], shell=False, capture_output=True, text=True)
    

    if result.returncode == 0:
        notebook_token = generate_token()

        commands = (f"source activate_alt {environment}"+
            f"&& {PYENV} version"+
            "&& ~/.pyenv/shims/pip show notebook"+
            # "&& ~/.pyenv/shims/jupyter notebook")
            f"&& ~/.pyenv/shims/jupyter notebook --no-browser --NotebookApp.token={notebook_token}")
        print(f"Python environment: {environment}")
        print(f"Jupyter Notebook is running at:\n{url+notebook_token}")
        webbrowser.open(url+notebook_token)
        result = subprocess.run(["wsl", "bash", "-c", commands], 
                         shell=False, capture_output=True, text=True)
    else:
        messagebox.showerror("Error", f"{package} is not installed in the selected environment.")

root = tk.Tk()
HEIGHT = 200
WIDTH = 300

root.geometry(f"{WIDTH}x{HEIGHT}")  # Set the width and height of the window
root.title("PySelect 1.0")

# Create and configure the dropdown menu
################### Environments
def get_virtualenvs(DO_WSL = False):
    command = f"{PYENV} virtualenvs"
    # process = subprocess.Popen(make_wsl(command, DO_WSL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output, _ = process.communicate()
    # output = output.decode().strip()

    output = subprocess.run(
        make_wsl(command, DO_WSL),
        capture_output=True,
        text=True,
        shell=False
    )
    if output.returncode != 0:
        print(f"Error executing command: {output.stderr}")

    return parse_virtualenvs(output.stdout)
    

def parse_virtualenvs(output):
     # Split the output into individual lines
    lines = output.strip().split('\n')

    # Initialize two empty lists to store environment names
    env_names = []
    env_paths = []

    # Loop through each line
    for line in lines:

        # Extract the environment name and path
        env_path = line.split(' (')[0].strip()
        env_name = env_path.split('/')[-1].strip()

        # Add to the respective lists only if the environment name is not already present
        if env_name not in env_names:
            env_names.append(env_name)
            env_paths.append(env_path)

    # Sort the lists alphabetically
    # env_names.sort()
    env_paths.sort()

    return env_paths

def main():

    def launch_jupyter_notebook():
        selected_environment = environment_combobox.get()
        # activate_environment(selected_environment)
        launch_jupyter("Jupyter Notebook", selected_environment)

    def launch_jupyter_lab():
        selected_environment = environment_combobox.get()
        # activate_environment(selected_environment)
        launch_jupyter("Jupyter Lab", selected_environment)

    def launch_terminal():
        selected_environment = environment_combobox.get()
        # activate_environment(selected_environment)
        env_command = f"source activate {selected_environment}; ipython; import mod"
        # subprocess.Popen(make_wsl(env_command, DO_WSL), shell=True)

        # TODO: Does not activate venv correctly, need to fix.
        process = subprocess.Popen(make_wsl(env_command, DO_WSL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        output, _ = process.communicate()
        output = output.decode().strip()
        print(output)


    operating_system = get_operating_system()
    print(operating_system)
    
    DO_WSL = True if operating_system == "Windows" else False

    # Example usage
    environments = get_virtualenvs(DO_WSL)
    #######################

    selected_environment = tk.StringVar(root)
    selected_environment.set(environments[0])

    environment_combobox = ttk.Combobox(root, 
                                        textvariable=selected_environment, 
                                        values=environments, 
                                        width=max(len(env) for env in environments)+2)
    environment_combobox.pack()

    # Create and configure the radio buttons
    server_type = tk.StringVar(root)
    server_type.set("Jupyter Notebook")
    radio_button_notebook = ttk.Radiobutton(root, text="Jupyter Notebook", variable=server_type, value="Jupyter Notebook")
    radio_button_lab = ttk.Radiobutton(root, text="Jupyter Lab", variable=server_type, value="Jupyter Lab")
    radio_button_terminal = ttk.Radiobutton(root, text="Terminal", variable=server_type, value="Terminal")
    radio_button_lab.pack()
    radio_button_notebook.pack()
    radio_button_terminal.pack()

    # Create the launch button
    launch_button = ttk.Button(root, text="Launch", command=lambda: launch_jupyter_lab() if server_type.get() == "Jupyter Lab" else (launch_jupyter_notebook() if server_type.get() == "Jupyter Notebook" else launch_terminal()))
    launch_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()