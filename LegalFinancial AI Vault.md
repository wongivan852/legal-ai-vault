# Legal/Financial AI Vault  
#   
#  (6-GPU Server)  
## Technology Stack  
  
  
yaml  
Core Components:  
├── Operating System: Ubuntu 22.04 LTS Server  
├── Container Runtime: Docker 24.x + Docker Compose  
├── Inference Engine: vLLM 0.5.x (multi-GPU support)  
├── Workflow Engine: Dify 0.6.x (self-hosted)  
├── Vector Database: Qdrant 1.8.x  
├── Relational Database: PostgreSQL 15  
├── Web Framework: FastAPI 0.110.x (Python 3.11)  
├── Frontend: React 18 + TypeScript + Tailwind CSS  
├── Reverse Proxy: Nginx 1.24.x  
├── Monitoring: Prometheus + Grafana  
└── Security: fail2ban, UFW firewall, AppArmor  
## System Architecture  
  
  
┌─────────────────────────────────────────────────────────────────┐  
│                    LEGAL AI VAULT ARCHITECTURE                  │  
│                    (Client's Internal Network)                  │  
└─────────────────────────────────────────────────────────────────┘  
  
                        ┌──────────────────┐  
                        │  Nginx Reverse   │  
                        │  Proxy (HTTPS)   │  
                        │  Port: 443       │  
                        └────────┬─────────┘  
                                 │  
                ┌────────────────┼────────────────┐  
                │                │                │  
        ┌───────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐  
        │   Web UI     │  │  API Layer │  │   Admin    │  
        │  (React)     │  │  (FastAPI) │  │  Dashboard │  
        │  Port: 3000  │  │  Port: 8000│  │  Port: 9090│  
        └───────┬──────┘  └─────┬──────┘  └─────┬──────┘  
                │                │                │  
                └────────────────┼────────────────┘  
                                 │  
                    ┌────────────▼───────────────┐  
                    │   Dify Workflow Engine     │  
                    │   - Agent Orchestration    │  
                    │   - Prompt Management      │  
                    │   - Tool Integration       │  
                    │   Port: 5001               │  
                    └────────────┬───────────────┘  
                                 │  
                ┌────────────────┼────────────────┐  
                │                │                │  
        ┌───────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐  
        │   vLLM GPU0-1│  │  vLLM GPU2 │  │  vLLM GPU3-4│  
        │  (Qwen-14B)  │  │ (Qwen-14B) │  │  (Qwen-7B)  │  
        │  Contract    │  │ Compliance │  │  Routing    │  
        │  Port: 8001  │  │ Port: 8002 │  │  Port: 8003 │  
        └──────────────┘  └────────────┘  └──────────────┘  
                  
                ┌─────────────────────────────┐  
                │   Embedding Service GPU5    │  
                │   (bge-large-en-v1.5)       │  
                │   Port: 8004                │  
                └────────────┬────────────────┘  
                             │  
                ┌────────────▼────────────────┐  
                │   Qdrant Vector Database    │  
                │   - Legal docs index        │  
                │   - Case law embeddings     │  
                │   Port: 6333                │  
                └─────────────────────────────┘  
                  
                ┌─────────────────────────────┐  
                │   PostgreSQL Database       │  
                │   - User accounts           │  
                │   - Audit logs              │  
                │   - Session management      │  
                │   Port: 5432                │  
                └─────────────────────────────┘  
  
                ┌─────────────────────────────┐  
                │   Encrypted Storage         │  
                │   /data/models   (1TB)      │  
                │   /data/documents (2TB)     │  
                │   /data/vectors  (500GB)    │  
                │   /data/backups  (500GB)    │  
                └─────────────────────────────┘  
## Directory Structure  
  
  
bash  
/opt/legal-ai-vault/  
├── docker-compose.yml              *# Main orchestration file*  
├── .env.production                 *# Environment variables (encrypted)*  
├── nginx/  
│   ├── nginx.conf                  *# Main Nginx config*  
│   ├── ssl/  
│   │   ├── server.crt              *# TLS certificate*  
│   │   └── server.key              *# TLS private key*  
│   └── conf.d/  
│       ├── api.conf                *# API routing rules*  
│       └── security.conf           *# Security headers*  
├── api/  
│   ├── Dockerfile  
│   ├── requirements.txt  
│   ├── main.py                     *# FastAPI application entry*  
│   ├── config.py                   *# Configuration management*  
│   ├── models/  
│   │   ├── user.py                 *# User model*  
│   │   ├── document.py             *# Document model*  
│   │   └── audit_log.py            *# Audit log model*  
│   ├── routers/  
│   │   ├── auth.py                 *# Authentication endpoints*  
│   │   ├── documents.py            *# Document management*  
│   │   ├── agents.py               *# Agent interaction*  
│   │   └── admin.py                *# Admin operations*  
│   ├── services/  
│   │   ├── inference.py            *# LLM inference service*  
│   │   ├── embedding.py            *# Embedding generation*  
│   │   ├── vector_store.py         *# Qdrant operations*  
│   │   ├── document_processor.py   *# PDF/DOCX parsing*  
│   │   └── audit.py                *# Audit logging*  
│   ├── agents/  
│   │   ├── base_agent.py           *# Base agent class*  
│   │   ├── contract_review.py      *# Contract review agent*  
│   │   ├── compliance.py           *# Compliance monitoring*  
│   │   ├── legal_research.py       *# Legal research agent*  
│   │   └── document_router.py      *# Document classification*  
│   └── security/  
│       ├── auth.py                 *# JWT authentication*  
│       ├── rbac.py                 *# Role-based access control*  
│       └── encryption.py           *# Data encryption utilities*  
├── frontend/  
│   ├── Dockerfile  
│   ├── package.json  
│   ├── tsconfig.json  
│   ├── src/  
│   │   ├── App.tsx  
│   │   ├── components/  
│   │   │   ├── DocumentUpload.tsx  
│   │   │   ├── ChatInterface.tsx  
│   │   │   ├── AgentSelector.tsx  
│   │   │   └── AuditViewer.tsx  
│   │   ├── pages/  
│   │   │   ├── Dashboard.tsx  
│   │   │   ├── ContractReview.tsx  
│   │   │   ├── Compliance.tsx  
│   │   │   └── Admin.tsx  
│   │   ├── services/  
│   │   │   └── api.ts              *# API client*  
│   │   └── hooks/  
│   │       ├── useAuth.ts  
│   │       └── useAgent.ts  
│   └── public/  
│       └── index.html  
├── dify/  
│   ├── docker-compose.dify.yml     *# Dify-specific services*  
│   └── config/  
│       └── config.yaml             *# Dify configuration*  
├── vllm/  
│   ├── docker-compose.vllm.yml     *# vLLM services*  
│   ├── launch_gpu0_1.sh            *# Contract review (14B)*  
│   ├── launch_gpu2.sh              *# Compliance (14B)*  
│   ├── launch_gpu3_4.sh            *# Routing (7B)*  
│   └── launch_gpu5.sh              *# Embeddings*  
├── scripts/  
│   ├── init_database.py            *# Database initialization*  
│   ├── create_admin.py             *# Create admin user*  
│   ├── backup.sh                   *# Automated backup script*  
│   ├── health_check.sh             *# System health monitoring*  
│   └── update_models.py            *# Model update utility*  
├── monitoring/  
│   ├── prometheus.yml              *# Prometheus config*  
│   ├── grafana/  
│   │   └── dashboards/  
│   │       ├── gpu_metrics.json  
│   │       └── api_performance.json  
│   └── alerts/  
│       └── alert_rules.yml  
└── docs/  
    ├── API.md                      *# API documentation*  
    ├── DEPLOYMENT.md               *# Deployment guide*  
    ├── TROUBLESHOOTING.md          *# Common issues*  
    └── USER_GUIDE.md               *# End-user manual*  
## Docker Compose Configuration  
  
  
yaml  
*# docker-compose.yml*  
version: '3.8'  
  
services:  
  *# PostgreSQL Database*  
  postgres:  
    image: postgres:15-alpine  
    container_name: legal-ai-postgres  
    environment:  
      POSTGRES_DB: legal_ai_vault  
      POSTGRES_USER: ${DB_USER}  
      POSTGRES_PASSWORD: ${DB_PASSWORD}  
    volumes:  
      - postgres_data:/var/lib/postgresql/data  
    ports:  
      - "127.0.0.1:5432:5432"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# Qdrant Vector Database*  
  qdrant:  
    image: qdrant/qdrant:v1.8.0  
    container_name: legal-ai-qdrant  
    volumes:  
      - qdrant_data:/qdrant/storage  
    ports:  
      - "127.0.0.1:6333:6333"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# vLLM Contract Review (GPU 0-1)*  
  vllm-contract:  
    image: vllm/vllm-openai:latest  
    container_name: vllm-contract-review  
    runtime: nvidia  
    environment:  
      NVIDIA_VISIBLE_DEVICES: "0,1"  
      VLLM_TENSOR_PARALLEL_SIZE: 2  
    command: >  
      --model /models/qwen2.5-14b-instruct  
      --port 8001  
      --tensor-parallel-size 2  
      --max-model-len 32768  
      --gpu-memory-utilization 0.95  
      --disable-log-requests  
    volumes:  
      - /data/models:/models:ro  
    ports:  
      - "127.0.0.1:8001:8001"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
    deploy:  
      resources:  
        reservations:  
          devices:  
            - driver: nvidia  
              device_ids: ['0', '1']  
              capabilities: [gpu]  
  
  *# vLLM Compliance (GPU 2)*  
  vllm-compliance:  
    image: vllm/vllm-openai:latest  
    container_name: vllm-compliance  
    runtime: nvidia  
    environment:  
      NVIDIA_VISIBLE_DEVICES: "2"  
    command: >  
      --model /models/qwen2.5-14b-instruct  
      --port 8002  
      --max-model-len 32768  
      --gpu-memory-utilization 0.95  
      --disable-log-requests  
    volumes:  
      - /data/models:/models:ro  
    ports:  
      - "127.0.0.1:8002:8002"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
    deploy:  
      resources:  
        reservations:  
          devices:  
            - driver: nvidia  
              device_ids: ['2']  
              capabilities: [gpu]  
  
  *# vLLM Router (GPU 3-4)*  
  vllm-router:  
    image: vllm/vllm-openai:latest  
    container_name: vllm-router  
    runtime: nvidia  
    environment:  
      NVIDIA_VISIBLE_DEVICES: "3,4"  
      VLLM_TENSOR_PARALLEL_SIZE: 2  
    command: >  
      --model /models/qwen2.5-7b-instruct  
      --port 8003  
      --tensor-parallel-size 2  
      --max-model-len 16384  
      --gpu-memory-utilization 0.90  
    volumes:  
      - /data/models:/models:ro  
    ports:  
      - "127.0.0.1:8003:8003"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
    deploy:  
      resources:  
        reservations:  
          devices:  
            - driver: nvidia  
              device_ids: ['3', '4']  
              capabilities: [gpu]  
  
  *# Embedding Service (GPU 5)*  
  embedding-service:  
    build: ./api  
    container_name: embedding-service  
    runtime: nvidia  
    environment:  
      NVIDIA_VISIBLE_DEVICES: "5"  
      MODEL_PATH: /models/bge-large-en-v1.5  
      SERVICE_PORT: 8004  
    command: python embedding_server.py  
    volumes:  
      - /data/models:/models:ro  
    ports:  
      - "127.0.0.1:8004:8004"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
    deploy:  
      resources:  
        reservations:  
          devices:  
            - driver: nvidia  
              device_ids: ['5']  
              capabilities: [gpu]  
  
  *# FastAPI Backend*  
  api:  
    build: ./api  
    container_name: legal-ai-api  
    environment:  
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/legal_ai_vault  
      QDRANT_HOST: qdrant  
      QDRANT_PORT: 6333  
      VLLM_CONTRACT_URL: http://vllm-contract:8001/v1  
      VLLM_COMPLIANCE_URL: http://vllm-compliance:8002/v1  
      VLLM_ROUTER_URL: http://vllm-router:8003/v1  
      EMBEDDING_URL: http://embedding-service:8004  
      JWT_SECRET: ${JWT_SECRET}  
      ENCRYPTION_KEY: ${ENCRYPTION_KEY}  
    volumes:  
      - /data/documents:/app/documents  
      - /var/log/legal-ai:/app/logs  
    ports:  
      - "127.0.0.1:8000:8000"  
    depends_on:  
      - postgres  
      - qdrant  
      - vllm-contract  
      - vllm-compliance  
      - vllm-router  
      - embedding-service  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# React Frontend*  
  frontend:  
    build: ./frontend  
    container_name: legal-ai-frontend  
    environment:  
      REACT_APP_API_URL: https://legal-ai.client.internal  
    ports:  
      - "127.0.0.1:3000:3000"  
    depends_on:  
      - api  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# Nginx Reverse Proxy*  
  nginx:  
    image: nginx:1.24-alpine  
    container_name: legal-ai-nginx  
    volumes:  
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro  
      - ./nginx/conf.d:/etc/nginx/conf.d:ro  
      - ./nginx/ssl:/etc/nginx/ssl:ro  
    ports:  
      - "443:443"  
      - "80:80"  
    depends_on:  
      - frontend  
      - api  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# Prometheus Monitoring*  
  prometheus:  
    image: prom/prometheus:latest  
    container_name: legal-ai-prometheus  
    volumes:  
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro  
      - prometheus_data:/prometheus  
    ports:  
      - "127.0.0.1:9091:9090"  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
  *# Grafana Dashboards*  
  grafana:  
    image: grafana/grafana:latest  
    container_name: legal-ai-grafana  
    environment:  
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}  
      GF_USERS_ALLOW_SIGN_UP: false  
    volumes:  
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro  
      - grafana_data:/var/lib/grafana  
    ports:  
      - "127.0.0.1:3001:3000"  
    depends_on:  
      - prometheus  
    restart: unless-stopped  
    networks:  
      - legal-ai-network  
  
volumes:  
  postgres_data:  
    driver: local  
  qdrant_data:  
    driver: local  
  prometheus_data:  
    driver: local  
  grafana_data:  
    driver: local  
  
networks:  
  legal-ai-network:  
    driver: bridge  
## FastAPI Backend - Core Files  
**api/main.py**  
  
  
python  
"""  
Legal AI Vault - Main FastAPI Application  
On-premises AI inference for legal/financial workflows  
"""  
  
from fastapi import FastAPI, Request, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import JSONResponse  
import logging  
from datetime import datetime  
import sys  
  
from config import settings  
from routers import auth, documents, agents, admin  
from services.audit import AuditService  
from database import engine, Base  
  
*# Configure logging*  
logging.basicConfig(  
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[  
        logging.FileHandler('/app/logs/api.log'),  
        logging.StreamHandler(sys.stdout)  
    ]  
)  
logger = logging.getLogger(__name__)  
  
*# Initialize FastAPI app*  
app = FastAPI(  
    title="Legal AI Vault API",  
    description="On-premises AI inference for legal workflows",  
    version="1.0.0",  
    docs_url="/api/docs",  *# Swagger UI*  
    redoc_url="/api/redoc"  *# ReDoc*  
)  
  
*# CORS configuration (strict internal network only)*  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=settings.ALLOWED_ORIGINS,  *# Internal IPs only*  
    allow_credentials=True,  
    allow_methods=["GET", "POST", "PUT", "DELETE"],  
    allow_headers=["*"],  
)  
  
*# Initialize database*  
@app.on_event("startup")  
async def startup_event():  
    """Initialize database and services on startup"""  
    logger.info("Starting Legal AI Vault API...")  
      
    *# Create database tables*  
    Base.metadata.create_all(bind=engine)  
    logger.info("Database tables initialized")  
      
    *# Initialize audit service*  
    AuditService.initialize()  
    logger.info("Audit service initialized")  
      
    *# Health check for GPU services*  
    from services.inference import InferenceService  
    inference = InferenceService()  
    health = await inference.health_check()  
    logger.info(f"GPU Services Health: {health}")  
  
@app.on_event("shutdown")  
async def shutdown_event():  
    """Cleanup on shutdown"""  
    logger.info("Shutting down Legal AI Vault API...")  
  
*# Request logging middleware*  
@app.middleware("http")  
async def log_requests(request: Request, call_next):  
    """Log all API requests for audit purposes"""  
    start_time = datetime.utcnow()  
      
    *# Process request*  
    response = await call_next(request)  
      
    *# Calculate duration*  
    duration = (datetime.utcnow() - start_time).total_seconds()  
      
    *# Log request*  
    logger.info(  
        f"{request.method} {request.url.path} "  
        f"Status: {response.status_code} "  
        f"Duration: {duration:.3f}s "  
        f"Client: {request.client.host}"  
    )  
      
    return response  
  
*# Global exception handler*  
@app.exception_handler(Exception)  
async def global_exception_handler(request: Request, exc: Exception):  
    """Handle unexpected errors"""  
    logger.error(f"Unhandled exception: {exc}", exc_info=True)  
      
    return JSONResponse(  
        status_code=500,  
        content={  
            "error": "Internal server error",  
            "message": "An unexpected error occurred. Please contact support.",  
            "timestamp": datetime.utcnow().isoformat()  
        }  
    )  
  
*# Include routers*  
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])  
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])  
app.include_router(agents.router, prefix="/api/agents", tags=["AI Agents"])  
app.include_router(admin.router, prefix="/api/admin", tags=["Administration"])  
  
*# Health check endpoint*  
@app.get("/health")  
async def health_check():  
    """System health check"""  
    return {  
        "status": "healthy",  
        "timestamp": datetime.utcnow().isoformat(),  
        "version": "1.0.0"  
    }  
  
*# Root endpoint*  
@app.get("/")  
async def root():  
    """API root information"""  
    return {  
        "name": "Legal AI Vault API",  
        "version": "1.0.0",  
        "docs": "/api/docs",  
        "deployment": "on-premises"  
    }  
  
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(  
        "main:app",  
        host="0.0.0.0",  
        port=8000,  
        log_level="info",  
        access_log=True  
    )  
**api/config.py**  
  
  
python  
"""  
Configuration Management  
Loads settings from environment variables  
"""  
  
from pydantic_settings import BaseSettings  
from typing import List  
import os  
  
class Settings(BaseSettings):  
    *# Application*  
    APP_NAME: str = "Legal AI Vault"  
    VERSION: str = "1.0.0"  
    DEBUG: bool = False  
      
    *# Security*  
    JWT_SECRET: str  
    JWT_ALGORITHM: str = "HS256"  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  
    ENCRYPTION_KEY: str  
      
    *# Database*  
    DATABASE_URL: str  
      
    *# Vector Database*  
    QDRANT_HOST: str = "qdrant"  
    QDRANT_PORT: int = 6333  
      
    *# vLLM Endpoints*  
    VLLM_CONTRACT_URL: str  
    VLLM_COMPLIANCE_URL: str  
    VLLM_ROUTER_URL: str  
    EMBEDDING_URL: str  
      
    *# File Storage*  
    DOCUMENT_STORAGE_PATH: str = "/app/documents"  
    MAX_UPLOAD_SIZE_MB: int = 100  
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".doc", ".txt"]  
      
    *# CORS*  
    ALLOWED_ORIGINS: List[str] = [  
        "https://legal-ai.client.internal",  
        "http://localhost:3000"  *# For development only*  
    ]  
      
    *# Audit Logging*  
    AUDIT_LOG_PATH: str = "/app/logs/audit.log"  
    AUDIT_LOG_RETENTION_DAYS: int = 2555  *# 7 years*  
      
    *# Inference Settings*  
    DEFAULT_MAX_TOKENS: int = 4096  
    DEFAULT_TEMPERATURE: float = 0.3  
    INFERENCE_TIMEOUT_SECONDS: int = 120  
      
    class Config:  
        env_file = ".env.production"  
        case_sensitive = True  
  
settings = Settings()  
**api/services/inference.py**  
  
  
python  
"""  
Inference Service - Handles communication with vLLM endpoints  
"""  
  
import aiohttp  
import asyncio  
from typing import Dict, List, Optional  
import logging  
from datetime import datetime  
  
from config import settings  
from services.audit import AuditService  
  
logger = logging.getLogger(__name__)  
  
class InferenceService:  
    """Manages LLM inference requests across GPU services"""  
      
    def __init__(self):  
        self.endpoints = {  
            "contract_review": settings.VLLM_CONTRACT_URL,  
            "compliance": settings.VLLM_COMPLIANCE_URL,  
            "router": settings.VLLM_ROUTER_URL  
        }  
        self.audit = AuditService()  
      
    async def generate(  
        self,  
        prompt: str,  
        agent_type: str,  
        user_id: str,  
        max_tokens: int = None,  
        temperature: float = None,  
        system_prompt: Optional[str] = None  
    ) -> Dict:  
        """  
        Generate response from specified agent  
          
        Args:  
            prompt: User query  
            agent_type: One of "contract_review", "compliance", "router"  
            user_id: User identifier for audit logging  
            max_tokens: Maximum response length  
            temperature: Sampling temperature  
            system_prompt: Optional system instruction  
              
        Returns:  
            Dict with 'response', 'tokens_used', 'latency'  
        """  
          
        if agent_type not in self.endpoints:  
            raise ValueError(f"Unknown agent type: {agent_type}")  
          
        endpoint = self.endpoints[agent_type]  
        start_time = datetime.utcnow()  
          
        *# Prepare request payload (OpenAI-compatible format)*  
        payload = {  
            "model": agent_type,  
            "messages": [],  
            "max_tokens": max_tokens or settings.DEFAULT_MAX_TOKENS,  
            "temperature": temperature or settings.DEFAULT_TEMPERATURE,  
            "stream": False  
        }  
          
        *# Add system prompt if provided*  
        if system_prompt:  
            payload["messages"].append({  
                "role": "system",  
                "content": system_prompt  
            })  
          
        *# Add user prompt*  
        payload["messages"].append({  
            "role": "user",  
            "content": prompt  
        })  
          
        try:  
            async with aiohttp.ClientSession() as session:  
                async with session.post(  
                    f"{endpoint}/chat/completions",  
                    json=payload,  
                    timeout=aiohttp.ClientTimeout(total=settings.INFERENCE_TIMEOUT_SECONDS)  
                ) as response:  
                      
                    if response.status != 200:  
                        error_text = await response.text()  
                        logger.error(f"Inference error: {response.status} - {error_text}")  
                        raise Exception(f"Inference failed: {response.status}")  
                      
                    result = await response.json()  
                      
                    *# Extract response*  
                    response_text = result["choices"][0]["message"]["content"]  
                    tokens_used = result["usage"]["total_tokens"]  
                      
                    *# Calculate latency*  
                    latency = (datetime.utcnow() - start_time).total_seconds()  
                      
                    *# Audit log*  
                    await self.audit.log_inference(  
                        user_id=user_id,  
                        agent_type=agent_type,  
                        prompt=prompt,  
                        response=response_text,  
                        tokens_used=tokens_used,  
                        latency=latency  
                    )  
                      
                    logger.info(  
                        f"Inference complete - Agent: {agent_type}, "  
                        f"Tokens: {tokens_used}, Latency: {latency:.2f}s"  
                    )  
                      
                    return {  
                        "response": response_text,  
                        "tokens_used": tokens_used,  
                        "latency": latency,  
                        "agent": agent_type,  
                        "timestamp": start_time.isoformat()  
                    }  
          
        except asyncio.TimeoutError:  
            logger.error(f"Inference timeout for agent: {agent_type}")  
            raise Exception("Inference request timed out")  
          
        except Exception as e:  
            logger.error(f"Inference error: {e}", exc_info=True)  
            raise  
      
    async def health_check(self) -> Dict:  
        """Check health of all GPU services"""  
          
        health_status = {}  
          
        for agent_type, endpoint in self.endpoints.items():  
            try:  
                async with aiohttp.ClientSession() as session:  
                    async with session.get(  
                        f"{endpoint}/health",  
                        timeout=aiohttp.ClientTimeout(total=5)  
                    ) as response:  
                        health_status[agent_type] = {  
                            "status": "healthy" if response.status == 200 else "unhealthy",  
                            "endpoint": endpoint  
                        }  
            except Exception as e:  
                health_status[agent_type] = {  
                    "status": "unhealthy",  
                    "error": str(e),  
                    "endpoint": endpoint  
                }  
          
        return health_status  
**api/agents/contract_review.py**  
  
  
python  
"""  
Contract Review Agent  
Analyzes contracts for risks, obligations, and key terms  
"""  
  
from typing import Dict, List  
import logging  
from datetime import datetime  
  
from services.inference import InferenceService  
from services.document_processor import DocumentProcessor  
from services.vector_store import VectorStoreService  
  
logger = logging.getLogger(__name__)  
  
class ContractReviewAgent:  
    """AI Agent for contract analysis"""  
      
    SYSTEM_PROMPT = """You are an expert legal AI assistant specializing in contract review.   
Your role is to analyze contracts and identify:  
1. Key obligations and deadlines  
2. Potential legal risks or unfavorable terms  
3. Missing clauses or ambiguous language  
4. Recommended actions or clarifications  
  
Provide clear, structured analysis with specific clause references.  
Use professional legal terminology but remain accessible."""  
      
    def __init__(self):  
        self.inference = InferenceService()  
        self.doc_processor = DocumentProcessor()  
        self.vector_store = VectorStoreService()  
      
    async def analyze_contract(  
        self,  
        document_id: str,  
        user_id: str,  
        analysis_type: str = "comprehensive"  
    ) -> Dict:  
        """  
        Analyze a contract document  
          
        Args:  
            document_id: ID of uploaded document  
            user_id: User requesting analysis  
            analysis_type: "comprehensive" | "risk_only" | "obligations_only"  
              
        Returns:  
            Dict with analysis results  
        """  
          
        logger.info(f"Starting contract analysis - Doc: {document_id}, Type: {analysis_type}")  
          
        *# 1. Retrieve document text*  
        doc_text = await self.doc_processor.get_document_text(document_id)  
          
        *# 2. Check document length and chunk if necessary*  
        if len(doc_text) > 30000:  *# ~7500 tokens*  
            chunks = self.doc_processor.chunk_document(doc_text, chunk_size=20000)  
            logger.info(f"Document chunked into {len(chunks)} parts")  
        else:  
            chunks = [doc_text]  
          
        *# 3. Retrieve similar contract clauses from vector database (RAG)*  
        similar_clauses = await self.vector_store.search(  
            collection="legal_contracts",  
            query_text=doc_text[:1000],  *# Use first 1000 chars for similarity*  
            limit=3  
        )  
          
        *# 4. Build analysis prompt*  
        prompt = self._build_analysis_prompt(  
            document_text=chunks[0],  *# Start with first chunk*  
            analysis_type=analysis_type,  
            similar_clauses=similar_clauses  
        )  
          
        *# 5. Run inference*  
        result = await self.inference.generate(  
            prompt=prompt,  
            agent_type="contract_review",  
            user_id=user_id,  
            system_prompt=self.SYSTEM_PROMPT,  
            max_tokens=4096,  
            temperature=0.2  *# Low temperature for consistency*  
        )  
          
        *# 6. Structure results*  
        analysis = {  
            "document_id": document_id,  
            "analysis_type": analysis_type,  
            "analysis": result["response"],  
            "tokens_used": result["tokens_used"],  
            "latency": result["latency"],  
            "timestamp": result["timestamp"],  
            "chunks_analyzed": len(chunks),  
            "rag_sources": len(similar_clauses)  
        }  
          
        *# 7. If multi-chunk, analyze remaining chunks*  
        if len(chunks) > 1:  
            additional_analyses = []  
            for i, chunk in enumerate(chunks[1:], start=2):  
                logger.info(f"Analyzing chunk {i}/{len(chunks)}")  
                chunk_result = await self._analyze_chunk(chunk, user_id)  
                additional_analyses.append(chunk_result)  
              
            analysis["additional_sections"] = additional_analyses  
          
        logger.info(f"Contract analysis complete - Doc: {document_id}")  
        return analysis  
      
    def _build_analysis_prompt(  
        self,  
        document_text: str,  
        analysis_type: str,  
        similar_clauses: List[Dict]  
    ) -> str:  
        """Build the analysis prompt with context"""  
          
        prompt_parts = []  
          
        *# Add RAG context if available*  
        if similar_clauses:  
            prompt_parts.append("### Reference Clauses (from similar contracts):")  
            for i, clause in enumerate(similar_clauses, 1):  
                prompt_parts.append(f"\n**Reference {i}:**\n{clause['text']}\n")  
          
        *# Add main document*  
        prompt_parts.append("### Contract to Analyze:")  
        prompt_parts.append(document_text)  
          
        *# Add specific instructions based on analysis type*  
        if analysis_type == "risk_only":  
            prompt_parts.append("\n### Focus your analysis on identifying legal risks and unfavorable terms.")  
        elif analysis_type == "obligations_only":  
            prompt_parts.append("\n### Focus your analysis on listing all obligations and deadlines.")  
        else:  
            prompt_parts.append("\n### Provide a comprehensive analysis covering risks, obligations, and recommendations.")  
          
        return "\n".join(prompt_parts)  
      
    async def _analyze_chunk(self, chunk: str, user_id: str) -> Dict:  
        """Analyze a single document chunk"""  
          
        result = await self.inference.generate(  
            prompt=f"Continue analyzing this contract section:\n\n{chunk}",  
            agent_type="contract_review",  
            user_id=user_id,  
            system_prompt=self.SYSTEM_PROMPT,  
            max_tokens=2048,  
            temperature=0.2  
        )  
          
        return {  
            "analysis": result["response"],  
            "tokens_used": result["tokens_used"]  
        }  
      
    async def compare_contracts(  
        self,  
        document_id_1: str,  
        document_id_2: str,  
        user_id: str  
    ) -> Dict:  
        """Compare two contracts and highlight differences"""  
          
        logger.info(f"Comparing contracts: {document_id_1} vs {document_id_2}")  
          
        *# Retrieve both documents*  
        doc1_text = await self.doc_processor.get_document_text(document_id_1)  
        doc2_text = await self.doc_processor.get_document_text(document_id_2)  
          
        *# Build comparison prompt*  
        prompt = f"""Compare these two contracts and identify:  
1. Key differences in terms and conditions  
2. Differences in obligations or liabilities  
3. Which contract is more favorable and why  
  
### Contract A:  
{doc1_text[:15000]}  
  
### Contract B:  
{doc2_text[:15000]}  
  
Provide a detailed comparison with specific clause references."""  
          
        result = await self.inference.generate(  
            prompt=prompt,  
            agent_type="contract_review",  
            user_id=user_id,  
            system_prompt=self.SYSTEM_PROMPT,  
            max_tokens=4096,  
            temperature=0.3  
        )  
          
        return {  
            "document_1": document_id_1,  
            "document_2": document_id_2,  
            "comparison": result["response"],  
            "tokens_used": result["tokens_used"],  
            "timestamp": result["timestamp"]  
        }  
## Database Models  
**api/models/document.py**  
  
  
python  
"""  
Document Model - Represents uploaded legal documents  
"""  
  
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Boolean, BigInteger  
from sqlalchemy.orm import relationship  
from datetime import datetime  
import uuid  
  
from database import Base  
  
class Document(Base):  
    __tablename__ = "documents"  
      
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  
    filename = Column(String, nullable=False)  
    original_filename = Column(String, nullable=False)  
    file_size_bytes = Column(BigInteger, nullable=False)  
    file_type = Column(String, nullable=False)  *# .pdf, .docx, etc.*  
    mime_type = Column(String)  
      
    *# Storage*  
    storage_path = Column(String, nullable=False)  
    encrypted = Column(Boolean, default=True)  
      
    *# Metadata*  
    uploaded_by = Column(String, ForeignKey("users.id"), nullable=False)  
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)  
      
    *# Document classification*  
    document_type = Column(String)  *# "contract", "brief", "correspondence", etc.*  
    category = Column(String)       *# "M&A", "employment", "real_estate", etc.*  
      
    *# Processing status*  
    processed = Column(Boolean, default=False)  
    text_extracted = Column(Boolean, default=False)  
    vectorized = Column(Boolean, default=False)  
      
    *# Extracted content*  
    text_content = Column(Text)     *# Full text extraction*  
    page_count = Column(Integer)  
    word_count = Column(Integer)  
      
    *# Vector database reference*  
    vector_collection = Column(String)  
    vector_id = Column(String)  
      
    *# Relationships*  
    user = relationship("User", back_populates="documents")  
    analyses = relationship("Analysis", back_populates="document", cascade="all, delete-orphan")  
      
    def __repr__(self):  
        return f"<Document(id={self.id}, filename={self.filename})>"  
**api/models/audit_log.py**  
  
  
python  
"""  
Audit Log Model - Comprehensive logging for compliance  
"""  
  
from sqlalchemy import Column, String, DateTime, Integer, Text, Float  
from datetime import datetime  
import uuid  
  
from database import Base  
  
class AuditLog(Base):  
    __tablename__ = "audit_logs"  
      
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  
      
    *# User information*  
    user_id = Column(String, nullable=False, index=True)  
    user_email = Column(String)  
    user_role = Column(String)  
    client_ip = Column(String)  
      
    *# Action details*  
    action_type = Column(String, nullable=False)  *# "inference", "document_upload", "login", etc.*  
    resource_type = Column(String)                *# "document", "agent", "user", etc.*  
    resource_id = Column(String)  
      
    *# AI-specific fields*  
    agent_type = Column(String)                   *# "contract_review", "compliance", etc.*  
    prompt_hash = Column(String)                  *# SHA-256 hash of user prompt*  
    response_hash = Column(String)                *# SHA-256 hash of AI response*  
    tokens_used = Column(Integer)  
    inference_latency = Column(Float)             *# Seconds*  
      
    *# Additional context*  
    metadata = Column(Text)                       *# JSON string for extra data*  
    status = Column(String)                       *# "success", "error", "warning"*  
    error_message = Column(Text)  
      
    *# Retention (for automated cleanup)*  
    retention_until = Column(DateTime)            *# Auto-calculated: timestamp + 7 years*  
      
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)  
        *# Auto-calculate retention date (7 years for legal compliance)*  
        if not self.retention_until:  
            from datetime import timedelta  
            self.retention_until = self.timestamp + timedelta(days=2555)  
      
    def __repr__(self):  
        return f"<AuditLog(id={self.id}, action={self.action_type}, user={self.user_id})>"  
  
