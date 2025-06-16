import os

from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o",api_key=OPENAI_API_KEY)
prompt_template=PromptTemplate(
    input_variables=["country","no_of_paras","language"],
    template="""You are an expert in traditional cusines.
    You provide information about a specific dish from a specific country.
    About giving information about fictional places. If the country is fictional
    or non-existant answer: I don't know.
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} short paras in {language}
    """
)

st.title("Cuisine Info")

country=st.text_input("Enter the country:")
no_of_paras=st.number_input("Enter the number of paras", min_value=1, max_value=5)
language=st.text_input("Enter the language:")

if country:
    response=llm.invoke(prompt_template.format(country=country, no_of_paras=no_of_paras, language=language))
    st.write(response.content)