# Import necessary libraries
import os
import streamlit as st
import google.generativeai as genai 
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Google Generative AI with the API key
genai.configure(api_key=api_key)

# Set the page configuration for the Streamlit app
st.set_page_config(
    page_title="FixBot with Google Gemini",
    page_icon="🤖"
)

# Check if the Google API key is provided in the sidebar
with st.sidebar:
    if 'GOOGLE_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        api_key = st.secrets['GOOGLE_API_KEY']
    else:
        api_key = st.text_input('Enter Google API Key:', type='password')
        if not (api_key.startswith('AI')):
            st.warning('Please enter your API Key!', icon='⚠️')
        else:
            st.success('Success!', icon='✅')
    os.environ['GOOGLE_API_KEY'] = api_key
    "[Get a Google Gemini API key](https://ai.google.dev/)"
    "[View the source code](https://github.com/lg-pereira/FixBot/streamliApp.py)"
    

# Set the title and caption for the Streamlit app
st.title("🤖 FixBot - seu consultor para consertos")
st.caption("🚀 FixBot powered by Google Gemini")

# Create tabs for the Streamlit app
tab1, tab2 = st.tabs(["🌏 Perguntas - FixBot", "🖼️ Envio de fotos e vídeos - FixBot Vision"])

# Code for Gemini Pro model
with tab1:
    st.write("💬 FixBot - Apenas perguntas")
    st.subheader("🛠️ Consultor para pequenas manutenções")
    
    fix_issue = st.text_input("Descreva seu problema: \n\n",key="fix_issue",value="Meu celular não funciona")
    level_Expertise = st.text_input("Qual seu nível de experiência? \n\n",key="level_Expertise",value="Leigo")
    other_info = st.text_input("Alguma outra informações relevante? \n\n",key="other_info",value="Meu celular caiu na água suja da enchente")
        
    prompt = f"""Você é um especialista em manutenção pós-desastres. Leve em conta que meu nível de conhecimento sobre o assunto é: {level_Expertise} e que isso aconteceu: {other_info}. Me dê um passo a passo para resolver: {fix_issue}. 
    """
    
    config = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 32,
        "max_output_tokens": 2048,
        }
    safety = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]
    
    generate_t2t = st.button("Me ajude!", key="generate_t2t")
    model = genai.GenerativeModel("gemini-pro", generation_config=config, safety_settings=safety)
    if generate_t2t and prompt:
        with st.spinner("Buscando as informações para te ajudar..."):
            plan_tab, prompt_tab = st.tabs(["Passo a passo", "Prompt solicitado"])
            with plan_tab: 
                response = model.generate_content(prompt)
                if response:
                    st.write("Guia passo a passo")
                    st.write(response.text)
            with prompt_tab: 
                st.text(prompt)

# Code for Gemini Pro Vision model
with tab2:
    st.write("🤖 FixBot Vision - Envie fotos")
    st.subheader("🥽 Eu vou ver como posso te ajudar!")
    
    image_prompt = st.text_input("Descreva seu problema:", placeholder="Prompt", label_visibility="visible", key="image_prompt")
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    image = ""

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit=st.button("Gere o passo a passo")

    if submit:
        model = genai.GenerativeModel('gemini-pro-vision')
        with st.spinner("Buscando as informações para te ajudar..."):
            if image_prompt!="":
                response = model.generate_content([image_prompt,image])
            else:
                response = model.generate_content(image)
        response = response.text
        st.subheader("Guia passo a passo")
        st.write(response)

    
