
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key

class FIRForm(FlaskForm):
    complainant_name = StringField("Complainant's Name")
    complainant_address = TextAreaField("Complainant's Address and Contact Details")
    incident_date_time_location = StringField("Incident Date, Time, and Location")
    incident_nature = TextAreaField("Nature of the Incident or Crime")
    incident_description = TextAreaField("Description of Events")
    accused_details = TextAreaField("Details of the Accused")
    witness_information = TextAreaField("Witness Information")
    property_details = TextAreaField("Property Details")
    injuries_or_damages = TextAreaField("Injuries or Damages Information")
    fir_number = StringField("FIR Number")
    fir_date_time = StringField("Date and Time of FIR Registration")
    police_station_details = StringField("Police Station Details")
    complainant_signature = StringField("Complainant's Signature")
    submit = SubmitField('Generate FIR')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FIRForm()

    if form.validate_on_submit():
        generate_fir_pdf(form)
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

def generate_fir_pdf(form):
    pdf_filename = f"FIR_{form.complainant_name.data.replace(' ', '_')}.pdf"
    
    with open(pdf_filename, 'w+b') as file:
        pdf = canvas.Canvas(file)
        pdf.drawString(100, 800, f"Complainant's Name: {form.complainant_name.data}")
        pdf.drawString(100, 780, f"Complainant's Address and Contact Details: {form.complainant_address.data}")
        pdf.drawString(100, 760, f"Incident Date, Time, and Location: {form.incident_date_time_location.data}")
        pdf.drawString(100, 740, f"Nature of the Incident or Crime: {form.incident_nature.data}")
        pdf.drawString(100, 720, f"Description of Events: {form.incident_description.data}")
        pdf.drawString(100, 700, f"Details of the Accused: {form.accused_details.data}")
        pdf.drawString(100, 680, f"Witness Information: {form.witness_information.data}")
        pdf.drawString(100, 660, f"Property Details: {form.property_details.data}")
        pdf.drawString(100, 640, f"Injuries or Damages Information: {form.injuries_or_damages.data}")
        pdf.drawString(100, 620, f"FIR Number: {form.fir_number.data}")
        pdf.drawString(100, 600, f"Date and Time of FIR Registration: {form.fir_date_time.data}")
        pdf.drawString(100, 580, f"Police Station Details: {form.police_station_details.data}")
        pdf.drawString(100, 560, f"Complainant's Signature: {form.complainant_signature.data}")
        pdf.save()

if __name__ == '__main__':
    app.run(debug=True)
