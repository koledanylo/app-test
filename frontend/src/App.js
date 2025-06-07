import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [link, setLink] = useState('');
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setLink('');
    setStatus('');
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setStatus('Uploading...');
      const res = await axios.post('http://localhost:5000/upload', formData);
      setLink(res.data.link);
      setStatus('Upload successful!');
    } catch (err) {
      setStatus('Upload failed.');
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h2>Upload a File</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>Upload</button>

      <div style={{ marginTop: '1rem' }}>
        {status && <p>{status}</p>}
        {link && (
          <p>
            Download Link: <a href={link} target="_blank" rel="noreferrer">{link}</a>
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
