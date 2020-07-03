from flask import Flask
import requests, spacy, json
from flask import jsonify

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')
def sanitize_names(text):
    docx = nlp(text)
    redacted_sentences = []
    for entity in docx.ents:
        if entity.label_ == 'PERSON':
            redacted_sentences.append('[REDACT]')
        else:
            redacted_sentences.append(entity.text)
    return "".join(redacted_sentences)

def title_process(text):
    array = text.split(" - ")
    output = []
    for i in array:
        output.append(sanitize_names(i))
    return " - ".join(output)

def content_html_process(text):
    array = text.split("\n\n")
    output = []
    for i in array:
        output.append(sanitize_names(i))
    return "\n\n".join(output)

def read_json_data(text):
    if isinstance(text, dict):
        output = {}
        for i, j in text.items():
            if isinstance(j, str):
                if i == 'title':
                    output[i] = title_process(j)
                elif i == 'content_html':
                    output[i] = content_html_process(j)
                else:
                    output[i] = sanitize_names(j)
            else:
                output[i] = read_json_data(j)
        return output
    if isinstance(text, list):
        output = []
        for i in text:
            output.append(read_json_data(i))
        return output



@app.route('/')
def index():
    resp = requests.get('http://therecord.co/feed.json', headers={'Content-Type':'application/json'})
    input = json.loads(resp)
    output = read_json_data(input)
    output['redact'] = 'redacted'
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)