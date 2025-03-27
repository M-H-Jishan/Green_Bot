# Green Bot: Intelligent University Student Support System

## Project Overview

Green Bot is an advanced AI-powered chatbot system designed specifically to enhance student support services at universities. By leveraging cutting-edge natural language processing and machine learning technologies, Green Bot provides immediate, accurate, and personalized assistance to students 24/7.

## 🌟 Key Features

### Core Capabilities
- **Intelligent Query Processing**: Advanced NLP for accurate query understanding
- **Multi-Source Information**: Combines knowledge base, university data, and AI
- **Context Awareness**: Maintains conversation context for better responses
- **Smart Categorization**: Organizes information hierarchically
- **Related Questions**: Suggests relevant follow-up questions
- **Prerequisites Tracking**: Identifies and suggests prerequisite information

### Technical Features
- **Modern Architecture**: Django backend + React frontend
- **RESTful API**: Well-documented endpoints for easy integration
- **Database Integration**: Hybrid approach using PostgreSQL and JSON
- **Security**: Token-based authentication and rate limiting
- **Swagger Documentation**: Interactive API documentation
- **Docker Support**: Easy deployment with containers

## 📁 Project Structure

```
Green_Bot/
├── ChatbotServer/        # Django Backend
│   ├── chatbot/         # Main chatbot application
│   ├── data/           # University data and configurations
│   └── requirements.txt # Python dependencies
├── Frontend/            # React Frontend
│   ├── src/            # Source code
│   └── package.json    # Node.js dependencies
└── docs/               # Documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL (optional, can use SQLite)
- Docker (optional)

### Backend Setup
1. Navigate to ChatbotServer:
   ```bash
   cd ChatbotServer
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up database:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to Frontend:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

## 📚 Data Structure

### 1. Knowledge Base
Managed through Django Admin interface (`/admin`):
- Categories (e.g., Admissions, Courses, Campus Life)
- Questions and Answers
- Related Questions
- Prerequisites

### 2. University Data
Stored in `university_data.json`:
- University Information
- Academic Programs
- Facilities
- Faculty Information
- Admission Details
- Financial Information

For detailed data structure templates, see [Data Structure Documentation](docs/DATA_STRUCTURE.md).

## 🔧 Configuration

### Environment Variables
Create `.env` file in ChatbotServer:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URL
```

### API Configuration
- Base URL: `http://localhost:8000/api/`
- Authentication: Token-based
- Rate Limiting: 100 requests/hour

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

---
*This project was developed as part of the university's digital transformation initiative to enhance student support services.*
