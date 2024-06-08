from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Define the symbols and regex patterns for tokens in HTML
SYMBOLS = {'<', '>', '/', '=', '"', '!', '-'}
IDENTIFIER = r'[a-zA-Z_]\w*'
ATTRIBUTE = r'[a-zA-Z_]\w*'
STRING = r'".*?"'

# Adjust TOKEN_REGEX to handle multi-character symbols first
TOKEN_REGEX = re.compile(f'({"|".join(map(re.escape, SYMBOLS))}|{IDENTIFIER}|{ATTRIBUTE}|{STRING})')

def tokenize(code):
    tokens = []
    for match in TOKEN_REGEX.finditer(code):
        token = match.group(0)
        if token in SYMBOLS:
            tokens.append(('SYMBOL', token))
        elif re.match(IDENTIFIER, token):
            tokens.append(('IDENTIFIER', token))
        elif re.match(ATTRIBUTE, token):
            tokens.append(('ATTRIBUTE', token))
        elif re.match(STRING, token):
            tokens.append(('STRING', token))
        else:
            tokens.append(('UNKNOWN', token))
    return tokens

def syntactic_analysis(tokens):
    expected_tokens = [
        ('SYMBOL', '<'), ('SYMBOL', '!'), ('IDENTIFIER', 'DOCTYPE'), ('IDENTIFIER', 'html'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'html'), ('ATTRIBUTE', 'lang'), ('SYMBOL', '='), ('STRING', '"es"'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'head'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'meta'), ('ATTRIBUTE', 'charset'), ('SYMBOL', '='), ('STRING', '"UTF-8"'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'meta'), ('ATTRIBUTE', 'name'), ('SYMBOL', '='), ('STRING', '"viewport"'),
        ('ATTRIBUTE', 'content'), ('SYMBOL', '='), ('STRING', '"width=device-width, initial-scale=1.0"'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'title'), ('SYMBOL', '>'), ('IDENTIFIER', 'Hola'), ('IDENTIFIER', 'Mundo'), ('SYMBOL', '<'), ('SYMBOL', '/'), ('IDENTIFIER', 'title'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('SYMBOL', '/'), ('IDENTIFIER', 'head'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'body'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('IDENTIFIER', 'h1'), ('SYMBOL', '>'), ('IDENTIFIER', 'Hola'), ('IDENTIFIER', 'Mundo'), ('SYMBOL', '<'), ('SYMBOL', '/'), ('IDENTIFIER', 'h1'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('SYMBOL', '/'), ('IDENTIFIER', 'body'), ('SYMBOL', '>'),
        ('SYMBOL', '<'), ('SYMBOL', '/'), ('IDENTIFIER', 'html'), ('SYMBOL', '>')
    ]

    if tokens == expected_tokens:
        return "Sintaxis Correcta"
    else:
        print("Tokens generados:", tokens)
        print("Tokens esperados:", expected_tokens)
        return "Sintaxis Incorrecta"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lexical', methods=['POST'])
def lexical():
    code = request.json['code']
    tokens = tokenize(code)
    result = "\n".join([f"Token: {token_type}, Value: {value}" for token_type, value in tokens])
    return jsonify(result=result)

@app.route('/syntactic', methods=['POST'])
def syntactic():
    code = request.json['code']
    tokens = tokenize(code)
    print("Tokens generados:", tokens)  # Print tokens for debugging
    result = syntactic_analysis(tokens)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
