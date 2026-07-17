# AI-Powered Text Analysis API

A RESTful API built with FastAPI that provides advanced text analysis capabilities, including sentiment analysis, keyword extraction, and text classification.

## Features

- Sentiment analysis (positive, negative, neutral)
- Keyword extraction
- Text classification
- Easy-to-use REST endpoints
- Fast and asynchronous with FastAPI

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/text-analysis-api.git
cd text-analysis-api
```

2. Install dependencies:

```bash
pip install fastapi uvicorn
```

3. Run the API server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Usage

### Analyze Text

**Endpoint:** `POST /analyze`

**Request body (JSON):**

```json
{
  "text": "I love this product!"
}
```

**Response (JSON):**

```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "keywords": ["love", "product"]
}
```

## Testing

A test endpoint is available to verify the API is running:

**Endpoint:** `GET /test`

**Response:**

```json
{
  "message": "API is working!"
}
```

## Project Structure

```
text-analysis-api/
├── main.py          # Main application entry point
├── models.py        # Data models and schemas
├── services.py      # Text analysis logic
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.