"""
Model Loader - Handles loading and caching of AI models
"""

import torch
from diffusers import StableVideoDiffusionPipeline, DiffusionPipeline
from pathlib import Path
import os

class ModelLoader:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.loaded_models = {}
        
        print(f"🖥️  Device: {self.device}")
        if self.device == "cuda":
            print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    
    def load_stable_video_diffusion(self, model_id="stabilityai/stable-video-diffusion-img2vid-xt"):
        """Load Stable Video Diffusion model"""
        if model_id in self.loaded_models:
            return self.loaded_models[model_id]
        
        print(f"📥 Loading {model_id}...")
        
        pipe = StableVideoDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            variant="fp16" if self.device == "cuda" else None
        )
        
        pipe = pipe.to(self.device)
        
        # Optimizations
        if self.device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()
            
            # Try to enable xformers if available
            try:
                pipe.enable_xformers_memory_efficient_attention()
                print("✅ xformers enabled")
            except:
                print("⚠️  xformers not available")
        
        self.loaded_models[model_id] = pipe
        print(f"✅ Model loaded: {model_id}")
        
        return pipe
    
    def load_text_to_video(self, model_id="damo-vilab/text-to-video-ms-1.7b"):
        """Load Text-to-Video model"""
        if model_id in self.loaded_models:
            return self.loaded_models[model_id]
        
        print(f"📥 Loading {model_id}...")
        
        pipe = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            variant="fp16" if self.device == "cuda" else None
        )
        
        pipe = pipe.to(self.device)
        
        # Optimizations
        if self.device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()
        
        self.loaded_models[model_id] = pipe
        print(f"✅ Model loaded: {model_id}")
        
        return pipe
    
    def unload_model(self, model_id):
        """Unload a model to free memory"""
        if model_id in self.loaded_models:
            del self.loaded_models[model_id]
            if self.device == "cuda":
                torch.cuda.empty_cache()
            print(f"🗑️  Model unloaded: {model_id}")
    
    def get_device(self):
        """Get current device"""
        return self.device
    
    def get_dtype(self):
        """Get current dtype"""
        return self.dtype
