"""
Modal Cloud Deployment Recipe
Run the Hackathon Factory autonomously on Modal's serverless GPU/CPU cloud.
Complete End-to-End: Scanning -> Comp Intel -> Ideation -> Codebase Build -> GitHub Repo Creation.
"""

from pathlib import Path
import os
import modal

app = modal.App("hackathon-agent-factory")

ROOT_DIR = Path(__file__).parent.parent

# Define cloud container image
factory_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "curl", "build-essential", "unzip")
    .pip_install(
        "agno>=3.0.5",
        "httpx>=0.28.1",
        "pydantic>=2.10.4",
        "rich>=13.9.4",
        "python-dotenv>=1.0.1",
        "openai>=1.40.0"
    )
    .run_commands(
        "curl -fsSL https://bun.sh/install | bash",
        "curl -fsSL https://opencode.ai/install.sh | bash || true",
        # Install GitHub CLI
        "curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg",
        "chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg",
        "echo 'deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main' | tee /etc/apt/sources.list.d/github-cli.list > /dev/null",
        "apt update && apt install gh -y"
    )
    .env({
        "PATH": "/root/.bun/bin:/root/.opencode/bin:/usr/local/bin:/usr/bin:/bin",
        "TINYFISH_API_KEY": os.getenv("TINYFISH_API_KEY", "oat_O56NK5QJZMY7BBZ6FJRH7S3ZFYZNJSTS"),
        "NIA_API_KEY": os.getenv("NIA_API_KEY", "nk_JPOVIPNqKJvYMwNq1coc42dv2aNM1d3P"),
        "PARALLEL_TASK_KEY": os.getenv("PARALLEL_TASK_KEY", "GZH5U44pQHrEVjBaQcTN7CKabWsfE4tk1rQPponw")
    })
    .add_local_dir(str(ROOT_DIR), remote_path="/app", ignore=[".git", ".venv", "__pycache__", ".agents"])
)

# Persistent volume for project repositories and build deliverables
builds_volume = modal.Volume.from_name("hackathon-builds-volume", create_if_missing=True)

# Use Modal Secret for GitHub token to keep it secure
@app.function(
    image=factory_image,
    volumes={"/root/builds": builds_volume},
    secrets=[modal.Secret.from_name("github-secret", required_keys=["GH_TOKEN"])],
    timeout=3600,
    schedule=modal.Cron("0 6 * * *")  # Runs daily at 06:00 UTC
)
def run_daily_hackathon_factory():
    """Daily autonomous trigger: Scout -> Intel -> Ideate -> Build -> Create GitHub Repo."""
    import sys
    sys.path.append("/app")
    from factory.agno_orchestrator import build_hackathon_factory_agent

    print("⚡ [Modal Cloud] Launching Autonomous End-to-End Hackathon Factory...")
    agent = build_hackathon_factory_agent(Path("/root/builds"))
    
    prompt = """
    Execute the full end-to-end hackathon workflow:
    1. Scan open hackathons with prize pool >= $10k across all platforms.
    2. Pick the top-yield competition with highest win potential.
    3. Synthesize competitive intelligence and 10x concept with unfair advantages.
    4. Scaffold the project workspace and trigger OpenCode build.
    5. Generate the 5-tool demo video shotlist.
    6. Automatically create a remote public repository on GitHub under Ash-Blanc and push the project code.
    Report the final live GitHub repository URL and submission readiness summary.
    """
    
    response = agent.run(prompt)
    print("✔ [Modal Cloud] Pipeline finished successfully. Deliverables stored in Modal Volume.")
    return str(response)

@app.local_entrypoint()
def trigger_now():
    """Manual trigger from terminal: modal run scripts/modal_app.py"""
    print("Triggering cloud factory loop on Modal...")
    result = run_daily_hackathon_factory.remote()
    print(f"\n[Modal Cloud Result]:\n{result}")
