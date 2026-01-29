import React, { useState } from 'react';
import axios from 'axios';
import './VideoGenerator.css';

function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [numFrames, setNumFrames] = useState(24);
  const [fps, setFps] = useState(8);
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  const examplePrompts = [
    "A serene lake with mountains in the background at sunset",
    "A cat walking on a beach, waves gently crashing",
    "Drone footage flying over a dense forest",
    "Time-lapse of clouds moving across a blue sky",
    "A flower blooming in fast motion"
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(0);
    setVideoUrl(null);

    try {
      const response = await axios.post('/api/generate/text-to-video', {
        prompt,
        num_frames: numFrames,
        fps
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
    <div className="video-generator">
      <h2>Generate Video from Text</h2>
      <p className="description">
        Describe the video you want to create and our AI will generate it for you.
      </p>

      <div className="form-group">
        <label>Prompt</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your video... (e.g., 'A cat walking on a beach at sunset')"
          rows={4}
          disabled={loading}
        />
      </div>

      <div className="example-prompts">
        <p>Try these examples:</p>
        <div className="prompt-chips">
          {examplePrompts.map((example, index) => (
            <button
              key={index}
              className="prompt-chip"
              onClick={() => setPrompt(example)}
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <div className="settings-row">
        <div className="form-group">
          <label>Number of Frames: {numFrames}</label>
          <input
            type="range"
            min="16"
            max="48"
            value={numFrames}
            onChange={(e) => setNumFrames(parseInt(e.target.value))}
            disabled={loading}
          />
          <small>More frames = longer video but slower generation</small>
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
          <p className="progress-text">{progress}% - Generating your video...</p>
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
        disabled={loading || !prompt.trim()}
      >
        {loading ? '⏳ Generating...' : '🎬 Generate Video'}
      </button>
    </div>
  );
}

export default VideoGenerator;
