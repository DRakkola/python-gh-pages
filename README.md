# React GitHub Pages Deployment Script

This script automates the process of deploying a React app to GitHub Pages using the `gh-pages` npm package.

## Prerequisites

- Node.js (Tested with Node v16.13.2)
- npm (Node Package Manager)

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. **Run the deployment script:**

    ```bash
    python deploy_script.py
    ```

## Configuration

Before running the deployment script, make sure to adjust the configuration:

- Open the `config.json` file in the root this script.
- Set the values for:
    - `github_username`: Your GitHub username.
    - `repo_name`: Your GitHub repository name.
    - `project_root`: The root directory of your React project.

## Deployment Details

- At this point, the GitHub repository contains a branch named gh-pages, which contains the files that make up the distributable version of the React app.

- After deployment, you can view your website by navigating to the [GitHub Pages settings page](https://github.com/your-username/your-repo/settings/pages):

    - In your web browser, navigate to the GitHub repository.
    - Above the code browser, click on the tab labeled "Settings."
    - In the sidebar, in the "Code and automation" section, click on "Pages."

    If your build is not being deployed, configure the "Build and deployment" settings like this:

    - Source: Deploy from a branch
    - Branch:
        - Branch: gh-pages
    - Folder: / (root)

    Click on the "Save" button.

## Important Note

- This script is tested with Node v16.13.2. Make sure you have a compatible version of Node.js installed.

## License

This project is licensed under the [MIT License](LICENSE).
