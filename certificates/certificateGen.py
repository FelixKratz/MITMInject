import os
import subprocess
from config import Config
from typing import List, Tuple

def getCertificate(hostname) -> Tuple[str, str]:
    certFile, keyFile = Config.CERTIFICATE_FOLDER + hostname + ".crt", Config.CERTIFICATE_FOLDER + hostname + ".key"
    if not os.path.isfile(certFile) or not os.path.isfile(keyFile):
        print("No cert on disk for: " + hostname + "... Creating new one")
        generateSingleDomainCertificate(hostname)
        print("Cert for: " + hostname + " has been created")
    return certFile, keyFile

def generateSingleDomainCertificate(domain : str) -> None:
    subprocess.call(['./certificates/certGen.sh', domain])

# Kind of deprecated
def generateMultipleDomainCertificate(domains : List[str]) -> None:
    altDomains = ["www." + domain for domain in domains]
    domains += altDomains
    subprocess.call(['./certificates/certGen.sh', *domains])
