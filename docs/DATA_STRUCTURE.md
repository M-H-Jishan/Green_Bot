# Data Structure Documentation

This document provides detailed templates for both the Knowledge Base and University Data structures used in Green Bot.

## 1. Knowledge Base Data Structure

The knowledge base consists of three main components:

### Categories
```json
{
    "name": "string",
    "description": "string"
}
```
Example categories:
- Academic Programs
- Admission Requirements
- Campus Life
- Financial Aid
- Research
- Student Services

### Knowledge Base Entries
```json
{
    "question": "string",
    "answer": "string",
    "category": "string (category name)",
    "prerequisites": ["list of related question IDs"],
    "related_questions": ["list of related question IDs"],
    "source_url": "string (optional)"
}
```

Example entry:
```json
{
    "question": "What are the admission requirements for undergraduate programs?",
    "answer": "General admission requirements include:\n1. Completed application form\n2. High school transcripts\n3. Standardized test scores (SAT/ACT)\n4. Letters of recommendation\n5. Personal statement",
    "category": "Admission Requirements",
    "prerequisites": [],
    "related_questions": ["How to apply?", "What is the application deadline?"],
    "source_url": "https://university.edu/admissions"
}
```

## 2. University Data Structure (university_data.json)

```json
{
    "university_info": {
        "name": "string",
        "established": "year",
        "location": {
            "address": "string",
            "city": "string",
            "country": "string",
            "coordinates": {
                "latitude": "float",
                "longitude": "float"
            }
        },
        "contact": {
            "phone": "string",
            "email": "string",
            "website": "string"
        }
    },
    "academic_programs": {
        "undergraduate": [
            {
                "name": "string",
                "degree": "string",
                "department": "string",
                "duration": "string",
                "description": "string",
                "requirements": ["list of strings"],
                "career_prospects": ["list of strings"]
            }
        ],
        "graduate": [
            {
                "name": "string",
                "degree": "string",
                "department": "string",
                "duration": "string",
                "description": "string",
                "requirements": ["list of strings"],
                "research_areas": ["list of strings"]
            }
        ]
    },
    "facilities": {
        "libraries": [
            {
                "name": "string",
                "location": "string",
                "hours": "string",
                "resources": ["list of strings"]
            }
        ],
        "laboratories": [
            {
                "name": "string",
                "department": "string",
                "equipment": ["list of strings"]
            }
        ],
        "housing": {
            "dormitories": [
                {
                    "name": "string",
                    "type": "string",
                    "capacity": "integer",
                    "amenities": ["list of strings"]
                }
            ]
        },
        "sports": [
            {
                "facility": "string",
                "sports": ["list of strings"],
                "hours": "string"
            }
        ]
    },
    "faculty": {
        "departments": [
            {
                "name": "string",
                "head": "string",
                "programs_offered": ["list of strings"],
                "contact": {
                    "email": "string",
                    "phone": "string",
                    "office": "string"
                }
            }
        ]
    },
    "admission": {
        "deadlines": {
            "undergraduate": {
                "fall": "string",
                "spring": "string"
            },
            "graduate": {
                "fall": "string",
                "spring": "string"
            }
        },
        "requirements": {
            "undergraduate": ["list of strings"],
            "graduate": ["list of strings"],
            "international": ["list of strings"]
        },
        "process": ["list of steps"]
    },
    "financial": {
        "tuition": {
            "undergraduate": {
                "domestic": "float",
                "international": "float"
            },
            "graduate": {
                "domestic": "float",
                "international": "float"
            }
        },
        "scholarships": [
            {
                "name": "string",
                "amount": "string",
                "eligibility": ["list of strings"],
                "deadline": "string"
            }
        ]
    }
}
```

### For University Data
1. Create a `university_data.json` file in the `chatbot/data/` directory
2. Follow the structure above
3. Fill in your university's specific information
4. The chatbot will automatically use this data to answer queries

## Important Notes

1. All dates should be in ISO format (YYYY-MM-DD)
2. All monetary values should be in the local currency
3. URLs should be complete (including https://)
4. Keep answers concise but informative
5. Use markdown formatting in answers for better readability

## Best Practices

1. **Consistency**: Use consistent terminology throughout the data
2. **Completeness**: Fill in all relevant fields for comprehensive responses
3. **Updates**: Keep information current, especially for deadlines and requirements
4. **Language**: Use clear, professional language
5. **Links**: Include relevant URLs for detailed information
6. **Structure**: Maintain the hierarchical structure for easy navigation
