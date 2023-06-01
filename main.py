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

CONDA_path = "~/miniconda3/etc/profile.d/conda.sh"
def run_command(command, # str of commands
                isWSL=True, 
                isBash=True, 
                conda=False,
                conda_env=None,
                shell=False, 
                capture_output=True, 
                text=True):
    if conda_env is not None: conda = True

    command_list = []
    if isWSL: command_list.append("wsl")
    if isBash: command_list += ["bash", "-c"]
    
    payload = []
    if conda: payload.append(f". {CONDA_path}")
    if conda_env is not None:
        payload.append(f"conda activate {conda_env}")
    payload.append(command)
    payload = " && ".join(payload)

    command_list.append(payload)

    # print(command_list)
    result = subprocess.run(command_list, 
                    shell=False, capture_output=True, text=True)
    return(result)

def launch_jupyter(server_type, environment):
    if server_type == "Jupyter Lab":
        package = "lab"
        pip_name = "jupyterlab"
        url = "http://localhost:8888/lab?token="
    else:
        package = pip_name = "notebook"
        url = "http://localhost:8888/?token="



    print(environment)
    result = run_command(f"pip show {pip_name}", conda_env=environment)
    # print(result.returncode)

    if result.returncode == 0:
        token = generate_token()
        command = f"jupyter {package} --no-browser --NotebookApp.token={token}"

        print(f"Python environment: {environment}")
        print(f"{server_type} is running at:\n{url+token}")
        webbrowser.open(url+token)
        result = run_command(command, conda=True, conda_env=environment)
    else:
        messagebox.showerror("Error", f"{server_type} is not installed in the {environment} environment.")

root = tk.Tk()
HEIGHT = 200
WIDTH = 300

root.geometry(f"{WIDTH}x{HEIGHT}")  # Set the width and height of the window
root.title("PySelect 1.0")

# Create and configure the dropdown menu
################### Environments
def get_virtualenvs():
    output = run_command("conda info --envs", conda=True)

    if output.returncode != 0:
        print(f"Error executing command: {output.stderr}")

    return parse_virtualenvs(output.stdout)

def parse_virtualenvs(out):
    envs = out.strip().split('\n')[2:]
    return sorted([x.split()[0] for x in envs])


def main():

    def launch_jupyter_notebook():
        selected_environment = environment_combobox.get()
        # activate_environment(selected_environment)
        launch_jupyter("Jupyter Notebook", selected_environment)

    def launch_jupyter_lab():
        selected_environment = environment_combobox.get()
        # activate_environment(selected_environment)
        launch_jupyter("Jupyter Lab", selected_environment)


    operating_system = get_operating_system()
    print(operating_system)
    
    # Example usage
    environments = get_virtualenvs()
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
    radio_button_lab.pack()
    radio_button_notebook.pack()

    # Create the launch button
    launch_button = ttk.Button(root, text="Launch", command=lambda: launch_jupyter_lab() if server_type.get() == "Jupyter Lab" else launch_jupyter_notebook())
    launch_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()