"""
Image-to-Video Generator
Animates static images into videos using Stable Video Diffusion
"""

import torch
from PIL import Image
import numpy as np
import imageio

class ImageToVideoGenerator:
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.pipe = self.model_loader.load_stable_video_diffusion()
    
    def generate(self, image_path, num_frames=25, fps=8, output_path=None, progress_callback=None):
        """
        Generate video from image
        
        Args:
            image_path: Path to input image
            num_frames: Number of frames to generate
            fps: Frames per second
            output_path: Where to save the video
            progress_callback: Function to call with progress updates
        
        Returns:
            dict with output_path and metadata
        """
        if progress_callback:
            progress_callback(10)
        
        print(f"🖼️  Loading image: {image_path}")
        
        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        
        # Resize to optimal size (SVD works best with 1024x576)
        image = image.resize((1024, 576))
        
        if progress_callback:
            progress_callback(30)
        
        print(f"🎬 Generating {num_frames} frames...")
        
        try:
            # Generate video frames
            frames = self.pipe(
                image,
                num_frames=num_frames,
                decode_chunk_size=8,
                num_inference_steps=25,
                min_guidance_scale=1.0,
                max_guidance_scale=3.0
            ).frames[0]
            
            if progress_callback:
                progress_callback(80)
            
            # Save video
            if output_path is None:
                output_path = f"output_{hash(image_path)}.mp4"
            
            self._save_video(frames, output_path, fps)
            
            if progress_callback:
                progress_callback(100)
            
            print(f"✅ Video saved to: {output_path}")
            
            return {
                'output_path': output_path,
                'num_frames': num_frames,
                'fps': fps,
                'input_image': image_path
            }
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            raise
    
    def _save_video(self, frames, output_path, fps):
        """Save frames as video file"""
        # Convert PIL images to numpy arrays if needed
        if isinstance(frames[0], Image.Image):
            frames = [np.array(frame) for frame in frames]
        
        # Save as MP4
        imageio.mimsave(output_path, frames, fps=fps, codec='libx264')
