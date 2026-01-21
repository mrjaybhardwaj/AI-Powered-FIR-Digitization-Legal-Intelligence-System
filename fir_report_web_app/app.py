from flask import Flask, render_template, request
from fpdf import FPDF

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    complainant_name = request.form['complainant_name']
    complainant_address = request.form['complainant_address']
    phone_number = request.form['phone_number']
    incident_date = request.form['incident_date']
    incident_time = request.form['incident_time']
    incident_location = request.form['incident_location']
    offense_description = request.form['offense_description']
    individuals_involved = request.form['individuals_involved']
    witness_details = request.form['witness_details']
    complaint_narrative = request.form['complaint_narrative']
    law_sections = request.form['law_sections']
    police_officer_name = request.form['police_officer_name']
    registration_number = request.form['registration_number']
    complainant_signature = request.form['complainant_signature']
    additional_info = request.form['additional_info']

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="First Information Report (FIR)", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Complainant's Information:", ln=True)
    pdf.cell(200, 10, txt=f"Name: {complainant_name}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {complainant_address}", ln=True)
    pdf.cell(200, 10, txt=f"Phone Number: {phone_number}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Details of the Incident:", ln=True)
    pdf.cell(200, 10, txt=f"Incident Date: {incident_date}", ln=True)
    pdf.cell(200, 10, txt=f"Incident Time: {incident_time}", ln=True)
    pdf.cell(200, 10, txt=f"Incident Location: {incident_location}", ln=True)
    pdf.cell(200, 10, txt=f"Offense Description: {offense_description}", ln=True)
    pdf.cell(200, 10, txt=f"Individuals Involved: {individuals_involved}", ln=True)
    pdf.cell(200, 10, txt=f"Witness Details: {witness_details}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Complaint Narrative:", ln=True)
    pdf.multi_cell(0, 10, txt=complaint_narrative)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Sections of the Law:", ln=True)
    pdf.multi_cell(0, 10, txt=law_sections)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Officer Recording the FIR:", ln=True)
    pdf.cell(200, 10, txt=f"Name: {police_officer_name}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Registration Number:", ln=True)
    pdf.cell(200, 10, txt=f"Registration Number: {registration_number}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Signature of Complainant:", ln=True)
    pdf.cell(200, 10, txt=f"Signature/Thumb Impression: {complainant_signature}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Other Relevant Information:", ln=True)
    pdf.multi_cell(0, 10, txt=additional_info)

    pdf_output_path = f"FIR_{registration_number}.pdf"
    pdf.output(pdf_output_path)

    return render_template('result.html', pdf_output_path=pdf_output_path)

if __name__ == '__main__':
    app.run(debug=True)
