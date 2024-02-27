### Assignment guidance
# The goal of this assignment is to create a word2vec-based question-answer chatbot application that should be able
# to give the best answer based on vector search toward both question set and answer set. 
# Our exercise only showed how to apply question set for vector search. You can follow the hints to generate the chatbot. 
# What you need to submit for this assignment: an app url (You should publish your chatbot application on Streamlit Cloud. 
# Your chatbot assignment will be evaluated based on query questions listed as below:
# (1) A year before improving and popularizing the electrophorus, what did Volta become?
# (2) Does the Hymenoptera order include ants?
# (3) Who invented the voltaic pile?
# (4) Does Avogadro Law talk about the relationship between same volume masses?
###

import streamlit as st
import pandas as pd
import faiss
import gensim
import numpy as np

# load question-answer dataset 
df = pd.read_csv("data/Question_Answer_Dataset_v1.2_S10.csv")

# load question and answer vectors generated from pre-trained word2vec model
vector = ...
ques_vec = ...
ans_vec = ...

# load th trained word2vec model 
# Hint: You should use the word2vec model pre-trained with both question and answer sets.
trained_w2v = ...

# App title
st.set_page_config(page_title="Word2vec Question and Answer Chatbot")

# Add header image 
st.image("data/header-chat-box.png")

# chat title 
st.title("Word2vec Question and Answer Chatbot")

# Store generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messagess
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate the embedding for query question
def trained_sentence_vec(sent):
    # Filter out terms that are not in the vocabulary from the question sentence
    # Hint: Use model.wv to get the whole vocabulary
    qu_voc = ...
    # Get the embedding of the characters
    # Hint: Stack arrays in sequence vertically using np.vstack
    emb = ...
    # Calculate the arithmetic mean for the vectors of each included word along the column 
    # to get the vector of the question
    ave_vec = ...
    return ave_vec

# Function to find the answer through vector search
### Hint ###
# Function inputs: qr_sentence, ques_vec, and ans_vec
# Function output: the index of the optimal answer
# Function goal: do vector search among both question and answer sets
###
def find_answer(qr_sentence, ques_vec, ans_vec):
    # use one query sentence to retrieve answer
    qr_sentence = gensim.utils.simple_preprocess(qr_sentence)
    qr_sentence = token(qr_sentence)
    qr_sent_vec = trained_sentence_vec(qr_sentence)

    # perform vector search through similarity comparison
    # define the number of feature (vector) dimensions
    n_dim = ...
    # define the number of pairs of question and answer
    n_q_a = ... 
    # define ques_vec as a numpy array that is a float of size 32 bits
    x = ...
    # define ans_vec as a numpy array that is a float of size 32 bits
    y = ...
    # reshape qr_sent_vec
    q = qr_sent_vec.reshape(1, -1)
    # build the faiss index, n_dim=size of vectors using faiss.index_factory with METRIC_INNER_PRODUCT parameter
    index = ...
	
    # add all questions into the faiss index
    faiss.normalize_L2(x)
    index.add(x)
	
    # add all answers into the faiss index
    faiss.normalize_L2(y)
    index.add(y)
	
    # do vector search for the query sentence
    # return similarity score and idx using index.search function
    faiss.normalize_L2(q)
    similarity, idx = ...
    ans_idx = idx[0][0]
	
    # find out the optimal answer index
    # Hint: if ans_idx is over the number of question-answer pairs, we need to make a if-statement to 
    # return an answer index align with our question-answer dataset
    if...
      
    return ans_idx


# User-provided prompt
if prompt := st.chat_input("What's your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ans_idx = find_answer(prompt, ques_vec)
            response = df["Answer"][ans_idx]
            st.write(response)
            
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

