import subprocess
import os
import time

# Get the current directory (the folder the script is in)
current_dir = os.path.dirname(os.path.realpath(__file__))

# List of Python scripts to execute in order
scripts = [
    "00job_scraper_master2.5.py",
    "job_classifier1.3.py",
    "job2telegram1.5.py",
    "JobListUpdateMessage.py"
]

# Function to run a script with live output
def run_script(script_name):
    script_path = os.path.join(current_dir, script_name)
    print(f"\n🎬 Running {script_name}...\n")
    try:
        result = subprocess.run(['python', script_path], check=True)
        print(f"✅ {script_name} completed.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_name}:")
        print(e)
        # Optional: Exit the full pipeline on error
        # raise e

# Run the scripts in sequence with 10-second breaks
for i, script in enumerate(scripts):
    run_script(script)

    # Add a 10-second break after each script (except the last one)
    if i < len(scripts) - 1:
        print("⏳ Waiting for 10 seconds before the next script...\n")
        time.sleep(10)
