from flask import Flask, render_template, jsonify
import os
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        hostname=socket.gethostname(),
        commit_sha=os.environ.get('GITHUB_SHA', 'unknown')[:7],
        branch=os.environ.get('GITHUB_REF_NAME', 'unknown'),
        deploy_time=os.environ.get('DEPLOY_TIME', 'unknown'),
        pipeline=os.environ.get('GITHUB_WORKFLOW', 'Deploy — Dev'),
        env='dev',
        version='1.0.0'
    )

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'version': '1.0.0',
        'env': 'dev',
        'hostname': socket.gethostname(),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)