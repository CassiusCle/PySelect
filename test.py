import subprocess

def run_command_wsl(command):
    # Command to execute in WSL
    wsl_command = f"wsl ~/.pyenv/bin/pyenv {command}"

    # Run the command in WSL and capture the output
    output = subprocess.run(
        wsl_command,
        capture_output=True,
        text=True,
        shell=False
    )

    # Check if there was an error
    if output.returncode != 0:
        print(f"Error executing command: {output.stderr}")
    else:
        # Print the output
        print(output.stdout)
        print(len(output.stdout.strip().split('\n')))


# Run pyenv command in WSL terminal
run_command_wsl("virtualenvs")
