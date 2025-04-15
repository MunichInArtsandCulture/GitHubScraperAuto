import os
import runpy
import sys
import io

# Directory containing the scrapers (current directory)
scrapers_dir = os.getcwd()

# List of scraper filenames
scraper_files = [
    "job_scraper_adbk.py",
    "job_scraper_bahnwaerterthiel.py",
    "job_scraper_bergson.py",
    "job_scraper_buehnenjobs1.2.py",
    "job_scraper_feierwerk.py",
    "job_scraper_gaertnerplatztheater1.2.py",
    "job_scraper_glockenbachwerkstatt.py",
    "job_scraper_HDK1.6.py",
    "job_scraper_kultweet1.3.py",
    "job_scraper_kunsthalle-muc.py",
    "job_scraper_museum-brandhorst.py",
    "job_scraper_museum-fuenf-kontinente.py",
    "job_scraper_pasinger-fabrik1.2.py",
    "job_scraper_philharmoniker.py",
    "job_scraper_pinakothek.py",
    "job_scraper_residenztheater1.2.py",
    "job_scraper_staatsoper_buehne.py",
    "job_scraper_staatsoper_buero.py",
    "job_scraper_staatsoper_praktika-ausbildung.py",
    "job_scraper_theaterakademie-august-everding.py",
    "job_scraper_theater-hochx1.2.py",
    "job_scraper_tollwood_jobs.py",
    "job_scraper_tollwood_praktikum.py",
    "job_scraper_unterfahrts.py",
    "job_scraper_wow.py",
    "job_scraper_arbeitsagentur_teil3.py",
    "job_scraper_muenchen.de1.2.py",
    "job_scraper_blitz.py",
]

# Setze den Headless-Modus
headless_mode = True  # Kann auf False gesetzt werden, falls der Headless-Modus nicht gewünscht ist
os.environ['HEADLESS_MODE'] = 'True' if headless_mode else 'False'


def execute_scripts():
    all_output = ""
    for script in scraper_files:
        script_path = os.path.join(scrapers_dir, script)
        if os.path.exists(script_path):
            try:
                print(f"Executing {script}...")

                # Capture stdout and stderr
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()

                runpy.run_path(script_path)  # Execute the script

                stdout_output = sys.stdout.getvalue()
                stderr_output = sys.stderr.getvalue()

                sys.stdout = old_stdout
                sys.stderr = old_stderr

                # Format the output with the "---" around the script name
                all_output += f"\n--- \n{script} \n---\n"  # Format with the script name surrounded by "---"
                all_output += stdout_output
                if stderr_output:
                    all_output += f"\n--- {script} Errors ---\n"
                    all_output += stderr_output

                print(stdout_output)  # Print to console as well
                if stderr_output:
                    print(stderr_output)

            except Exception as e:
                all_output += f"Error executing {script}: {e}\n"
                print(f"Error executing {script}: {e}")  # Print to console as well
        else:
            all_output += f"Script {script} not found!\n"
            print(f"Script {script} not found!")  # Print to console as well
    return all_output


# Main function to run the scraping and save the output
def main():
    # Step 1: Execute all scrapers and collect the jobs
    all_output = execute_scripts()

    # Step 2: Save all output to a text file
    with open('cooljobs.txt', 'w', encoding='utf-8') as f:  # Use utf-8 encoding
        f.write(all_output)

    print("Scraping complete. Output saved to cooljobs.txt")


if __name__ == "__main__":
    main()
