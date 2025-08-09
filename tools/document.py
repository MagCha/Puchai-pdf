"""
Document processing tools for Puch AI MCP server.
Handles document upload, processing, and search functionality using WhatsApp phone numbers as session IDs.
"""

from __future__ import annotations

from fastmcp import FastMCP
from pydantic import BaseModel, Field
import os
import base64
import io
import uuid
from typing import Annotated, Dict, Any
from pathlib import Path

# Document storage using WhatsApp phone numbers as keys
document_storage: Dict[str, Dict[str, Any]] = {}

class DocumentProcessor:
    """Helper class for processing different document types"""
    
    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX files"""
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            
            text_content = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_content.append(" | ".join(row_text))
            
            return "\n\n".join(text_content)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_doc(file_bytes: bytes) -> str:
        """Extract text from DOC files"""
        try:
            import olefile
            
            ole = olefile.OleFileIO(file_bytes)
            
            if ole._olestream_size is None:
                raise Exception("Invalid DOC file")
            
            text = "DOC file detected but full text extraction requires additional libraries. Please convert to DOCX format for better support."
            ole.close()
            return text
            
        except Exception as e:
            try:
                # Fallback: try to read as plain text
                return file_bytes.decode('latin-1', errors='ignore')
            except:
                raise Exception(f"Failed to extract text from DOC: {str(e)}")
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF files"""
        try:
            import PyPDF2
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n{text}")
                except:
                    text_content.append(f"--- Page {page_num + 1} ---\n[Text extraction failed for this page]")
            
            return "\n\n".join(text_content)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_bytes: bytes) -> str:
        """Extract text from TXT files"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    return file_bytes.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            return file_bytes.decode('utf-8', errors='replace')
            
        except Exception as e:
            raise Exception(f"Failed to extract text from TXT: {str(e)}")

def register(mcp: FastMCP):
    """Register document processing tools with the FastMCP server"""
    
    @mcp.tool(description="Upload and process documents (Word, PDF, TXT) for further analysis")
    async def upload_document(
        document_data: Annotated[str, Field(description="Base64-encoded document data")],
        filename: Annotated[str, Field(description="Original filename with extension")],
        phone_number: Annotated[str, Field(description="WhatsApp phone number (with country code, e.g., +1234567890)")] = "default_user"
    ) -> str:
        """Upload and process a document, storing it for the specific WhatsApp user"""
        
        try:
            # Clean and validate phone number
            clean_phone = phone_number.strip().replace(" ", "").replace("-", "")
            if not clean_phone.startswith("+"):
                clean_phone = "+" + clean_phone if clean_phone.startswith("1") or len(clean_phone) > 10 else "+1" + clean_phone
            
            # Decode the document
            file_bytes = base64.b64decode(document_data)
            file_extension = Path(filename).suffix.lower()
            
            # Generate unique document ID
            doc_id = str(uuid.uuid4())[:8]
            
            # Extract text based on file type
            extracted_text = ""
            
            if file_extension in ['.docx']:
                extracted_text = DocumentProcessor.extract_text_from_docx(file_bytes)
            elif file_extension in ['.doc']:
                extracted_text = DocumentProcessor.extract_text_from_doc(file_bytes)
            elif file_extension in ['.pdf']:
                extracted_text = DocumentProcessor.extract_text_from_pdf(file_bytes)
            elif file_extension in ['.txt']:
                extracted_text = DocumentProcessor.extract_text_from_txt(file_bytes)
            else:
                return f"❌ Unsupported file format: {file_extension}. Supported formats: .docx, .doc, .pdf, .txt"
            
            # Store document data using phone number as key
            document_storage[clean_phone] = {
                "doc_id": doc_id,
                "filename": filename,
                "file_type": file_extension,
                "extracted_text": extracted_text,
                "file_bytes": file_bytes,
                "phone_number": clean_phone,
                "upload_time": str(os.popen('date /t').read().strip() if os.name == 'nt' else 'now')
            }
            
            # Return preview and wait for instructions
            preview = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
            
            return f"""📄 **Document Uploaded Successfully**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}
🔍 **Document ID:** {doc_id}
📊 **Type:** {file_extension.upper()}
📏 **Size:** {len(extracted_text)} characters extracted

📖 **Content Preview:**
---
{preview}
---

✅ **Document processed and ready for further instructions!**

🎯 **Available Actions:**
• Use 'process_document' to analyze, summarize, or transform the content
• Use 'search_document' to find specific information

💡 **What would you like me to do with this document?**
"""
            
        except Exception as e:
            return f"❌ **Error processing document:** {str(e)}\n\n💡 Please ensure the file is not corrupted and is in a supported format."

    @mcp.tool(description="Process uploaded documents with various operations")
    async def process_document(
        phone_number: Annotated[str, Field(description="WhatsApp phone number (with country code)")] = "default_user",
        operation: Annotated[str, Field(description="Operation: summarize, analyze, extract_key_points, word_count, format_clean")] = "summarize",
        instructions: Annotated[str, Field(description="Specific instructions for processing")] = ""
    ) -> str:
        """Process the uploaded document based on user instructions"""
        
        # Clean phone number
        clean_phone = phone_number.strip().replace(" ", "").replace("-", "")
        if not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone if clean_phone.startswith("1") or len(clean_phone) > 10 else "+1" + clean_phone
        
        if clean_phone not in document_storage:
            return f"❌ **No document found for {clean_phone}.** Please upload a document first using 'upload_document'."
        
        doc_data = document_storage[clean_phone]
        text = doc_data["extracted_text"]
        filename = doc_data["filename"]
        
        if operation == "summarize":
            words = text.split()
            word_count = len(words)
            
            sentences = text.replace('\n', ' ').split('. ')
            summary = '. '.join(sentences[:3]) + '.'
            
            return f"""📋 **Document Summary**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}
📊 **Statistics:** {word_count} words, {len(text)} characters

📝 **Summary:**
{summary}

🔍 **Key Points:**
• Document contains {len(sentences)} sentences
• Average words per sentence: {word_count/len(sentences):.1f}
• Estimated reading time: {word_count//200 + 1} minutes
"""
        
        elif operation == "analyze":
            lines = text.split('\n')
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            words = text.split()
            
            return f"""📊 **Document Analysis**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}

📈 **Structure Analysis:**
• Total lines: {len(lines)}
• Paragraphs: {len(paragraphs)}
• Words: {len(words)}
• Characters: {len(text)}
• Unique words: {len(set(word.lower().strip('.,!?;:"()[]{}') for word in words))}

📝 **Content Analysis:**
• Average paragraph length: {len(words)/len(paragraphs):.1f} words
• Longest paragraph: {max(len(p.split()) for p in paragraphs) if paragraphs else 0} words
• Document density: {"High" if len(words)/len(paragraphs) > 50 else "Medium" if len(words)/len(paragraphs) > 20 else "Low"}

💡 **Document appears to be:** {
    "Technical/Formal" if any(word in text.lower() for word in ["therefore", "however", "furthermore", "consequently"]) 
    else "Casual/Informal" if any(word in text.lower() for word in ["like", "really", "pretty", "kinda"])
    else "Standard"
}
"""
        
        elif operation == "extract_key_points":
            sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if len(s.strip()) > 20]
            
            important_sentences = []
            keywords = ["important", "key", "main", "significant", "critical", "essential", "primary", "major", "conclusion", "result"]
            
            for sentence in sentences[:10]:
                if any(keyword in sentence.lower() for keyword in keywords):
                    important_sentences.append(sentence + ".")
            
            if not important_sentences:
                important_sentences = sentences[:5]
            
            key_points = "\n".join([f"• {point}" for point in important_sentences[:5]])
            
            return f"""🎯 **Key Points Extracted**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}

🔑 **Main Points:**
{key_points}

📊 **Extraction Summary:**
• Analyzed {len(sentences)} sentences
• Identified {len(important_sentences)} key points
• Based on keyword analysis and sentence structure
"""
        
        elif operation == "word_count":
            words = text.split()
            from collections import Counter
            
            word_freq = Counter(word.lower().strip('.,!?;:"()[]{}') for word in words)
            most_common = word_freq.most_common(10)
            
            return f"""📊 **Word Count Analysis**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}

📈 **Statistics:**
• Total words: {len(words)}
• Unique words: {len(word_freq)}
• Characters (with spaces): {len(text)}
• Characters (without spaces): {len(text.replace(' ', ''))}

🏆 **Most Frequent Words:**
{chr(10).join([f"• {word}: {count} times" for word, count in most_common])}

📖 **Reading Metrics:**
• Estimated reading time: {len(words)//200 + 1} minutes
• Average word length: {sum(len(word) for word in words)/len(words):.1f} characters
"""
        
        elif operation == "format_clean":
            lines = text.split('\n')
            clean_lines = []
            
            for line in lines:
                line = line.strip()
                if line:
                    clean_lines.append(line)
            
            clean_text = '\n\n'.join(clean_lines)
            
            return f"""✨ **Cleaned Document**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **Original File:** {filename}

📝 **Cleaned Content:**
---
{clean_text[:2000]}{"..." if len(clean_text) > 2000 else ""}
---

🧹 **Cleaning Summary:**
• Removed extra whitespace
• Standardized line breaks
• Preserved paragraph structure
• Original lines: {len(text.split(chr(10)))}
• Cleaned lines: {len(clean_lines)}
"""
        
        else:
            return f"❌ **Unknown operation:** {operation}\n\n✅ **Available operations:** summarize, analyze, extract_key_points, word_count, format_clean"

    @mcp.tool(description="Search within uploaded documents")
    async def search_document(
        search_query: Annotated[str, Field(description="Text to search for in the document")],
        phone_number: Annotated[str, Field(description="WhatsApp phone number (with country code)")] = "default_user",
        case_sensitive: Annotated[bool, Field(description="Whether search should be case sensitive")] = False
    ) -> str:
        """Search for specific text within the uploaded document for a specific WhatsApp user"""
        
        # Clean phone number
        clean_phone = phone_number.strip().replace(" ", "").replace("-", "")
        if not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone if clean_phone.startswith("1") or len(clean_phone) > 10 else "+1" + clean_phone
        
        if clean_phone not in document_storage:
            return f"❌ **No document found for {clean_phone}.** Please upload a document first using 'upload_document'."
        
        doc_data = document_storage[clean_phone]
        text = doc_data["extracted_text"]
        filename = doc_data["filename"]
        
        search_text = text if case_sensitive else text.lower()
        query = search_query if case_sensitive else search_query.lower()
        
        # Find all occurrences
        occurrences = []
        start = 0
        
        while True:
            pos = search_text.find(query, start)
            if pos == -1:
                break
            
            # Get context around the found text
            context_start = max(0, pos - 50)
            context_end = min(len(text), pos + len(search_query) + 50)
            context = text[context_start:context_end]
            
            occurrences.append({
                "position": pos,
                "context": context
            })
            
            start = pos + 1
            
            if len(occurrences) >= 10:  # Limit results
                break
        
        if not occurrences:
            return f"""🔍 **Search Results**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}
🔎 **Query:** "{search_query}"

❌ **No matches found.**

💡 Try different keywords or check spelling.
"""
        
        results_text = ""
        for i, occurrence in enumerate(occurrences, 1):
            results_text += f"\n**Match {i}:**\n...{occurrence['context']}...\n"
        
        return f"""🔍 **Search Results**
{'═' * 50}

📱 **WhatsApp:** {clean_phone}
📁 **File:** {filename}
🔎 **Query:** "{search_query}"
✅ **Found:** {len(occurrences)} match{"es" if len(occurrences) != 1 else ""}

📋 **Results:**
{results_text}

{"📝 **Note:** Showing first 10 matches only." if len(occurrences) >= 10 else ""}
"""

    print("✓ Document tools registered with WhatsApp phone number support")