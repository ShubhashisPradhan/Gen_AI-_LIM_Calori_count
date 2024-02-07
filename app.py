import streamlit as st
import google.generativeai as genai 
import os
from dotenv import load_dotenv
load_dotenv() # loading all the environment variable
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    #check the file if uploaded
    if uploaded_file is not None:
        #read the file into byte
        bytes_data=uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type":uploaded_file.type ,# get the mime type
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileExistsError("No file uploaded")
    

#intialising health app FRONTEND
st.set_page_config(page_title="Calories calculation app")
st.header("Calories calculation app")
uploaded_file=st.file_uploader('choose an image .......',type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image", use_column_width=True)

submit=st.button("tell me about the calori content of my food")    


input_prompt= """ 
you are an expert nutrionist where you need to see the food from theimage and calculate calories , 
also provides the details of in the below format

1 Item 1 - no of calories
2 Item 2 - no of calories
----
----

finally you can also mention whether the food is healthy or not also mention the percentage split 
of the ration of carbohydrates, fats,fibers,sugars and other important things in our diet


"""
#google gemini pro vision

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header( " The response is ")
    st.write(response)