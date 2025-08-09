# Puch AI MCP Server

A comprehensive Model Context Protocol (MCP) server for document processing, designed to integrate with AI platforms like Puch AI. This server provides advanced document analysis, processing, and search capabilities through a robust MCP implementation.

## 🚀 Features

### Document Processing Tools
- **Multi-format Support**: DOCX, DOC, PDF, TXT, RTF, ODT
- **Smart Analysis**: Auto-detects document types (code, research papers, business documents)
- **Comprehensive Processing**: Summarization, analysis, key point extraction, word counting
- **Advanced Search**: Context-aware search within uploaded documents
- **Session Management**: WhatsApp phone number-based user sessions

### Server Capabilities
- **Real-time Processing**: Live document analysis via MCP protocol
- **Fallback Processing**: Handles preprocessing failures gracefully
- **Debug Logging**: Comprehensive logging for monitoring and troubleshooting
- **Authentication**: Token-based security with configurable access control
- **Watermarking System**: Built-in response tracking and identification

## 📁 Project Structure

```
word-to-pdf-mcp/
├── main.py                 # ASGI server entry point
├── tools/
│   ├── validate.py         # Server validation and health check tools
│   └── document.py         # Document processing tools
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Required Python packages (see requirements.txt)

### Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd word-to-pdf-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file with:
   ```env
   AUTH_TOKEN=your_secure_token_here
   MY_NUMBER=+1234567890
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8086
   ```

## 🔧 Available Tools

### Document Processing
1. **`upload_document`** - Upload and process documents with base64 encoding
2. **`process_document`** - Analyze uploaded documents with various operations
3. **`search_document`** - Search within uploaded documents with context
4. **`handle_document_direct`** - Direct processing when preprocessing fails
5. **`process_any_document`** - Process any text content directly (recommended for reliability)
6. **`handle_preprocessing_failure`** - Guidance when document processing fails

### Server Management
7. **`validate_server`** - Health check and status verification
8. **`get_owner_phone`** - Retrieve server owner information
9. **`validate`** - Quick server validation
10. **`list_available_tools`** - Display all available tools with descriptions
11. **`list_supported_formats`** - Show supported document formats and capabilities

## 🌐 Deployment Options

### Local Development
```bash
# Standard local deployment
uvicorn main:app --host 0.0.0.0 --port 8086
```

### Production with ngrok (Recommended for testing)
```bash
# Terminal 1: Start the server
uvicorn main:app --host 0.0.0.0 --port 8086

# Terminal 2: Expose via ngrok
ngrok http 8086
```

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8086"]
```

## 🧪 Testing & Integration

### AI Platform Integration
This MCP server has been successfully tested with:
- **Puch AI**: Full integration with tool calling and parameter passing
- **Real-time Processing**: Confirmed working with live AI conversations
- **Response Handling**: AI platforms may post-process responses for consistency

### Testing Tools Explicitly
To ensure your MCP tools are being used by AI platforms:

```
"Use the process_any_document tool to analyze this text: [your content]"
"Call upload_document with this document data"
"Use handle_document_direct for processing this file"
```

### Debug Monitoring
Monitor server console for debug output:
```
🔧 DEBUG: MCP received text_content length: 1847
🔧 DEBUG: Document type: text
🔧 DEBUG: Analysis type: comprehensive
🔧 DEBUG: Detected document type: General Document
🔧 DEBUG: MCP returning response length: 2341
```

## 🔍 Key Discoveries

### AI Platform Behavior
During integration testing, we discovered:

1. **Tool Discovery**: AI platforms successfully discover and list MCP tools
2. **Selective Usage**: Platforms call MCP tools when explicitly requested
3. **Response Processing**: Platforms may rewrite responses for UX consistency
4. **Fallback Mechanisms**: Platforms have internal processing as backup
5. **Session Management**: Each AI conversation maintains separate tool sessions

### Integration Patterns
- **Backend Service Model**: MCP serves as processing backend while AI controls UX
- **Explicit Tool Calling**: Most reliable when users explicitly mention tool names
- **Content Filtering**: AI platforms may sanitize or reformat responses
- **Error Handling**: Robust fallback mechanisms essential for reliability

## 📊 Performance Features

### Smart Document Detection
- **Code Recognition**: Python, JavaScript, C/C++ automatic detection
- **Academic Papers**: Research document structure analysis
- **Business Documents**: Meeting notes, reports, formal documents
- **General Content**: Fallback analysis for any text content

### Advanced Analytics
- **Statistical Analysis**: Word count, character analysis, reading time
- **Content Structure**: Paragraph analysis, sentence structure
- **Key Point Extraction**: Intelligent identification of important information
- **Search Capabilities**: Context-aware text search with highlights

## 🔐 Security Features

- **Token Authentication**: Secure API access control
- **Session Isolation**: User-specific document storage
- **Input Validation**: Comprehensive parameter validation
- **Error Handling**: Secure error messages without information leakage

## 📈 Monitoring & Debugging

### Server Health
- Real-time health checks via `validate_server`
- Connection status monitoring
- Tool availability verification

### Debug Features
- Comprehensive request/response logging
- Processing time monitoring
- Error tracking and reporting
- Tool usage analytics

## 🚀 Future Enhancements

### Planned Features
- [ ] OCR support for scanned documents
- [ ] Multi-language document support
- [ ] Advanced document comparison tools
- [ ] Batch processing capabilities
- [ ] Document format conversion
- [ ] Enhanced security features

### Integration Improvements
- [ ] WebSocket support for real-time updates
- [ ] Streaming response capabilities
- [ ] Advanced caching mechanisms
- [ ] Performance optimization

## 🤝 Contributing

This project demonstrates successful MCP implementation with real AI platform integration. Contributions welcome for:
- Additional document format support
- Enhanced analysis capabilities
- Performance improvements
- Security enhancements

## 📝 License

[Your License Here]

---

## 🎯 Hackathon Notes

This MCP server successfully demonstrates:
- ✅ **Full MCP Protocol Implementation**: Complete tool registration, discovery, and execution
- ✅ **Real AI Integration**: Confirmed working with Puch AI platform
- ✅ **Advanced Document Processing**: Multi-format support with intelligent analysis
- ✅ **Production-Ready Architecture**: Authentication, error handling, debugging
- ✅ **Scalable Design**: Session management and user isolation

**Key Achievement**: Proven that external MCP servers can successfully integrate with AI platforms, providing extended capabilities while maintaining platform UX control.