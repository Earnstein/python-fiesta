import glob
import pandas as pd
from fpdf import FPDF
from pathlib  import Path

filepaths = glob.glob("Invoices/*.xlsx")
for filepath in filepaths:
    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    filename = Path(filepath).stem
    invoice_nr_list = filename.split("-")
    invoice_nr = invoice_nr_list[0]
    text = f"Invoices nr. {invoice_nr}"
    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=text, align="R")
    pdf.output(f"PDFs/{filename}.pdf")