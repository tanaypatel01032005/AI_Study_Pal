# AI Study Pal 🎓

> **A Flagship AI-Powered Learning Platform**

AI Study Pal is a modern, production-ready educational platform designed to transform raw documents into interactive, personalized learning experiences. Built with a scalable microservices architecture, it leverages advanced Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to serve as your personal AI Tutor.

## ✨ Features

- **Document Ingestion & RAG Pipeline**: Upload PDFs or text documents. The system automatically chunks, embeds, and indexes them using FAISS and HuggingFace for lightning-fast, context-aware querying.
- **AI Tutor Chat**: Engage in a conversational interface with an AI tutor that strictly answers questions based on your uploaded curriculum.
- **Smart Quizzes & Flashcards**: Auto-generate targeted assessments and flashcards from your study materials to reinforce learning.
- **Personalized Study Plans**: Break down complex subjects into structured, daily milestones.
- **Learning Insights**: Receive AI-generated analytics on your strong/weak concepts and personalized recommendations.
- **Modern UI**: A premium, glassmorphism-inspired React dashboard built with Vite, Tailwind CSS, and shadcn/ui.

## 🚀 Technology Stack

### Backend
- **FastAPI**: High-performance asynchronous API.
- **SQLite / SQLAlchemy / Alembic**: Robust database architecture, ready for PostgreSQL migration.
- **LangChain / HuggingFace Hub**: Core orchestration for LLMs and embeddings.
- **FAISS**: High-speed vector similarity search.
- **Pytest**: Comprehensive endpoint testing.

### Frontend
- **React 18 & TypeScript**: Robust UI development.
- **Vite**: Next-generation frontend tooling.
- **Tailwind CSS & shadcn/ui**: Modern, accessible, and stunning component library.

### Infrastructure
- **Docker & Docker Compose**: Full containerization for both frontend and backend services.

## 🛠️ Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional, for containerized deployment)
- Hugging Face API Token

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI_Study_Pal.git
   cd AI_Study_Pal
   ```

2. **Backend Setup:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Add your HUGGINGFACEHUB_API_TOKEN to .env
   
   # Run migrations
   alembic upgrade head
   
   # Start the API
   uvicorn backend.main:app --reload --port 8000
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Open `http://localhost:5173` to view the application and `http://localhost:8000/docs` for the Swagger API documentation.

## 🐳 Docker Deployment

To run the entire stack using Docker Compose:

```bash
docker-compose up --build
```
The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:80`.

## 📜 License
MIT License
