Maintained by Mawio Maintainer

# FastAPI Hello Endpoint

A simple FastAPI application with a single endpoint:

- **GET /hello** – Returns the string `HeLLLOOO ALOHA`.

## Running the application

```bash
uvicorn app:app --reload
```

Visit `http://127.0.0.1:8000/hello` in your browser or use curl:

```bash
curl http://127.0.0.1:8000/hello
```
