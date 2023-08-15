import pandas as pd
from fpdf import FPDF


pdf = FPDF(orientation="P", unit="mm", format="A4")
df = pd.read_csv("topic.csv")

for index, row in df.iterrows():
    num_of_pages = row["Pages"]
    for i in range(num_of_pages):
        pdf.add_page()
        pdf.set_font(family="Times", style="B", size=24)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=0, h=12, txt=row["Topic"], align="L", ln=1)
        pdf.line(10.5, 20.5, 199.5, 20.5)


pdf.output("output.pdf")

