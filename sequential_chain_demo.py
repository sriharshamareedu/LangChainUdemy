import os

from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o",api_key=OPENAI_API_KEY)
title_prompt=PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
    You need to craft an impactful title for a speech
    on the following topic: {topic}
    Answer exactly with one title.
    """
)

speech_prompt=PromptTemplate(
    input_variables=["title","emotion"],
    template="""You need to write a powerful {emotion} speech of 350 words
    for the following title: {title}
    Format the output with 2 keys: 'title', 'speech', and fill them
    with the respective values  
    """
)

first_chain=title_prompt|llm|StrOutputParser()|(lambda title:(st.write(title),title)[1])
second_chain=speech_prompt|llm|JsonOutputParser()
final_chain=first_chain|(lambda title:{"title":title,"emotion":emotion})|second_chain

st.title("Speech Generator")

topic=st.text_input("Enter the topic:")
emotion=st.text_input("Enter the emotion:")

if topic and emotion:
    response=final_chain.invoke({"topic":topic, "emotion":emotion})
    st.write(response)
    st.write(response['title'])