import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

load_dotenv()  # load all the env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

## Extract image from the PDF

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)): # iterate over all the pages of the pdf doc
        page = reader.pages[page]
        text += str(page.extract_text) # extract text from each page and then conver that to the string and then add to text variable
    return text

## Prompt template - can be customized 

input_prompt = """
Hi, act like a very experienced ATS(Application tracking system) with a deep understanding of tech field,
software engineering, data science, data analysis, data engineering and machine learning engineering.
Your task is to evaluate each resume based on the given job description. You must consider the job market, which
is extremely competitive and you should be able to provide the best assistance for improving the resumes.
Assign the percentage match based on the job description and missing keywords with high accuracy.
resume: {text}
description: {jd}

I want a one liner response having this structure 
{{'Job description match: ': '%', 'Missing keywords: []', 'Profile summary':""}}
"""

## creating the streamlit app

st.title('Smart ATS')
st.text('Improve your resume with this ATS')
jd = st.text_area('Paste the job description here')
uploaded_file = st.file_uploader('Upload your resume', type='pdf', help='Please upload only pdf')
submit = st.button('Submit')

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)  # converting the uploaded file into text
        response = get_gemini_response(input_prompt)
        st.subheader(response) # displaying the response