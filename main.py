from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Credentials (replace with env vars or secrets if needed)
USERNAME = os.getenv("EVEREADY_USERNAME")
PASSWORD = os.getenv("EVEREADY_PASSWORD")
DEVICE_SN = os.getenv("EVEREADY_SERIAL")

@app.route('/eveready/battery', methods=['GET'])
def get_battery_status():
    try:
        session = requests.Session()

        # Login
        login_payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "lang": "en"
        }
        login_resp = session.post("https://app.evereadysolarstorage.com/cloud/login", data=login_payload, verify=False)
        if login_resp.status_code != 200:
            return jsonify({"error": "Login failed"}), 401

        # Get device info
        info_url = f"https://app.evereadysolarstorage.com/cloud/monitor/site/getStoreOrAcDevicePowerInfo?plantuid=&devicesn={DEVICE_SN}"
        data_resp = session.get(info_url, verify=False)
        data = data_resp.json()

        # Just return storeDevicePower portion
        return jsonify(data.get("storeDevicePower", {}))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)