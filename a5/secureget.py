import socket
import ssl

# Server configuration
hostname = 'www.google.com'
port = 443

# Create SSL context with default settings
context = ssl.create_default_context()

# Establish TCP connection
with socket.create_connection((hostname, port)) as raw_socket:
    with context.wrap_socket(raw_socket, server_hostname=hostname) as secure_socket:
        print(f"[+] SSL connection established to {hostname}:{port}")
        print(f"    Cipher suite: {secure_socket.cipher()}")
        print(f"    SSL/TLS version: {secure_socket.version()}")

        # Send HTTP GET request
        http_request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        secure_socket.sendall(http_request.encode('utf-8'))

        # Receive HTTP response
        full_response = b""
        while True:
            chunk = secure_socket.recv(4096)
            if not chunk:
                break
            full_response += chunk

# Save the response with error handling
try:
    separator_pos = full_response.find(b"\r\n\r\n")
    if separator_pos == -1:
        print("[-] Warning: Could not find HTTP header separator, saving entire response")
        html_content = full_response
    else:
        html_content = full_response[separator_pos + 4:]

    # Save HTML content to file
    with open("response.html", "wb") as output_file:
        output_file.write(html_content)
    print(f"[+] Successfully saved {len(html_content)} bytes to response.html")

except IOError as e:
    print(f"[-] File operation error: {e}")
except Exception as e:
    print(f"[-] Unexpected error during response processing: {e}")