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

# Function to run a script
def run_script(script_name):
    script_path = os.path.join(current_dir, script_name)
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(['python', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Output of {script_name}:\n{result.stdout.decode('utf-8', errors='ignore')}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}:\n{e.stderr.decode()}")

# Run the scripts in sequence with 10-second breaks
for i, script in enumerate(scripts):
    run_script(script)

    # Add a 10-second break after each script (except the last one)
    if i < len(scripts) - 1:
        print("Waiting for 10 seconds before the next script...")
        time.sleep(10)
