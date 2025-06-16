
Scripture Threads (Thematic Bible Visualizer)
Welcome to Scripture Threads, a sophisticated, AI-powered web application designed for comprehensive and interactive biblical study. The application transforms static scripture into a dynamic, interconnected, and semantically searchable knowledge base, allowing users to explore thematic connections across the Bible in a visually engaging way.
The system is built on a modern stack, featuring a React (Vite) frontend, a Python (FastAPI) backend, and leverages the powerful synergy between Google's Generative AI and MongoDB's Vector Search capabilities.
✨ Features
User Interface & Visualization
 * Interactive Biblical Timeline: A grid-based visualization of all 66 books of the Bible, organized by testament and category.
 * Dynamic Theme Connections: Visually trace the connections of theological themes across different books of the Bible using elegantly rendered SVG arcs.
 * Three-Panel Layout: An intuitive interface that separates theme discovery, the biblical timeline, and a contextual insights panel for a clear user experience.
 * Responsive Design: A fully adaptive layout that provides an optimized experience on desktop, tablet, and mobile devices.
 * Interactive Bible Reader: A built-in reader for exploring chapters and verses directly within the interface.
AI & Data Analysis
 * Semantic Search: Go beyond simple keyword matching. Find relevant passages and theological concepts based on their meaning and context, powered by vector-based search.
 * AI-Powered Explanations: Generate detailed, context-aware explanations for biblical events and individual verses using Google's Gemini models.
 * Theological Summaries: Access AI-generated overviews, key scripture references, and theological context for every book of the Bible.
 * Interconnected Knowledge Base: Explore the rich relationships between theological concepts, biblical books, and key events.
 * Intelligent Caching: Faster response times and reduced API costs by caching AI-generated content in MongoDB.
🛠️ System Architecture
The application is composed of a frontend, a backend API, a database, and an offline data processing pipeline.
 * Frontend: A responsive Single Page Application (SPA) built with React and Vite. It provides a rich, component-driven user interface for visualization and interaction.
 * Backend: A RESTful API service built with FastAPI (Python). It serves data to the frontend, manages the database, and integrates with Google's AI services to perform complex tasks like semantic search and content generation.
 * Database: A MongoDB database hosted on Atlas, which serves as the core data platform. It utilizes Vector Search to enable high-performance semantic queries across all biblical text, commentaries, and theological concepts.
 * Data Processing: An initial data pipeline processes raw sources like the Bible in XML and PDF commentaries. Using Google AI models, it extracts, structures, and generates vector embeddings for all content, creating an enriched and interconnected knowledge base.
💡 Google AI + MongoDB Synergy
This project demonstrates the powerful integration between Google's Generative AI and MongoDB's intelligent data platform.
 * Semantic Search Excellence: Google's text-embedding-004 model transforms text into high-dimensional vector embeddings, capturing its semantic meaning. These embeddings are stored in MongoDB, and MongoDB's native Vector Search capabilities enable lightning-fast similarity queries that understand context far beyond simple keyword matching.
 * Intelligent Content Generation: The backend uses Google's Gemini models to generate nuanced and contextually rich content, such as theological summaries and detailed explanations of Bible verses. This AI-generated content is then stored in MongoDB's flexible document model, ensuring that responses are grounded in authoritative biblical sources through a Retrieval-Augmented Generation (RAG) architecture.
 * Scalable and Efficient: Storing vector embeddings directly within MongoDB alongside the source content is highly efficient. The system is further optimized by caching AI-generated responses in dedicated MongoDB collections, which reduces API costs and significantly improves response times for users.
📑 Data Processing Notebook
The project includes a notebooks folder containing the Scripture.ipynb Jupyter Notebook.
This notebook documents and executes the entire multi-stage data pipeline used to build the project's knowledge base. It was run in a Google Colab environment and performs all the essential one-time setup tasks:
 * Extraction: Extracts text from source PDFs using the PyMuPDF library.
 * Structuring: Organizes the raw text into structured JSON objects.
 * Embedding: Uses Google's text-embedding-004 model to generate vector embeddings for text chunks.
 * Enrichment: Leverages the Gemini model to generate theological summaries, descriptions, and other key metadata.
 * Loading: Cleans, normalizes, and ingests all the enriched data and their vector embeddings into the various MongoDB collections.
🚀 Getting Started
Prerequisites
 * Node.js (v18 or later)
 * Python 3.8+
 * NPM or Yarn
 * Pip (Python package manager)
Backend Setup
 * Navigate to the backend directory:
   cd backend

 * Create and activate a virtual environment:
   # Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

 * Install Python dependencies:
   pip install -r requirements.txt

 * Start the backend server:
   uvicorn app.main:app --reload

   The API will be available at http://localhost:8000.
Frontend Setup
 * In a new terminal, navigate to the frontend folder.
 * Install Node.js dependencies:
   npm install
# or
yarn install

 * Start the development server:
   npm run dev
# or
yarn dev

 * Open http://localhost:5173 (or the port specified by Vite) in your browser.
⚙️ Configuration
Create a .env file in both the frontend and backend directories.
Frontend (frontend/.env)
VITE_API_BASE_URL=http://localhost:8000/api/v1

Backend (backend/.env)
# Your MongoDB Atlas connection string
MONGO_DB_URI="mongodb+srv://..."

# Your Google AI API Key
GOOGLE_API_KEY="your-google-api-key"

📚 API Documentation
When the backend is running, you can access the interactive API documentation at:
 * Swagger UI: http://localhost:8000/docs
 * ReDoc: http://localhost:8000/redoc
💻 Technology Stack
Frontend
 * Framework: React 18
 * Build Tool: Vite
 * Styling: Custom CSS3 (Grid, Flexbox, Custom Properties)
 * Icons: Lucide React
 * Typography: Inter Typeface
Backend
 * Framework: FastAPI
 * Server: Uvicorn
 * Data Validation: Pydantic
 * AI/ML: Google Generative AI (Gemini, text-embedding-004)
 * Vector Operations: NumPy
Database
 * Platform: MongoDB Atlas
 * Core Technology: MongoDB with Vector Search
Data Processing & Development
 * Environment: Google Colab, Docker
 * PDF Extraction: PyMuPDF
📄 License
This project is licensed under the MIT License.
