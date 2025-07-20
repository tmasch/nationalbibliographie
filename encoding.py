
import requests
import unicodedata as ud

# grep für Sonderzeichen [^a-z0-9<>/ =\"\-(),\n\[\];\\|\.?:\&#]


def main():

    bibliographie="25A07"
    # https://www.dnb.de/DE/Professionell/Metadatendienste/Datenbezug/metadatenBezugUndFormate.html
    # https://www.dnb.de/SharedDocs/Downloads/DE/Professionell/Metadatendienste/Rundschreiben/rundschreibenUmstellungUTF8.html?nn=58304
    # Die DNB gibt UTF-8 decomposed zurück.
    url = r'https://services.dnb.de/sru/dnb?version=1.1&operation=searchRetrieve&query=WVN%3D'+bibliographie + r'&recordSchema=MARC21-xml&maximumRecords=100'
    print(url)
    antwort_roh = requests.get(url, timeout = 10)
    t=antwort_roh.content

    # ud.normalize funktioniert nur mit strings, nicht bytes
    tt=ud.normalize('NFC',t)
    print(tt)



if __name__ == "__main__":
    main()
