# nationalbibliographie
Dieses Programm gibt Katalogisate aus, die von der Deutschen Nationalbibliothek einer bestimmten Reihe der Nationalbibliografie zugeordnet werden. 

Der Start efolgt durch den Befehl "python nationalbibliographie.py"

Die Eingabe der gewünschten Reihe erfolgt in folgendem Format: 
- Jahr (zweistellig)
- Name der Reihe (meist "A", "B" oder "H")
- Nummer des Hefts im Jahr zweistellig

Beispiele wären: "24H01" oder "25A29"

In der Datei 'nationalbibliographie - config' ist eine Liste der DDC-Sachgruppen hinterlegt. Um eine einzelne Sachgruppe auszuschließen, muss man lediglich das 'True' hinter ihrem Namen durch 'False' ersetzen. 

Das Ergebnis wird als PDF ausgegeben, der Dateiname entspricht dem Titel der gewünschten Reihe. 

Die Ausgabe des Ergebnisses erfolgt in dem Verzeichnis, von dem aus das Programm gestartet wurde. 

Zur Umwandlung in ein PDF wird das Programm fpdf verwendet. Die dort eingebauten Schriften können die zahlreichen Akzentbuchstaben der Katalogisate nicht verarbeiten und führen zum Programmabsturz. Daher ist es nötig, eine eigene Schrift zu importieren (wenn es keine Unicode-Schrift ist, werden einige Zeichen nicht gedruckt, was aber wohl kein großes Problem darstellen sollte.) Diese Schrift (in normal, fett und kursiv) wird mit dem Befehl add_font in Zeilen 526-528 geladen. 
Momentan wird hier auf eine Windows-Standardschrift im Windows-Standardverzeichnis für Schriften zurückgegriffen, was auf den meisten Windows-PCs funktionieren sollte - ansonsten muss man hier eine andere Schrift (mit Pfad der Datei) einsetzen. 

Ich plane, künftig noch GND-Sätze von Personen- und Ortsschlagwörtern (und Erstem Geistigem Schöpfer bei einigen Sachgruppen, wie Literatur und Bildende Kunst) mit der GND abzugleichen und die Sätze, bei denen relevante regionale Bezüge (in meinem Fall zum Regierungsbezirk Schwaben) bestehe, zu markieren. 