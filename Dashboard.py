#!/usr/bin/env python
# coding: utf-8

# # Libraries

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import ast
import os


# # Reading files

# In[2]:



def reading_files(file,sep=','):
    df = pd.read_csv(file,sep) #'C:/Users/omidg/Downloads/Datasets/'+
    return df

abstract_cities = reading_files('abstract_cities_30.csv',sep = ';')
abstract_total = reading_files('abstract_total_30.csv',sep = ';')
abstract_universities = reading_files('abstract_universities_30.csv',sep = ';')
    
Akeywords_cities = reading_files('Akeywords_cities_30.csv',sep = ';')
Akeywords_total = reading_files('Akeywords_total_30.csv',sep = ';')
Akeywords_universities = reading_files('Akeywords_universities_30.csv',sep = ';')
    
Ikeywords_cities = reading_files('Ikeywords_cities_30.csv',sep = ';')
Ikeywords_total = reading_files('Ikeywords_total_30.csv',sep = ';')
Ikeywords_universities = reading_files('Ikeywords_universities_30.csv',sep = ';')
    
italy_unis = reading_files('Italy_universities_Scopus.csv')
eter = reading_files('selected_eter.csv')

keywords_authors_out_city = reading_files('keywords_authors_out_city.csv')
keywords_index_out_city = reading_files('keywords_index_out_city.csv')
keywords_authors_out_unis = reading_files('keywords_authors_out_unis.csv')
keywords_index_out_unis = reading_files('keywords_index_out_unis.csv')
keywords_authors_out_total = reading_files('keywords_authors_out_total.csv')
keywords_index_out_total = reading_files('keywords_index_out_total.csv')
    
source_cities = reading_files('source_cities.csv')
source_total = reading_files('source_total.csv')
source_universities = reading_files('source_universities.csv')
    
title_cities = reading_files('title_cities_30.csv',sep = ';')
title_total = reading_files('title_total_30.csv',sep = ';')
title_universities = reading_files('title_universities_30.csv',sep = ';')


# # Webpage info

# In[13]:


st.title('Analysis dashboard of Automatic extraction and integration of webometric data on Italian universities thesis')
st.text("Facoltà dell’Infromazione, Corso di Laurea in Data Science")
st.text("Condidate: Omid Ghamiloo")
st.sidebar.title('Thesis Advisor:')
st.sidebar.text('Prof. Daraio Cinzia')
st.sidebar.text('Prof. Bruni Renato')
st.sidebar.text('Ing. Bianchi Giampiero')


# # General Information

# ### Functions

# In[102]:


def pie_chart_uni(uni_name):
    cat = italy_unis.loc[(italy_unis['articles_category'].isna()==False) &
                     (italy_unis['University']==uni_name)]['articles_category'].values[0]
    df = pd.DataFrame.from_dict(ast.literal_eval(cat),orient='index')
    df = df.reset_index()
    df.columns = ['category','number of articles']
    fig = px.pie(df, values='number of articles', names='category', title='Articles Categories in '+uni_name)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

def pie_chart_city(city):
    df = italy_unis[italy_unis['state']==city]
    result = {}
    for i in df['articles_category']:
        result = {key: result.get(key, 0) + ast.literal_eval(i).get(key, 0) for key in set(result) | set(ast.literal_eval(i))}
    df = pd.DataFrame.from_dict(result,orient='index')
    df = df.reset_index()
    df.columns = ['category','number of articles']
    fig = px.pie(df, values='number of articles', names='category', title='Articles Categories in '++city)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)
    
def pie_chart_total():
    result = {}
    for i in italy_unis['articles_category']:
        result = {key: result.get(key, 0) + ast.literal_eval(i).get(key, 0) for key in set(result) | set(ast.literal_eval(i))}
    df = pd.DataFrame.from_dict(result,orient='index')
    df = df.reset_index()
    df.columns = ['category','number of articles']
    fig = px.pie(df, values='number of articles', names='category', title='Articles Categories in Italy')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

def source_plot_uni(uni_name): #if you wanted to change the other value in publisher, change this section
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    df = source_universities[source_universities['affID']==int(affID)]
    df = df.sort_values('count',ascending=False)
    df = df[1:20]
    fig = px.bar(df, x='Publisher', y='count',title='Top 20 publishers in '+uni_name)
    st.plotly_chart(fig)
    
def source_plot_city(city): #if you wanted to change the other value in publisher, change this section
    df = source_cities[source_cities['state']==city]
    df = df.sort_values('count',ascending=False)
    df = df[1:20]
    fig = px.bar(df, x='Publisher', y='count',title='Top 20 publishers in '+city)
    st.plotly_chart(fig)

def source_plot_total(): #if you wanted to change the other value in publisher, change this section
    df = source_total.sort_values('count',ascending=False)[:20]
    fig = px.bar(df, x='Publisher', y='count',title='Top 20 publishers in Italy')
    st.plotly_chart(fig)
    
def general_info_university(uni_name):
    st.sidebar.title('University Information')
    df = italy_unis[italy_unis['University']==uni_name]
    unis_name = '<p style="font-family:Courier; color:White; font-size: 16px;">University name: '+df['University'].values[0]+'</p>'
    affID = '<p style="font-family:Courier; color:White; font-size: 16px;">University name: '+str(int(df['affiliationID'].values[0]))+'</p>'
    local_ranking = '<p style="font-family:Courier; color:White; font-size: 16px;">Local Rank: '+str(df['ranking'].values[0])+'</p>'
    world_ranking = '<p style="font-family:Courier; color:White; font-size: 16px;">World Rank: '+str(df['World Rank'].values[0])+'</p>'
    state = '<p style="font-family:Courier; color:White; font-size: 16px;">City: '+df['state'].values[0]+'</p>'
    address = '<p style="font-family:Courier; color:White; font-size: 16px;">Address: '+df['street'].values[0]+'</p>'
    st.sidebar.markdown(unis_name, unsafe_allow_html=True)
    st.sidebar.markdown(affID, unsafe_allow_html=True)
    st.sidebar.markdown(local_ranking, unsafe_allow_html=True)
    st.sidebar.markdown(world_ranking, unsafe_allow_html=True)
    st.sidebar.markdown(state, unsafe_allow_html=True)
    st.sidebar.markdown(address, unsafe_allow_html=True)
    pie_chart_uni(uni_name)
    source_plot_uni(uni_name)

def general_info_city(city):
    df = italy_unis[italy_unis['state']==city]
    st.sidebar.title('City Information')
    city_name = '<p style="font-family:Courier; color:White; font-size: 16px;">City name: '+city+'</p>'
    number_unis = '<p style="font-family:Courier; color:White; font-size: 16px;">Number of unviersities: '+str(int(len(df)))+'</p>'
    st.sidebar.markdown(city_name, unsafe_allow_html=True)
    st.sidebar.markdown(number_unis, unsafe_allow_html=True)
    pie_chart_city(city)
    source_plot_city(city)
    
def general_info_total():
    st.sidebar.title('Italy Information')
    number_city = '<p style="font-family:Courier; color:White; font-size: 16px;">number of citis: '+str(int(len(italy_unis['state'].unique())))+'</p>'
    number_unis = '<p style="font-family:Courier; color:White; font-size: 16px;">Number of unviersities: '+str(int(len(italy_unis)))+'</p>'
    st.sidebar.markdown(number_city, unsafe_allow_html=True)
    st.sidebar.markdown(number_unis, unsafe_allow_html=True)
    pie_chart_total()
    source_plot_total()


# # Keywords function

# In[85]:


def Important_author_keywords_out_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords_lists = ast.literal_eval(keywords_authors_out_unis.loc[keywords_authors_out_unis['affID']==affID,'authors_keywords'].values[0])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 authors keywords of "+uni_name)
    st.pyplot(fig)
    
def Important_author_keywords_out_city(city):
    keywords_lists = ast.literal_eval(keywords_authors_out_city.loc[keywords_authors_out_city['state']==city,'authors_keywords'].values[0])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 authors keywords of "+city)
    st.pyplot(fig)
    
def Important_index_keywords_out_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords_lists = ast.literal_eval(keywords_index_out_unis.loc[keywords_index_out_unis['affID']==affID,'index_keywords'].values[0])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords of "+uni_name)
    st.pyplot(fig)
    
def Important_index_keywords_out_city(city):
    keywords_lists = ast.literal_eval(keywords_index_out_city.loc[keywords_index_out_city['state']==city,'index_keywords'].values[0])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords of "+city)
    st.pyplot(fig)
    
def Important_author_keywords_out_total():
    keywords_lists = ast.literal_eval(keywords_authors_out_total.loc[0,'author_keywords'])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 authors keywords of Italy")
    st.pyplot(fig)
    
def Important_index_keywords_out_total():
    keywords_lists = ast.literal_eval(keywords_index_out_total.loc[0,'index_keywords'])
    #keywords_lists = {}
    #for i in keywords:
    #    keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords of Italy")
    st.pyplot(fig)


# # Text mining

# ### title

# In[231]:


def Important_title_keywords_lemma_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(title_universities.loc[title_universities['Unnamed: 0']==affID,'title_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by lemmatizing of "+uni_name)
    st.pyplot(fig)
    
def Important_title_keywords_lemma_city(city):
    keywords = ast.literal_eval(title_cities.loc[title_cities['Unnamed: 0']==city,'title_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by lemmatizing of "+city)
    st.pyplot(fig)
    
def Important_title_keywords_lemma_total():
    keywords = ast.literal_eval(title_total.loc[0,'title_lemma'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by lemmatizing of Italy")
    st.pyplot(fig)
    
def Important_title_keywords_pos_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(title_universities.loc[title_universities['Unnamed: 0']==affID,'title_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 1, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by part of speech of "+uni_name)
    st.pyplot(fig)
    
def Important_title_keywords_pos_city(city):
    keywords = ast.literal_eval(title_cities.loc[title_cities['Unnamed: 0']==city,'title_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by part of speech of "+city)
    st.pyplot(fig)
    
def Important_title_keywords_pos_total():
    keywords = ast.literal_eval(title_total.loc[0,'title_pos'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 title keywords by part of speech of Italy")
    st.pyplot(fig)


# ### abstract

# In[ ]:


def Important_abstract_keywords_lemma_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(abstract_universities.loc[abstract_universities['Unnamed: 0']==affID,'abstract_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by lemmatizing of "+uni_name)
    st.pyplot(fig)
    
def Important_abstract_keywords_lemma_city(city):
    keywords = ast.literal_eval(abstract_cities.loc[abstract_cities['Unnamed: 0']==city,'abstract_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by lemmatizing of "+city)
    st.pyplot(fig)
    
def Important_abstract_keywords_lemma_total():
    keywords = ast.literal_eval(abstract_total.loc[0,'abstract_lemma'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by lemmatizing of Italy")
    st.pyplot(fig)
    
def Important_abstract_keywords_pos_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(abstract_universities.loc[abstract_universities['Unnamed: 0']==affID,'abstract_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 1, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by part of speech of "+uni_name)
    st.pyplot(fig)
    
def Important_abstract_keywords_pos_city(city):
    keywords = ast.literal_eval(abstract_cities.loc[abstract_cities['Unnamed: 0']==city,'abstract_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by part of speech of "+city)
    st.pyplot(fig)
    
def Important_abstract_keywords_pos_total():
    keywords = ast.literal_eval(abstract_total.loc[0,'abstract_pos'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 abstract keywords by part of speech of Italy")
    st.pyplot(fig)


# ### Akeywords

# In[69]:


def Important_Akeywords_keywords_lemma_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(Akeywords_universities.loc[Akeywords_universities['Unnamed: 0']==affID,'Akeywords_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Author keywords by lemmatizing of "+uni_name)
    st.pyplot(fig)
    
def Important_Akeywords_keywords_lemma_city(city):
    keywords = ast.literal_eval(Akeywords_cities.loc[Akeywords_cities['Unnamed: 0']==city,'Akeywords_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Authors keywords by lemmatizing of "+city)
    st.pyplot(fig)
    
def Important_Akeywords_keywords_lemma_total():
    keywords = ast.literal_eval(Akeywords_total.loc[0,'Akeywords_lemma'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Authors keywords by lemmatizing of Italy")
    st.pyplot(fig)
    
def Important_Akeywords_keywords_pos_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(Akeywords_universities.loc[Akeywords_universities['Unnamed: 0']==affID,'Akeywords_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 1, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Authors keywords by part of speech of "+uni_name)
    st.pyplot(fig)
    
def Important_Akeywords_keywords_pos_city(city):
    keywords = ast.literal_eval(Akeywords_cities.loc[Akeywords_cities['Unnamed: 0']==city,'Akeywords_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Authors keywords by part of speech of "+city)
    st.pyplot(fig)
    
def Important_Akeywords_keywords_pos_total():
    keywords = ast.literal_eval(Akeywords_total.loc[0,'Akeywords_pos'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 Authors keywords by part of speech of Italy")
    st.pyplot(fig)


# ### Ikeywords

# In[ ]:


def Important_Ikeywords_keywords_lemma_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(Ikeywords_universities.loc[Ikeywords_universities['Unnamed: 0']==affID,'Ikeywords_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by lemmatizing of "+uni_name)
    st.pyplot(fig)
    
def Important_Ikeywords_keywords_lemma_city(city):
    keywords = ast.literal_eval(Ikeywords_cities.loc[Ikeywords_cities['Unnamed: 0']==city,'Ikeywords_lemma'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by lemmatizing of "+city)
    st.pyplot(fig)
    
def Important_Ikeywords_keywords_lemma_total():
    keywords = ast.literal_eval(Ikeywords_total.loc[0,'Akeywords_lemma'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[i[0]] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by lemmatizing of Italy")
    st.pyplot(fig)
    
def Important_Ikeywords_keywords_pos_unis(uni_name):
    affID = italy_unis.loc[italy_unis['University']==uni_name,'affiliationID'].values[0]
    keywords = ast.literal_eval(Ikeywords_universities.loc[Ikeywords_universities['Unnamed: 0']==affID,'Ikeywords_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 1, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by part of speech of "+uni_name)
    st.pyplot(fig)
    
def Important_Ikeywords_keywords_pos_city(city):
    keywords = ast.literal_eval(Ikeywords_cities.loc[Akeywords_cities['Unnamed: 0']==city,'Ikeywords_pos'].values[0])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by part of speech of "+city)
    st.pyplot(fig)
    
def Important_Ikeywords_keywords_pos_total():
    keywords = ast.literal_eval(Akeywords_total.loc[0,'Akeywords_pos'])
    keywords_lists = {}
    for i in keywords:
        keywords_lists[str(i[0])] = i[1]
    name_keywords = list(keywords_lists.keys())
    number_keywords = list(keywords_lists.values())
    fig = plt.figure(figsize = (15, 10))
    plt.barh(name_keywords[:20], number_keywords[:20])
    for i, v in enumerate(number_keywords[:20]):
        plt.text(v + 3, i , str(v), color='black', fontweight='bold')
    plt.xlabel("The number of repetitions")
    plt.ylabel("Keywords")
    plt.title("Top 20 index keywords by part of speech of Italy")
    st.pyplot(fig)


# # webpage

# In[237]:


main_option = st.selectbox('Please choose your type of analysis:',(' ','General Information','Important keywords','Text mining'))
#general_info
if main_option == 'General Information':
    genreal_info_option = st.selectbox('Please choose the type of genreal information',(' ','By university','By city','Italy'))
    if genreal_info_option == 'By university':
        uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
        general_info_university(uni_name)
    elif genreal_info_option == 'By city':
        city = st.selectbox('Please choose the city',list(italy_unis['state'].unique()))
        general_info_city(city)
    elif genreal_info_option == 'Italy':
        general_info_total()
#Important_keywords
elif main_option == 'Important keywords':
    important_keywords = st.selectbox('Please choose the type of keywords',(' ','Author keywords','Index Keywords'))
    if important_keywords == 'Author keywords':
        Author_keywords = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
        if Author_keywords == 'By university':
            uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
            Important_author_keywords_out_unis(uni_name)
        elif Author_keywords == 'By city':
            city = st.selectbox('Please choose the city',list(keywords_authors_out_city['state'].unique()))
            Important_author_keywords_out_city(city)
        elif Author_keywords == 'Italy':
            Important_author_keywords_out_total()
    elif important_keywords == 'Index Keywords':
        index_keywords = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
        if index_keywords == 'By university':
            uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
            Important_index_keywords_out_unis(uni_name)
        elif index_keywords == 'By city':
            city = st.selectbox('Please choose the city',list(keywords_index_out_city['state'].unique()))
            Important_index_keywords_out_city(city)
        elif index_keywords == 'Italy':
            Important_index_keywords_out_total()
#text_mining
elif main_option == 'Text mining':
    text_mining = st.selectbox('Please choose the variable',(' ','Title','Abstract','Author Keywords','Index Keywords'))
    if text_mining == 'Title':
        title_option = st.selectbox('Please choose the type of text mining',(' ','lemmatize','part of speech'))
        if title_option == 'lemmatize':
            title_lemma = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if title_lemma == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_title_keywords_lemma_unis(uni_name)
            elif title_lemma == 'By city':
                city = st.selectbox('Please choose the city',list(title_cities['Unnamed: 0'].unique()))
                Important_title_keywords_lemma_city(city)
            elif title_lemma == 'Italy':
                Important_title_keywords_lemma_total()
        elif title_option == 'part of speech':
            title_pos = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if title_pos == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_title_keywords_pos_unis(uni_name)
            elif title_pos == 'By city':
                city = st.selectbox('Please choose the city',list(title_cities['Unnamed: 0'].unique()))
                Important_title_keywords_pos_city(city)
            elif title_pos == 'Italy':
                Important_title_keywords_pos_total()
                
    elif text_mining == 'Abstract':
        abstract_option = st.selectbox('Please choose the type of text mining',(' ','lemmatize','part of speech'))
        if abstract_option == 'lemmatize':
            abstract_lemma = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if abstract_lemma == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_abstract_keywords_lemma_unis(uni_name)
            elif abstract_lemma == 'By city':
                city = st.selectbox('Please choose the city',list(title_cities['Unnamed: 0'].unique()))
                Important_abstract_keywords_lemma_city(city)
            elif abstract_lemma == 'Italy':
                Important_abstract_keywords_lemma_total()
        elif abstract_option == 'part of speech':
            abstract_pos = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if abstract_pos == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_abstract_keywords_pos_unis(uni_name)
            elif abstract_pos == 'By city':
                city = st.selectbox('Please choose the city',list(abstract_cities['Unnamed: 0'].unique()))
                Important_abstract_keywords_pos_city(city)
            elif abstract_pos == 'Italy':
                Important_abstract_keywords_pos_total()
                
    elif text_mining == 'Author Keywords':
        Akeywords_option = st.selectbox('Please choose the type of text mining',(' ','lemmatize','part of speech'))
        if Akeywords_option == 'lemmatize':
            Akeywords_lemma = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if Akeywords_lemma == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_Akeywords_keywords_lemma_unis(uni_name)
            elif Akeywords_lemma == 'By city':
                city = st.selectbox('Please choose the city',list(Akeywords_cities['Unnamed: 0'].unique()))
                Important_Akeywords_keywords_lemma_city(city)
            elif Akeywords_lemma == 'Italy':
                Important_Akeywords_keywords_lemma_total()
        elif Akeywords_option == 'part of speech':
            Akeywords_pos = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if Akeywords_pos == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_Akeywords_keywords_pos_unis(uni_name)
            elif Akeywords_pos == 'By city':
                city = st.selectbox('Please choose the city',list(Akeywords_cities['Unnamed: 0'].unique()))
                Important_Akeywords_keywords_pos_city(city)
            elif Akeywords_pos == 'Italy':
                Important_Akeywords_keywords_pos_total()
                
    elif text_mining == 'Index Keywords':
        Ikeywords_option = st.selectbox('Please choose the type of text mining',(' ','lemmatize','part of speech'))
        if Ikeywords_option == 'lemmatize':
            Ikeywords_lemma = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if Ikeywords_lemma == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_Ikeywords_keywords_lemma_unis(uni_name)
            elif Ikeywords_lemma == 'By city':
                city = st.selectbox('Please choose the city',list(Ikeywords_cities['Unnamed: 0'].unique()))
                Important_Ikeywords_keywords_lemma_city(city)
            elif Akeywords_lemma == 'Italy':
                Important_Ikeywords_keywords_lemma_total()
        elif Ikeywords_option == 'part of speech':
            Ikeywords_pos = st.selectbox('Please choose the type of analysis',(' ','By university','By city','Italy'))
            if Ikeywords_pos == 'By university':
                uni_name = st.selectbox('Please choose the university',list(italy_unis['University'].values))
                Important_Ikeywords_keywords_pos_unis(uni_name)
            elif Ikeywords_pos == 'By city':
                city = st.selectbox('Please choose the city',list(Ikeywords_cities['Unnamed: 0'].unique()))
                Important_Ikeywords_keywords_pos_city(city)
            elif Ikeywords_pos == 'Italy':
                Important_Ikeywords_keywords_pos_total()
    


