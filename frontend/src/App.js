import React, { useState } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError(null);

    try {
      const response = await fetch('https://app-test-lha5.onrender.com/upload', {
  method: 'POST',
  body: formData,
});

      const data = await response.json();

      if (response.ok) {
        const newEntry = {
          url: data.url,
          name: file.name,
          time: new Date().toLocaleString()
        };
        setUploadedFiles([newEntry, ...uploadedFiles]);
        setFile(null);
      } else {
        setError(data.error || 'Upload failed.');
      }
    } catch (err) {
      console.error(err);
      setError('Something went wrong.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h2>Upload a File</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading} style={{ marginLeft: '1rem' }}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p style={{ color: 'red' }}>❌ {error}</p>}
      <br />

      {uploadedFiles.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Uploaded Files</h3>
          <ul>
            {uploadedFiles.map((file, index) => (
              <li key={index}>
                <a href={file.url} target="_blank" rel="noopener noreferrer">
                  {file.name}
                </a>{' '}
                <span style={{ color: 'gray', fontSize: '0.9em' }}>
                  ({file.time})
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
