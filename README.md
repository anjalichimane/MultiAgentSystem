# 🔬 MultiAgent AI Research System

An AI-powered Multi-Agent Research Assistant built using **LangGraph**, **Groq LLM**, **Tavily Search**, **FastAPI**, and **Streamlit**.

This system automatically:

* Searches the web for information
* Scrapes useful content from websites
* Generates a detailed research report
* Critiques and scores the generated report

---

# 🚀 Features

✅ Multi-Agent Workflow using LangGraph
✅ Web Search with Tavily API
✅ Website Scraping with BeautifulSoup
✅ AI Report Generation using Groq LLM
✅ Critic Agent for Report Evaluation
✅ Streamlit Modern UI
✅ FastAPI Backend
✅ Google Colab Deployment Support
✅ ngrok Public API Support

---

# 🧠 Agents Used

| Agent           | Responsibility                            |
| --------------- | ----------------------------------------- |
| 🔍 Search Agent | Searches the web for relevant information |
| 📖 Reader Agent | Scrapes and reads web content             |
| ✍️ Writer Agent | Generates research report                 |
| 🧐 Critic Agent | Reviews and scores the report             |

---

# 🛠️ Tech Stack

* Python
* LangGraph
* LangChain
* Groq API
* Tavily Search API
* BeautifulSoup4
* FastAPI
* Streamlit
* ngrok
* Google Colab

---

# 📂 Project Structure

```bash
MultiAgentSystem/
│
├── app.py                 # Streamlit frontend
├── backend_colab.py       # FastAPI backend in Colab
├── requirements.txt
├── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/MultiAgentSystem.git
cd MultiAgentSystem
```

---

## 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

# 🔑 API Keys Required

Create the following API keys:

* Groq API Key
* Tavily API Key
* ngrok Auth Token

---

# ▶️ Running Backend (Google Colab)

1. Open `backend_colab.py` in Google Colab
2. Add your API keys
3. Run all cells
4. Copy the generated ngrok URL

Example:

```bash
https://abcd-12-34-56.ngrok-free.app
```

---

# ▶️ Running Streamlit Frontend

```bash
streamlit run app.py
```

Paste the ngrok backend URL inside the Streamlit sidebar.

---

# 🖥️ Application Workflow

1. User enters research topic
2. Search Agent searches web
3. Reader Agent scrapes top websites
4. Writer Agent creates report
5. Critic Agent reviews report
6. Final report displayed in Streamlit UI

---

# 📸 Project Screenshots

## 🏠 Images

<img width="1904" height="884" alt="Screenshot 2026-06-09 130855" src="https://github.com/user-attachments/assets/7227a906-c6ed-4208-89db-c6ee55d32edf" />

<img width="1919" height="871" alt="Screenshot 2026-06-09 131036" src="https://github.com/user-attachments/assets/ecdf117c-cb09-4488-8a7c-b821fbf9eb55" />

<img width="1916" height="877" alt="Screenshot 2026-06-09 131147" src="https://github.com/user-attachments/assets/c4e27aa2-7159-4c88-9ffc-0024ac5420af" />

<img width="1919" height="878" alt="Screenshot 2026-06-09 131249" src="https://github.com/user-attachments/assets/f5ed1954-3292-4b07-b613-94a7e7bb3316" />

---

# 🎥 Demo Video

[▶️ Watch Demo Video](https://drive.google.com/file/d/1W3n0wSt9nQwDLxKo2BoNMM-DgOiLE6r0/view?usp=drive_link)

---

# 📈 Future Improvements

* PDF Export
* Memory-enabled Agents
* Multi-language Research
* Voice Input
* Real-time Streaming Output
* Citation Generation

---
