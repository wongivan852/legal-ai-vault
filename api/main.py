"""
Legal AI Vault - Main FastAPI Application
Uses your local llama3.3:70b model via Ollama
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import logging
import sys
import os

from services.ollama_service import OllamaService
from database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal AI Vault API",
    description="On-premises legal AI using llama3.3:70b",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ollama_service = OllamaService()


# Pydantic models
class GenerateRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 4096


class EmbedRequest(BaseModel):
    text: str


class SetModelRequest(BaseModel):
    model_name: str
    model_type: str = "llm"  # "llm" or "embedding"


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Legal AI Vault API...")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    # Check Ollama connection
    health = await ollama_service.health_check()
    logger.info(f"Ollama status: {health}")


# Health check endpoint
@app.get("/health")
async def health_check():
    """System health check"""
    try:
        ollama_health = await ollama_service.health_check()

        return {
            "status": "healthy",
            "ollama": ollama_health,
            "api_version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


# Mount static files (frontend)
# Check if frontend directory exists
frontend_path = "/app/frontend"
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=f"{frontend_path}/static"), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve frontend UI"""
        return FileResponse(f"{frontend_path}/index.html")
else:
    # Fallback if frontend not mounted
    @app.get("/")
    async def root():
        """API information"""
        return {
            "name": "Legal AI Vault API",
            "version": "1.0.0",
            "model": "llama3.3:70b",
            "docs": "/docs",
            "health": "/health"
        }


# Text generation endpoint
@app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    """
    Generate text using llama3.3:70b

    Example:
    ```
    curl -X POST http://localhost:8000/api/generate \
      -H "Content-Type: application/json" \
      -d '{"prompt": "Explain contract law in Hong Kong", "max_tokens": 500}'
    ```
    """
    try:
        result = await ollama_service.generate(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return {
            "success": True,
            "response": result["response"],
            "model": result["model"],
            "stats": {
                "total_duration_ms": result["total_duration"] // 1000000,
                "prompt_tokens": result["prompt_eval_count"],
                "completion_tokens": result["eval_count"]
            }
        }

    except Exception as e:
        logger.error(f"Generation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Embedding endpoint
@app.post("/api/embed")
async def generate_embedding(request: EmbedRequest):
    """
    Generate embeddings using nomic-embed-text

    Example:
    ```
    curl -X POST http://localhost:8000/api/embed \
      -H "Content-Type: application/json" \
      -d '{"text": "What are my employment rights?"}'
    ```
    """
    try:
        embedding = await ollama_service.embed(request.text)

        return {
            "success": True,
            "embedding": embedding,
            "dimension": len(embedding),
            "model": ollama_service.embedding_model
        }

    except Exception as e:
        logger.error(f"Embedding error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# List models endpoint
@app.get("/api/models")
async def list_models():
    """
    List available Ollama models

    Shows all models from your ~/.ollama/models directory
    """
    try:
        models = await ollama_service.list_models()

        return {
            "success": True,
            "models": models,
            "total": len(models),
            "active_llm": ollama_service.model,
            "active_embedding": ollama_service.embedding_model
        }

    except Exception as e:
        logger.error(f"List models error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Set model endpoint
@app.post("/api/models/set")
async def set_model(request: SetModelRequest):
    """
    Switch the active model

    Example:
    ```
    curl -X POST http://localhost:8000/api/models/set \
      -H "Content-Type: application/json" \
      -d '{"model_name": "llama3.1:8b", "model_type": "llm"}'
    ```
    """
    try:
        if request.model_type == "llm":
            ollama_service.set_model(request.model_name)
            return {
                "success": True,
                "message": f"LLM model switched to {request.model_name}",
                "active_llm": ollama_service.model,
                "active_embedding": ollama_service.embedding_model
            }
        elif request.model_type == "embedding":
            ollama_service.set_embedding_model(request.model_name)
            return {
                "success": True,
                "message": f"Embedding model switched to {request.model_name}",
                "active_llm": ollama_service.model,
                "active_embedding": ollama_service.embedding_model
            }
        else:
            raise HTTPException(status_code=400, detail="model_type must be 'llm' or 'embedding'")

    except Exception as e:
        logger.error(f"Set model error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
