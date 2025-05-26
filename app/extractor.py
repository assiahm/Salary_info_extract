import re

def extract_entities(text):
    data = {}
    data['nom'] = re.findall(r"Nom\s*:\s*(\w+ \w+)", text)
    data['salaire'] = re.findall(r"Salaire.*?:\s*([0-9]+[\.,]?[0-9]*)", text)
    return data