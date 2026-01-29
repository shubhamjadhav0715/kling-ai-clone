import React, { useState } from 'react';
import './App.css';
import VideoGenerator from './components/VideoGenerator';
import ImageToVideo from './components/ImageToVideo';
import JobList from './components/JobList';

function App() {
  const [activeTab, setActiveTab] = useState('text-to-video');

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1 className="logo">
            <span className="logo-icon">🎬</span>
            Kling AI Clone
          </h1>
          <p className="tagline">Open Source Video Generation Platform</p>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'text-to-video' ? 'active' : ''}`}
              onClick={() => setActiveTab('text-to-video')}
            >
              📝 Text to Video
            </button>
            <button
              className={`tab ${activeTab === 'image-to-video' ? 'active' : ''}`}
              onClick={() => setActiveTab('image-to-video')}
            >
              🖼️ Image to Video
            </button>
            <button
              className={`tab ${activeTab === 'jobs' ? 'active' : ''}`}
              onClick={() => setActiveTab('jobs')}
            >
              📋 My Videos
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'text-to-video' && <VideoGenerator />}
            {activeTab === 'image-to-video' && <ImageToVideo />}
            {activeTab === 'jobs' && <JobList />}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>
            Built with ❤️ using Stable Diffusion • 
            <a href="https://github.com/shubhamjadhav0715/kling-ai-clone" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
