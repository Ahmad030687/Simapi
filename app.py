from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# 🔑 آپ کی پرائیویٹ کی (Secret Key)
RDX_SECRET = "ahmad_rdx_private_786"

@app.route('/download', methods=['GET'])
def download():
    # سیکیورٹی چیک
    key = request.args.get('key')
    if key != RDX_SECRET:
        return jsonify({"error": "Unauthorized"}), 403

    url = request.args.get('url')
    media_type = request.args.get('type') # audio or video

    ydl_opts = {
        'format': 'bestaudio/best' if media_type == 'audio' else 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success",
                "downloadUrl": info['url'],
                "title": info.get('title', 'Music')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
