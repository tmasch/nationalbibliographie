"""
Das ist eine Konfigurationsdatei für die Exzerpte aus der Nationalbibliographie. 
"""


def umlaut_nach_unicode(text):
    """
    Im Exportformat der GND wrden Buchstaben mit Umlauten oder Akzenten 
    als Kombination des Grundbuchstaben und eines Akzents oder Tremas 
    Sie werden hier durch die korrekten Unicode-Zeichen ersetzt. 
    Das wurde vor allem eingerichtet, weil LaTeX, das ich zuerst verwendete,
    bei der Verwendung nicht-vorgesehener Zeichen abstürzte
        """
    encoding_list = {"Ä" : "Ä", "Ö": "Ö", "Ü": "Ü", \
                     "ä": "ä", "á" : "á", "ă" : "ă", "ǎ" : "ă", "â" : "â", "å" : "å", "ā" : "ā", "å" : "å", "à" : "à", "ã" : "ã", "ẩ" : "ẩ", "Ā" : "Ā", "Á" : "Á", "À" : "À", "ą" : "ą", "ӑ" : "ă",\
                     "ç" : "ç", "č" : "č", "ć" : "ć", "Č" : "Č", "cʹ" : "ć", \
                     "Đ" : "Đ", "dʹ" : "ď", \
                     "É" : "É", "é": "é", "ě" : "ě" , "ē" : "ē", "ë" : "ë", "è" : "è", "ę" : "ę", "ǝ" : "\textschwa", "ǝ̀" : "ə\textschwa", "ė" : "ė", "ê" : "ê", "Ė" : "Ë", "È" : "È",\
                     "ǧ" : "ǧ", "ğ" : "ğ", "ģ" : "ģ", "ġ" : "ġ",  \
                     "ḥ": "ḥ", "ḫ" : "\textsubwedge{h}", "ḫ" : "\textsubwedge{h}", "Ḫ" : "\textsubwedge{H}", "ʰ" : "^h", \
                     "í" : "í", "ï" : "ï", "ī" : "ī",  "ì" : "ì", "Í" : "Í", "î" : "î", "ĺ" : "í", \
                     "ḳ" : r"\textsubdot{k}", \
                     "ł" : "ł", "lʹ" : "ľ", \
                     "ñ" : "ñ", "ń" : "ń", \
                    "ö": "ö", "ö" : "ö", "ó" : "ó", "ō" : "ō", "ò" : "ò", "õ" : "õ", "o͏̈" : "ő", "Ó" : "Ó", "ő" : "ő", \
                    "ř" : "ř", "ṛ" : "ṛ", "Ř" : "Ř", \
                     "Š" : "Š", "š" : "š", "ș" : "ş", "ş" : "ş", "Ś" : "Ś", "ṣ" : "ṣ", "š" : "š", "Š" : "Š", "sʹ" : "s'", "ś" : "ś",\
                     "ṭ" : u"\u1E6D", "ţ" : "\textsubdot{T}", "tʹ" : "ť", "ṯ" : "ṯ", "t̕’" : "ť", "Ṭ" : "\textsubdot{T}", "ṯ" : "ṯ", "t̕" : "ť", "Ţ" : "Ţ","ᵗ" : "^t", \
                    "ü": "ü", "ū" : "ū", "ù" : "ù", "ú" : "ú", "ů" : "ů", "ų" : "ų", "ữ" : "ṹ", "ứ" : "ứ", "ŭ" : "ù", "ǔ" : "ù", \
                    "ý" : "ý", \
                    "ž" : "ž", "ż" : "ż", "z̆" : "ž", "ź" : "ź", \
                    "Δ" : "\Delta", 
                    "⁹" : "^9",
                    "&" : r"\&", "#" : r"\#", "%" : "\%", "♥" :"", "ʿ" : "'", u'u200E' : "", u'u2009' : " ", u'\u0098' : '', u'\u009C' : '', u'\034F' : ""}
    for old, new in encoding_list.items():
        text = text.replace(old, new)

    return text


def sachgruppenliste():
    """
    Diese Funktion gibt ein Dictionary der in der Nationalbibliographie verwendeten DDCs zurück. 
    Die DDC ist der key, der Value ist ein Tupel aus der zu druckenden Überschrift und einem logischen 
    Feld, mit dem man einzelne Felder von der Anzeige ausschließen kann. 
    """
    sachgruppenliste = { "000" : ("000 Allgemeines, Wissenschaft", True),\
                  "004" : ("004 Informatik", True), \
                  "010" : ("010 Bibliografien", True), \
                  "020" : ("020 Bibliotheks- und Informationswissenschaft", True), \
                  "030" : ("030 Enyklopädien", True), \
                  "050" : ("050 Zeitschriften, fortlaufende Sammelwerke", True), \
                  "060" : ("060 Organisationen, Museumswissenschaft", True), \
                  "070" : ("070 Nachrichtenmedien, Journalismus, Verlagswesen", True), \
                  "080" : ("080 Allgemeine Sammelwerke", True), \
                  "100" : ("100 Philosophie", True), \
                  "130" : ("130 Parapsychologie, Okkultismus", True), \
                  "150" : ("150 Psychologie", True), \
                  "200" : ("200 Religion, Religionsphilosophie", True), \
                  "220" : ("220 Bibel", True), \
                  "230" : ("230 Theologie, Christentum", True), \
                  "290" : ("290 Andere Religionen", True), \
                  "300" : ("300 Sozialwissenschaften, Soziologie, Anthropoliege", True), \
                  "310" : ("310 Allgemeine Statistiken", True), \
                  "320" : ("320 Politik", True), \
                  "330" : ("330 Wirtschaft", True), \
                  "333.7" : ("333.7 Natürliche Ressourcen, Energie und Umwelt", True), \
                  "340" : ("340 Reht", True), \
                  "350" : ("350 Öffentliche Verwaltung", True), \
                  "355" : ("355 Militär", True), \
                  "360" : ("360 Soziale Probleme, Sozialdienste, Versicherungen", True), \
                  "370" : ("370 Erziehung, Schul- und Bildungswesen", True), \
                  "380" : ("380 Handel, Kommunikation, Verkehr", True), \
                  "390" : ("390 Bräuche, Etikette, Folklore", True), \
                  "400" : ("400 Sprache, Linguistik", True), \
                  "420" : ("420 Englisch", True), \
                  "430" : ("430 Deutsch", True), \
                  "439" : ("439 Andere Germanische Sprachen", True), \
                  "440" : ("440 Französisch, Romanische Sprachen allgemein", True), \
                  "450" : ("450 Italienisch, Rumänisch, Rätoromanisch", True), \
                  "460" : ("460 Spanisch, Portusiesisch", True), \
                  "470" : ("470 Latein", True), \
                  "480" : ("480 Griechisch", True), \
                  "490" : ("490 Andere Sprachen", True), \
                  "491.8" : ("491.8 Slawischen Sprachen", True), \
                  "500" : ("500 Naturwissenschaften", True), \
                  "510" : ("510 Mathematik", True), \
                  "520" : ("520 Astronomie, Kartografie", True), \
                  "530" : ("530 Physik", True), \
                  "540" : ("540 Chemie", True), \
                  "550" : ("550 Geowissenschaften", True), \
                  "560" : ("560 Paläontologie", True), \
                  "570" : ("570 Biowissenschaften, Biologie", True), \
                  "580" : ("580 Pflanzen (Botanik)", True), \
                  "590" : ("590 Tiere (Zoologie)", True), \
                  "600" : ("600 Technik", True), \
                  "610" : ("610 Medizin, Gesundheit", True), \
                  "620 " : ("620 Ingenieurwissenschaften und Maschinenbau", True), \
                  "621.3" : ("621.3 Elektrotechnik, Elektronik", True), \
                  "624" : ("624 Ingenieurbau und Umwelttechnik", True), \
                  "630" : ("630 Landwirtschaft, Veterinärmedizin", True), \
                  "640" : ("640 Hauswirtschaft und Familienleben", True), \
                  "650" : ("650 Management", True), \
                  "660" : ("660 Technische Chemie", True), \
                  "670" : ("670 Industrielle und handwerkliche Fertigung", True), \
                  "680" : ("680 Hausbau, Bauhandwerk", True), \
                  "700" : ("700 Künste, Bildende Kunst allgemein", True), \
                  "710" : ("710 Landschaftsgestaltung, Raumplanung", True), \
                  "720" : ("720 Architektur", True), \
                  "730" : ("730 Plastik, Numismatik, Keramik, Metallkunst", True), \
                  "740" : ("740 Grafik, Angewandte Kunst", True), \
                  "741.5" : ("741.5 Comics, Cartoons, Karikaturen", True), \
                  "750" : ("750 Malerei", True), \
                  "760" : ("760 Druckgrafik Drucke", True), \
                  "770" : ("770 Fotografie, Video, Computerkunst", True), \
                  "780" : ("780 Musik", True), \
                  "790" : ("790 Freizeitgestalltung, Darstellende Kunst", True), \
                  "791" : ("791 Öffentliche Darbietungen, Film, Rundfunk", True), \
                  "792" : ("792 Theater, Tanz", True), \
                  "793" : ("793 Spiel", True), \
                  "796" : ("796 Sport", True), \
                  "800" : ("800 Literatur, Rhetorik, Literaturwissenschaft", True), \
                  "810" : ("810 Englische Literatur Amerikas", True), \
                  "820" : ("820 Englische Literatur", True), \
                  "830" : ("830  Deutsche Literatur", True), \
                  "839" : ("839 Literatur in anderen germanischen Sprachen", True), \
                  "840" : ("840 Französische Literatur", True), \
                  "850" : ("850 Italienische, rumänische, rätoromanische Literatur", True), \
                  "860" : ("860 Spanische und portugiesische Literatur", True), \
                  "870" : ("870 Lateinische Literatur", True), \
                  "880" : ("880 Griechische Literatur", True), \
                  "890" : ("890 Literatur in anderen Sprachen", True), \
                  "891.8" : ("891.8 Slawische Literatur", True), \
                  "900" : ("900 Geschichte", True), \
                  "910" : ("910 Geografe, Reisen", True), \
                  "914.3" : ("914.3 Geografie, Reisen (Deutschland)", True), \
                  "920" : ("920 Biographie, Genealogie, Heraldik", True), \
                  "930" : ("930 Alte Geschichte, Archäologie", True), \
                  "940" : ("940 Geschichte Europas", True), \
                  "943" : ("943 Geschichte Deutschlands", True), \
                  "950" : ("950 Geschichte Asiens", True), \
                  "960" : ("960 Geschichte Afrikas", True), \
                  "970" : ("970 Geschichte Nordamerikas", True), \
                  "980" : ("980 Geschichte Südamerikas", True), \
                  "990" : ("990 Geschichte der übrigen Welt", True), \
                  "B" : ("B Belletristik", True), \
                  "K" : ("K Kinder- und Jugendliteratur", True), \
                  "S" : ("S Schulbücher", True)}
    return sachgruppenliste