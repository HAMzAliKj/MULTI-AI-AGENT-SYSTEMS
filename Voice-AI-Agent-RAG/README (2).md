# VOICE_AGENT_RAG_POWER
RAG-powered Pakistan Law Chatbot with voice support. 🎙️ Ask legal questions by speaking, the bot retrieves answers from law PDFs using Qdrant + Cohere embeddings, processes with Gemini/Groq LLM, summarizes, and converts into speech via ElevenLabs. Built with Streamlit + LangGraph. ⚖️

<img width="1004" height="629" alt="law" src="https://github.com/user-attachments/assets/9c36e6ab-14cc-4244-93f5-74efdc49b2fa" />

🇵🇰 Pakistan Law RAG Chatbot (Voice Enabled)

An AI-powered chatbot designed to answer Pakistan law-related questions using Retrieval-Augmented Generation (RAG). Users can ask questions via voice, the bot retrieves answers from law-trained PDFs, generates a reliable response, and then speaks the answer back.

✨ Features

🎙️ Voice Input – Ask questions through speech.

📚 RAG-based Retrieval – Fetches context-aware answers from uploaded Pakistan law PDFs.

⚖️ Accurate Legal Responses – Powered by Cohere embeddings + Qdrant vector DB.

🤖 LLM Integration – Uses Gemini / Groq LLM for natural language answers.

🔊 Voice Output – Converts answers into speech via ElevenLabs API.

🌐 Streamlit UI – Simple, clean, and user-friendly interface.

🔄 Chat History – Keeps track of previous questions & answers.

🛠️ Tech Stack

Python 🐍

Streamlit – Web app framework

LangChain + LangGraph – RAG workflow & orchestration

Qdrant – Vector database for embeddings

Cohere Embeddings – Document representation

Groq / Gemini LLMs – Response generation

ElevenLabs – Text-to-speech

SpeechRecognition – For voice input

🚀 How It Works

Upload Pakistan Law PDFs 📑

Ask a question via voice or text 🎤⌨️

System retrieves relevant context using RAG 🔍

LLM generates a clear answer 🤖

Answer is spoken back via ElevenLabs voice 🔊

📂 Project Structure
├── app.py          # Main Streamlit app
├── requirements.txt # Dependencies
├── .env             # API keys & secrets
├── data/            # Law PDFs
└── utils/           # Helper functions

⚡ Setup Instructions

Clone the repo

git clone https://github.com/yourusername/pakistan-law-rag-chatbot.git
cd pakistan-law-rag-chatbot


Install dependencies

pip install -r requirements.txt


Add your API keys in .env

COHERE_API_KEY=your_key
QDRANT_API_KEY=your_key
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key


Run the app

streamlit run app.py

📸 Demo Preview

(Add screenshot or demo GIF here)

🔮 Future Work

Add multi-language support (Urdu + English).

Improve accuracy with fine-tuned embeddings.

Mobile app integration.

🤝 Contributing

Pull requests are welcome! Feel free to fork, raise issues, or suggest features.

📜 License

MIT License – Free to use and modify.
