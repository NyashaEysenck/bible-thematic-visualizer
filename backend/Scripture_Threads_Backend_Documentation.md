# Thematic Bible Visualizer API Documentation

## Overview

The Thematic Bible Visualizer is a sophisticated FastAPI-based application that provides intelligent biblical text analysis through advanced AI-powered search and explanation capabilities. The system leverages Google's Generative AI and MongoDB's vector search capabilities to deliver contextually rich biblical insights.

## Architecture

### Core Components

**FastAPI Application Server**
- Modern async web framework providing RESTful API endpoints
- Built-in OpenAPI documentation and validation
- Comprehensive error handling and CORS support
- Static file serving for Single Page Application (SPA) deployment

**Google AI Integration**
- **Gemini 2.0 Flash**: Primary generative model for creating detailed biblical explanations
- **Text Embedding 004**: Advanced embedding model for semantic search and content similarity
- Contextual AI responses enriched with Retrieval-Augmented Generation (RAG)

**MongoDB Database**
- Document-based storage with vector search capabilities
- Specialized collections for different content types
- Vector indexing for high-performance semantic search

### Technology Stack

- **Backend Framework**: FastAPI (Python)
- **AI/ML**: Google Generative AI (Gemini, Text Embeddings)
- **Database**: MongoDB with Vector Search
- **Vector Operations**: NumPy for embedding computations
- **Environment**: Docker-ready with uvicorn ASGI server
- **Frontend**: React SPA (served via static files)

## Database Schema

### Collections

**theology**
- Theological concepts and themes
- Vector embeddings for semantic search
- Theme connections and relationships
- Color coding for visualization

**commentary_chunks**
- Biblical commentary excerpts
- Verse-specific annotations
- Source attribution and references
- Vector embeddings for contextual search

**bible_esv**
- Complete ESV Bible text
- Structured by book, chapter, and verse
- Searchable biblical content

**books**
- Biblical book metadata
- Testament and category classifications
- Detailed insights and overviews

**event_explanations** & **verse_explanations**
- Cached AI-generated explanations
- Performance optimization through intelligent caching

## Core Functions

### Vector Search Operations

**Embedding Generation**
- Transforms text queries into high-dimensional vectors using Google's Text Embedding 004
- Enables semantic similarity matching beyond keyword search
- Supports both document indexing and query processing

**Theology Vector Search**
- Searches theological concepts using vector similarity
- Returns ranked results with relevance scores
- Configurable result limits for performance optimization

**Commentary Vector Search**
- Locates relevant biblical commentary passages
- Cross-references verse locations and sources
- Provides contextual biblical scholarship

### AI-Powered Explanation Generation

**Event Explanation**
- Combines theological concepts with commentary insights
- Generates comprehensive explanations of biblical events
- Contextualizes events within broader theological themes
- Integrates historical and cultural perspectives

**Verse Explanation**
- Provides detailed verse-by-verse analysis
- Incorporates multiple contextual sources
- Offers practical applications and theological significance
- Connects individual verses to broader biblical narratives

### Data Management

**Intelligent Caching**
- Stores generated explanations to reduce API costs
- Implements cache-first retrieval strategy
- Maintains explanation consistency across requests

**Fallback Mechanisms**
- JSON file fallbacks for database connectivity issues
- Graceful degradation ensuring system availability
- Robust error handling throughout the application

## API Endpoints

### Core Data Endpoints

**GET /api/v1/themes**
- Retrieves all biblical themes with metadata
- Includes color coding for visualization
- Returns structured theme information

**GET /api/v1/books**
- Lists all biblical books with classifications
- Testament and category organization
- Ordered presentation for consistent navigation

**GET /api/v1/themes/{theme_id}/connections**
- Provides theme-to-book relationship mapping
- Includes prominence scores and event listings
- Enables thematic visualization and analysis

### Bible Content Endpoints

**GET /api/v1/books/{book}/chapters**
- Chapter listings with verse counts
- Structured navigation support
- Book-specific content organization

**GET /api/v1/books/{book}/chapters/{chapter}/verses**
- Complete verse listings for chapters
- Full text content with reference metadata
- Sequential verse ordering

### AI-Powered Analysis Endpoints

**POST /api/v1/explain-event**
- Generates contextual event explanations
- Combines multiple data sources through RAG
- Caches results for performance optimization

**POST /api/v1/explain-verse**
- Provides comprehensive verse analysis
- Integrates theological and commentary insights
- Delivers scholarly yet accessible explanations

## Google AI + MongoDB Integration Highlights

### Powerful Synergy

The application demonstrates exceptional integration between Google's AI capabilities and MongoDB's document database features:

**Semantic Search Excellence**
- Google's Text Embedding 004 creates rich semantic representations
- MongoDB's vector search enables lightning-fast similarity queries
- Combined system understands context beyond simple keyword matching

**Intelligent Content Generation**
- Gemini 1.5 Flash generates nuanced, contextually appropriate explanations
- RAG architecture ensures AI responses are grounded in authoritative sources
- MongoDB's flexible schema accommodates diverse content types seamlessly

**Scalable Architecture**
- Vector embeddings stored efficiently in MongoDB
- AI processing optimized through intelligent caching strategies
- Async operations ensure responsive user experience

**Contextual Understanding**
- AI models access rich theological and commentary databases
- MongoDB's aggregation pipelines enable complex query operations
- System delivers explanations that consider multiple perspectives and sources

### Performance Optimization

**Caching Strategy**
- AI-generated content cached in MongoDB collections
- Reduces API costs and improves response times
- Intelligent cache invalidation and management

**Vector Index Optimization**
- MongoDB vector indexes enable sub-second search operations
- Configurable search parameters balance accuracy and performance
- Efficient embedding storage and retrieval

## Deployment Features

### Production Readiness

**Static File Serving**
- Integrated SPA support for React frontend
- Optimized asset delivery with proper MIME types
- Catch-all routing for client-side navigation

**Environment Configuration**
- Secure environment variable management
- Flexible configuration for different deployment scenarios
- Docker containerization support

**Health Monitoring**
- Built-in health check endpoints
- Comprehensive error handling and logging
- Graceful failure modes and recovery strategies

## Security & Best Practices

### API Security
- CORS configuration for cross-origin requests
- Input validation through Pydantic models
- Secure environment variable handling

### Database Security
- Connection string encryption
- Proper error handling without information leakage
- Input sanitization for database queries

### AI Integration Security
- API key management through environment variables
- Rate limiting considerations for AI API usage
- Error handling for AI service failures

This architecture represents a sophisticated implementation of modern AI-powered biblical study tools, combining the semantic understanding of Google's AI with the flexible, scalable storage capabilities of MongoDB to deliver an exceptional user experience for biblical research and education.