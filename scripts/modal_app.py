"""
Modal Cloud Deployment Recipe
Run the Hackathon Factory autonomously on Modal's serverless GPU/CPU cloud.
Scheduled cron execution: Runs every 24 hours to scout, synthesize, and build.
"""

from pathlib import Path
import os
import modal

app = modal.App("hackathon-agent-factory")

ROOT_DIR = Path(__file__).parent.parent

# Define cloud container image
factory_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "curl", "build-essential")
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
        "curl -fsSL https://opencode.ai/install.sh | bash || true"
    )
    .env({
        "PATH": "/root/.bun/bin:/root/.opencode/bin:/usr/local/bin:/usr/bin:/bin",
        "TINYFISH_API_KEY": "oat_O56NK5QJZMY7BBZ6FJRH7S3ZFYZNJSTS",
        "NIA_API_KEY": "nk_JPOVIPNqKJvYMwNq1coc42dv2aNM1d3P",
        "PARALLEL_TASK_KEY": "GZH5U44pQHrEVjBaQcTN7CKabWsfE4tk1rQPponw"
    })
    .add_local_dir(str(ROOT_DIR), remote_path="/app")
)

# Persistent volume for project repositories and build deliverables
builds_volume = modal.Volume.from_name("hackathon-builds-volume", create_if_missing=True)

@app.function(
    image=factory_image,
    volumes={"/root/builds": builds_volume},
    timeout=3600,
    schedule=modal.Cron("0 6 * * *")  # Runs daily at 06:00 UTC
)
def run_daily_hackathon_factory():
    """Daily autonomous trigger."""
    import sys
    sys.path.append("/app")
    from factory.agno_orchestrator import build_hackathon_factory_agent

    print("⚡ Launching Cloud Hackathon Factory on Modal...")
    agent = build_hackathon_factory_agent(Path("/root/builds"))
    response = agent.run("Scan open hackathons with prize pool >= $10k, pick the top target, synthesize winning intel, and scaffold the build workspace.")
    print("Execution complete. Deliverables stored in Modal Volume.")
    return str(response)

@app.local_entrypoint()
def trigger_now():
    """Manual trigger from terminal: modal run scripts/modal_app.py"""
    print("Triggering cloud factory loop on Modal...")
    result = run_daily_hackathon_factory.remote()
    print(f"Cloud result:\n{result}")
