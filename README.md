# Puch AI MCP Server

A Model Context Protocol (MCP) server built with FastMCP that provides document processing and validation tools for Puch AI integration.

## Features

- **Document Processing**: Read and process documents sent by users through MCP tools
- **Server Validation**: Validate server connectivity and retrieve owner information
- **Token-based Authentication**: Secure authentication using static token verification
- **Phone Number Integration**: Owner phone number validation and retrieval
- **FastMCP Integration**: Built on FastMCP framework for efficient MCP operations
- **ASGI Web Server**: Runs as a web service with uvicorn

## Prerequisites

- Python 3.7+
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MagCha/Puchai-pdf.git
cd Puchai-pdf
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values with your credentials:

```properties
AUTH_TOKEN=your_auth_token_here
MY_NUMBER=your_phone_number_here
```

## Configuration

Create a `.env` file in the root directory with the following variables:

- `AUTH_TOKEN`: Your authentication token for MCP client access
- `MY_NUMBER`: Your phone number (used for validation and identification)

## Usage

### Starting the MCP Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8086
```

The server will be available at: `http://0.0.0.0:8086/mcp/`

### Available MCP Tools

1. **Validate Tool** (`tools.validate`)
   - Validates server connectivity
   - Returns owner's phone number
   - Used for server health checks

2. **Document Tool** (`tools.document`)
   - Processes documents sent by users
   - Enables Puch AI to read document content
   - Handles various document formats

### Authentication

The server uses token-based authentication:
- Clients must provide the `AUTH_TOKEN` to access MCP tools
- Token verification is handled by `StaticTokenVerifier`
- Authorized clients get `read` and `write` scopes

## Project Structure

```
├── main.py            # ASGI server entrypoint
├── tools/             # MCP tool implementations
│   ├── validate.py    # Server validation tool
│   └── document.py    # Document processing tool
├── .env               # Environment variables (not in git)
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Development

### Running in Development
```bash
uvicorn main:app --host 0.0.0.0 --port 8086 --reload
```

### Adding New Tools
1. Create a new tool file in the `tools/` directory
2. Implement the `register(mcp: FastMCP)` function
3. Import and register the tool in `main.py`

## Security Notes

- Never commit your `.env` file to version control
- Keep your `AUTH_TOKEN` secure and don't share it
- The server validates all incoming requests with token authentication
- Phone numbers are stored without the '+' prefix for consistency

## API Endpoint

- **MCP Endpoint**: `http://0.0.0.0:8086/mcp/`
- **Protocol**: Streamable HTTP MCP
- **Authentication**: Bearer token required

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the GitHub repository.

## Technical Details

- **Framework**: FastMCP
- **Server**: uvicorn (ASGI)
- **Authentication**: StaticTokenVerifier
- **Language**: Python 3.7+
- **Protocol**: Model Context Protocol (MCP)