/**
 * Google Apps Script Webhook für "MIAAC App Sheet" -> Tab "Jobs"
 * 
 * Anleitung zur Einrichtung:
 * 1. Öffne dein Google Sheet: https://docs.google.com/spreadsheets/d/1bhbz9838vMFmwHM6Pk_MjwyMgIw0l0nIPwVtFQqA1-g
 * 2. Klicke im Menü auf: Erweiterungen (Extensions) -> Apps Script
 * 3. Lösche dort den gesamten bestehenden Code und füge diesen Code hier ein.
 * 4. Klicke oben rechts auf: Bereitstellen (Deploy) -> Neue Bereitstellung (New deployment)
 * 5. Wähle Typ: "Web-App" (Zahnrad-Symbol)
 *    - Beschreibung: "Job Scraper Webhook"
 *    - Ausführen als: "Ich" (Me)
 *    - Wer hat Zugriff: "Jeder" (Anyone)
 * 6. Klicke auf "Bereitstellen" (Deploy), bestätige die Berechtigungen (Erweitert -> Weiter)
 *    und kopiere die erzeugte Web-App-URL (sieht aus wie https://script.google.com/macros/s/.../exec).
 * 7. Trage diese URL in deine .env Datei ein als:
 *    GOOGLE_SHEET_WEBHOOK_URL=https://script.google.com/macros/s/.../exec
 */

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Jobs");
    
    if (!sheet) {
      sheet = ss.insertSheet("Jobs");
      sheet.appendRow(["Category", "Job Title", "Employer", "Link"]);
    }
    
    // Parse incoming JSON payload
    var payload = JSON.parse(e.postData.contents);
    var jobs = Array.isArray(payload) ? payload : (payload.jobs || []);
    
    // Clear old entries and rewrite header to ensure backend is fully refreshed
    sheet.clearContents();
    sheet.getRange(1, 1, 1, 4).setValues([["Category", "Job Title", "Employer", "Link"]]);
    
    var rowsToInsert = [];
    var seenLinks = {};
    
    for (var i = 0; i < jobs.length; i++) {
      var job = jobs[i];
      var category = job.category || "Other";
      var title = job.title || "";
      var employer = job.employer || "";
      var link = (job.link || "").trim();
      
      // Prevent internal duplicates in the same batch
      var dedupeKey = link ? link : (title + "||" + employer);
      if (seenLinks[dedupeKey]) {
        continue;
      }
      seenLinks[dedupeKey] = true;
      
      if (title) {
        rowsToInsert.push([category, title, employer, link]);
      }
    }
    
    // Bulk write all current active rows
    if (rowsToInsert.length > 0) {
      sheet.getRange(2, 1, rowsToInsert.length, 4).setValues(rowsToInsert);
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "success",
        written: rowsToInsert.length,
        total_submitted: jobs.length,
        total_rows_now: sheet.getLastRow()
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "error",
        message: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      status: "active",
      message: "MIAAC Job Scraper Google Apps Script Webhook is running!"
    }))
    .setMimeType(ContentService.MimeType.JSON);
}
