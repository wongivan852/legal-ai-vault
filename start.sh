#!/bin/bash
# Quick start script for Legal AI Vault

set -e

echo "🚀 Starting Legal AI Vault"
echo "Using your llama3.3:70b model from ~/.ollama"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your settings!${NC}"
    echo ""
    echo "Generate secure keys with:"
    echo "  openssl rand -hex 32"
    echo ""
    read -p "Press Enter to continue after editing .env, or Ctrl+C to exit..."
fi

# Start services
echo -e "${GREEN}Starting Docker services...${NC}"
docker-compose up -d

# Wait for services
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check health
echo ""
echo -e "${GREEN}Checking service health...${NC}"

# Check Ollama
echo -n "Ollama: "
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Not ready yet${NC}"
fi

# Check PostgreSQL
echo -n "PostgreSQL: "
if docker-compose exec -T postgres pg_isready -U legal_vault_user > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Not ready yet${NC}"
fi

# Check Qdrant
echo -n "Qdrant: "
if curl -s http://localhost:6333/health > /dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Not ready yet${NC}"
fi

# Check API
echo -n "API: "
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠️  Not ready yet (may need 30-60s)${NC}"
fi

# Display access info
echo ""
echo "================================"
echo -e "${GREEN}✅ Services Started!${NC}"
echo "================================"
echo ""
echo "Access points:"
echo "  📖 API Docs: http://localhost:8000/docs"
echo "  💚 Health Check: http://localhost:8000/health"
echo "  🤖 Ollama: http://localhost:11434"
echo "  🔍 Qdrant: http://localhost:6333/dashboard"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Test generation:"
echo '  curl -X POST http://localhost:8000/api/generate \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"prompt": "Explain contract law", "max_tokens": 200}'"'"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
