function getDataFromGoogleDoc() {
  var docId = '1xT5Ovg8pouKkpwHXKdU45J9vlyqEYD__ZGuKZErmhTU';  // Ersetze mit deiner tatsächlichen Google-Dokument-ID
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  // Durchsuche alle Tabellen im Dokument
  var tables = body.getTables();

  for (var i = 0; i < tables.length; i++) {
    var table = tables[i];

    // Durchlaufe jede Zelle in der Tabelle
    for (var row = 0; row < table.getNumRows(); row++) {
      for (var col = 0; col < table.getRow(row).getNumCells(); col++) {
        var cell = table.getCell(row, col);  // Die aktuelle Zelle

        var text = cell.getText();

          // Überprüfe, ob der String "02.02." in der Zelle vorkommt
          if (text.indexOf("02.02.") !== -1) {
            // Formatiere den Text (fügt Zeilenumbrüche vor Emojis hinzu und markiert fettgedruckten Text)
            var formattedText = addFormatting(text, cell); // Übergabe der Zelle an addFormatting

            // Sende den formatierten Text an Telegram
            postToTelegram(formattedText);   // Sende die Nachricht
          }
  // ... (dein bestehender Code)
}

function addFormatting(text, cell) {  // Parameter für die Zelle hinzufügen
  // Emojis mit Zeilenumbrüchen versehen
  var emojiRegex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{2300}-\u{23FF}\u{2B50}\u{23F0}\u{1F004}\u{1F0CF}\u{1F201}-\u{1F251}\u{1F004}\u{1F0CF}]/gu;
  text = text.replace(emojiRegex, function(match, offset, string) {
    if (offset > 0 && string[offset - 1] !== '\n') {
      return '\n' + match;
    }
    return match;
  });

  // Fettgedruckten Text mit ** umschließen
  var formattedText = "";
  for (var i = 0; i < text.length; i++) {
    var style = cell.getTextStyle(i, i + 1);
    if (style.isBold()) {
      formattedText += "**" + text[i] + "**";
    } else {
      formattedText += text[i];
    }
  }
  return formattedText;
}

function postToTelegram(message) {
  var botToken = '7088435202:AAEiMKtFxJQvA3Shdcv8sQP6vGxyOKt7Ktw';  // Ersetze mit deinem Telegram Bot Token
  var chatId = '-1002339250618';  // Ersetze mit der Chat-ID deiner Gruppe
  var url = 'https://api.telegram.org/bot' + botToken + '/sendMessage';
  var payload = {
    'chat_id': chatId,
    'text': message
  };

  var options = {
    'method': 'post',
    'payload': payload
  };

  UrlFetchApp.fetch(url, options);  // Sendet die Nachricht an Telegram
}
