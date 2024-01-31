from openai import OpenAI

from pypdf import PdfReader
from pathlib import Path

def read_resume(file_path:str) -> str:
    reader = PdfReader(Path(file_path))
    text_data = ""
    for page in reader.pages:
        text_data = page.extract_text() + "\n"
    return text_data

text_data = read_resume(r"")
api_key = ""
client = OpenAI(api_key=api_key)
model = "gpt-3.5-turbo"
messages = [
    {"role":"system", "content": "You are a Recruiter."},
    {"role":"user", "content":"From the resume given below, summerize if the candidate is suitatble for devops role."},
    {"role":"assistant","content":"Please provide the candidate details."},
    {"role":"user","content":f"{text_data}"},
]



response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages
)

print(response.choices[0].message)
