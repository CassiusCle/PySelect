import subprocess  
import re

DO_WSL = True

def make_wsl(command, DO_WSL):
    if DO_WSL:
        return f"wsl {command}"
    else:
        return [command]


import secrets

def generate_token(length = 16):
    return secrets.token_hex(token_length)

environment = "sandbox_3.11.3"
PYENV = "~/.pyenv/bin/pyenv"

notebook_token = generate_token()
commands = (f"source activate_alt {environment}"+
            f"&& {PYENV} version"+
            "&& ~/.pyenv/shims/pip show notebook"+
            # "&& ~/.pyenv/shims/jupyter notebook")
            f"&& ~/.pyenv/shims/jupyter notebook --no-browser --NotebookApp.token={notebook_token}")

result = subprocess.run(["wsl", "bash", "-c", commands], 
                         shell=False, capture_output=True, text=True)
print("First result")
print(result.stdout)
print(result.returncode)
print(result.stderr)

# Extract the access token from the output using regular expressions
token_pattern = r"token=(\w+)"
match = re.search(token_pattern, result.stdout)
if match:
    access_token = match.group(1)
    print("Access token:", access_token)
else:
    print("Access token not found.")


# result2 = subprocess.run(["wsl", "bash", "-c", f"{PYENV} version"], 
#                          shell=False, capture_output=True, text=True)

# print("Second result")
# print(result2.stdout)
# print(result2.returncode)
# print(result2.stderr)

