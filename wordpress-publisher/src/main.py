
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>WordPress Publisher - Thrive Studio Digital Labs</h1>
    <p>WordPress automation service is running!</p>
    <p><a href="/health">Health Check</a></p>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'wordpress-publisher'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
