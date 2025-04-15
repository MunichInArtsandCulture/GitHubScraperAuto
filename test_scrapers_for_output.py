import os
import runpy
import sys
import io
from datetime import datetime

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

log_filename = f"scraper_output_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

def test_scrapers():
    with open(log_filename, "w", encoding="utf-8") as logfile:
        for script in scraper_files:
            if not os.path.exists(script):
                msg = f"❌ {script} nicht gefunden."
                print(msg)
                logfile.write(msg + "\n")
                continue

            header = f"\n🔍 Teste {script}..."
            print(header)
            logfile.write(header + "\n")

            # Stdout abfangen
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            try:
                runpy.run_path(script)
                output = sys.stdout.getvalue().strip()
            except Exception as e:
                output = f"❌ Fehler beim Ausführen: {e}"
            finally:
                sys.stdout = old_stdout

            if not output:
                msg = f"⚠️  {script} hat **keine Ausgabe geliefert**."
            else:
                short = output[:400] + ("..." if len(output) > 400 else "")
                msg = f"✅ {script} liefert Ausgabe:\n{short}"

            print(msg)
            logfile.write(msg + "\n")

if __name__ == "__main__":
    test_scrapers()
