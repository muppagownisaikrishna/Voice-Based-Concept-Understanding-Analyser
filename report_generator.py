from reportlab.pdfgen import canvas
import os
def generate_pdf(transcription, similarity, score, grade):
    os.makedirs("reports", exist_ok=True)
    pdf = canvas.Canvas("reports/Result_Report.pdf")
    pdf.setFont("Helvetica-Bold",16)
    pdf.drawString(150,800,"Communication Analysis Report")
    pdf.setFont("Helvetica",12)
    pdf.drawString(50,760,"Transcription:")
    pdf.drawString(50,740,transcription)
    pdf.drawString(50,700,f"Semantic Similarity : {similarity:.2f}")
    pdf.drawString(50,680,f"Understanding Score : {score}")
    pdf.drawString(50,660,f"Classification : {grade}")
    pdf.save()