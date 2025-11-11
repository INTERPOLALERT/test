"""
KimiGPT - Main Web Application
Flask application that serves the web interface
"""

import os
import sys
import logging
import uuid
import json
import zipfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.multi_agent_system import get_multi_agent_system
from src.api.api_manager import get_api_manager
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'kimigpt-secret-key-change-in-production')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated_sites'
TEMP_FOLDER = 'temp'
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Initialize multi-agent system
try:
    multi_agent_system = get_multi_agent_system()
    api_manager = get_api_manager()
    logger.info("✓ Multi-Agent System initialized")
except Exception as e:
    logger.error(f"Failed to initialize system: {e}")
    multi_agent_system = None
    api_manager = None


@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@app.route('/generate')
def generate_page():
    """Generator page"""
    return render_template('generator.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for website generation"""
    try:
        # Get user input
        user_prompt = request.form.get('prompt', '')
        if not user_prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400

        # Handle file uploads
        attachments = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)

                    # Determine file type
                    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                    file_type = 'unknown'
                    if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                        file_type = 'image'
                    elif file_ext in ['mp4', 'webm', 'mov']:
                        file_type = 'video'
                    elif file_ext in ['mp3', 'wav', 'ogg']:
                        file_type = 'audio'
                    elif file_ext in ['pdf', 'docx', 'txt']:
                        file_type = 'document'

                    attachments.append({
                        'name': filename,
                        'path': file_path,
                        'type': file_type,
                        'size': os.path.getsize(file_path)
                    })

        logger.info(f"Generating website with prompt: {user_prompt[:100]}...")

        # Generate website using multi-agent system
        if not multi_agent_system:
            return jsonify({'success': False, 'error': 'System not initialized'}), 500

        result = multi_agent_system.generate_website(user_prompt, attachments)

        if not result.get('success'):
            return jsonify(result), 500

        # Create session ID
        session_id = str(uuid.uuid4())

        # Save generated files to temp directory
        session_dir = os.path.join(TEMP_FOLDER, session_id)
        os.makedirs(session_dir, exist_ok=True)

        # Extract files from result
        outputs = result.get('outputs', {})
        deployment_output = outputs.get(max(outputs.keys())) if outputs else None

        if deployment_output and 'files' in deployment_output:
            files = deployment_output['files']
            for file_path, content in files.items():
                full_path = os.path.join(session_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Create ZIP file
            zip_filename = f"website_{session_id}.zip"
            zip_path = os.path.join(GENERATED_FOLDER, zip_filename)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path, content in files.items():
                    zipf.writestr(file_path, content)

            # Prepare response
            response_data = {
                'success': True,
                'session_id': session_id,
                'preview_url': f'/preview/{session_id}/',
                'download_url': f'/api/download/{session_id}',
                'project_name': deployment_output.get('project_name', 'website'),
                'qa_score': deployment_output.get('qa_score', 0),
                'analysis': result.get('analysis', {}),
                'files_count': len(files)
            }

            return jsonify(response_data)

        else:
            return jsonify({'success': False, 'error': 'No files generated'}), 500

    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/download/<session_id>')
def api_download(session_id):
    """Download generated website as ZIP"""
    try:
        zip_filename = f"website_{session_id}.zip"
        zip_path = os.path.join(GENERATED_FOLDER, zip_filename)

        if not os.path.exists(zip_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename
        )

    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/preview/<session_id>/')
@app.route('/preview/<session_id>/<path:filename>')
def serve_preview(session_id, filename='index.html'):
    """Serve preview files"""
    preview_dir = os.path.join(TEMP_FOLDER, session_id)

    if not os.path.exists(preview_dir):
        return "Preview not found", 404

    try:
        file_path = os.path.join(preview_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        else:
            return "File not found", 404
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return str(e), 500


@app.route('/api/status')
def api_status():
    """Get system status"""
    try:
        if not multi_agent_system or not api_manager:
            return jsonify({'status': 'not_initialized'}), 500

        status = {
            'system': 'online',
            'agents': multi_agent_system.get_system_status(),
            'api_status': api_manager.get_status()
        }

        return jsonify(status)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test-apis')
def api_test_apis():
    """Test all API connections"""
    try:
        if not api_manager:
            return jsonify({'error': 'API Manager not initialized'}), 500

        results = api_manager.test_apis()
        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Start the application"""
    port = int(os.getenv('FLASK_PORT', 5000))

    print("╔════════════════════════════════════════════════╗")
    print("║              KIMIGPT LAUNCHER                   ║")
    print("║       Multi-Agent AI Website Builder            ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    print(f"🌐 Dashboard: http://localhost:{port}")
    print(f"🎨 Generator: http://localhost:{port}/generate")
    print(f"📊 API Status: http://localhost:{port}/api/status")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development',
        threaded=True
    )


if __name__ == '__main__':
    main()
