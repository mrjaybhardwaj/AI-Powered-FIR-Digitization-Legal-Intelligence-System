from flask import Flask, render_template, request
from fpdf import FPDF
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sentence_transformers import SentenceTransformer, util
import pickle

app = Flask(__name__)

# Load the pre-trained model for sentence embeddings
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Stem words
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    # Join the words back into a single string
    preprocessed_text = ' '.join(words)

    return preprocessed_text

# Load the pre-processed data from the pickle file
new_ds = pickle.load(open('preprocess_data1.pkl', 'rb'))
new_ds['In_Simple_Words'] = new_ds['Description'].apply(lambda x: (re.search(r'in Simple Words\s*([^"]+)?', x, re.DOTALL | re.IGNORECASE).group(1).strip() if re.search(r'in Simple Words\s*([^"]+)?', x, re.DOTALL | re.IGNORECASE) and re.search(r'in Simple Words', x, re.IGNORECASE) and re.search(r'in Simple Words\s*([^"]+)?', x, re.DOTALL | re.IGNORECASE).group(1) else '') if re.search(r'in Simple Words', x, re.IGNORECASE) else '')

def suggest_sections(complaint, dataset, min_suggestions=5):
    # Preprocess the complaint
    preprocessed_complaint = preprocess_text(complaint)

    # Calculate embeddings for the complaint and section descriptions
    complaint_embedding = model.encode(preprocessed_complaint)
    section_embeddings = model.encode(dataset['Combo'].tolist())

    # Calculate cosine similarity between the complaint and each section
    similarities = util.pytorch_cos_sim(complaint_embedding, section_embeddings)[0]

    # Start with a high similarity threshold
    similarity_threshold = 0.9
    relevant_indices = []

    # Iterate until you get enough suggestions
    while len(relevant_indices) < min_suggestions and similarity_threshold > 0:
        # Filter out suggestions below the dynamic similarity threshold
        relevant_indices = [i for i, sim in enumerate(similarities) if sim > similarity_threshold]
        similarity_threshold -= 0.05  # Adjust the step size based on your preference

    # Sort suggestions based on similarity scores in descending order
    sorted_indices = sorted(relevant_indices, key=lambda i: similarities[i], reverse=True)
    suggestions = dataset.iloc[sorted_indices][['Description', 'In_Simple_Words', 'Offense', 'Punishment', 'Cognizable', 'Bailable', 'Court']].to_dict(orient='records')

    return suggestions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    complaint = request.form['complaint']
    suggested_sections = suggest_sections(complaint, new_ds)

    if suggested_sections:
        # Pass the suggestions to the result.html template
        return render_template('result.html', complaint=complaint, suggestions=suggested_sections)
    else:
        return render_template('result.html', complaint=complaint, suggestions=None)

@app.route('/generate_fir', methods=['POST'])
def generate_fir():
    # Extract form data
    print("Inside generate_fir()")
    
    # Extract form data
    complainant_name = request.form['complainant_name']
    complainant_address = request.form['complainant_address']
    # ... (add print statements for other form fields)

    # Print form field values
    print(f"Complainant Name: {complainant_name}")
    print(f"Complainant Address: {complainant_address}")
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

    # Access the selected section from the form data
    selected_section = request.form['selected_section']
    # You can use 'selected_section' to get details of the selected section from the suggestions if needed

    # Generate PDF (same code as before with minor modifications)
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
    # Include the selected section in the PDF
    pdf.multi_cell(0, 10, txt=f"Selected Section: {selected_section}")
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
    print(f"Selected Section: {selected_section}")
    print(f"PDF Output Path: {pdf_output_path}")

    return render_template('result1.html', pdf_output_path=pdf_output_path, selected_section=selected_section)

@app.route('/fir_registration', methods=['GET'])
def fir_registration():
    return render_template('fir_registration.html')

if __name__ == '__main__':
    app.run(port=5001)

