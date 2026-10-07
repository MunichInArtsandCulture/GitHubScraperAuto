# 🎭 Universal Art & Culture Job Scraper (Munich)

Ein moderner, flexibler und token-effizienter Scraper für Münchner Kunst- und Kultur-Jobs.

---

## 🚀 Was ist neu im Vergleich zum alten System?

| Altes System | Neues Universelles System |
|---|---|
| **30+ einzelne Skripte** (für jede Website eins) | **1 zentrales Skript** (`universal_scraper.py`) |
| Starre CSS-/XPath-Selektoren (gingen bei Redesigns kaputt) | **Inhaltsbasierte Markdown-Extraktion** (unabhängig vom Layout) |
| Riesige HTML-Blobs an LLM geschickt | **85–98% Token-Ersparnis** durch Vorfilterung & Smart Markdown |
| Aufwändige manuelle Pflege | Neue Websites einfach als 1 Zeile in `sources.json` eintragen |

---

## 🛠️ Funktionsweise

1. **HTML & Boilerplate Removal:**  
   Header, Navigationen, Footer, Cookie-Banner, Popups und Tracking-Skripte werden automatisch herausgefiltert.
2. **Dense Markdown Conversion:**  
   Links werden in absolute URLs umgewandelt (`[Titel](https://...)`) und Text wird auf die relevanten Inhaltsblöcke komprimiert.
3. **LLM Extraction & Categorization:**  
   Ein LLM (z.B. `gpt-4o-mini`) extrahiert Titel, Arbeitgeber, Link und ordnet den Job automatisch einer der 11 Telegram-Kategorien zu.
4. **Export:**  
   Speichert das Ergebnis in:
   - `categorized_jobs.txt` (für `job2telegram1.5.py`)
   - `jobs.json` (für Webseiten, APIs oder Datenbanken)
   - `scraped_history.json` (verhindert doppeltes Posten von Jobs)

---

## 📦 Setup & Installation

1. Abhängigkeiten installieren:
   ```bash
   pip install requests beautifulsoup4 trafilatura python-dotenv openai aiogram
   ```

2. `.env` Datei anlegen:
   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## 🏃 Verwendung

### 1. Alle 28 Kultur-Websites scrapen:
```bash
python scraper_repo/universal_scraper.py
```

### 2. Nur eine einzelne Website testen:
```bash
python scraper_repo/universal_scraper.py --url https://bergson.com/jobs
```

### 3. Neue Websites hinzufügen:
Öffne `scraper_repo/sources.json` und füge die neue Quelle hinzu:
```json
{
  "name": "Dein Kulturort",
  "url": "https://dein-kulturort.de/karriere"
}
```

### 4. Jobs an Telegram senden:
```bash
python scraper_repo/job2telegram1.5.py
```
