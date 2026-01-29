# 🚀 Quick Start Guide

Get your Kling AI Clone up and running in minutes!

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python version (need 3.10+)
python --version

# Check Node.js version (need 18+)
node --version

# Check if you have NVIDIA GPU
nvidia-smi
```

## Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/shubhamjadhav0715/kling-ai-clone.git
cd kling-ai-clone
```

### 2️⃣ Backend Setup (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download AI models (this takes time!)
python scripts/download_models.py

# Start backend server
python app.py
```

✅ Backend should now be running on `http://localhost:5000`

### 3️⃣ Frontend Setup (Terminal 2)

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm start
```

✅ Frontend should open automatically at `http://localhost:3000`

## 🎉 You're Ready!

1. Open `http://localhost:3000` in your browser
2. Try the **Text-to-Video** tab
3. Enter a prompt like: "A cat walking on a beach at sunset"
4. Click "Generate Video"
5. Wait for the magic! ✨

## ⚡ Quick Tips

### For Faster Setup
- Start with lower resolution (256x256)
- Use fewer frames (16-24)
- Close other GPU applications

### If Models Take Too Long to Download
Download specific models only:
```bash
# Just download Stable Video Diffusion
python scripts/download_models.py --model svd
```

### If You Get "Out of Memory" Errors
Edit `backend/config.py`:
```python
ENABLE_CPU_OFFLOAD = True  # Change to True
```

## 🐛 Common Issues

### "CUDA not available"
- Make sure you have NVIDIA GPU
- Install CUDA toolkit 11.8+
- Reinstall PyTorch with CUDA support

### "Port already in use"
- Backend: Change PORT in `backend/config.py`
- Frontend: Set PORT environment variable: `PORT=3001 npm start`

### Models downloading slowly
- Check internet connection
- Try downloading during off-peak hours
- Models are 5-10GB each

## 📚 Next Steps

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Star ⭐ the repo if you find it useful!

## 💬 Need Help?

Open an issue on GitHub: https://github.com/shubhamjadhav0715/kling-ai-clone/issues

---

**Happy Video Generating! 🎬**
