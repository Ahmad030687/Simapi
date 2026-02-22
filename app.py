from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_yt():
    # Security Key
    key = request.args.get('key')
    if key != "ahmad_rdx_private_786":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    query = request.args.get('q')
    if not query:
        return jsonify({"status": "error", "message": "Kuch likh toh sahi! 😏"}), 400

    # 🔥 Bulletproof Settings to prevent Hanging
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'skip_download': True,
        'source_address': '0.0.0.0', # Force IPv4 (YouTube IPv6 ko jaldi block karta hai)
        'socket_timeout': 10,        # 10 second baad agar response na mile toh cancel kar do
        'noprogress': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search logic
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return jsonify({
                    "status": "success",
                    "result": {
                        "title": video.get('title'),
                        "url": f"https://www.youtube.com/watch?v={video.get('id')}",
                        "id": video.get('id'),
                        "duration": video.get('duration'),
                        "uploader": video.get('uploader')
                    }
                })
            else:
                return jsonify({"status": "error", "message": "Result not found"}), 404

    except Exception as e:
        # Agar block ho jaye toh yahan error dikhayega
        return jsonify({"status": "error", "message": "YouTube ne block kiya ya timeout ho gaya!", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
