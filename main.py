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

# Add comprehensive tool listing with fallback information
@mcp.tool()
def list_available_tools() -> str:
    """List all available document processing tools with fallback options"""
    return """🛠️ **Available Document Processing Tools:**

**📄 Standard Document Processing:**
1. **upload_document** - Upload DOCX, DOC, PDF, TXT files
2. **process_document** - Analyze uploaded documents
3. **search_document** - Search within uploaded documents

**🔄 Direct Processing (Bypass Preprocessing):**
4. **handle_document_direct** - Process documents directly when preprocessing fails
5. **process_any_document** - Analyze any text content immediately (RECOMMENDED)
6. **handle_preprocessing_failure** - Get help when preprocessing fails

**🔍 Server Tools:**
7. **validate_server** - Check server health
8. **get_owner_phone** - Get server owner info

**💡 Quick Start Guide:**
- **Document upload failing?** → Use `process_any_document`
- **Preprocessing errors?** → Use `handle_document_direct`
- **Need immediate analysis?** → Copy text and use `process_any_document`

**📋 Supported Formats:** DOCX, DOC, PDF, TXT, RTF, ODT
**🎯 Smart Detection:** Automatically detects code, academic papers, reports, etc.
"""

@mcp.tool()
def list_supported_formats() -> str:
    """List all supported document formats and processing capabilities"""
    return """📄 **Comprehensive Format Support:**

**Microsoft Office:**
• DOCX - Word documents (2007+) ✅
• DOC - Legacy Word documents ✅

**Adobe:**
• PDF - Portable Document Format ✅

**Text Formats:**
• TXT - Plain text files ✅
• RTF - Rich Text Format ✅

**OpenDocument:**
• ODT - OpenDocument Text ✅

**🤖 Smart Processing Features:**
✅ **Auto-detection**: Automatically identifies document type
✅ **Code Analysis**: Detects and analyzes programming languages
✅ **Academic Papers**: Special handling for research documents
✅ **Fallback Processing**: Works even when preprocessing fails
✅ **Multi-language**: Handles various text encodings

**🔄 Fallback Options When Processing Fails:**
1. Direct text processing via `process_any_document`
2. Manual content input with smart analysis
3. Alternative processing methods automatically suggested

**💪 Reliability Features:**
• Multiple extraction methods per format
• Error recovery and alternative processing
• Comprehensive text analysis regardless of source format
"""

print("Registering tools...")
validate_tool.register(mcp)
document_tool.register(mcp)
print("✓ All tools registered")
print("📄 Supported formats: DOCX, DOC, PDF, TXT, RTF, ODT")
print("🔄 Fallback processing: Available for failed preprocessing")
print("🚀 Direct processing: Bypass preprocessing with smart tools")

# Expose ASGI app for uvicorn
app = mcp.http_app()  # Default path: /mcp/

print("Server setup complete. Available at http://0.0.0.0:8086/mcp/")