import requests
from typing import Optional, List
from lxml import etree
from pydantic import BaseModel
#from fpdf import FPDF

import nationalbibliographie_config

class Normdaten(BaseModel):
    name : Optional[str] = ""
    id : Optional[str] = ""
    relevant : Optional[bool] = False

class Katalogisat(BaseModel):
    bibliographische_angaben: Optional[str] = ""
    ddc_zum_sortieren: Optional[str] = ""
    normdaten_liste: Optional[List[Normdaten]] = []
    schon_abgedruckt : Optional[bool] = False


def main():
    """
    Modul called for starting programme
    """
    bibliographie_liste = []
    bibliographie = input("Bitte Jahr, Reihe und Monat eingeben, z.B. 25A07: ")
    eintragsliste = lade_datensaetze_herunter(bibliographie)
    counter = 0
    for eintragsliste_teil in eintragsliste:
        if len(eintragsliste_teil) > 0:
            for eintrag in eintragsliste_teil:
                counter = counter + 1
                #print(counter)
                katalogisat = stelle_katalogisat_zusammen(eintrag)
                bibliographie_liste.append(katalogisat)
    txt_datei_erzeugen_alt(bibliographie_liste)
    #pdf_erzeugen(bibliographie_liste)

    
    
def txt_datei_erzeugen_alt(bibliographie_liste):
    sachgruppenliste = nationalbibliographie_config.sachgruppenliste()
    sachgruppennummernliste = list(sachgruppenliste.keys())
    #

    for sachgruppennummer in sachgruppennummernliste:
        print("Eintrag für folgende Sachgruppennummer")
        print(sachgruppennummer)
        print(sachgruppenliste[sachgruppennummer])
        liste_für_sachgruppe = []
        for katalogisat in bibliographie_liste:
            if sachgruppennummer in katalogisat.ddc_zum_sortieren and katalogisat.schon_abgedruckt is False and sachgruppenliste[sachgruppennummer][1] is True:
                katalogisat.schon_abgedruckt = True
                liste_für_sachgruppe.append(katalogisat)
        with open(r"C:\Users\berth\documents\Warburg\Experimente - Python\Nationalbibliographie\datensatzliste.txt", "a", encoding = "utf-8") as d:
            heading = r"\textbf{" + sachgruppenliste[sachgruppennummer][0] + r"}" +  r"\\" + r"\\"
            d.writelines(heading)
            for katalogisat in liste_für_sachgruppe:
                d.writelines(katalogisat.bibliographische_angaben + "; " + str(katalogisat.normdaten_liste) +  r"\\" + r"\\")
        
        



   


def find_datafields(record,tag_id):
    """
    Returns a list of all datafields of a MARCXML Document with the same field number
    """
    datafields=record.findall("{*}recordData/{*}record/{*}datafield[@tag='"+tag_id+"']")
    return datafields



def find_subfields(datafield,subfield_id):
    """
    Returns a list of all subfields of a datafield in a MARCXML 
    Document with the same subfield number
    """
    r=[]
    subfields=datafield.findall("{*}subfield")
    for subfield in subfields:
        key= subfield.get("code")
        value=subfield.text
        if key == subfield_id:
            value = nationalbibliographie_config.umlaut_nach_unicode(value)
            r.append(value)
    return r



def lade_datensaetze_herunter(bibliographie):
    """
    lädt die entsprechende Liste aus der GND herunter und gibt sie zurück
    """
    #bibliography = input("Bitte Jahr, Reihe und Monat eingeben, z.B. 25A07")
    url = r'https://services.dnb.de/sru/dnb?version=1.1&operation=searchRetrieve&query=WVN%3D'+bibliographie + r'&recordSchema=MARC21-xml&maximumRecords=100'
    antwort_roh = requests.get(url, timeout = 10)
    antwort = antwort_roh.content
    #print(antwort)
    root = etree.XML(antwort)
    if root[1].text:
        record_count = int(root[1].text)
    else:
        record_count = 0
    print('Number of records found')
    print(record_count)
    eintragsliste = []
    eintragsliste_teil = root.find("records", namespaces=root.nsmap)
    eintragsliste.append(eintragsliste_teil)
    start_record = 101
    while record_count > 100:
        print("start record")
        print(start_record)
        url = r'https://services.dnb.de/sru/dnb?version=1.1&operation=searchRetrieve&query=WVN%3D'+bibliographie + r'&recordSchema=MARC21-xml&maximumRecords=100&startRecord='+str(start_record)
        antwort_roh = requests.get(url, timeout = 10)
        antwort = antwort_roh.content
        #print(antwort)
        root = etree.XML(antwort)
        eintragsliste_teil = root.find("records", namespaces=root.nsmap)
        #print(eintragsliste_neu)
        eintragsliste.append(eintragsliste_teil)
        start_record = start_record + 100
        record_count = record_count-100

    return eintragsliste


def stelle_katalogisat_zusammen(eintrag):
    katalogisat = Katalogisat()
    katalogisat.ddc_zum_sortieren = ""
    ddc = lade_ddc(eintrag)
    if ddc:
        #print("DDC aus der Datenbank")
        #print(ddc)
        katalogisat.ddc_zum_sortieren = ddc

    bibliographische_angaben = ""
    erster_geistiger_schoepfer_name_fett, erster_geistiger_schoepfer_name, erster_geistiger_schoepfer_id = lade_ersten_geistigen_schoepfer(eintrag)
    if erster_geistiger_schoepfer_name_fett:
        bibliographische_angaben = bibliographische_angaben + erster_geistiger_schoepfer_name_fett
    if erster_geistiger_schoepfer_id: # muss noch auf bestimmte DDC-Klassen beschränkt werden
        normdaten = Normdaten(name=erster_geistiger_schoepfer_name, id=erster_geistiger_schoepfer_id)
        katalogisat.normdaten_liste.append(normdaten)
    titelangabe = lade_titel(eintrag)
    if titelangabe:
        bibliographische_angaben = bibliographische_angaben + titelangabe
    ausgabebezeichnung = lade_ausgabebezeichnung(eintrag)
    if ausgabebezeichnung:
        bibliographische_angaben = bibliographische_angaben + ausgabebezeichnung
    entstehungsangaben_liste = lade_entstehungsangaben(eintrag)
    if entstehungsangaben_liste:
        for entstehungsangaben in entstehungsangaben_liste:
            bibliographische_angaben = bibliographische_angaben + entstehungsangaben
    umfangsangaben = lade_umfangsangaben(eintrag)
    if umfangsangaben:
        bibliographische_angaben = bibliographische_angaben + umfangsangaben
    serienangaben_liste = lade_serienangaben(eintrag)
    if serienangaben_liste:
        for serienangabe in serienangaben_liste:
            bibliographische_angaben = bibliographische_angaben + serienangabe
    hochschulschriftenvermerk = lade_hochschulschriftenvermerk(eintrag)
    if hochschulschriftenvermerk:
        bibliographische_angaben = bibliographische_angaben + hochschulschriftenvermerk
    isbn_liste = lade_isbn(eintrag)
    if isbn_liste:
        for isbn in isbn_liste:
            bibliographische_angaben = bibliographische_angaben + isbn

    #print("x")
    #print(bibliographische_angaben)
    katalogisat.bibliographische_angaben = bibliographische_angaben
    return katalogisat


def lade_ddc(eintrag):
    """
    Offenbar gibt die DNB die DDC in Feld 082 an. Falls eine längere DDC vorliegt,
    steht in 083 eine Kurzfassung - falls nicht, steht die Kurzfassung in 082, und 
    nichts in 083. 
    Daher liest dieses System 082 aus und ersetzt die Angabe durch 083, wenn das vorliegt. 
    """
    ddc = []
    datafields = find_datafields(eintrag, "082")
    if datafields: 
        for datafield in datafields:
            subfields = find_subfields(datafield, "a")
            if subfields:
                for subfield in subfields:
                    ddc.append(subfield)
    datafields = find_datafields(eintrag, "083")
    if datafields:
        for datafield in datafields:
            subfields = find_subfields(datafield, "a")
            if subfields:
                for subfield in subfields:
                    ddc.append(subfield)
    # Manchmal ist versehentlich eine ausführliche Notation
    # in Feld 083, hoffentlich stets zusammen mit einer kurzen. 
    # Daher prüfe ich, ob es mehrere Unterfelder 083a gibt, und lösche
    # das mit einer längeren Notation (dabei nochmals Prüfung, ob es noch
    # weitere Notationen gibt, damit die Liste möglichst nicht leer wird. )
    ddc_fertig = []
    if len(ddc) ==1:
        ddc_fertig = ddc
    else:
        for notation in ddc:
            if len(notation)==3 or notation in ["333.7", "491.8", "621.3", "741.5", "891.8", "914.3", "B", "K", "S"]:
                ddc_fertig.append(notation)


    return ddc_fertig

def lade_ersten_geistigen_schoepfer(eintrag):
    """
    wertet das Feld MARC 100 (Erster Geistiger Schöpfer) aus - die GND-ID wird noch mitgenommen
    """
    person_name_fett, person_name, person_id = "", "", ""
    datafields = find_datafields(eintrag, "100")
    if datafields:
        subfields = find_subfields(datafields[0], "a")
        if subfields:
            person_name = subfields[0]
            if person_name:
                person_name_fett = r"\textbf{" + person_name + r"} : "
        subfields = find_subfields(datafields[0], "0")
        if subfields:
            person_id = subfields[0]
            if person_id[0:8] in ["(DE-101)", "(DE-588)"]:
                person_id = person_id[9:]
    return person_name_fett, person_name, person_id


def lade_titel(eintrag):
    """wertet das Feld MARC 245 (Titel + Titelzusatz + Verantwortlichkeitsangabe) aus"""
    titelangabe, titel, titelzusatz, bandangabe, verantwortlichkeitsangabe = "", "", "", "", ""
    datafields = find_datafields(eintrag, "245")
    if datafields:
        subfields = find_subfields(datafields[0], "a")
        if subfields:
            titel = subfields[0]
            #print(titel)
        subfields = find_subfields(datafields[0], "b")
        if subfields:
            titelzusatz = subfields[0]
            titelzusatz = " : " + titelzusatz

        subfields = find_subfields(datafields[0], "n")
        if subfields:
            bandangabe = subfields[0]
            bandangabe = " ; " + bandangabe # Hier bin ich mir wegen Trennzeichen nicht sicher

        subfields = find_subfields(datafields[0], "c")
        if subfields:
            verantwortlichkeitsangabe = subfields[0]
        if verantwortlichkeitsangabe:
            verantwortlichkeitsangabe = " / " + verantwortlichkeitsangabe
        titelangabe = titel + titelzusatz + bandangabe + verantwortlichkeitsangabe

    return titelangabe

def lade_ausgabebezeichnung(eintrag):
    """
    wertet das Feld MARC 250 (Ausgabebezeichnung) aus
    """
    ausgabebezeichnung = ""
    datafields = find_datafields(eintrag, "250")
    if datafields:
        subfields = find_subfields(datafields[0], "a")
        if subfields:
            ausgabebezeichnung = subfields[0]
    if ausgabebezeichnung:
        ausgabebezeichnung = ". - " + ausgabebezeichnung
    return ausgabebezeichnung

def lade_entstehungsangaben(eintrag):
    """
    wertet das Feld MARC 250 (Entstehungsangaben) aus - hier wird angenommen dass es mehrere Serien von Entstehungsangaben geben kann
    """
    entstehungsangaben_liste = []    
    datafields = find_datafields(eintrag, "264")
    if datafields:
        for datafield in datafields:
            entstehungsangaben, ort, verlag, jahr= "", "", "", ""
            entstehungsangaben = ""
            subfields = find_subfields(datafield, "a")
            if subfields:
                ort = subfields[0]
                entstehungsangaben = entstehungsangaben + ort
            subfields = find_subfields(datafield, "b")
            if subfields:
                verlag = subfields[0]
                if (verlag and entstehungsangaben):
                    entstehungsangaben = entstehungsangaben + " : " + verlag
            subfields = find_subfields(datafield, "c")
            if subfields:
                jahr = subfields[0]
                if (entstehungsangaben and ort) or (entstehungsangaben and verlag):
                    entstehungsangaben = entstehungsangaben + ", " + jahr
            entstehungsangaben_liste.append(entstehungsangaben)
            if entstehungsangaben_liste[0]:
                entstehungsangaben_liste[0] = ". - " + entstehungsangaben_liste[0]
            if len(entstehungsangaben_liste) > 1:
                for i in range(1, len(entstehungsangaben_liste)):
                    entstehungsangaben_liste[i] = "; " + entstehungsangaben_liste[i]
    #print("Entstehungsangaben: ")
    #print(entstehungsangaben_liste)
    return entstehungsangaben_liste

def lade_umfangsangaben(eintrag):
    """
    Wertet die Umfangangaben in Feld MARC 300 aus
    """
    umfangsangaben = ""
    umfangsangaben, seitenzahl, illustrationen, format = "", "", "", ""
    datafields = find_datafields(eintrag, "300")
    if datafields:
        subfields = find_subfields(datafields[0], "a")
        if subfields:
            seitenzahl = subfields[0]
        subfields = find_subfields(datafields[0], "b")
        if subfields:
            illustrationen = subfields[0]
            if seitenzahl and illustrationen:
                illustrationen = " : " + illustrationen
        subfields = find_subfields(datafields[0], "c")
        if subfields:
            format = subfields[0]
            if (seitenzahl and format) or (illustrationen and format):
                format = " ; " + format
        umfangsangaben = seitenzahl + illustrationen + format
        if umfangsangaben:
            umfangsangaben = ". - " + umfangsangaben
    return umfangsangaben

def lade_serienangaben(eintrag):
    """
    Wertet die Angaben zu Serien in Feld MARC 490 aus
    """
    serienangaben_liste = []
    datafields = find_datafields(eintrag, "490")
    if datafields:
        for datafield in datafields:
            serienangaben, serienname, bandnummer = "", "", ""
            subfields = find_subfields(datafield, "a")
            if subfields:
                serienname = subfields[0]
                #print("Serie gefunden")
                #print(serienname)
            subfields = find_subfields(datafield, "v")
            if subfields:
                bandnummer = subfields[0]
                bandnummer = " ; " + bandnummer 
                # ich brauche kein 'if', da es Bandnummern ohne Serie nicht geben sollte
            serienangaben = serienname + bandnummer
            serienangaben_liste.append(serienangaben)
            if len(serienangaben_liste) > 1:
                for i in range(1, len(serienangaben_liste)):
                    serienangaben_liste[i] = "; " + serienangaben_liste[i]
    if serienangaben_liste:
        serienangaben_liste[0] = ". - (" + serienangaben_liste[0]
        serienangaben_liste[-1] = serienangaben_liste[-1] + ")"

    return serienangaben_liste

def lade_hochschulschriftenvermerk(eintrag):
    """
    Wertet den Hochschulschriftenvermerk in MARC 502 aus
    """
    hochschulschriftenvermerk, typ, einrichtung, jahr = "", "", "", ""
    datafields = find_datafields(eintrag, "502")
    if datafields:
        subfields = find_subfields(datafields[0], "b")
        if subfields:
            typ = subfields[0]
        subfields = find_subfields(datafields[0], "c")
        if subfields:
            einrichtung = subfields[0]
            if typ:
                einrichtung = ", " + einrichtung
        subfields = find_subfields(datafields[0], "d")
        if subfields:
            jahr = subfields[0]
            if (typ or einrichtung):
                jahr = ", " + jahr
        hochschulschriftenvermerk = typ + einrichtung + jahr
    if hochschulschriftenvermerk:
        hochschulschriftenvermerk = ". - " + hochschulschriftenvermerk
    return hochschulschriftenvermerk


def lade_isbn(eintrag):
    """
    wertet ISBN-Nummer uind Preis aus MARC 020 aus. 
    Ich frage mnich, ob man, wenn es mehrere ISBN-Nummern gibt, 
    prüfen soll, ob sie bis auf Präfix 978 gleich sind, und dann das ohne
    Präfix wegläßt?
    """
    isbn_liste = []
    isbn_gesamt = ""
    datafields = find_datafields(eintrag, "020")
    for datafield in datafields:
        isbn_nummer, isbn_kommentar = "", ""
        subfields = find_subfields(datafield, "9")
        if subfields:
            isbn_nummer = subfields[0]
            #print("ISBN gefunden")
            #print(isbn_nummer)
        subfields = find_subfields(datafield, "c")
        if subfields:
            isbn_kommentar = subfields[0]
            if isbn_nummer:
                isbn_kommentar = " " + isbn_kommentar
        isbn_gesamt = isbn_nummer + isbn_kommentar
        isbn_liste.append(isbn_gesamt)
    if isbn_liste:
        isbn_liste[0] = ". - " + isbn_liste[0]
    if len(isbn_liste) > 1:
        for i in range(1, len(isbn_liste)):
                    isbn_liste[i] = "; " + isbn_liste[i]
    return isbn_liste


def erzeuge_pdf():
    pass

                    

if __name__ == "__main__":
    main()