"""
Text-to-Video Generator
Generates videos from text prompts using AI models
"""

import torch
from PIL import Image
import numpy as np
from pathlib import Path
import imageio

class TextToVideoGenerator:
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.pipe = None
        self.load_model()
    
    def load_model(self):
        """Load the text-to-video model"""
        try:
            self.pipe = self.model_loader.load_text_to_video()
        except Exception as e:
            print(f"⚠️  Could not load text-to-video model: {e}")
            print("📝 Falling back to image generation + SVD pipeline")
            # Fallback: We'll generate an image first, then use SVD
            self.pipe = None
    
    def generate(self, prompt, num_frames=24, fps=8, output_path=None, progress_callback=None):
        """
        Generate video from text prompt
        
        Args:
            prompt: Text description of the video
            num_frames: Number of frames to generate
            fps: Frames per second
            output_path: Where to save the video
            progress_callback: Function to call with progress updates
        
        Returns:
            dict with output_path and metadata
        """
        if progress_callback:
            progress_callback(10)
        
        print(f"🎬 Generating video from prompt: '{prompt}'")
        
        if self.pipe is None:
            # Fallback method: Generate image first, then animate
            return self._generate_via_image(prompt, num_frames, fps, output_path, progress_callback)
        
        try:
            # Generate video frames
            if progress_callback:
                progress_callback(30)
            
            video_frames = self.pipe(
                prompt,
                num_frames=num_frames,
                num_inference_steps=25,
                guidance_scale=9.0
            ).frames
            
            if progress_callback:
                progress_callback(80)
            
            # Save video
            if output_path is None:
                output_path = f"output_{hash(prompt)}.mp4"
            
            self._save_video(video_frames[0], output_path, fps)
            
            if progress_callback:
                progress_callback(100)
            
            print(f"✅ Video saved to: {output_path}")
            
            return {
                'output_path': output_path,
                'num_frames': num_frames,
                'fps': fps,
                'prompt': prompt
            }
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            raise
    
    def _generate_via_image(self, prompt, num_frames, fps, output_path, progress_callback):
        """
        Fallback: Generate image first, then animate with SVD
        """
        from diffusers import StableDiffusionPipeline
        
        print("📸 Generating initial image from prompt...")
        
        # Load Stable Diffusion for image generation
        sd_pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=self.model_loader.get_dtype()
        ).to(self.model_loader.get_device())
        
        if progress_callback:
            progress_callback(20)
        
        # Generate image
        image = sd_pipe(prompt, num_inference_steps=30).images[0]
        
        if progress_callback:
            progress_callback(40)
        
        # Now animate the image using SVD
        print("🎞️  Animating image with Stable Video Diffusion...")
        svd_pipe = self.model_loader.load_stable_video_diffusion()
        
        if progress_callback:
            progress_callback(60)
        
        frames = svd_pipe(
            image,
            num_frames=num_frames,
            decode_chunk_size=8
        ).frames[0]
        
        if progress_callback:
            progress_callback(90)
        
        # Save video
        if output_path is None:
            output_path = f"output_{hash(prompt)}.mp4"
        
        self._save_video(frames, output_path, fps)
        
        if progress_callback:
            progress_callback(100)
        
        print(f"✅ Video saved to: {output_path}")
        
        return {
            'output_path': output_path,
            'num_frames': num_frames,
            'fps': fps,
            'prompt': prompt
        }
    
    def _save_video(self, frames, output_path, fps):
        """Save frames as video file"""
        # Convert PIL images to numpy arrays if needed
        if isinstance(frames[0], Image.Image):
            frames = [np.array(frame) for frame in frames]
        
        # Save as MP4
        imageio.mimsave(output_path, frames, fps=fps, codec='libx264')
