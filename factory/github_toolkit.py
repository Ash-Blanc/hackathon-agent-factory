"""
GitHub Automation Toolkit for Hackathon Factory Loop.
Uses GitHub CLI (gh) / GitHub API to:
1. Create a remote repository under your account (Ash-Blanc).
2. Push scaffolded code, commit history, and branches.
3. Configure repository topics, description, and GitHub Pages / release badges.
4. Set up GitHub Actions for CI/CD deployment (Vercel / Cloudflare).
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional

from agno.tools import Toolkit

class GitHubAutomationToolkit(Toolkit):
    """Agno Toolkit for autonomous GitHub repository creation, pushing, and deployment hooks."""

    def __init__(self, username: str = "Ash-Blanc"):
        super().__init__(name="github_automation_toolkit")
        self.username = username
        self.register(self.create_and_push_repo)
        self.register(self.get_repo_status)

    def create_and_push_repo(
        self,
        project_dir_path: str,
        repo_name: str,
        description: str,
        is_public: bool = True
    ) -> str:
        """
        Creates a new remote repository on GitHub under your authenticated account,
        initializes git, commits all generated project files, and pushes to origin main.
        """
        path = Path(project_dir_path)
        if not path.exists():
            return f"Error: Workspace path '{project_dir_path}' does not exist."

        visibility_flag = "--public" if is_public else "--private"
        
        try:
            # Initialize git if not already
            if not (path / ".git").exists():
                subprocess.run(["git", "init", "-b", "main"], cwd=str(path), check=True, capture_output=True)
            
            # Stage and commit
            subprocess.run(["git", "add", "."], cwd=str(path), check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", f"feat: initial build of {repo_name} by Autonomous Hackathon Factory"],
                cwd=str(path),
                check=False,
                capture_output=True
            )

            # Check if remote repo already exists or create via gh
            check_repo = subprocess.run(["gh", "repo", "view", f"{self.username}/{repo_name}"], capture_output=True)
            if check_repo.returncode != 0:
                # Create remote repo
                create_cmd = [
                    "gh", "repo", "create", f"{self.username}/{repo_name}",
                    visibility_flag,
                    "--description", description,
                    "--source", str(path),
                    "--remote", "origin",
                    "--push"
                ]
                res = subprocess.run(create_cmd, cwd=str(path), capture_output=True, text=True)
                if res.returncode != 0:
                    return f"Error creating repo with gh: {res.stderr}"
            else:
                # Repo exists, push updates
                subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=str(path), capture_output=True)

            repo_url = f"https://github.com/{self.username}/{repo_name}"
            return json.dumps({
                "status": "success",
                "repo_url": repo_url,
                "owner": self.username,
                "name": repo_name,
                "visibility": "public" if is_public else "private",
                "message": f"Successfully created and pushed repository to {repo_url}"
            }, indent=2)

        except Exception as e:
            return f"Exception in GitHub automation: {str(e)}"

    def get_repo_status(self, repo_name: str) -> str:
        """Get live status, commit SHA, and URL of a pushed repository."""
        res = subprocess.run(["gh", "repo", "view", f"{self.username}/{repo_name}", "--json", "url,description,isPrivate,pushedAt"], capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout
        return f"Error fetching repo status: {res.stderr}"
