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
    
    // Get existing links from Column D to prevent duplicates in the sheet
    var lastRow = sheet.getLastRow();
    var existingLinks = {};
    
    if (lastRow > 1) {
      var linksRange = sheet.getRange(2, 4, lastRow - 1, 1).getValues();
      for (var r = 0; r < linksRange.length; r++) {
        var linkVal = String(linksRange[r][0]).trim();
        if (linkVal) {
          existingLinks[linkVal] = true;
        }
      }
    }
    
    var addedCount = 0;
    var rowsToAppend = [];
    
    for (var i = 0; i < jobs.length; i++) {
      var job = jobs[i];
      var category = job.category || "Other";
      var title = job.title || "";
      var employer = job.employer || "";
      var link = (job.link || "").trim();
      
      // Duplicate check based on link (or title + employer if link is generic)
      if (link && existingLinks[link]) {
        continue;
      }
      
      if (title) {
        rowsToAppend.push([category, title, employer, link]);
        if (link) {
          existingLinks[link] = true;
        }
        addedCount++;
      }
    }
    
    // Bulk write new rows
    if (rowsToAppend.length > 0) {
      sheet.getRange(lastRow + 1, 1, rowsToAppend.length, 4).setValues(rowsToAppend);
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "success",
        added: addedCount,
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
