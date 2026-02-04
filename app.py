import streamlit as st 
import google.generativeai as genai 
from PIL import Image
import datetime as dt
import os 

# Configure the model 

gemini_api_key = os.getenv("test-project-1")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# Lets create sidebar for image upload
st.sidebar.title(':red[Upload the Images here:]')
uploaded_image=st.sidebar.file_uploader('Images',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)
uploaded_image=[Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Images has been loaded Succesfully')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main page 

st.title('STRUCTURAL DEFECT DETECTION:- AI Assisted Structural Defect Identifier')
st.markdown('#### This application takes the images of the structural defect from the construction site and prepare the AI assisted report.')
title = st.text_input('Enter the title of the report: ')
name = st.text_input('Enter the name of the person who has prepared the report: ')
desig = st.text_input('Enter the designation of the person who has prepared the report.')
org = st.text_input('Enter the name of the organization.')

if st.button('SUBMIT'):
    with st.spinner('Processing...'):
        prompt = f"""
Role:
You are an expert structural engineer with 20+ years of experience in the construction industry.

Goal:
Prepare a detailed structural defect inspection report based on the uploaded images.

Report Format Instructions:
- Add the report title: {title}
- Include prepared by details and date:
  Name: {name}
  Designation: {desig}
  Organization: {org}
  Date: {dt.datetime.now().date()}

Content Requirements:
- Identify and classify all visible defects (cracks, spalling, corrosion, honeycombing, etc.)
- Multiple defects may exist; analyze each separately
- Describe each defect and its potential structural impact
- Assign severity level: Low / Medium / High
- Mention whether the defect is avoidable or inevitable
- Provide:
  - Short-term repair solution
  - Long-term repair solution
  - Estimated cost (INR)
  - Estimated repair time
- List preventive measures for future avoidance

Constraints:
- No HTML tags
- Use bullet points and tables where applicable
- Keep the report within 3 pages
"""

        response=model.generate_content([prompt,*uploaded_image],generation_config={'temperature':0.5})
        st.write(response.text)

    if st.download_button(
            label = 'Click to Download',
            data = response.text,
            file_name='structural_defect_report.txt',
            mime = 'text/plain'
        ):
            st.success('File downloaded')


