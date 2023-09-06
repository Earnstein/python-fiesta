import glob
import pandas as pd
from fpdf import FPDF
from pathlib import Path


def create_invoice_pdf(filepath):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoices nr. {invoice_nr}", align="L", ln=1)

    pdf.set_font(family="Times", size=12, style="B")
    pdf.cell(w=50, h=8, txt=f"Date: {date}", align="L", ln=1)

    # Add table header
    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    headers = df.columns
    headers = [header.replace("_", " ").title() for header in headers]
    pdf.set_font(family="Times", size=8, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=headers[0], border=1)
    pdf.cell(w=70, h=8, txt=headers[1], border=1)
    pdf.cell(w=30, h=8, txt=headers[2], border=1)
    pdf.cell(w=30, h=8, txt=headers[3], border=1)
    pdf.cell(w=30, h=8, txt=headers[4], border=1, ln=1)

    # Add rows to the table
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    # Output row
    total_price = str(df["total_price"].sum())
    pdf.set_font(family="Times", size=8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=total_price, border=1, ln=1)

    # Invoice message
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is {total_price}", ln=1)

    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=25, h=8, txt=f"Earnstein")
    pdf.image("Image/logo.jpg", w=10)

    # Output the PDF file
    pdf.output(f"PDFs/{filename}.pdf")


if __name__ == "__main__":
    # List all Excel files in the "Invoices" directory
    filepaths = glob.glob("Invoices/*.xlsx")

    # Process each invoice file
    for filepath in filepaths:
        create_invoice_pdf(filepath)
