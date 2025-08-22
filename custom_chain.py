import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt Template
prompt = PromptTemplate(
    input_variables=["information"],
    template="""
You are a professional resume writer.
Create a clean, ATS-friendly resume in the following structure:
[Full Name]
[Contact Information]

Professional Summary:
[Summary]

Experience:
[List experiences in reverse chronological order with job title, company, years, and bullet points for achievements.]

Skills:
[List bullet points of skills.]

Education:
[Degree, Institution, Year]

Here is the provided information:
{information}
"""
)

# LLM Chain
llm_chain = LLMChain(llm=gemini, prompt=prompt)

# Function to save CV in JSON
def save_resume_to_json(text, filename="CV.json"):
    data = {"resume": text}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.append(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    name = input("Enter your full name: ")
    contact = input("Enter your contact info (email, phone, LinkedIn): ")
    summary = input("Enter your professional summary: ")
    experience = input("Enter your work experience (jobs, years, achievements): ")
    skills = input("Enter your skills (comma-separated): ")
    education = input("Enter your education details: ")

    information = f"""
    Name: {name}
    Contact: {contact}
    Summary: {summary}
    Experience: {experience}
    Skills: {skills}
    Education: {education}
    """

    response = llm_chain.run(information=information)
    save_resume_to_json(response, "CV.json")
    print("\n✅ Resume generated and saved in 'CV.json'")
