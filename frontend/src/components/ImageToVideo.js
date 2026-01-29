import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import './ImageToVideo.css';

function ImageToVideo() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [numFrames, setNumFrames] = useState(25);
  const [fps, setFps] = useState(8);
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxFiles: 1,
    disabled: loading
  });

  const handleGenerate = async () => {
    if (!image) {
      setError('Please upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(0);
    setVideoUrl(null);

    const formData = new FormData();
    formData.append('image', image);
    formData.append('num_frames', numFrames);
    formData.append('fps', fps);

    try {
      const response = await axios.post('/api/generate/image-to-video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const newJobId = response.data.job_id;
      setJobId(newJobId);

      // Poll for status
      pollJobStatus(newJobId);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start generation');
      setLoading(false);
    }
  };

  const pollJobStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/status/${id}`);
        const status = response.data;

        setProgress(status.progress || 0);

        if (status.status === 'completed') {
          clearInterval(interval);
          setLoading(false);
          setVideoUrl(`/api/download/${id}`);
        } else if (status.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
          setError(status.error || 'Generation failed');
        }
      } catch (err) {
        clearInterval(interval);
        setLoading(false);
        setError('Failed to check status');
      }
    }, 2000);
  };

  return (
    <div className="image-to-video">
      <h2>Animate Your Images</h2>
      <p className="description">
        Upload an image and watch it come to life with AI-powered animation.
      </p>

      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''} ${loading ? 'disabled' : ''}`}>
        <input {...getInputProps()} />
        {imagePreview ? (
          <div className="image-preview">
            <img src={imagePreview} alt="Preview" />
            {!loading && <p className="change-text">Click or drag to change image</p>}
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="upload-icon">📤</div>
            <p>Drag & drop an image here, or click to select</p>
            <small>Supports: PNG, JPG, JPEG, WebP</small>
          </div>
        )}
      </div>

      <div className="settings-row">
        <div className="form-group">
          <label>Number of Frames: {numFrames}</label>
          <input
            type="range"
            min="14"
            max="50"
            value={numFrames}
            onChange={(e) => setNumFrames(parseInt(e.target.value))}
            disabled={loading}
          />
          <small>More frames = smoother animation but slower generation</small>
        </div>

        <div className="form-group">
          <label>FPS: {fps}</label>
          <input
            type="range"
            min="4"
            max="24"
            value={fps}
            onChange={(e) => setFps(parseInt(e.target.value))}
            disabled={loading}
          />
          <small>Frames per second</small>
        </div>
      </div>

      <div className="video-info">
        <p>Video duration: ~{(numFrames / fps).toFixed(1)} seconds</p>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {loading && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
          <p className="progress-text">{progress}% - Animating your image...</p>
        </div>
      )}

      {videoUrl && (
        <div className="result-container">
          <h3>✅ Video Generated Successfully!</h3>
          <video controls src={videoUrl} className="generated-video" />
          <a href={videoUrl} download className="download-button">
            📥 Download Video
          </a>
        </div>
      )}

      <button
        className="generate-button"
        onClick={handleGenerate}
        disabled={loading || !image}
      >
        {loading ? '⏳ Animating...' : '🎬 Animate Image'}
      </button>
    </div>
  );
}

export default ImageToVideo;
