import regex as re
# TODO: Load from external text file maybe?
# TODO: Make settings available in OPNSense

class Config:
    ### Flask Server
    # IP of the injection server
    HOST_IP = "10.6.0.1"
    # Secret Key for https
    SECRET_KEY = b'aigdf3in002r98e2698378R1e19812798'
    
    ### DNS Server
    # Port for the built in DNS Server to listen on
    DNS_PORT = 53
    # Resolve against this fallback DNS server (e.g. 8.8.8.8) 
    FALLBACK_DNS_RESOLVER = "127.0.0.1"
    # Fallback DNS port (e.g. 53)
    FALLBACK_DNS_PORT = 5353
    # Activate full override mode and redirect *ALL* DNS requests to
    # this server -- good for security research and traffic monitoring
    # may be slow however
    DNS_FULL_OVERRIDE = False
    # The URL maps listed here will be overriden by the DNS server
    # and redirected to this proxy
    DNS_OVERRIDES = [re.compile(r"captive\.portal\."), 
                     re.compile(r"(www.|m.|)youtube\.com\."), 
                     re.compile(r"(www.|m.|)twitch\.tv\.")]
    
    ### Captive Portal & Known Client handler
    # Still work in progress: Idea is to redirect unknown clients
    # to the configuration page, where they can install the certificate
    # and customize the behaviour
    REDIRECT_UNKNOWN_DEVICES = False

    ### Frontend
    STATIC_PATH = "static"
    # Path for API calls on hijacked websites
    INJECTOR_API_PATH = "injectorAPI/"
    # The configuration site of the injection server is http
    PREFERENCES_DOMAIN = "injection.config"
    TEMPLATE_FOLDER = "frontend/templates/"

    ### Certificates
    CERTIFICATE_FOLDER = "certificates/certs/"

    ### Injection
    # Injection Caching will drastically reduce disk read operations, 
    # turn off whilr developing injections for them to be hotloaded
    INJECTION_CACHING = True 
    # Only these content types will be injected with the payload
    INJECTION_CONTENT_TYPES = ["text/html", "text/html; charset=utf-8", "text/html; charset=UTF-8"]
    # File name of the injection is bound to a URL map - contents of the file are
    # injected into all matching URLS with above content types
    INJECTION_MAP = {"www.youtube.com.js" : re.compile(r"(www.|m.|)youtube\.com/.*"),
                     "www.twitch.tv.js" : re.compile(r"(www.|m.|)twitch\.tv/.*")}

    ### Filtering
    # Modify default behaviour for unspecified filter actions
    DEFAUT_RESPONSE_RULE = "block"
    # A list of all lister lists
    FILTER_LISTS = ["www.youtube.com"]

    ### Monitoring
    # DNS Monitoring will save all DNS queries to a log of length MAY_HISTORY_LEN
    MONITOR_DNS = False
    # Request Monitoring saves the request made from the client to the server
    MONITOR_REQUESTS = False
    # Response Monitoring saves the response sent from the server to the client
    MONITOR_RESPONSES = False
    # Length of the history for all monitors
    MAX_HISTORY_LEN = 200

    ### Performance Settings
    # If JavaScript is unpacked for modification it can either be recompressed,
    # or it can be sent uncompressed -- sending it uncompressed is generally faster
    RECOMPRESS_JS = False
    # Same for HTML, however, recompressing the HTML is generally faster
    RECOMPRESS_HTML = True
