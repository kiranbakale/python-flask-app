from flask import Flask, render_template
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__, template_folder='Templates')

def get_secret(secret_name="mysql-creds"):
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary']
    except ClientError as e:
        # Handle the error
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    secret_value = get_secret()
    if secret_value:
        return render_template('index.html', secret=secret_value)
    else:
        return "Failed to retrieve secret."

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


