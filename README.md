Maintained by Mawio Maintainer

## Usage

### fib.py
Run the Fibonacci script:
```
python fib.py 10
```
Expected output:
```
0 1 1 2 3 5 8 13 21 34
```

### prime.py
Run the prime check script:
```
python prime.py 17
```
Expected output:
```
17 is a prime number.
```

### main.py (FastAPI)
Start the FastAPI server:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
Make a request to the health endpoint:
```
curl http://localhost:8000/healthy
```
Sample response:
```json
{
  "status": "healthy"
}
```
Or for the analyze endpoint:
```
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"text":"Hello world"}'
```
Sample response:
```json
{
  "analysis": "Positive sentiment"
}
```