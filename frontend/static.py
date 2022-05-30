from flask import send_from_directory

def getInjectorStatic(path : str) -> str:
    return send_from_directory('frontend/', path)