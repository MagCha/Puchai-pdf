"""
ASGI entrypoint for the Puch AI MCP server.

Run with:
  uvicorn main:app --host 0.0.0.0 --port 8086

Exposes MCP over Streamable HTTP at /mcp/ path.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier

# Load environment variables from .env
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

# Initialize MCP (removed unsupported parameters)
mcp = FastMCP(
    "Puch MCP Server", 
    auth=StaticTokenVerifier({
        TOKEN: {
            "client_id": "puch_client", 
            "scopes": ["read", "write"]
        }
    })
)

# Add project root to sys.path to ensure `tools` module can be found
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# External tools
from tools import validate as validate_tool
from tools import document as document_tool

print("Registering tools...")
validate_tool.register(mcp)
document_tool.register(mcp)
print("✓ All tools registered")

# Expose ASGI app for uvicorn
app = mcp.http_app()  # Default path: /mcp/

print("Server setup complete. Available at http://0.0.0.0:8086/mcp/")