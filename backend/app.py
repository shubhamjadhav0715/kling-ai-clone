"""
Kling AI Clone - Main Flask Application
Video Generation API Server
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
import threading
from queue import Queue

from config import Config
from models.model_loader import ModelLoader
from models.text_to_video import TextToVideoGenerator
from models.image_to_video import ImageToVideoGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Create necessary directories
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.MODEL_DIR, exist_ok=True)

# Initialize model loader
model_loader = ModelLoader()

# Job queue and status tracking
job_queue = Queue()
job_status = {}

# Initialize generators
text_to_video_gen = None
image_to_video_gen = None


def initialize_models():
    """Initialize AI models on startup"""
    global text_to_video_gen, image_to_video_gen
    
    print("🚀 Initializing AI models...")
    try:
        if Config.ENABLE_TEXT_TO_VIDEO:
            print("📝 Loading Text-to-Video model...")
            text_to_video_gen = TextToVideoGenerator(model_loader)
            print("✅ Text-to-Video model loaded")
        
        if Config.ENABLE_IMAGE_TO_VIDEO:
            print("🖼️  Loading Image-to-Video model...")
            image_to_video_gen = ImageToVideoGenerator(model_loader)
            print("✅ Image-to-Video model loaded")
        
        print("🎉 All models initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing models: {str(e)}")
        print("⚠️  Server will start but video generation will fail")


def process_job_queue():
    """Background worker to process video generation jobs"""
    while True:
        job = job_queue.get()
        job_id = job['job_id']
        
        try:
            job_status[job_id]['status'] = 'processing'
            job_status[job_id]['progress'] = 0
            
            if job['type'] == 'text_to_video':
                result = text_to_video_gen.generate(
                    prompt=job['prompt'],
                    num_frames=job.get('num_frames', 24),
                    fps=job.get('fps', 8),
                    output_path=job['output_path'],
                    progress_callback=lambda p: update_progress(job_id, p)
                )
            elif job['type'] == 'image_to_video':
                result = image_to_video_gen.generate(
                    image_path=job['image_path'],
                    num_frames=job.get('num_frames', 24),
                    fps=job.get('fps', 8),
                    output_path=job['output_path'],
                    progress_callback=lambda p: update_progress(job_id, p)
                )
            
            job_status[job_id]['status'] = 'completed'
            job_status[job_id]['progress'] = 100
            job_status[job_id]['output_path'] = result['output_path']
            job_status[job_id]['completed_at'] = datetime.now().isoformat()
            
        except Exception as e:
            job_status[job_id]['status'] = 'failed'
            job_status[job_id]['error'] = str(e)
            print(f"❌ Job {job_id} failed: {str(e)}")
        
        job_queue.task_done()


def update_progress(job_id, progress):
    """Update job progress"""
    if job_id in job_status:
        job_status[job_id]['progress'] = progress


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'text_to_video': text_to_video_gen is not None,
            'image_to_video': image_to_video_gen is not None
        },
        'queue_size': job_queue.qsize(),
        'active_jobs': len([j for j in job_status.values() if j['status'] == 'processing'])
    })


@app.route('/api/generate/text-to-video', methods=['POST'])
def generate_text_to_video():
    """Generate video from text prompt"""
    if not text_to_video_gen:
        return jsonify({'error': 'Text-to-video model not loaded'}), 503
    
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Create job
    job_id = str(uuid.uuid4())
    output_filename = f"{job_id}.mp4"
    output_path = os.path.join(Config.OUTPUT_DIR, output_filename)
    
    job = {
        'job_id': job_id,
        'type': 'text_to_video',
        'prompt': prompt,
        'num_frames': data.get('num_frames', 24),
        'fps': data.get('fps', 8),
        'output_path': output_path
    }
    
    job_status[job_id] = {
        'status': 'queued',
        'progress': 0,
        'created_at': datetime.now().isoformat(),
        'prompt': prompt
    }
    
    job_queue.put(job)
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Video generation job queued successfully'
    })


@app.route('/api/generate/image-to-video', methods=['POST'])
def generate_image_to_video():
    """Generate video from image"""
    if not image_to_video_gen:
        return jsonify({'error': 'Image-to-video model not loaded'}), 503
    
    if 'image' not in request.files:
        return jsonify({'error': 'Image file is required'}), 400
    
    image_file = request.files['image']
    
    # Save uploaded image
    job_id = str(uuid.uuid4())
    image_filename = f"{job_id}_input.png"
    image_path = os.path.join(Config.UPLOAD_DIR, image_filename)
    image_file.save(image_path)
    
    output_filename = f"{job_id}.mp4"
    output_path = os.path.join(Config.OUTPUT_DIR, output_filename)
    
    job = {
        'job_id': job_id,
        'type': 'image_to_video',
        'image_path': image_path,
        'num_frames': int(request.form.get('num_frames', 24)),
        'fps': int(request.form.get('fps', 8)),
        'output_path': output_path
    }
    
    job_status[job_id] = {
        'status': 'queued',
        'progress': 0,
        'created_at': datetime.now().isoformat()
    }
    
    job_queue.put(job)
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Video generation job queued successfully'
    })


@app.route('/api/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get status of a video generation job"""
    if job_id not in job_status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job_status[job_id])


@app.route('/api/download/<job_id>', methods=['GET'])
def download_video(job_id):
    """Download generated video"""
    if job_id not in job_status:
        return jsonify({'error': 'Job not found'}), 404
    
    job = job_status[job_id]
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Video not ready yet'}), 400
    
    output_path = job.get('output_path')
    
    if not output_path or not os.path.exists(output_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_file(output_path, as_attachment=True, download_name=f"video_{job_id}.mp4")


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'jobs': [
            {
                'job_id': job_id,
                **status
            }
            for job_id, status in job_status.items()
        ]
    })


if __name__ == '__main__':
    # Start background worker thread
    worker_thread = threading.Thread(target=process_job_queue, daemon=True)
    worker_thread.start()
    
    # Initialize models
    initialize_models()
    
    # Start Flask server
    print(f"\n🚀 Server starting on http://{Config.HOST}:{Config.PORT}")
    print(f"📁 Output directory: {Config.OUTPUT_DIR}")
    print(f"📁 Model directory: {Config.MODEL_DIR}\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
