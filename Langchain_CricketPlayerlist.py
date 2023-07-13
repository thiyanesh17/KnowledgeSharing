from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


import os
os.environ['OPENAI_API_KEY'] = "Use your key"

llm = OpenAI(temperature=0.7)

def country_playerlist(country):

    PromptTemplate_name = PromptTemplate(input_variables=['country'],template="List me the current cricket players in {country}")

    name_chain = LLMChain(llm=llm,prompt=PromptTemplate_name,output_key="playerslist")
    #list_players = name_chain.run("England")
    #print(list_players)

    PromptTemplate_senior = PromptTemplate(input_variables=['playerslist'],template="""Tell me the senior most player in {playerslist} list of players""")
    senior_name_Chain = LLMChain(llm=llm,prompt=PromptTemplate_senior,output_key="seniorplayer")

    chain = SequentialChain(
    chains=[name_chain,senior_name_Chain],
    input_variables=['country'],
    output_variables=['playerslist','seniorplayer'])


    response = chain({'country':country})

    return response


import streamlit as st
st.title("Get the Cricket players list for any country")
country = st.sidebar.selectbox("Pick a country", ("India", "Australia", "England", "Paskistan", "Srilanka","New zealand","Bangladesh"))

if country:

    response = country_playerlist(country)
    player_list = response['playerslist'].strip().split(",")
    st.header(response['seniorplayer'].strip())
    st.write("*********************Players List *********************")

    for player in player_list:
        st.write("-", player)
   






