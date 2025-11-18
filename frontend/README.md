# Legal AI Vault - Frontend UI

A modern, responsive web interface for testing and interacting with your Legal AI Vault.

## Features

### 📝 Text Generation
- Ask legal questions and get AI-powered responses
- Customize system prompts for specialized legal contexts
- Adjust temperature and max tokens for response control
- View generation statistics (duration, tokens, speed)

### 🔢 Embeddings
- Generate vector embeddings for legal text
- View embedding dimensions and preview vectors
- Perfect for testing semantic search capabilities

### 🤖 Models
- View all available Ollama models
- See which models are currently active
- Display model size, parameters, and quantization info

### 📖 Documentation
- Quick reference for API endpoints
- Code examples and request formats
- Links to interactive API docs

## Access

The frontend is served directly from the FastAPI backend:

```
http://localhost:8000/
```

**Additional URLs:**
- Interactive API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Qdrant Dashboard: http://localhost:6333/dashboard

## Usage

### 1. Text Generation

1. Navigate to the "Text Generation" tab (default)
2. Optionally add a system prompt (e.g., "You are a Hong Kong legal expert")
3. Enter your legal query
4. Adjust parameters:
   - **Max Tokens**: Maximum length of response (50-4096)
   - **Temperature**: Creativity level (0 = precise, 1 = creative)
5. Click "Generate Response"
6. View the AI response with performance stats

**Example Queries:**
```
- What are the essential elements of a contract in Hong Kong?
- Explain the notice period requirements for employment termination
- What is the difference between common law and equity?
- How does the Sale of Goods Ordinance protect consumers?
```

### 2. Embeddings

1. Navigate to the "Embeddings" tab
2. Enter text you want to convert to a vector
3. Click "Generate Embeddings"
4. View:
   - Vector dimensions (typically 768)
   - Preview of first 50 values
   - Model used for generation

**Use Cases:**
- Test document similarity
- Prepare for semantic search
- Understand embedding quality

### 3. Models

1. Navigate to the "Models" tab
2. Click "Refresh Models"
3. View all available models with:
   - Size in GB
   - Parameter count
   - Quantization level
   - Last modified date
   - Active status (LLM or Embedding)

## Architecture

```
frontend/
├── index.html          # Main HTML structure
├── static/
│   ├── css/
│   │   └── style.css   # Modern UI styling
│   └── js/
│       └── app.js      # API integration & UI logic
└── README.md           # This file
```

## Technology Stack

- **HTML5**: Semantic, accessible markup
- **CSS3**: Modern design with CSS variables, grid, flexbox
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Google Fonts**: Inter font family
- **REST API**: FastAPI backend integration

## API Integration

The frontend communicates with the backend via these endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check |
| `/api/generate` | POST | Text generation |
| `/api/embed` | POST | Generate embeddings |
| `/api/models` | GET | List available models |

All API calls use `fetch()` with JSON payloads.

## Design Highlights

### Color Scheme
- **Primary**: Blue (#2563eb) for actions and highlights
- **Success**: Green (#10b981) for healthy status
- **Background**: Gradient purple backdrop
- **Content**: Clean white panels

### Responsive Design
- Mobile-friendly layout
- Touch-optimized buttons
- Adaptive grid for model cards
- Smooth animations and transitions

### UX Features
- Real-time health status indicator
- Loading states with spinners
- Smooth tab transitions
- Auto-scroll to results
- Form validation
- Clear error messages

## Customization

### Change API URL

Edit `frontend/static/js/app.js`:

```javascript
const API_BASE_URL = 'http://your-server:8000';
```

### Modify Colors

Edit `frontend/static/css/style.css`:

```css
:root {
    --primary-color: #2563eb;  /* Change to your brand color */
    --primary-dark: #1d4ed8;
    /* ... other variables ... */
}
```

### Add New Features

1. Add HTML in `index.html`
2. Style in `static/css/style.css`
3. Add logic in `static/js/app.js`

## Troubleshooting

### Frontend Not Loading

1. Check API is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify frontend is mounted:
   ```bash
   docker exec legal-ai-api ls /app/frontend
   ```

3. Check browser console for errors (F12)

### API Calls Failing

1. Verify CORS is enabled (already configured)
2. Check network tab in browser dev tools
3. Ensure backend containers are running:
   ```bash
   docker-compose ps
   ```

### Styling Issues

1. Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)
2. Check CSS file is loading in Network tab
3. Verify static files are mounted correctly

## Development

### Live Reload

The frontend uses volume mounting, so changes are reflected immediately:

1. Edit HTML/CSS/JS files
2. Refresh browser (Ctrl+R / Cmd+R)
3. No restart needed!

### Testing

Open browser console (F12) to see:
- API requests/responses
- JavaScript errors
- Network timing

## Future Enhancements

Potential features to add:
- [ ] Legal document upload and analysis
- [ ] Chat history persistence
- [ ] Multiple conversation threads
- [ ] Export responses to PDF
- [ ] Dark mode toggle
- [ ] User authentication
- [ ] Search through HK legal database
- [ ] Response streaming (real-time)
- [ ] Markdown formatting for responses
- [ ] Code syntax highlighting

## Support

For issues or questions:
1. Check the main [README.md](../README.md)
2. View [QUICKSTART.md](../QUICKSTART.md)
3. Check API docs at http://localhost:8000/docs

## License

Part of Legal AI Vault - On-Premises Legal AI System
