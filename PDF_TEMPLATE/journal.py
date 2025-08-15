from fpdf import FPDF
import random
import sys
class IdealJournalPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=False, margin=15)
        # List of inspirational quotes for footer
        self.quotes = [
            "The journey of a thousand miles begins with a single step. - Lao Tzu",
            "What you do today can improve all your tomorrows. - Ralph Marston",
            "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            "The best way to predict the future is to create it. - Peter Drucker"
        ]

    def header(self):
        # Decorative top border
        self.set_line_width(0.3)
        self.set_draw_color(150, 150, 150)
        self.line(10, 8, 200, 8)
        
        # Days of the week with checkboxes (centered)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(80, 80, 80)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        x_start = 60
        for day in days:
            self.set_xy(x_start, 12)
            self.cell(15, 6, f"[ ] {day}", 0, 0, "C")
            x_start += 20
        
        # Memo No and Date (stacked on the left)
        self.set_font("Helvetica", "B", 12)
        self.set_xy(10, 25)
        self.cell(40, 6, f"Memo No: {self.page_no()}", 0, 1, "L")
        self.set_xy(10, 31)
        self.cell(40, 6, "Date:", 0, 0, "L")
        # Date underlines (DD/MM/YYYY)
        date_x = 25
        date_y = 35
        self.line(date_x, date_y, date_x + 15, date_y)      # Day
        self.line(date_x + 20, date_y, date_x + 35, date_y)  # Month
        self.line(date_x + 40, date_y, date_x + 60, date_y)  # Year
        self.set_xy(date_x + 16, 31)
        self.cell(4, 6, "/", 0, 0, "C")
        self.set_xy(date_x + 36, 31)
        self.cell(4, 6, "/", 0, 0, "C")
        
        # Mood tracking (right side)
        self.set_font("Helvetica", "", 10)
        self.set_xy(140, 25)
        self.cell(30, 6, "Mood:", 0, 0, "L")
        self.cell(30, 6, "[ ] Happy [ ] OK [ ] Sad", 0, 1, "L")
        
        # Section separator
        self.set_line_width(0.5)
        self.line(10, 45, 200, 45)

    def priorities_section(self):
        """Top 3 priorities for the day"""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 80)
        self.set_xy(10, 50)
        self.cell(0, 6, "Today's Priorities", 0, 1, "L")
        self.set_line_width(0.2)
        self.line(10, 55, 100, 55)
        self.set_font("Helvetica", "", 10)
        for i in range(5):
            y_pos = 60 + (i * 6)
            self.set_xy(10, y_pos)
            self.cell(0, 6, f"{i+1}. ______________________________", 0, 1, "L")
            self.line(15, y_pos + 6, 100, y_pos + 6)

    def habit_tracker(self):
        """Grid for tracking 5 habits"""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 80)
        self.set_xy(110, 50)
        self.cell(0, 6, "Habit Tracker", 0, 1, "L")
        self.line(110, 55, 200, 55)
        self.set_font("Helvetica", "", 9)
        habits = ["Habit 1", "Habit 2", "Habit 3", "Habit 4", "Habit 5"]
        for i, habit in enumerate(habits):
            y_pos = 60 + (i * 6)
            self.set_xy(110, y_pos)
            self.cell(30, 6, habit, 0, 0, "L")
            x_start = 140
            for j in range(5):  # 5 days for tracking
                self.set_xy(x_start, y_pos)
                self.cell(10, 6, "[ ]", 0, 0, "C")
                x_start += 12
            self.line(110, y_pos + 6, 200, y_pos + 6)

    def reflection_section(self):
        """Gratitude and lessons learned prompts"""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 80)
        self.set_xy(10, 100)
        self.set_xy(10, 100)
        self.cell(0, 6, "Reflection", 0, 1, "L")
        self.line(10, 105, 200, 105)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(120, 120, 120)
        self.set_xy(10, 110)
        self.cell(0, 6, "What am I grateful for today?", 0, 1, "L")
        for i in range(3):
            y_pos = 115 + (i * 6)
            self.line(10, y_pos, 195, y_pos)
        self.set_xy(10, 135)
        self.cell(0, 6, "What did I learn today?", 0, 1, "L")
        for i in range(3):
            y_pos = 140 + (i * 6)
            self.line(10, y_pos, 195, y_pos)

    def note_area(self):
        """Lined and blank area for notes/sketches"""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 80)
        self.set_xy(10, 160)
        self.cell(0, 6, "Notes & Sketches", 0, 1, "L")
        self.line(10, 165, 200, 165)
        self.set_line_width(0.2)
        # Half lined, half blank for flexibility
        for y in range(170, 230, 8):
            self.line(10, y, 200, y)

    def footer(self):
        """Inspirational quote and page number"""
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.set_xy(10, 287)
        quote = random.choice(self.quotes)
        self.cell(0, 5, f"{quote} | Page {self.page_no()}", 0, 1, "R")
        

    def journal_page(self):
        """Create a complete journal page"""
        self.header()
        self.priorities_section()
        self.habit_tracker()
        self.reflection_section()
        self.note_area()
        self.footer()

# Create the PDF
pdf = IdealJournalPDF()
for i in range(100):
    pdf.add_page()
    pdf.journal_page()

# Save the PDF

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        pdf.output("Ideal_Journal_100_Pages.pdf")
        print("PDF journal created successfully: Ideal_Journal_100_Pages.pdf")
    else:
        pdf.output(f"{args[0]}.pdf")
        print(f"PDF journal created successfully: {args[0]}" if len(args) == 1 else "PDF journal created successfully: Ideal_Journal_100_Pages.pdf")