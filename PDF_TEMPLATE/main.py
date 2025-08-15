import pandas as pd
from fpdf import FPDF
from datetime import datetime
from typing import Optional
import sys

class NotebookGenerator:
    def __init__(self):
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=False, margin=0)
    
    def header(self, title):
        """Creates journal-style header"""
        # Decorative top border
        self.pdf.set_line_width(0.3)
        self.pdf.line(10.5, 8, 199.5, 8)
        
        # Journal title with decorative flourish
        # self.pdf.set_font(family="Times", style="B", size=18)
        # self.pdf.set_text_color(80, 80, 80)
        # self.pdf.set_xy(10, 12)
        # self.pdf.cell(w=0, h=8, txt=f"~ {title} ~", align="C", ln=1)
        
        # Date section - more prominent for diary feel
        self.pdf.set_xy(10, 25)
        self.pdf.set_font(family="Times", style="", size=12)
        self.pdf.set_text_color(100, 100, 100)
        self.pdf.cell(w=60, h=6, txt="Date:", align="L", ln=0)
        
        # Date fill-in with underlines
        self.pdf.set_font(family="Times", style="", size=10)
        date_x = 35  # Starting position for date
        date_y = 30  # Y position for date
        
        # Draw underlines for date (month/day/year)
        self.pdf.line(date_x, date_y, date_x + 15, date_y)      # Month
        self.pdf.line(date_x + 20, date_y, date_x + 35, date_y) # Day  
        self.pdf.line(date_x + 40, date_y, date_x + 60, date_y) # Year
        
        # Add slash separators
        self.pdf.set_xy(date_x + 16, 25)
        self.pdf.cell(w=4, h=6, txt="/", align="C", ln=0)
        self.pdf.set_xy(date_x + 36, 25)
        self.pdf.cell(w=4, h=6, txt="/", align="C", ln=0)
        
        # Weather and mood section (right side)
        self.pdf.set_xy(120, 25)
        self.pdf.set_font(family="Times", style="", size=11)
        self.pdf.cell(w=30, h=6, txt="Weather:", align="L", ln=0)
        self.pdf.cell(w=25, h=6, txt="[ ] Sun [ ] Cloud [ ] Rain", align="L", ln=0)
        
        # Mood tracking
        self.pdf.set_xy(120, 33)
        self.pdf.cell(w=30, h=6, txt="Mood:", align="L", ln=0)
        self.pdf.cell(w=40, h=6, txt="[ ] Great [ ] OK [ ] Meh", align="L", ln=1)
        
        # Inspirational prompt
        self.pdf.set_xy(10, 42)
        self.pdf.set_font(family="Times", style="I", size=10)
        self.pdf.set_text_color(120, 120, 120)
        self.pdf.cell(w=0, h=5, txt="\"Today I am grateful for...\"", align="C", ln=1)
        
        # Add underlines for writing gratitude
        gratitude_start_y = 50
        line_spacing = 4
        for i in range(3):  # 3 lines for gratitude
            y_pos = gratitude_start_y + (i * line_spacing)
            self.pdf.line(15, y_pos, 195, y_pos)  # Full width lines for writing
        
        # Decorative separator line
        self.pdf.set_line_width(0.5)
        self.pdf.line(10.5, 65, 199.5, 65)

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
            self.note_lines(y_cor=75)

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
    args = sys.argv[1:]
    if len(args) == 0:
        generator.generate_notebook("topic.csv")
    else:
        generator.generate_notebook("topic.csv", args[0])
