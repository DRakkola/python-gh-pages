import subprocess
import json
import os
import shutil

def run_command(command, cwd=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    output, error = process.communicate()
    output_str = output.decode('utf-8')
    error_str = error.decode('utf-8')
    print(f"Command: {command}")
    print(f"Output:\n{output_str}")
    print(f"Error:\n{error_str}")
    print(f"Return Code: {process.returncode}")
    print('-' * 50)
    return output_str, error_str, process.returncode

def read_config():
    config = {}
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        pass  # Handle the case where config.json is not found
    return config

def is_remote_added(remote_url):
    output, _, _ = run_command('git remote -v')
    return remote_url in output

def does_branch_exist(branch_name):
    output, _, _ = run_command('git show-ref --verify refs/heads/{}'.format(branch_name))
    return 'fatal: Not a valid ref' not in output

def main():
    # Read config from config.json
    config = read_config()

    # Step 1: Create 'build' directory as the working directory
    build_dir = 'build'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)  # Remove existing directory
    os.makedirs(build_dir)
    os.chdir(build_dir)

    # Step 2: Clone the repository specified in the config
    repo_url = 'https://github.com/{}/{}.git'.format(config.get('github_username', ''), config.get('repo_name', ''))
    
    output, error, return_code = run_command('git clone {} .'.format(repo_url))
    if return_code == 0:
        print("Repository cloned successfully.")
    else:
        print("Error cloning repository.")
        return

    # Step 3: Run npm install
    output, error, return_code = run_command('npm install')
    if return_code == 0:
        print("npm packages installed successfully.")
    else:
        print("Error installing npm packages.")
        return

    # Step 4: Open package.json file and add homepage property
    package_json_path = 'package.json'
    with open(package_json_path, 'r') as file:
        data = json.load(file)
        data['homepage'] = 'https://{}.github.io/{}'.format(config.get('github_username', ''), config.get('repo_name', ''))
    with open(package_json_path, 'w') as file:
        json.dump(data, file, indent=2)
    print("Homepage property added to package.json.")

    # Step 5: Add deployment scripts to package.json file
    data['scripts']['predeploy'] = 'npm run build'
    data['scripts']['deploy'] = 'gh-pages -d build'
    with open(package_json_path, 'w') as file:
        json.dump(data, file, indent=2)
    print("Deployment scripts added to package.json.")

    # Step 6: Initialize a Git repository if not already initialized
    if not os.path.exists('.git'):
        output, error, return_code = run_command('git init')
        if return_code == 0:
            print("Git repository initialized successfully.")
        else:
            print("Error initializing Git repository.")
    else:
        print("Git repository already initialized.")

    # Step 7: Add a remote that points to the GitHub repository if not already added
    remote_url = 'https://github.com/{}/{}.git'.format(config.get('github_username', ''), config.get('repo_name', ''))
    if not is_remote_added(remote_url):
        output, error, return_code = run_command('git remote add origin {}'.format(remote_url))
        if return_code == 0:
            print("Remote added successfully.")
        else:
            print("Error adding remote.")
    else:
        print("Remote already added.")

    # Step 8: Check if 'gh-pages' branch exists
    if does_branch_exist('gh-pages'):
        print("Branch 'gh-pages' already exists. Removing 'gh-pages' cache directory.")
        shutil.rmtree('node_modules/gh-pages/.cache')

    # Step 9: Push the React app to the GitHub repository
    output, error, return_code = run_command('npm run deploy')
    if return_code == 0:
        print("React app deployed to GitHub Pages.")

    print("Deployment completed.")

if __name__ == "__main__":
    main()
