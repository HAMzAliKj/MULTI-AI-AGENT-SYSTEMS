# 🤖 CHATTER AI

**CHATTER AI** is an AI-powered RAG (Retrieval-Augmented Generation) application that lets you chat with different types of content. Simply provide a YouTube video, a website URL, or upload a PDF, and CHATTER AI answers your questions based on that content instead of relying only on the LLM's general knowledge.

---

## ✨ Features

* 🎥 Chat with YouTube videos
* 🌐 Chat with website articles
* 📄 Chat with uploaded PDF documents
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔍 Semantic search using vector embeddings
* 💬 Interactive chat interface
* ⚡ Fast document retrieval and response generation

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini
* FAISS / Vector Database
* YouTube Transcript API
* BeautifulSoup
* PyPDF

---

## 🚀 How It Works

1. Select a data source:

   * YouTube Video
   * Website URL
   * PDF File

2. The application extracts the content.

3. The content is split into smaller chunks.

4. Embeddings are generated for each chunk.

5. The embeddings are stored in a vector database.

6. When you ask a question:

   * Relevant chunks are retrieved.
   * The retrieved context is sent to Gemini.
   * Gemini generates an accurate answer based on the retrieved information.

---

## 📂 Supported Sources

* ✅ YouTube Videos
* ✅ Website Articles
* ✅ PDF Documents

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/HAMzAliKj/CHATTER_AI_.git
```

Move into the project directory:

```bash
cd CHATTER_AI_
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📸 Demo

You can add screenshots or a GIF of the application here.

Example:

```
images/home.png
images/chat.png
```

---

## 📁 Project Structure

```text
CHATTER_AI_
│
├── app.py
├── requirements.txt
├── README.md
├── assets/
├── utils/
├── data/
└── ...
```

---

## 🎯 Example Questions

### YouTube

* Summarize this video.
* What are the key points?
* Explain the main concept.

### Website

* Summarize this article.
* What are the important facts?
* Explain this topic in simple words.

### PDF

* Give me a summary.
* What does page 10 discuss?
* List the important points.

---

## 🔮 Future Improvements

* Chat history
* Multiple PDF support
* Multiple website support
* Citation with page numbers
* Source highlighting
* Conversation memory
* Support for DOCX and TXT files
* Deploy online

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Hamza Ali Khan**

GitHub: https://github.com/HAMzAliKj

If you found this project useful, consider giving it a ⭐ on GitHub!
