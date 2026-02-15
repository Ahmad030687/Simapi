from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/sim', methods=['GET'])
def get_sim_data():
    number = request.args.get('q')
    if not number:
        return jsonify({"status": "error", "message": "Number missing!"})

    # Number format fix (0 hatao)
    if number.startswith("0"):
        number = number[1:]

    target_url = f"https://sim.f-a-k.workers.dev/?q={number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    try:
        # Yahan hum request bhej rahe hain
        response = requests.get(target_url, headers=headers, timeout=10)
        data = response.json()
        
        # Apna custom format
        return jsonify({
            "status": "success",
            "developer": "AHMAD RDX",
            "result": data.get("data", [])
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
