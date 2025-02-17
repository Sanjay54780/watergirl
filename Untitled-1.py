import requests
import json

# GitHub API URL to fetch repository contents
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# Function to get the contents of a GitHub repository
def fetch_github_repo(owner, repo, path=""):
    url = GITHUB_API_URL.format(owner=owner, repo=repo, path=path)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Returns the file/folder data as JSON
    else:
        print(f"Failed to fetch repository data. Status code: {response.status_code}")
        return None

# Function to fetch all files from a specific GitHub repository
def fetch_all_files_from_repo(owner, repo):
    contents = fetch_github_repo(owner, repo)
    if contents:
        file_list = []
        for item in contents:
            if item['type'] == 'file':  # Only fetch files, not directories
                file_list.append(item['download_url'])
        return file_list
    return []

# Function to analyze a file from its URL
def analyze_code_from_url(file_url):
    # Fetch the raw file content from GitHub
    response = requests.get(file_url)
    
    if response.status_code == 200:
        file_content = response.text
        
        # Basic analysis: Count lines and functions
        lines_of_code = file_content.split("\n")
        num_lines = len(lines_of_code)
        num_functions = file_content.count("def ")  # Count the number of functions
        
        return {
            "lines_of_code": num_lines,
            "num_functions": num_functions
        }
    else:
        print(f"Failed to fetch file. Status code: {response.status_code}")
        return None

# Function to generate a personalized learning path based on analysis
def generate_learning_path(analysis):
    learning_path = []
    
    if analysis["num_functions"] < 3:
        learning_path.append("Learn about creating modular code with functions.")
    
    if analysis["lines_of_code"] > 200:
        learning_path.append("Break down large files into smaller, manageable modules.")
    
    if analysis["num_functions"] > 5:
        learning_path.append("Explore advanced Python techniques like decorators or generators.")
    
    return learning_path

# Example: Use a real GitHub repository to fetch files and analyze
owner = "octocat"  # GitHub username or organization
repo = "Hello-World"  # GitHub repository name

# Fetch all files from the repository
files = fetch_all_files_from_repo(owner, repo)

if files:
    for file_url in files:
        # Analyze each file's code
        analysis = analyze_code_from_url(file_url)
        if analysis:
            print(f"Analysis for {file_url}:")
            print(f"- Lines of code: {analysis['lines_of_code']}")
            print(f"- Number of functions: {analysis['num_functions']}")
            
            # Generate personalized learning path based on analysis
            learning_path = generate_learning_path(analysis)
            print("Suggested Learning Path:")
            for suggestion in learning_path:
                print(f"- {suggestion}")
            print()
