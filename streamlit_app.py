from openai import OpenAI
import streamlit as st
from pypdf import PdfReader
from pathlib import Path

header = "AI Profile Summerizer"
st.header(header)
st.divider()


role_label = "What role do you want to check for?"

roles_avaialble = [
    "Data Engineer",
    # "Data Analyst",
    "Data Scientist",
    "Full-Stack Developer",
    "Devops Engineer",
    # "Machine Learning Engineer",
    # "Go Developer"
]

st.session_state["selected_role"] = st.selectbox(
    label=role_label, options=roles_avaialble
)

SKILL_DESCRIPTION = {
    "Data Engineer": "A Data Engineer should have the following skills: Python, SQL, any cloud experience, jupyter notebooks,pyspark/spark",
    "Data Scientist": "A Data scientist should have the following skills : Python, any one of ML libraries, experience in training/inference of the models, numpy,pandas",
    "Devops Engineer": "A Devops Engineer should have the following skills: One high level and low level programming language, any hands on experience in cloud, knowledge of infrastructure orchestration tools and automation tools",
    "Full-Stack Developer": "A Full-Stack Developer should have the following skills: Frontend languages and any one frontend framework, skilled in a programming langugae which can be used to develop web applications, experience in webframeworks, Git, cloud experience can also be handy",
}


def read_resume(file) -> str:
    reader = PdfReader(file)
    text_data = ""
    for page in reader.pages:
        text_data = page.extract_text() + "\n"
    api_key = st.secrets["api_key"]
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are a Recruiter."},
        {
            "role": "user",
            "content": f"From the resume given below, summerize if the candidate is suitatble for {st.session_state['selected_role']} role. Give me a single word answer Yes or No, then mention the skills the candidate have suitable for the role in a list.",
        },
        {
            "role": "user",
            "content": f"Giving you the context for what skills I am looking for in a role. {SKILL_DESCRIPTION[st.session_state['selected_role']]}. ",
        },
        {
            "role": "assistant",
            "content": "Please provide the candidate details. Sure I will just give you a single word answer Yes or No and list the skills the candidate have suitable for the role. I will also take the context you have given when I give my answer.",
        },
        {"role": "user", "content": f"{text_data}"},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=100
    )
    return response.choices[0].message.content


uploaded_file = st.file_uploader("Choose a file")
upload_button = st.button(label="Upload")
if uploaded_file is not None:
    if upload_button:
        text = read_resume(uploaded_file)
        st.divider()
        if "yes" in text.lower():

            st.success(f"{text}")
        else:
            st.warning(f"{text}")
