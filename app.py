from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_yt():
    # 1. Security Check (Ahmad RDX Private Key)
    key = request.args.get('key')
    if key != "ahmad_rdx_private_786":
        return jsonify({"status": "error", "message": "Oye saste hero! Unauthorized key. 😏🖕"}), 403

    query = request.args.get('q') # Search query
    if not query:
        return jsonify({"status": "error", "message": "Query missing! Kuch likh toh sahi. 😏"}), 400

    # 2. Optimized Search Options (Sirf metadata nikalne ke liye)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # Isse search super fast ho jati hai
        'skip_download': True,
        'source_address': '0.0.0.0'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ytsearch1: ka matlab hai sirf pehla result uthao
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            
            if 'entries' not in info or len(info['entries']) == 0:
                return jsonify({"status": "error", "message": "Kuch nahi mila! 🖕"}), 404

            video_data = info['entries'][0]
            
            # Response Structure
            return jsonify({
                "status": "success",
                "result": {
                    "title": video_data.get('title'),
                    "id": video_data.get('id'),
                    "url": f"https://www.youtube.com/watch?v={video_data.get('id')}",
                    "duration": video_data.get('duration'),
                    "uploader": video_data.get('uploader'),
                    "views": video_data.get('view_count')
                }
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render port binding
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
