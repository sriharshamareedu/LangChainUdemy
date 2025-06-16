import os

from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o",api_key=OPENAI_API_KEY)
outline_prompt=PromptTemplate(
    input_variables=["title"],
    template="""You are a professional blogger.
    Create an outline for a blog post on the following topic: {topic}
    The outline should include:
    - Introduction
    - 3 main points with subpoints
    - Conclusion
    """
)

introduction_prompt=PromptTemplate(
    input_variables=["title"],
    template="""You are a professional blogger.
    Write an engaging introduction paragraph based on the following outline:{outline}
    The introduction should hook the reader and provide a brief
    overview of the topic.
    """
)

first_chain=outline_prompt|llm|StrOutputParser()
second_chain=introduction_prompt|llm
overall_chain=first_chain|second_chain

st.title("Blog Post Generator")

topic=st.text_input("Enter the topic:")


if topic:
    response=overall_chain.invoke({"topic":topic})
    st.write(response.content)