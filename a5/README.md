
CS158A Assignment 5 - Secure Socket
-----------------------------------------------------------------
This project implements a secure HTTPS client that establishes SSL/TLS connections and retrieves web content.
The secureget.py is a standalone web client program:

- Uses raw TCP sockets with SSL/TLS encryption for secure communication
- Establishes connections using Python's ssl.create_default_context() for secure defaults
- Separates HTTP headers from body content and extracts pure HTML
- Provides detailed SSL connection information including cipher suite and TLS version
- Logs connection status and saves retrieved content to local file

HOW TO RUN THE PROGRAM

Setup: Place secureget.py in your working directory
In Terminal, run the program by typing:

python secureget.py

If the python file runs successfully, an html file named response.html will be created in the same directory. 

EXAMPLE OUTPUT

python secureget.py

[+] SSL connection established to www.google.com:443

    Cipher suite: ('TLS_AES_256_GCM_SHA384', 'TLSv1.3', 256)
    
    SSL/TLS version: TLSv1.3
    
[+] Successfully saved 54870 bytes to response.html

NOTES

 - Security: Uses modern SSL/TLS with secure default settings and proper certificate validation
 - Compatibility: Works with any HTTPS-enabled website that accepts HTTP/1.1 requests
 - Error Handling: Gracefully handles network timeouts, SSL errors, and malformed HTTP responses
 - File Output: Always saves content to response.html - existing files will be overwritten
 - Connection Management: Properly closes SSL connections to prevent resource leaks
 - HTTP Compliance: Sends properly formatted HTTP/1.1 requests with required Host header and connection close directive
 - Debugging: SSL cipher and version information helps troubleshoot connection issues
