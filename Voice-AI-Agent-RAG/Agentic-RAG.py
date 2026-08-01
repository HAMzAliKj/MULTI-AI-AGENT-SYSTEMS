from langgraph.graph import StateGraph , START, END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
import speech_recognition as sr
import sounddevice as sd 
import soundfile as sf
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from langchain_groq import ChatGroq
import os
import streamlit as st

load_dotenv()

# ------------------ API KEYS & CONFIG ------------------ #
# Add your own API keys below or load them from .env file

ELEVENLABS_API_KEY = "paste_your_elevenlabs_api_key_here"
VOICE_ID = "paste_your_voice_id_here"

GOOGLE_GENAI_MODEL = "gemini-2.5-flash"  # Example model

os.environ["COHERE_API_KEY"] = "paste_your_cohere_api_key_here"

QDRANT_URL = "paste_your_qdrant_url_here"
QDRANT_API_KEY = "paste_your_qdrant_api_key_here"

# ------------------------------------------------------- #

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
llm = ChatGoogleGenerativeAI(model=GOOGLE_GENAI_MODEL)

class Voice_Agent(TypedDict):
    text : str
    output : str
    voice_note: str
    text_short : str

filename="inputs.wav"
duration=10
fs=16000

r = sr.Recognizer()

def voice_to_text(state : Voice_Agent):
    st.write("🎙️ Speak Now...")
    recording = sd.rec(int(duration * fs) , samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename,recording,fs)
    with sr.AudioFile("inputs.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        state['text'] = text
        return state

from langchain_qdrant import QdrantVectorStore
from langchain_cohere import CohereEmbeddings

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
)

def RAG_Agent(text):
    db = QdrantVectorStore.from_existing_collection(
        collection_name="Pak_Law_Pdf",
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        embedding=embeddings
    )

    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain.chains import create_retrieval_chain

    template = ChatPromptTemplate([
        ("system",
        "You are a knowledgeable AI assistant specialized in legal document analysis. "
        "You will be provided with a context (retrieved from legal documents) and a user question. "
        "Your task is to carefully read the context and provide a clear, accurate, and concise answer "
        "based **only** on the information in the given context. "
        "If the context does not contain enough information, respond with: "
        "'The provided context does not contain sufficient information to answer this question.'\n\n"
        "'Whenever you find an answer explain it in simple English. "
        "Break complex terms into simple explanations.'"
        "Context:\n{context}"),
        ("user",
        "Question: {input}\n\n"
        "Please provide your answer strictly based on the context above.")
    ])

    doc_chain = create_stuff_documents_chain(llm,template)
    retriever = db.as_retriever()
    chain = create_retrieval_chain(retriever,doc_chain)

    response = chain.invoke({"input": text})
    return response["answer"]

def llm_node(state:Voice_Agent):
    message = state['text']
    response = RAG_Agent(message)
    state['output'] = response
    return state


from langchain.prompts import PromptTemplate

summarizer_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a text summarizer. 
I will give you some text, and you must shorten it so it contains fewer than 1900 characters 
Don't Make Them Too Short
(but keep the key meaning and natural flow). 
Do not add anything new. 
Only return the shortened text. 

Text:
{text}
"""
)

def short_Text(state: Voice_Agent):
    text = state['output']
    chain = summarizer_prompt | llm
    output = chain.invoke({"text": text}).content
    state['text_short'] = output
    return state

def output_to_speeech(state:Voice_Agent):
    audio_stream = client.text_to_speech.convert(
    voice_id=VOICE_ID,
    model_id="eleven_multilingual_v2",
    text=state['text_short'],
    output_format="mp3_44100_128"
)   
    with open("daily_news.mp3","wb") as f:
        for chuck in audio_stream:
            f.write(chuck)
    state['voice_note'] = "daily_news.mp3"        
    return state

graph = StateGraph(Voice_Agent)

graph.add_node("voice_to_text",voice_to_text)
graph.add_node("llm_node",llm_node)
graph.add_node("text_short",short_Text)
graph.add_node("text_to_speech",output_to_speeech)

graph.add_edge(START,"voice_to_text")
graph.add_edge("voice_to_text","llm_node")
graph.add_edge("llm_node","text_short")
graph.add_edge('text_short','text_to_speech')
graph.add_edge("text_to_speech",END)

response = graph.compile()

# ------------------ STREAMLIT FRONTEND ------------------ #
st.set_page_config(page_title="RAG Law Chatbot with Voice", page_icon="⚖️", layout="centered")

st.title("⚖️ PAKISTAN LAWS RAG POWER CHATBOT (VOICE AGENT)")

if st.button("🎤 GIVE YOUR QUESTION VOICE 🎤︎︎....."):
    res = response.invoke({"text": " "})
    st.subheader("🗣️ You said:")
    st.write(res['text'].upper())
    

    st.subheader("📖 Answer:")
    st.write(res['output'])

    st.subheader("🔊 Listen:")
    audio_bytes = open(res['voice_note'], "rb").read()
    st.audio(audio_bytes, format="audio/mp3")
