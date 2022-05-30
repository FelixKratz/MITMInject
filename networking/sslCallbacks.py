import ssl
from certificates.certificateGen import getCertificate

# Context caching reduces latency and disk usage
context_cache = {}

# This function is called immediately after the client requested a TLS handshake with the server
# in the request is the hostname of the server the client is trying to connect to
# --> create/load the certificate dynamically after the TLS handshake request and perform the handshake with it
def servername_callback(sock : ssl.SSLSocket, req_hostname : str, cb_context : ssl.SSLContext, as_callback : bool =True) -> None:
    if not req_hostname in context_cache:
        print("Loading ssl context for: ", req_hostname)
        context = ssl.SSLContext()
        certificate, key = getCertificate(req_hostname)
        context.load_cert_chain(certificate, key)
        context_cache[req_hostname] = context
    sock.context = context_cache[req_hostname]