from fpdf import FPDF

def main():
    erzeuge_pdf()


def erzeuge_pdf():
    """erzeugt eine PDF-Datei aus den Exzerpten"""
    pdf = FPDF()
    pdf.set_font("Times", size=10)
    pdf.add_page()
    pdf.write(text = "ABCD")
    pdf.output("nationalbibliographie_experiment.pdf")


                    

if __name__ == "__main__":
    main()