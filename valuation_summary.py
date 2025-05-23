import base64
from fpdf import FPDF

def generate_pdf_summary(data: dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Valuation Summary", ln=True, align="C")

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: Rs. {value:,.2f}", ln=True)  # Avoid ₹ to prevent encoding issues

    # Get PDF output as string using dest='S'
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64_pdf = base64.b64encode(pdf_output).decode('utf-8')

    # Create download link
    pdf_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="valuation_summary.pdf">📄 Download Valuation Summary PDF</a>'
    return pdf_link
