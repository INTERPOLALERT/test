"""
KimiGPT - Preview Server
Serves generated websites for real-time preview
"""

import logging
import os
from flask import Flask, send_from_directory, render_template_string
from flask_cors import CORS

logger = logging.getLogger(__name__)

# Create preview app
preview_app = Flask(__name__, static_folder='../../temp')
CORS(preview_app)


@preview_app.route('/preview/<session_id>/')
@preview_app.route('/preview/<session_id>/<path:filename>')
def serve_preview(session_id, filename='index.html'):
    """Serve preview files for a session"""
    preview_dir = os.path.join('temp', session_id)

    if not os.path.exists(preview_dir):
        return "Preview not found", 404

    try:
        return send_from_directory(preview_dir, filename)
    except Exception as e:
        logger.error(f"Error serving preview: {e}")
        return str(e), 500


@preview_app.route('/preview/<session_id>/iframe')
def preview_iframe(session_id):
    """Render preview in iframe"""
    iframe_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Website Preview</title>
        <style>
            * {{ margin: 0; padding: 0; }}
            html, body {{ height: 100%; overflow: hidden; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
    </head>
    <body>
        <iframe src="/preview/{session_id}/"></iframe>
    </body>
    </html>
    """
    return render_template_string(iframe_html)


def start_preview_server(port=3000):
    """Start the preview server"""
    logger.info(f"Starting preview server on port {port}...")
    preview_app.run(host='0.0.0.0', port=port, debug=False, threaded=True)


if __name__ == "__main__":
    start_preview_server()
