import os
import io
import base64
import json
import requests
import streamlit as st


auth_key = os.environ["AUTH_KEY"]
url = os.environ["ENDPOINT_URL"]

headers = {
  'Authorization': auth_key,
  'Content-Type': 'application/json'
}

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Image to text frontend app")

uploaded_image = st.file_uploader("Choose an image")
prompt = st.text_input("Optional: modify prompt", value="Provide a detailed description for the image")

do_sample = st.sidebar.checkbox(label='do sample', value=False)
num_beams = st.sidebar.slider(label='number of beams', min_value=1, max_value=10, value=5, step=1)
max_length = st.sidebar.slider(label='max length', min_value=64, max_value=512, value=256, step=64)
min_length = st.sidebar.slider(label='min length', min_value=1, max_value=10, value=1, step=1)
top_p = st.sidebar.slider(label='top p', min_value=0.1, max_value=2.0, value=0.9, step=0.1)
repetition_penalty = st.sidebar.slider(label='repetition penalty', min_value=1.0, max_value=2.0, value=1.5, step=0.1)
length_penalty = st.sidebar.slider(label='length penalty', min_value=0.1, max_value=2.0, value=1.0, step=0.1)
temperature = st.sidebar.slider(label='temperature', min_value=0.1, max_value=5.0, value=1.0, step=0.1)

press_button = st.button('Generate description')
if uploaded_image is not None:
    st.image(uploaded_image)
if press_button:
    if uploaded_image is not None:
        with st.spinner(text="This may take a moment..."):
            encoded_string = base64.b64encode(uploaded_image.read()).decode("utf-8")
            payload = json.dumps({
                "imgstring_b64": encoded_string, "prompt": prompt, "do_sample": do_sample, "num_beans": num_beams,
                "max_length": max_length, "min_length": min_length, "top_p": top_p,
                "repetition_penalty": repetition_penalty, "length_penalty": length_penalty, "temperature": temperature})
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                response_data = response.json()
                generated_text = response_data["result"]["description"]
                st.write("Result:")
                st.write(generated_text)
            except:
                st.error("There is no response, try again later")
    else:
        st.text("Please, specify an image")