import subprocess


def get_virtualenvs(wsl = False):
    command = ["pyenv virtualenvs"]
    if wsl:
        command = ["wsl", command]
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, _ = process.communicate()
    output = output.decode().strip()
    
    return parse_virtualenvs(output)
    

def parse_virtualenvs(output):
     # Split the output into individual lines
    lines = output.split('\n')

    # Initialize an empty set to store unique environment names
    unique_envs = set()

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

# Example usage
unique_envs = get_virtualenvs(wsl= False)

# Print the unique environment names
for env_name in unique_envs:
    print(env_name)