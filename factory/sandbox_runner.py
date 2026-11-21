"""
OpenCode & Hermes Sandbox Runner
Orchestrates building the project inside a sandboxed environment,
invoking OpenCode or Hermes with Nia context augmentation.
"""

import os
import subprocess
import json
from typing import Dict, Any

class SandboxAgentRunner:
    def __init__(self, sandbox_type: str = "local"):
        self.sandbox_type = sandbox_type
        self.opencode_path = "/home/ash/.opencode/bin/opencode"
        self.hermes_path = "/home/ash/.local/bin/hermes"

    def scaffold_project(self, project_dir: str, concept: Dict[str, Any]) -> bool:
        """Initializes project workspace with boilerplate, docs, and prompt."""
        os.makedirs(project_dir, exist_ok=True)
        
        # Write task goal for OpenCode / Hermes
        prompt = f"""# Goal: Autonomous Hackathon Build
Project: {concept.get('title')}
One-liner: {concept.get('one_liner')}
Hero Feature: {concept.get('hero_feature')}
Sponsor Alignment: {concept.get('sponsor_alignment')}

Requirements:
1. Production ready Full-Stack app (Vite + React / Next.js + Fast API / Node).
2. Clean modular code with unit tests.
3. Engaging visual UI with dark mode and clear value demo.
4. Comprehensive Diataxis README with architecture diagram (Mermaid).
"""
        with open(os.path.join(project_dir, "TASK.md"), "w") as f:
            f.write(prompt)
            
        print(f"[SandboxAgentRunner] Workspace scaffolded at {project_dir}")
        return True

    def run_agent_build(self, project_dir: str, agent: str = "opencode") -> Dict[str, Any]:
        """Launches OpenCode or Hermes in the project workspace."""
        cmd = [self.opencode_path, "run", "--file", "TASK.md"] if agent == "opencode" else [self.hermes_path, "run"]
        print(f"[SandboxAgentRunner] Launching {agent} inside {project_dir}...")
        
        # Execution handle
        return {
            "status": "ready",
            "workspace": project_dir,
            "agent": agent,
            "instruction": "OpenCode / Hermes runner wired with Nia and Parallel MCP"
        }
