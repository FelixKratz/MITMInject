import ssl
import sys
from __init__ import app
from config import Config
from flask import request
from networking.proxy import Proxy
from frontend.static import getInjectorStatic
from frontend.preferences import renderPreferenceSite
from networking.sslCallbacks import servername_callback
from networking.injectorAPI import handleInjectorAPICall

# TODO: Implement server side scripts and server client script communication, possibly even overriding
#       chrome API calls, like the storage API call for plug and play compatibility of chrome extensions
# TODO: Persistent settings for injections -> callable through API from script
# TODO: Implement configuration domain with a rendered configuration page where website plugins can be
#       activated/deactivated and modified/uploaded
# TODO: Setup a mySQL database with a database handler for easy, fast and reliable persistent storage
# TODO: Outsource the qn matching to the database -> speedup?
# TODO: Implement GUI for the network monitoring
# TODO: Implement GUI for the block lists
# TODO: Think about the use of "Captive Portals" for the first time connection where the certificate 
#       can be downloaded & install instructions are displayed
#       For this we need to keep a list of clients
#       -> If client not in list: resolve all DNS queries with own IP and redirect to captive portal site
#       in http mode.
#       -> On Captive Portal Site: try to load an https test file from this server, if it resolves the
#       certificate is already installed => have a nice day
#       Else: serve the certificate as download and check again.
#       Only then add client to known hosts and resolve DNS requests regularly
# TODO: Better and more dynamic DNS override system with dynamic IP overrides,
# paired to the client for better customizablility etc.

# TODO: Package the injection file, filter lists, static files and python addon for easy plugin management


# Basically: Accept requests from all domains and decide what to do
@app.route('/', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE'], host="<string:domain>")
@app.route('/<path:dummy>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE'], host="<string:domain>")
def captureAllDomains(dummy : str = "", domain : str = "") -> str:
    # Render the preference page
    if (domain == Config.PREFERENCES_DOMAIN):
        if ("/" in dummy and dummy.split("/")[0] == Config.STATIC_PATH):
            return getInjectorStatic(dummy)
        return renderPreferenceSite(request)

    # API Calls to this server from any injected website are handled here
    if (dummy == Config.INJECTOR_API_PATH):
        return handleInjectorAPICall(request)
    
    # All other requests are proxied and filtered
    return Proxy.getSite(request.url, domain, request)

# Flask "Debug" Mode if run from __main__
# TODO: Use production server, e.g. gunicorn
if (__name__ == "__main__"):
    # If the additional commandline argument "http" is given, start the
    # server in http mode.
    # Otherwise: start in https mode with dynamic certificate creation
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        print("Running in http mode")
        app.run(host=Config.HOST_IP, port=80, threaded=True)
    else:
        print("Running https mode with dynamic ssl certificates")
        context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        context.set_servername_callback(servername_callback)
        app.run(host=Config.HOST_IP, port=443, ssl_context=context, threaded=True)
