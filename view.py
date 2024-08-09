from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def home():
    secret_path = "/tmp/mysql-creds"  # Path where the secret is mounted
    secret_value = "Secret not found!"  # Default message if the secret file is missing

    if os.path.exists(secret_path):
        with open(secret_path, 'r') as secret_file:
            secret_value = secret_file.read().strip()
    
    return render_template('index.html', secret=secret_value)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

