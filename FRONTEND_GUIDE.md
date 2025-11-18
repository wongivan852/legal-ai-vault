# 🎨 Frontend UI Testing Guide

Your Legal AI Vault now has a beautiful, modern web interface for testing!

## 🚀 Quick Access

**Frontend URL**: http://localhost:8000

The browser should have automatically opened. If not, click the link above.

## ✨ Features Overview

### 1. **Text Generation Tab** (Default)
Generate AI responses to legal questions using your local LLM.

**How to Use:**
1. Enter your legal question in the "Legal Query" field
2. (Optional) Add a system prompt like "You are a Hong Kong legal expert"
3. Adjust settings:
   - **Max Tokens**: 50-4096 (default: 500)
   - **Temperature**: 0-1 (default: 0.3, lower = more precise)
4. Click "Generate Response"
5. View AI response with performance metrics

**Example Questions:**
```
✓ What are the essential elements of a valid employment contract in Hong Kong?
✓ Explain the notice period requirements under Hong Kong Employment Ordinance
✓ What remedies are available for breach of contract?
✓ How does the Sale of Goods Ordinance protect consumers?
```

### 2. **Embeddings Tab**
Generate vector embeddings for semantic search and document similarity.

**How to Use:**
1. Switch to "Embeddings" tab
2. Enter text to convert to vectors
3. Click "Generate Embeddings"
4. View:
   - Vector dimensions (768)
   - Preview of embedding values
   - Model used

**Use Cases:**
- Test document similarity
- Prepare for semantic search
- Understand vector representations

### 3. **Models Tab**
View all available Ollama models on your system.

**How to Use:**
1. Switch to "Models" tab
2. Click "🔄 Refresh Models"
3. View model cards showing:
   - Size (in GB)
   - Parameter count
   - Quantization level
   - Active status (LLM/Embedding)
   - Last modified date

### 4. **Documentation Tab**
Quick reference for API endpoints and examples.

**Features:**
- API endpoint descriptions
- Request/response examples
- Links to interactive docs
- Quick access to Qdrant dashboard

## 📊 What You'll See

### Header
- **System Status Indicator**:
  - 🟢 Green = Healthy
  - 🔴 Red = Unhealthy
- Current active model
- API version

### Response Display
After generating text, you'll see:
- **AI Response**: Full generated text
- **Model Used**: Which LLM generated the response
- **Statistics**:
  - Duration (seconds)
  - Prompt tokens
  - Completion tokens
  - Tokens/second (generation speed)

## 🎯 Testing Checklist

### ✅ Basic Tests

1. **Health Check**
   - Header should show "System Healthy" with green dot
   - Current model should show "llama3.1:8b"

2. **Text Generation Test**
   ```
   Prompt: "Explain contract law in Hong Kong in 2 sentences"
   Expected: Clear, concise legal explanation
   Time: ~10-20 seconds
   ```

3. **Embeddings Test**
   ```
   Text: "employment contract termination notice"
   Expected: 768-dimensional vector
   Time: ~1-2 seconds
   ```

4. **Models List Test**
   - Should show 6 models
   - llama3.1:8b marked as "ACTIVE LLM"
   - nomic-embed-text marked as "ACTIVE EMBEDDING"

### 🧪 Advanced Tests

1. **Temperature Comparison**
   - Try same question with temperature 0.1 (precise)
   - Try again with temperature 0.9 (creative)
   - Compare responses

2. **Token Limit Test**
   - Set max_tokens to 50 (short response)
   - Set max_tokens to 500 (detailed response)
   - Observe difference

3. **System Prompt Test**
   ```
   System: "You are a contract law expert. Be extremely concise."
   Query: "What makes a contract valid?"
   Expected: Very brief, focused answer
   ```

## 🎨 UI Features

### Modern Design
- **Gradient Background**: Purple gradient for visual appeal
- **Clean Panels**: White cards with shadows
- **Smooth Animations**: Fade-in effects, hover states
- **Responsive**: Works on desktop, tablet, mobile

### Interactive Elements
- **Tab Navigation**: Switch between features
- **Loading States**: Spinners during API calls
- **Auto-scroll**: Results scroll into view
- **Form Validation**: Required fields marked
- **Clear Buttons**: Reset forms easily

### Color Coding
- **Blue**: Primary actions, links
- **Green**: Success, healthy status
- **Gray**: Secondary actions
- **Purple**: Background gradient

## 📱 Mobile Friendly

The UI is fully responsive:
- Stacked layout on small screens
- Touch-optimized buttons
- Readable fonts
- Smooth scrolling

## 🔧 Technical Details

### Files Created
```
frontend/
├── index.html                  # Main UI structure
├── static/
│   ├── css/
│   │   └── style.css          # Modern styling (3KB)
│   └── js/
│       └── app.js             # API integration (7KB)
└── README.md                   # Detailed documentation
```

### Technology Stack
- **Pure HTML/CSS/JavaScript**: No frameworks needed
- **Google Fonts**: Inter typeface
- **REST API**: JSON communication
- **ES6+**: Modern JavaScript features

### How It Works
1. Frontend served from FastAPI at `http://localhost:8000/`
2. JavaScript calls API endpoints (`/api/generate`, `/api/embed`, etc.)
3. Results displayed in real-time
4. Health check runs every 30 seconds

## 🌐 Additional URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:8000 | This testing UI |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger docs |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Qdrant** | http://localhost:6333/dashboard | Vector database UI |
| **Health** | http://localhost:8000/health | System health JSON |

## 💡 Tips & Tricks

### 1. Faster Responses
- Use lower max_tokens (100-300) for testing
- First request is slower (model loading)
- Subsequent requests are much faster

### 2. Better Prompts
```
Good: "What are the 3 main types of contracts in HK law?"
Better: "List and briefly explain the 3 main types of contracts
         recognized under Hong Kong contract law, with examples."
```

### 3. System Prompts
```
General: "You are a legal expert"
Specific: "You are a Hong Kong barrister specializing in
           employment law. Cite relevant ordinances."
```

### 4. Temperature Guide
- **0.0-0.3**: Factual, precise (good for legal)
- **0.4-0.6**: Balanced
- **0.7-1.0**: Creative, varied

## 🐛 Troubleshooting

### Frontend Won't Load
```bash
# Check if API is running
curl http://localhost:8000/health

# Restart if needed
cd ~/Apps/legal-ai-vault
docker-compose restart api
```

### API Calls Failing
- Check browser console (F12)
- Verify backend is healthy (green status dot)
- Look for error messages in response

### Slow Generation
- Normal for first request (model loading)
- Reduce max_tokens
- Check Docker has enough memory (7+ GB)

### Model Not Found
```bash
# List available models
curl http://localhost:8000/api/models

# Check .env file
cat ~/Apps/legal-ai-vault/.env | grep OLLAMA_MODEL
```

## 📈 Performance Expectations

### llama3.1:8b (Current Model)
- **First request**: 20-30 seconds (model loading)
- **Subsequent**: 10-20 seconds
- **Tokens/sec**: 10-15 tokens/sec
- **Quality**: Excellent for legal questions

### Memory Usage
- **Model**: ~5 GB
- **Docker**: ~7.7 GB total
- **Browser**: Minimal

## 🚀 Next Steps

1. **Test All Features**: Try each tab
2. **Experiment**: Different prompts, temperatures
3. **Check Docs**: Visit http://localhost:8000/docs
4. **Import Data**: See `HK_LEGAL_DATA_INTEGRATION.md` (optional)
5. **Upgrade Model**: Increase Docker memory for llama3.3:70b

## 📚 Documentation

- **Frontend Details**: `frontend/README.md`
- **API Guide**: http://localhost:8000/docs
- **Setup Guide**: `QUICKSTART.md`
- **Main README**: `README.md`

## 🎉 Enjoy Your Legal AI Vault!

You now have a fully functional, beautiful testing interface for your on-premises legal AI system!

**Quick Test**:
1. Open http://localhost:8000
2. Enter: "What is contract law?"
3. Click "Generate Response"
4. Watch your local AI work! ⚖️🤖

---

**Need Help?**
- Check browser console (F12)
- View API logs: `docker-compose logs -f api`
- Check backend: `docker-compose ps`
