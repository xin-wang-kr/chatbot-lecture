import streamlit as st
import pandas as pd
import faiss
import gensim
import numpy as np

# load question-answer dataset 
df = pd.read_csv("data/Question_Answer_Dataset_v1.2_S10.csv")

# load question vector
vector = np.load('data/vector.npz')
ques_vec = vector['x']

# load th trained word2vec model 
trained_w2v = gensim.models.Word2Vec.load("data/w2v.model")

# App title
st.set_page_config(page_title="Word2vec Question and Answer Chatbot")

# Add header image 
st.image("data/header-chat-box.png")

# chat title 
st.title("Word2vec Question and Answer Chatbot")

# Store generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating response for query question
def trained_sentence_vec(sent):
    # Filter out terms that are not in the vocabulary from the question sentence
    qu_voc = [tm for tm in sent if tm in trained_w2v.wv]
    # Get the embedding of the characters
    emb = np.vstack([trained_w2v.wv[tm] for tm in sent if tm in trained_w2v.wv])
    # Calculate the vectors of each included word to get the vector of the question
    ave_vec = np.mean(emb, axis=0)
    return ave_vec

def find_answer(qr_sentence, ques_vec):
    # use one query sentence to retrieve answer
    qr_sentence = gensim.utils.simple_preprocess(qr_sentence)
    qr_sent_vec = trained_sentence_vec(qr_sentence)

    # perform vector search through similarity comparison
    n_dim = ques_vec.shape[1]
    x = np.vstack(ques_vec).astype(np.float32)
    q = qr_sent_vec.reshape(1, -1)
    index = faiss.index_factory(n_dim, "Flat", faiss.METRIC_INNER_PRODUCT)
    faiss.normalize_L2(x)
    index.add(x)
    faiss.normalize_L2(q)
    similarity, idx = index.search(q, k=index.ntotal)
    ans_idx = idx[0][0]
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

