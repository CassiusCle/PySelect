import subprocess
import os

# Open a terminal window
terminal_cmd = ['gnome-terminal', '--']

os.system("gnome-terminal -e 'bash -c \"exec bash; MY_COMMAND; exec bash\" '")

# # Run a command in the terminal
# command = 'ls'
# command_args = ['-l', '-a']

# # Combine the terminal command and the command to run
# terminal_cmd.extend([command] + command_args)

# # Execute the command in the terminal
# subprocess.call(terminal_cmd)
