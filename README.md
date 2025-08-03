# 📄 Gemini Resume Builder

A smart AI-powered Resume Builder built with **Streamlit** and **Google's Gemini API**.  
Users can generate, customize, and download professional resumes and cover letters—and even chat with Gemini to tailor their content.


## 🚀 Features

- 🧠 AI-generated resume based on user input
- 🎨 Multiple resume styles: Simple, Modern, Creative
- 💬 Chat with Gemini to edit or improve your resume
- 📄 Download your resume in **PDF format**
- 📨 AI-generated **cover letter** based on your resume
- ✅ Validates required fields and email format
- 🌐 Easily deployable on **Streamlit Cloud**


## 🛠 Tech Stack

- Python
- [Streamlit](https://streamlit.io)
- [Google Generative AI (Gemini)](https://ai.google.dev)
- dotenv (for environment variable management)
- ReportLab (for PDF generation)


## 🧪 How to Run Locally

1. **Clone the repository**
   git clone https://github.com/your-username/gemini-resume-builder.git
   cd gemini-resume-builder
# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key

Create a .env file in the root directory and add:
GEMINI_API_KEY=your_api_key_here

# 🤝 Contributions
Pull requests and feature suggestions are welcome!
If you'd like to improve resume formatting or add more templates, feel free to contribute.

# 🙋‍♀️ Acknowledgements
Thanks to Google AI for the Gemini API.

Inspired by job seekers who want a fast, modern way to build resumes.

# Run the app
streamlit run app.py
