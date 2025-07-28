import io
import re
from fpdf import FPDF
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Configure Google Generative AI
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it up.")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up Gemini model
MODEL = "models/gemini-1.5-flash"
client = genai.GenerativeModel(MODEL)

# Streamlit UI
st.set_page_config(page_title="Resume Builder", page_icon="📄")
st.title("📄 AI Resume Builder")
st.write("Fill in your details below. Gemini will generate a professional resume for you!")

# Input form
st.info("""
**Templates:**
- *Simple*: Basic, clean layout for all industries  
- *Modern*: Contemporary, sleek formatting  
- *Creative*: Slightly informal, personal tone (good for designers, freelancers)
""")

template = st.selectbox(
    "Choose Resume Style",
    ["Simple", "Modern", "Creative"]
)

with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    education = st.text_area("Education (e.g., degree, institute, years)")
    experience = st.text_area("Work Experience (e.g., company, role, duration, duties)")
    skills = st.text_area("Skills (comma-separated)")
    submit = st.form_submit_button("Generate Resume")

# Handle form submission
if submit:
    if not name or not email or not education:
        st.warning("Please fill in all required fields.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("Please enter a valid email address.")
    else:
        with st.spinner("Generating your resume..."):
            try:
                # Prompt Gemini
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
                response = client.generate_content(prompt)
                if not response or not response.text:
                    st.error("❌ Failed to generate resume. Please try again.")
                    raise ValueError("Empty response from Gemini")
                # response = client.generate_content([
                #     {
                #         "role": "system",
                #         "parts": [
                #             "You are an expert resume builder. Only help the user with resume-related questions such as formatting, writing, tailoring resumes for jobs, or generating professional resume content. Do NOT answer any unrelated queries."
                #         ]
                #     },
                #     {
                #         "role": "user",
                #         "parts": [prompt]
                #     }
                # ])
                resume_text = response.text

                # ✅ Show success
                st.success("✅ Resume generated successfully!")
                st.text_area("✍️ Your Resume", resume_text, height=500)

                # Generate PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in resume_text.split("\n"):
                    pdf.multi_cell(0, 10, line)
                # Output as string and encode
                pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' = return as string

                # Write to BytesIO
                pdf_buffer = io.BytesIO(pdf_output)
                # Show download button
                st.download_button(
                    label="📥 Download Resume as PDF",
                    data=pdf_buffer,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )

                # pdf.output(pdf_buffer, 'F')
                # pdf_buffer.seek(0)

                # st.download_button("📥 Download Resume as PDF", pdf_buffer, file_name="resume.pdf")

                # ✨ Resume Chat Improvement
                st.markdown("## 💬 Refine Your Resume")
                chat_input = st.text_input("Ask Gemini to improve your resume (e.g., 'Make it more concise', 'Add project section')")

                if chat_input:
                    with st.spinner("Updating your resume..."):
                        try:
                            chat_prompt = f"""
You previously generated this resume:

{resume_text}

Now improve it based on the following instruction: {chat_input}
Return only the updated resume in plain text (no explanation).
                            """
                            chat_response = client.generate_content(prompt)

                            # chat_response = client.generate_content([
                            #     {"role": "system", "parts": ["You are a resume improvement assistant. Only help with resume modifications."]},
                            #     {"role": "user", "parts": [chat_prompt]}
                            # ])
                            updated_resume = chat_response.text
                            st.success("🔄 Resume updated based on your feedback!")
                            st.text_area("📝 Updated Resume", updated_resume, height=500)
                        except Exception as e:
                            st.error(f"❌ Error updating resume: {str(e)}")

                # ✉️ Cover Letter Generator
                st.markdown("## ✉️ Generate a Cover Letter")
                job_title = st.text_input("Job Title You're Applying For")
                company_name = st.text_input("Company Name")

                if job_title and company_name:
                    with st.spinner("Generating cover letter..."):
                        try:
                            cover_prompt = f"""
Act as a professional career assistant. Based on the following resume, write a tailored cover letter for a {job_title} role at {company_name}:

Resume:
{resume_text}

Keep it formal, concise, and professional.
                            """
                            cover_response = client.generate_content(prompt)

                            # cover_response = client.generate_content([
                            #     {"role": "system", "parts": ["You are a cover letter writing expert."]},
                            #     {"role": "user", "parts": [cover_prompt]}
                            # ])
                            cover_letter = cover_response.text
                            st.success("✅ Cover letter generated!")
                            st.text_area("📄 Your Cover Letter", cover_letter, height=400)
                        except Exception as e:
                            st.error(f"❌ Error generating cover letter: {str(e)}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
