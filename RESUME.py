
#RESUME
import tempfile
import streamlit as st
import pandas as pd

import fitz  # PyMuPDF
import docx2txt

import nltk
import os

# Set a persistent path
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.append(nltk_data_path)

# Download NLTK resources to local folder
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)


# Load job description dataset
df = pd.read_excel(r"JOB DESCRIPTION.xlsx")

technical_skills = ['Python', 'Java', 'Git', 'REST APIs',
    'HTML', 'CSS', 'JavaScript', 'React', 'Angular',
    'Node.js', 'MongoDB',
    'Kotlin', 'Android', 'Swift', 'iOS', 'Flutter', 'React Native',
    'AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins',
    'SQL', 'Pandas', 'Scikit-learn', 'Statistics',
    'Excel', 'Power BI', 'Tableau',
    'TensorFlow', 'PyTorch', 'ML Ops',
    'NLP', 'Deep Learning', 'Research Writing',
    'Spark', 'Hadoop', 'ETL', 'Kafka',
    'SIEM', 'IDS/IPS', 'Firewalls', 'Risk Analysis',
    'Kali Linux', 'Metasploit', 'Wireshark',
    'Cisco', 'Routers/Switches', 'TCP/IP', 'CCNA',
    'Azure', 'GCP', 'IaC', 'Terraform',
    'Linux', 'Windows', 'Shell Scripting',
    'Monitoring tools',
    'Figma', 'Adobe XD', 'Prototyping', 'Wireframes',
    'User Research', 'Design Systems',
    'Roadmapping', 'JIRA', 'Agile', 'Communication',
    'Scrum', 'Team Management', 'Jira',
    'UML', 'Requirement Gathering']


def extract_resume_txt(resume):
    if resume.name.endswith(".pdf"):
        file_bytes = resume.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # for page in doc:
        #     text += page.get_text()
        doc.close()
    elif resume.name.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(resume.read())
            tmp_path = tmp.name
        text = docx2txt.process(tmp_path)       
    else:
        text = resume.read().decode('utf-8', errors='ignore')
    return text


def tokenize_txt(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    tokens = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]
    # tagged = pos_tag(tokens)
    
    # Filter for proper nouns (NNP, NNPS)
    # tokens = [word for word, tag in tagged if tag.startswith(('NNP', 'NNPS'))]
    
    return tokens

def find_matching_job_titles(tokens, df, min_match_count=2):
    resume_skills = set(word.lower() for word in tokens)
    matching_jobs = []

    for _, row in df.iterrows():
        job_title = row['Job Title']
        required_skills = [skill.strip().lower() for skill in row['Required Skills'].split(',')]

        # Count matching skills
        matched = resume_skills & set(required_skills)
        if len(matched) >= min_match_count:
            matching_jobs.append((job_title, matched))  # store title and matching skills

    return matching_jobs



def main():
    st.set_page_config(page_title="Resume Matcher", layout="wide")
    st.title("📄Resume Matcher Bot")
    st.subheader("Upload your resume to check matched technical skills")

    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_upload_1")


    if resume_file:
        # Extract raw text from the resume
        resume_text = extract_resume_txt(resume_file)

        # Tokenize and POS-tag
        tokens = tokenize_txt(resume_text)

        # Match skills
        matched_jobs = find_matching_job_titles(tokens, df)
        matched = set()
        for job_title, skills in matched_jobs:
            matched.update(skills)

        # Display resume content (optional)
        # with st.expander("📄 View Resume Text"):
            # st.write(resume_text)

        # Display results
        st.markdown("### 🧠Matched Skills:")
        if matched:
            for skill in matched:
                st.success(f"- {skill}")
        else:
            st.warning("No technical skills matched. Try refining your resume.")

        # Display eligible job roles
        st.markdown("### 💼 Eligible Job Roles:")
        if matched_jobs:
            for title, skills in matched_jobs:
                st.success(f"**{title}** (Matched: {', '.join(skills)})")
        else:
            st.warning("No matching job roles found.")

    else:
        st.info("Please upload your resume to proceed.")
if __name__ == "__main__":
    main()

