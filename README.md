# Kling AI Clone - Open Source Video Generation Platform

A powerful, open-source video generation AI platform similar to Kling AI. Generate high-quality videos from text prompts or animate images using state-of-the-art AI models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)

## 🌟 Features

- **Text-to-Video Generation**: Create videos from text descriptions
- **Image-to-Video Animation**: Bring static images to life
- **Multiple AI Models**: Support for Stable Video Diffusion, AnimateDiff, and more
- **Modern Web Interface**: Beautiful, responsive React UI
- **Local Processing**: Run everything on your own hardware
- **API Support**: RESTful API for integration
- **Queue Management**: Handle multiple generation requests
- **Progress Tracking**: Real-time generation progress updates

## 🎥 Demo

Generate videos like:
- "A cat walking on a beach at sunset"
- "Drone footage flying over mountains"
- "Time-lapse of a flower blooming"

## 📋 Requirements

### Minimum System Requirements
- **GPU**: NVIDIA RTX 3060 (12GB VRAM) or better
- **RAM**: 16GB system RAM
- **Storage**: 100GB free space (for models)
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS

### Recommended System Requirements
- **GPU**: NVIDIA RTX 4090 (24GB VRAM)
- **RAM**: 32GB+ system RAM
- **Storage**: 500GB NVMe SSD
- **OS**: Linux (Ubuntu 22.04)

### Software Requirements
- Python 3.10 or higher
- Node.js 18 or higher
- CUDA 11.8 or higher (for NVIDIA GPUs)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/shubhamjadhav0715/kling-ai-clone.git
cd kling-ai-clone
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download AI models (this will take time and space)
python scripts/download_models.py

# Start the backend server
python app.py
```

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will start on `http://localhost:3000`

### 4. Access the Application

Open your browser and navigate to `http://localhost:3000`

## 📁 Project Structure

```
kling-ai-clone/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   ├── text_to_video.py  # Text-to-video model
│   │   ├── image_to_video.py # Image-to-video model
│   │   └── model_loader.py   # Model management
│   ├── api/
│   │   ├── routes.py         # API endpoints
│   │   └── queue.py          # Job queue management
│   ├── scripts/
│   │   └── download_models.py # Model download script
│   └── config.py             # Configuration
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js            # Main React component
│       ├── components/
│       │   ├── VideoGenerator.js
│       │   ├── ImageUploader.js
│       │   └── ProgressBar.js
│       └── services/
│           └── api.js        # API client
├── models/                   # Downloaded AI models (gitignored)
├── outputs/                  # Generated videos (gitignored)
└── README.md
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# Model settings
MODEL_TYPE = "stable-video-diffusion"  # or "animatediff"
MAX_VIDEO_LENGTH = 120  # seconds
DEFAULT_FPS = 24
DEFAULT_RESOLUTION = "512x512"

# Server settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# GPU settings
USE_GPU = True
GPU_MEMORY_FRACTION = 0.9
```

## 🎨 Usage

### Text-to-Video

1. Enter your text prompt (e.g., "A serene lake with mountains in the background")
2. Adjust settings (duration, FPS, resolution)
3. Click "Generate Video"
4. Wait for processing (may take several minutes)
5. Download your video

### Image-to-Video

1. Upload an image
2. Optionally add a motion prompt
3. Adjust animation settings
4. Click "Animate"
5. Download the animated video

## 🔌 API Documentation

### Generate Video from Text

```bash
POST /api/generate/text-to-video
Content-Type: application/json

{
  "prompt": "A cat walking on a beach",
  "duration": 5,
  "fps": 24,
  "resolution": "512x512"
}
```

### Generate Video from Image

```bash
POST /api/generate/image-to-video
Content-Type: multipart/form-data

image: [file]
motion_prompt: "gentle swaying motion"
duration: 3
fps: 24
```

### Check Generation Status

```bash
GET /api/status/{job_id}
```

## 🤖 Supported Models

- **Stable Video Diffusion (SVD)**: High-quality image-to-video
- **Stable Video Diffusion XT**: Extended temporal consistency
- **AnimateDiff**: Text-to-video with motion modules
- **ModelScope**: Fast text-to-video generation
- **Zeroscope**: High-resolution video generation

## 🛠️ Advanced Setup

### Using Different Models

```bash
# Download specific model
python scripts/download_models.py --model stable-video-diffusion-xt

# Use in config
MODEL_TYPE = "stable-video-diffusion-xt"
```

### GPU Optimization

For better performance on limited VRAM:

```python
# In config.py
ENABLE_ATTENTION_SLICING = True
ENABLE_VAE_SLICING = True
ENABLE_CPU_OFFLOAD = True  # For GPUs with <12GB VRAM
```

### Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build
```

## 📊 Performance Tips

1. **Start with lower resolutions** (256x256 or 512x512) for faster generation
2. **Reduce video duration** for quicker results
3. **Use attention slicing** if you have limited VRAM
4. **Close other GPU applications** during generation
5. **Use SSD storage** for faster model loading

## 🐛 Troubleshooting

### CUDA Out of Memory
- Reduce resolution or video duration
- Enable CPU offload in config
- Close other GPU applications

### Slow Generation
- Check GPU utilization with `nvidia-smi`
- Ensure models are on SSD, not HDD
- Reduce batch size in config

### Model Download Fails
- Check internet connection
- Ensure sufficient disk space (100GB+)
- Try downloading models manually from Hugging Face

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) for Stable Video Diffusion
- [Hugging Face](https://huggingface.co/) for model hosting
- [AnimateDiff](https://github.com/guoyww/AnimateDiff) team
- Kling AI for inspiration

## 📧 Contact

Project Link: [https://github.com/shubhamjadhav0715/kling-ai-clone](https://github.com/shubhamjadhav0715/kling-ai-clone)

## ⚠️ Disclaimer

This is an educational project. Generated content should be used responsibly and in accordance with applicable laws and regulations.

---

**Star ⭐ this repository if you find it helpful!**
