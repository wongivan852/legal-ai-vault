#!/bin/bash
# Development Startup Script for Vault AI Platform
# Uses simplified configuration without GPU requirements

set -e

echo "🚀 Starting Vault AI Platform (Development Mode)"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo "Please start Docker Desktop or the Docker daemon"
    exit 1
fi

# Check if .env exists, if not use development defaults
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Using development defaults...${NC}"
    cp .env.development .env
    echo -e "${GREEN}✓ Created .env from .env.development${NC}"
fi

echo -e "${GREEN}Starting services with docker-compose.dev.yml...${NC}"
echo ""

# Stop any existing containers
docker compose -f docker-compose.dev.yml down 2>/dev/null || true

# Start services
docker compose -f docker-compose.dev.yml up -d

# Wait for services
echo ""
echo "Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo -e "${GREEN}Checking service health...${NC}"
echo ""

# Check Ollama
echo -n "Ollama (LLM Service): "
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Starting up...${NC}"
fi

# Check PostgreSQL
echo -n "PostgreSQL (Database): "
if docker compose -f docker-compose.dev.yml exec -T postgres pg_isready -U legal_vault_user > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Starting up...${NC}"
fi

# Check Qdrant
echo -n "Qdrant (Vector DB): "
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Starting up...${NC}"
fi

# Check API
echo -n "API (FastAPI Backend): "
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Starting up (may take 30-60s)...${NC}"
fi

# Display access info
echo ""
echo "================================"
echo -e "${GREEN}✅ Development Environment Started!${NC}"
echo "================================"
echo ""
echo "📍 Access Points:"
echo "  🌐 Web UI:       http://localhost:8000"
echo "  📖 API Docs:     http://localhost:8000/docs"
echo "  💚 Health Check: http://localhost:8000/health"
echo "  🤖 Ollama:       http://localhost:11434"
echo "  🔍 Qdrant:       http://localhost:6333/dashboard"
echo ""
echo "📊 Management Commands:"
echo "  View logs:       docker compose -f docker-compose.dev.yml logs -f"
echo "  Stop services:   docker compose -f docker-compose.dev.yml down"
echo "  Restart:         docker compose -f docker-compose.dev.yml restart"
echo "  Check status:    docker compose -f docker-compose.dev.yml ps"
echo ""
echo "⚙️  First-time setup:"
echo "  1. Pull the LLM model (small 8B version for dev):"
echo "     docker compose -f docker-compose.dev.yml exec ollama ollama pull llama3.1:8b"
echo "  2. Pull embedding model:"
echo "     docker compose -f docker-compose.dev.yml exec ollama ollama pull nomic-embed-text"
echo ""
echo "🧪 Test API:"
echo "  curl http://localhost:8000/api/agents/"
echo ""
