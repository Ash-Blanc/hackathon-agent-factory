"""
The 5-Tool Demo Video Production Automation Toolkit
Integrates the complete professional 5-tool workflow into the Hackathon Agent Factory:
1. EasyEffects (Live PipeWire RNNoise background mic cleaning)
2. Audacity / TTS Voice-First Modular Cue Engine (01_hook.wav, 02_problem.wav, 03_demo.wav, 04_under_the_hood.wav, 05_cta.wav)
3. OpenScreen / Chromium 1600x900 App Recording Automation (borderless, smooth cursor zoom, framing, drop-shadow)
4. Kdenlive Automation (Project template generator, 300%+ speed ramping for loading screens, auto-captions via Whisper/Vosk)
5. FFmpeg Ultra-Fast Hardware-Accelerated Export (NVENC/VAAPI, -qp 20 / -cq 20 crisp web-optimized MP4)
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from agno.tools import Toolkit

class DemoVideoProductionToolkit(Toolkit):
    """Agno Toolkit for automating the 5-Tool Demo Video Loop."""

    def __init__(self, workspace_dir: Path):
        super().__init__(name="demo_video_production_toolkit")
        self.workspace_dir = workspace_dir
        self.register(self.generate_voice_first_shotlist)
        self.register(self.scaffold_openscreen_capture_script)
        self.register(self.generate_kdenlive_assembly_manifest)
        self.register(self.render_ffmpeg_accelerated_mp4)

    def generate_voice_first_shotlist(
        self,
        project_name: str,
        problem: str,
        hero_feature: str,
        tech_stack: str
    ) -> str:
        """
        Step 1 & 2: Lock in voiceover clips first (01_hook.wav, 02_demo.wav...)
        Generates timed modular voice cues with exact pacing so the UI recording matches the audio.
        """
        clips = [
            {
                "id": "01_hook",
                "audio_file": "01_hook.wav",
                "video_file": "01_hook.mp4",
                "target_sec": 12,
                "script": f"Most hackathon teams don't lose on code—they lose in the last 6 hours trying to explain why their project matters. Meet {project_name}.",
                "ui_action": "Chromium window opens instantly on landing page hero card with smooth drop shadow."
            },
            {
                "id": "02_problem",
                "audio_file": "02_problem.wav",
                "video_file": "02_problem.mp4",
                "target_sec": 15,
                "script": f"Here's the friction: {problem}. Existing solutions leave developers stuck in manual configurations and fragmented tools.",
                "ui_action": "Pan down to show the painful status quo or terminal error log."
            },
            {
                "id": "03_demo",
                "audio_file": "03_demo.wav",
                "video_file": "03_demo.mp4",
                "target_sec": 35,
                "script": f"With {project_name}, everything changes. With a single click, our autonomous loop triggers {hero_feature}. Watch the live status update in real time.",
                "ui_action": "Smooth cursor glide to primary CTA, click trigger, observe real-time live data response (speed-ramped 300% on network wait)."
            },
            {
                "id": "04_under_the_hood",
                "audio_file": "04_under_the_hood.wav",
                "video_file": "04_under_the_hood.mp4",
                "target_sec": 20,
                "script": f"Under the hood, we leverage {tech_stack} with cloud sandbox isolation and verifiable outputs.",
                "ui_action": "Switch to architecture overview / network tab / inspect panel highlighting sponsor integration."
            },
            {
                "id": "05_cta",
                "audio_file": "05_cta.wav",
                "video_file": "05_cta.mp4",
                "target_sec": 10,
                "script": f"{project_name} is fully open source on GitHub and deployed live right now. Thank you!",
                "ui_action": "Zoom back to clean production dashboard with GitHub repository link."
            }
        ]

        shots_dir = self.workspace_dir / "demo_assets" / "clips"
        shots_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = self.workspace_dir / "demo_assets" / "shotlist.json"
        
        with open(manifest_path, "w") as f:
            json.dump(clips, f, indent=2)

        return json.dumps({
            "status": "ready",
            "shotlist_file": str(manifest_path),
            "clips_count": len(clips),
            "total_duration_sec": sum(c["target_sec"] for c in clips),
            "instructions": "Voice-First principle: Record or generate 01_hook.wav to 05_cta.wav first, then record matching 1600x900 window video clips."
        }, indent=2)

    def scaffold_openscreen_capture_script(self, target_url: str) -> str:
        """
        Step 3: OpenScreen / Chromium Borderless 1600x900 Capture Automation.
        Generates bash script to launch borderless Chromium window with auto-framing and cursor capture.
        """
        script_path = self.workspace_dir / "demo_assets" / "launch_capture_window.sh"
        content = f"""#!/usr/bin/env bash
# OpenScreen / Chromium Borderless 1600x900 Capture Launcher
# Runs borderless with exact 1600x900 dimensions for pixel-perfect recording.

TARGET_URL="{target_url}"
echo "🎥 Launching 1600x900 borderless capture window for $TARGET_URL..."

# Launch Chromium in app mode with fixed 1600x900 window size
chromium \\
  --app="$TARGET_URL" \\
  --window-size=1600,900 \\
  --window-position=100,100 \\
  --force-device-scale-factor=1 \\
  --disable-features=TranslateUI \\
  --no-first-run \\
  --no-default-browser-check &

PID=$!
echo "Window active (PID: $PID). Ready for OpenScreen / OBS recording matching voiceover clips."
"""
        with open(script_path, "w") as f:
            f.write(content)
        os.chmod(script_path, 0o755)

        return f"Capture script created at {script_path}. Run to open 1600x900 borderless stage."

    def generate_kdenlive_assembly_manifest(self) -> str:
        """
        Step 4: Kdenlive Assembly & Speed-Ramping.
        Builds the timeline configuration mapping 01_hook.wav + 01_hook.mp4, applying
        300%+ speed ramps during network/build waits, and setting up Whisper/Vosk subtitles.
        """
        template_spec = {
            "template_name": "Hackathon_Winning_Demo_1080p60",
            "resolution": "1920x1080",
            "fps": 60,
            "tracks": [
                {"name": "V2_Captions", "type": "subtitles", "engine": "whisper_burned_in"},
                {"name": "V1_Screencast", "type": "video", "source_clips": ["01_hook.mp4", "02_problem.mp4", "03_demo.mp4", "04_under_the_hood.mp4", "05_cta.mp4"]},
                {"name": "A1_Voiceover", "type": "audio", "source_clips": ["01_hook.wav", "02_problem.wav", "03_demo.wav", "04_under_the_hood.wav", "05_cta.wav"]},
                {"name": "A2_Ambience", "type": "audio", "volume": -22.0, "source": "subtle_synthwave_backing.mp3"}
            ],
            "speed_ramping_rules": [
                {"scene": "03_demo.mp4", "wait_condition": "spinner_or_load", "speed": "350%", "smooth_transition": True}
            ]
        }
        
        manifest_path = self.workspace_dir / "demo_assets" / "kdenlive_timeline.json"
        with open(manifest_path, "w") as f:
            json.dump(template_spec, f, indent=2)

        return f"Kdenlive timeline assembly specification saved to {manifest_path}."

    def render_ffmpeg_accelerated_mp4(
        self,
        input_video_path: str,
        output_mp4_path: str,
        accel: str = "cpu"  # cpu, nvenc, vaapi
    ) -> str:
        """
        Step 5: FFmpeg Ultra-Fast GPU-Accelerated Web-Optimized Export.
        Encodes crisp, low-latency MP4 (-qp 20 / -cq 20) with faststart for instant Devpost/Twitter streaming.
        """
        if accel == "nvenc":
            cmd = [
                "ffmpeg", "-y", "-i", input_video_path,
                "-c:v", "h264_nvenc", "-cq", "20", "-preset", "p6",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", output_mp4_path
            ]
        elif accel == "vaapi":
            cmd = [
                "ffmpeg", "-y", "-vaapi_device", "/dev/dri/renderD128",
                "-i", input_video_path,
                "-vf", "format=nv12,hwupload",
                "-c:v", "h264_vaapi", "-qp", "20",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", output_mp4_path
            ]
        else:
            # CPU fallback with libx264 -crf 20
            cmd = [
                "ffmpeg", "-y", "-i", input_video_path,
                "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", output_mp4_path
            ]

        return json.dumps({
            "command": " ".join(cmd),
            "instructions": f"Run command or invoke via pipeline to render final demo MP4 to {output_mp4_path}."
        }, indent=2)
