import pandas as pd
from fpdf import FPDF

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)
df = pd.read_csv("topic.csv")


def header(title):
    """Creates note title"""
    pdf.set_font(family="Times", style="B", size=24)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=12, txt=title, align="L", ln=1)
    pdf.line(10.5, 20.5, 199.5, 20.5)


def note_lines(y_cor: int):
    """Creates note lines that are 10mm apart"""
    for i in range(y_cor, 290, 10):
        pdf.line(10.5, i, 199.5, i)


def footer(title: str, line: int):
    """"Creates note footer style"""
    pdf.ln(line)
    pdf.set_font(family="Times", style="I", size=8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(w=0, h=10, txt=title, align="R")


def main():
    for index, row in df.iterrows():
        text = row["Topic"]
        num_of_pages = row["Pages"] - 1

        # HEADER
        pdf.add_page()
        header(text)

        # NOTE LINE
        note_lines(y_cor=30)

        # FOOTER
        footer(text, 265)
        for i in range(num_of_pages):
            pdf.add_page()
            pdf.line(10.5, 20.5, 199.5, 20.5)
            note_lines(y_cor=30)
            footer(text, 275)

    pdf.output("output.pdf")


if __name__ == '__main__':
    main()
