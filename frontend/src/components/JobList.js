import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './JobList.css';

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get('/api/jobs');
      setJobs(response.data.jobs.reverse());
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      queued: { emoji: '⏳', class: 'status-queued', text: 'Queued' },
      processing: { emoji: '⚙️', class: 'status-processing', text: 'Processing' },
      completed: { emoji: '✅', class: 'status-completed', text: 'Completed' },
      failed: { emoji: '❌', class: 'status-failed', text: 'Failed' }
    };
    const badge = badges[status] || badges.queued;
    return (
      <span className={`status-badge ${badge.class}`}>
        {badge.emoji} {badge.text}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="job-list">
        <h2>My Videos</h2>
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="job-list">
        <h2>My Videos</h2>
        <div className="empty-state">
          <div className="empty-icon">📹</div>
          <p>No videos generated yet</p>
          <small>Start by creating your first video!</small>
        </div>
      </div>
    );
  }

  return (
    <div className="job-list">
      <h2>My Videos ({jobs.length})</h2>
      <div className="jobs-grid">
        {jobs.map((job) => (
          <div key={job.job_id} className="job-card">
            <div className="job-header">
              {getStatusBadge(job.status)}
              <span className="job-date">
                {new Date(job.created_at).toLocaleDateString()}
              </span>
            </div>

            {job.prompt && (
              <div className="job-prompt">
                <strong>Prompt:</strong> {job.prompt}
              </div>
            )}

            {job.status === 'processing' && (
              <div className="job-progress">
                <div className="progress-bar-small">
                  <div
                    className="progress-fill-small"
                    style={{ width: `${job.progress}%` }}
                  ></div>
                </div>
                <span className="progress-text-small">{job.progress}%</span>
              </div>
            )}

            {job.status === 'completed' && (
              <div className="job-actions">
                <a
                  href={`/api/download/${job.job_id}`}
                  className="action-button download"
                  download
                >
                  📥 Download
                </a>
                <a
                  href={job.output_path}
                  className="action-button view"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  👁️ View
                </a>
              </div>
            )}

            {job.status === 'failed' && job.error && (
              <div className="job-error">
                <small>Error: {job.error}</small>
              </div>
            )}

            <div className="job-id">
              <small>ID: {job.job_id.substring(0, 8)}...</small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default JobList;
