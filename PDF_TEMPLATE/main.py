import pandas as pd
from fpdf import FPDF
from datetime import datetime
from typing import Optional


class NotebookGenerator:
    def __init__(self):
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=False, margin=0)
    
    def header(self, title):
        """Creates note title"""
        # Large title on the left
        self.pdf.set_font(family="Times", style="B", size=24)
        self.pdf.set_text_color(100, 100, 100)
        self.pdf.cell(w=120, h=12, txt=title, align="L", ln=0)
        
        # Small title on the right (top)
        self.pdf.set_font(family="Times", style="I", size=8)
        self.pdf.set_text_color(180, 180, 180)
        self.pdf.cell(w=0, h=6, txt=title, align="R", ln=1)
        
        # Date below the small title (right side)
        self.pdf.set_xy(120, 16)  # Position for date
        self.pdf.set_font(family="Times", style="", size=10)
        self.pdf.set_text_color(120, 120, 120)
        self.pdf.cell(w=0, h=6, txt="Date: ___/___/___", align="R", ln=1)
        
        self.pdf.line(10.5, 20.5, 199.5, 20.5)

    def note_lines(self, y_cor: int):
        """Creates note lines that are 10mm apart"""
        for i in range(y_cor, 290, 10):
            self.pdf.line(10.5, i, 199.5, i)

    def footer(self, title: str, line: int):
        """"Creates note footer style"""
        self.pdf.ln(line)
        self.pdf.set_font(family="Times", style="I", size=8)
        self.pdf.set_text_color(180, 180, 180)
        self.pdf.cell(w=0, h=10, txt=title, align="R")

    def generate_notebook(self, topics_file: str, name: Optional[str] = None):
        """Generate notebook from topics file"""
        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        df = pd.read_csv(topics_file)
        
        for index, row in df.iterrows():
            text = str(row["Topic"])
            num_of_pages = row["Pages"] - 1

            # HEADER
            self.pdf.add_page()
            self.header(text)

            # NOTE LINE
            self.note_lines(y_cor=30)

            # FOOTER
            self.footer(text, 265)
            for i in range(num_of_pages):
                self.pdf.add_page()
                self.pdf.line(10.5, 20.5, 199.5, 20.5)
                self.note_lines(y_cor=30)
                self.footer(text, 275)

        self.pdf.output(f"books/{name}.pdf")
        print(f"Notebook generated: {name}.pdf")


if __name__ == '__main__':
    generator = NotebookGenerator()
    generator.generate_notebook("topic.csv")
