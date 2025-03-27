# Green Bot API Documentation

## API Endpoints

### 1. Ask Question
Send questions to the chatbot and receive intelligent responses.

```http
POST /api/chatbot/ask/
```

#### Request
```json
{
    "query": "string",    // Required: The user's question
    "context": {          // Optional: Additional context
        "session_id": "string",
        "previous_query": "string"
    }
}
```

#### Response
```json
{
    "response": "string",         // The bot's answer
    "source": "string",          // Source of the answer (KB/AI/FB)
    "confidence": float,         // Confidence score (0-1)
    "category": "string",        // Category of the answer
    "intent": "string",          // Detected intent
    "related_questions": [       // Related questions
        "string"
    ],
    "source_url": "string",      // Reference URL (if available)
    "success": boolean          // Request success status
}
```

#### Example
```json
// Request
{
    "query": "What are the admission requirements for Computer Science?"
}

// Response
{
    "response": "For Computer Science admission, you need:\n1. Minimum GPA: 3.0\n2. Required subjects: Mathematics, Physics\n3. SAT Score: 1200+",
    "source": "KB",
    "confidence": 0.95,
    "category": "Admissions > Computer Science",
    "intent": "admission_inquiry",
    "related_questions": [
        "What is the application deadline?",
        "Are there any scholarships available?"
    ],
    "source_url": "https://university.edu/cs/admissions",
    "success": true
}
```

### 2. Get Categories
Retrieve available information categories.

```http
GET /api/chatbot/categories/
```

#### Response
```json
{
    "categories": [
        {
            "id": integer,
            "name": "string",
            "description": "string",
            "parent": integer,
            "subcategories": [
                // Recursive subcategories
            ]
        }
    ]
}
```

### 3. Get Intents
Retrieve available intents.

```http
GET /api/chatbot/intents/
```

#### Response
```json
{
    "intents": [
        {
            "id": integer,
            "name": "string",
            "description": "string",
            "keywords": [
                "string"
            ]
        }
    ]
}
```

### 4. Feedback
Submit feedback for a response.

```http
POST /api/chatbot/feedback/
```

#### Request
```json
{
    "query_id": "string",    // ID of the original query
    "rating": integer,       // Rating (1-5)
    "comment": "string"      // Optional feedback comment
}
```

### 5. Rate Limits
- 10 requests per minute per user
- 1000 requests per day per user

### Authentication
```http
Authorization: Token your_api_token
```

### Error Responses
```json
{
    "error": "string",       // Error message
    "code": "string",        // Error code
    "details": object       // Additional error details
}
```

Common error codes:
- `rate_limit_exceeded`
- `invalid_query`
- `unauthorized`
- `server_error`

## WebSocket API

### Connect
```javascript
const socket = new WebSocket('ws://your-domain/ws/chatbot/');
```

### Message Format
```json
{
    "type": "string",    // message_type
    "data": object      // message_data
}
```

### Events
1. `user_message`: Send user message
2. `bot_response`: Receive bot response
3. `typing_indicator`: Bot is typing
4. `error`: Error occurred

## Integration Example

### JavaScript
```javascript
async function askBot(question) {
    try {
        const response = await fetch('/api/chatbot/ask/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token your_api_token'
            },
            body: JSON.stringify({ query: question })
        });
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### Python
```python
import requests

def ask_bot(question, api_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}'
    }
    data = {'query': question}
    response = requests.post(
        'http://your-domain/api/chatbot/ask/',
        json=data,
        headers=headers
    )
    return response.json()
```
