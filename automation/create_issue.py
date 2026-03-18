import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

def create_issue():
    url = f"https://api.github.com/repos/{REPO}/issues"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    data = {
        "title": "🚨 Security Issues Detected in CI/CD",
        "body": "The pipeline detected vulnerabilities. Please review scan results."
    }

    requests.post(url, json=data, headers=headers)

create_issue()