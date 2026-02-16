from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    # 1. Security Check
    key = request.args.get('key')
    if key != "ahmad_rdx_private_786":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    url = request.args.get('url')
    mode = request.args.get('type') # audio or video
    
    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    # 2. Advanced YT-DLP Options (To prevent 500 Errors)
    ydl_opts = {
        'format': 'bestaudio/best' if mode == 'audio' else 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'socket_timeout': 30,
        'source_address': '0.0.0.0',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info hi asal kaam karta hai
            info = ydl.extract_info(url, download=False)
            
            # Direct link nikalna
            direct_link = info.get('url') or info.get('entries', [{}])[0].get('url')
            
            if not direct_link:
                return jsonify({"status": "error", "message": "Could not extract link"}), 500

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Unknown'),
                "downloadUrl": direct_link
            })

    except Exception as e:
        # Agar koi error aaye to bot ko bataye ke kya masla hai
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
