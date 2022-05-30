import regex as re
from config import Config
from filtering import Filter
from typing import Optional, Tuple
from networking.contentActions import Content

class Injection:
    # Caching Injections reduces latency and disk usage, but can be
    # disadvantageous for injection testing and development
    injectionCache = {}

    # Loads a specific injection from file/cache
    def loadInjectionFor(injectionName : str) -> bytes:
        if Config.INJECTION_CACHING:
            if injectionName in Injection.injectionCache:
                print("Loading injection from cache: " + injectionName)
                return Injection.injectionCache[injectionName]
        try:
            with open('injections/' + injectionName) as f:
                print("Injection loaded for: " + injectionName)
                data = str.encode(f.read())
                f.close()
                if Config.INJECTION_CACHING:
                    Injection.injectionCache[injectionName] = data
                return data
        except IOError:
            print("File not accessible")
        return b""

    # Map sites to injection names via the INJECTION_MAP
    def getInjectionNameForSite(site : str) -> Optional[str]:
        for name, url in Config.INJECTION_MAP.items():
            if re.match(url, site):
                return name
        return None

    # Injection into matching sites and content types
    def injectInto(site : str, domain : str, headers : dict, content : bytes) -> Tuple[dict, bytes]:
        contentType, encoding, encodingIndex = Content.getRawContentInfo(headers)
        if (contentType in Config.INJECTION_CONTENT_TYPES):
            injectionName = Injection.getInjectionNameForSite(site)
            if not injectionName:
                return headers, content
            print("Injecting into: ", site)
            # Decode the raw content
            content = Content.decodeRawContent(content, encoding)

            # Inject new info into decoded content
            content += b"<script>" \
                        + Injection.loadInjectionFor("system.js") \
                        + Injection.loadInjectionFor(injectionName) \
                        + Filter.pruneFilter.generateInjection(domain) \
                        + Filter.elementFilter.generateInjection(domain) \
                     + b"</script>"

            # Either reencode the decoded content, or pop the encoding header
            # and return content as plain
            if Config.RECOMPRESS_HTML:
                content = Content.encodeRawContent(content, encoding)
            elif encodingIndex > 0:
                headers.pop(encodingIndex)
        return headers, content


