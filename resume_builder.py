import re
import os
import io
import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

st.title("📄AI Resume Builder")
st.write("Fill in your details below. Gemini will generate a professional resume for you!")
st.image("https://resumaker.ai/assets/og/OG.png")

# Configure Google Generative AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it up.")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

prompt = " You have to build professional resumes based on user input. The resume should be clean, well-formatted, and ATS-friendly. Return resume text in plain formatting (no markdown, no explanation)."\
        "The Resume must look like a professional resume, with sections for contact information, education, work experience, and skills. Use a clean and modern layout suitable for all industries."\
        "Explain the resume in a professional tone, and ensure it is concise and relevant to the job market. Do not include any personal opinions or unnecessary information."\
        
#INFO
st.info("""
**Templates:**
- *Simple*: Basic, clean layout for all industries  
- *Modern*: Contemporary, sleek formatting  
- *Creative*: Slightly informal, personal tone (good for designers, freelancers)
""")
# Select Resume Style
template = st.selectbox(
    "Choose Resume Style",
    ["Simple", "Modern", "Creative"]
)
#Input Form
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    education = st.text_area("Education (e.g., degree, institute, years)")
    experience = st.text_area("Work Experience (e.g., company, role, duration, duties)")
    skills = st.text_area("Skills (comma-separated)")
    submit = st.form_submit_button("Generate Resume")
if submit:
    if not name or not email or not education:
        st.warning("Please fill in all required fields.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("Please enter a valid email address.")
    else:
        with st.spinner("Generating your resume..."):
            # Prompt Gemini
            try:
                prompt = f"""
Act as a professional resume writer. Create a clean, well-formatted, and ATS-friendly resume based on the following details:

Style: {template} resume
Full Name: {name}
Email: {email}
Phone: {phone}
Education: {education}
Experience: {experience}
Skills: {skills}

Return only the resume text in plain formatting (no markdown, no explanation).
    """

                response = model.generate_content(prompt)
                resume_text = response.text.strip()

                if resume_text:
                    st.success("✅ Resume generated successfully!")
                    st.text_area("✍️ Your Resume", resume_text, height=500)

                    # Generate PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    for line in resume_text.split("\n"):
                        pdf.multi_cell(0, 10, line)
                    pdf_output = pdf.output(dest='S').encode('latin1')

                    pdf_buffer = io.BytesIO(pdf_output)
                    st.download_button(
                        label="📥 Download Resume as PDF",
                        data=pdf_buffer,
                        file_name="resume.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Gemini returned an empty response.")
            except Exception as e:
                st.error(f"❌ An error occurred while generating the resume: {e}")
