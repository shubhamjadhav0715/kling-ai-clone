"""
Model Download Script
Downloads required AI models from Hugging Face
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download
import argparse

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

def download_model(model_id, model_name):
    """Download a model from Hugging Face"""
    print(f"\n{'='*60}")
    print(f"📥 Downloading: {model_name}")
    print(f"🔗 Model ID: {model_id}")
    print(f"{'='*60}\n")
    
    try:
        cache_dir = Config.MODEL_DIR / model_name.replace("/", "_")
        
        snapshot_download(
            repo_id=model_id,
            cache_dir=str(cache_dir),
            resume_download=True,
            local_files_only=False
        )
        
        print(f"\n✅ Successfully downloaded: {model_name}\n")
        return True
    except Exception as e:
        print(f"\n❌ Failed to download {model_name}: {str(e)}\n")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download AI models for Kling AI Clone')
    parser.add_argument(
        '--model',
        type=str,
        choices=['all', 'svd', 'svd-xt', 'text-to-video', 'sd'],
        default='all',
        help='Which model to download (default: all)'
    )
    
    args = parser.parse_args()
    
    # Create model directory
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    print("\n🚀 Kling AI Clone - Model Downloader")
    print(f"📁 Models will be saved to: {Config.MODEL_DIR}\n")
    
    models_to_download = []
    
    if args.model == 'all' or args.model == 'svd':
        models_to_download.append(
            ("stabilityai/stable-video-diffusion-img2vid", "Stable Video Diffusion")
        )
    
    if args.model == 'all' or args.model == 'svd-xt':
        models_to_download.append(
            ("stabilityai/stable-video-diffusion-img2vid-xt", "Stable Video Diffusion XT")
        )
    
    if args.model == 'all' or args.model == 'text-to-video':
        models_to_download.append(
            ("damo-vilab/text-to-video-ms-1.7b", "Text-to-Video")
        )
    
    if args.model == 'all' or args.model == 'sd':
        models_to_download.append(
            ("runwayml/stable-diffusion-v1-5", "Stable Diffusion v1.5")
        )
    
    print(f"📦 Will download {len(models_to_download)} model(s)\n")
    
    success_count = 0
    for model_id, model_name in models_to_download:
        if download_model(model_id, model_name):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"✅ Successfully downloaded: {success_count}/{len(models_to_download)} models")
    print("="*60 + "\n")
    
    if success_count == len(models_to_download):
        print("🎉 All models downloaded successfully!")
        print("🚀 You can now start the server with: python app.py\n")
    else:
        print("⚠️  Some models failed to download.")
        print("💡 You can try downloading them individually or check your internet connection.\n")

if __name__ == "__main__":
    main()
