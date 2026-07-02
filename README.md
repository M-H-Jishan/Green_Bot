# Green Bot — AI-Powered Chatbot

A production-ready chatbot with hybrid search (Knowledge Base + custom JSON data) and LLM fallback (OpenAI or Claude). Built with Django REST Framework, React + Vite, and Docker.

## Features

- **Hybrid Search**: Knowledge Base → Custom JSON data → LLM fallback
- **Multi-Provider LLM**: Switch between OpenAI and Claude via env var
- **Custom Data**: Drop in any JSON file — no code changes needed
- **JWT Authentication**: Secure API with token-based auth
- **Rate Limiting**: Configurable per-user rate limits
- **React Frontend**: Modern UI with Tailwind CSS, typing indicators, error states
- **Docker Ready**: Full docker-compose setup with Redis and optional PostgreSQL
- **API Docs**: Auto-generated Swagger docs via drf-spectacular

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- (Optional) Docker & Docker Compose

### Backend Setup

```bash
cd ChatbotServer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file and configure
cp .env.example .env
# Edit .env with your API keys and settings

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

### Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Copy env file and configure
cp .env.example .env
# Edit .env if your backend URL differs

# Start dev server
npm run dev
```

The frontend runs on `http://localhost:5173` and proxies API requests to `http://localhost:8000`.

### Docker Setup (Recommended)

```bash
# Copy and configure environment
cp ChatbotServer/.env.example ChatbotServer/.env
# Edit .env with your API keys

# Build and start all services
docker-compose up -d --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create admin user
docker-compose exec backend python manage.py createsuperuser
```

Services:
- Frontend: `http://localhost:80`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs/`
- Admin: `http://localhost:8000/admin/`

## Configuration

All configuration is via environment variables. See `.env.example` for all options.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `openai` | `openai` or `claude` |
| `OPENAI_API_KEY` | — | Required if using OpenAI |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `ANTHROPIC_API_KEY` | — | Required if using Claude |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` | Claude model to use |
| `DATA_FILE_PATH` | `chatbot/data/university_data.json` | Path to your custom JSON data |
| `DATABASE_URL` | SQLite | PostgreSQL URL for production |
| `REDIS_URL` | — | Redis URL for caching (optional) |
| `DEBUG` | `True` | Set to `False` in production |

### Using Custom Data

1. Create a JSON file with your data (see `chatbot/data/university_data.json` for format)
2. Set `DATA_FILE_PATH` in your `.env` to point to your file
3. Restart the server — no code changes needed

The JSON data is searched with fuzzy matching. If no match is found, the LLM is used as fallback (with the JSON data injected as context).

### Switching LLM Providers

Just change one env var:

```bash
# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Or use Claude
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
```

If no API key is set, the bot operates in KB-only mode (no LLM fallback).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/token/` | Get JWT token (username + password) |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| POST | `/api/chat/` | Send a chat query (requires auth) |
| GET | `/api/schema/` | OpenAPI schema |
| GET | `/api/docs/` | Swagger UI |
| GET | `/health/` | Health check |

### Chat API Example

```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'

# Send query
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"query": "What programs do you offer?"}'
```

## Running Tests

```bash
cd ChatbotServer
python manage.py test
```

## Project Structure

```
Green_Bot/
├── ChatbotServer/          # Django backend
│   ├── ChatbotServer/      # Django project settings
│   ├── chatbot/            # Chatbot app
│   │   ├── data/           # Custom JSON data files
│   │   ├── migrations/     # Database migrations
│   │   ├── admin.py        # Admin configuration
│   │   ├── llm_provider.py # LLM abstraction (OpenAI + Claude)
│   │   ├── models.py       # KnowledgeBase, QueryLog, Category
│   │   ├── serializers.py  # DRF serializers
│   │   ├── services.py     # Chatbot service logic
│   │   ├── tests.py        # Unit & API tests
│   │   ├── urls.py         # URL routing
│   │   └── views.py        # API views
│   ├── Dockerfile          # Backend Docker image
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── Frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main app
│   │   └── main.tsx        # Entry point
│   ├── Dockerfile          # Frontend Docker image
│   ├── nginx.conf          # Nginx config for production
│   └── package.json        # Node dependencies
├── docker-compose.yml      # Full stack orchestration
├── .gitignore
└── README.md
```

## License

This project is open source. Feel free to use and modify.
