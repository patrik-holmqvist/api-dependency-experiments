import os
from git import Repo

def clone_repo(repo_url, local_dir):
    Repo.clone_from(repo_url, local_dir)

def analyze_code(local_dir):
    # List all Python files
    python_files = []
    for root, _, files in os.walk(local_dir):
        for f in files:
            if f.endswith('.py'):
                python_files.append(os.path.join(root, f))
    return python_files

def generate_mermaid_code(files):
    # Simple Mermaid diagram: each file is a node
    mermaid = "graph TD\n"
    for f in files:
        mermaid += f'    {os.path.basename(f)}\n'
    return mermaid

def main():
    repo_url = input("Enter GitHub repo URL: ")
    local_dir = "temp_repo"
    clone_repo(repo_url, local_dir)
    files = analyze_code(local_dir)
    mermaid_code = generate_mermaid_code(files)
    print("Mermaid diagram code:\n", mermaid_code)

if __name__ == "__main__":
    main()