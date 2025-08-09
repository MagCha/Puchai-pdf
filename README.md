# Puch MCP Server

This project is a FastMCP server that provides document processing and validation tools.

## Setup and Run (Windows)

### Prerequisites

- Python 3.10+ installed
- Git installed

### 1. Clone the Repository

```bash
git clone <repository-url>
cd word-to-pdf-mcp
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
.venv\Scripts\pip.exe install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the following:

```
AUTH_TOKEN="your-secret-token"
MY_NUMBER="your-phone-number"
```

### 5. Running the Server

**NOTE:** The server is pre-configured to run on port 8086. If you need to run it manually, use the following command:

```bash
.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8086
```

## Testing the Tools

You can test the tools by sending HTTP requests to the running server on port 8086.

### Validate Tool

```bash
curl -X POST -H "Authorization: Bearer your-secret-token" -H "Content-Type: application/json" -d '{"tool":"validate"}' http://localhost:8086/mcp/
```

### Document Tools

**Upload a document:**

```bash
curl -X POST -H "Authorization: Bearer your-secret-token" -H "Content-Type: application/json" -d '{"tool":"upload", "doc_id":"doc1", "content":"This is a test document."}' http://localhost:8086/mcp/
```

**Process a document:**

```bash
curl -X POST -H "Authorization: Bearer your-secret-token" -H "Content-Type: application/json" -d '{"tool":"process", "doc_id":"doc1"}' http://localhost:8086/mcp/
```

**Search for a document:**

```bash
curl -X POST -H "Authorization: Bearer your-secret-token" -H "Content-Type: application/json" -d '{"tool":"search", "query":"test"}' http://localhost:8086/mcp/
```