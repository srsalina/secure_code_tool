import React, { useState } from 'react';
import UploadFile from './components/UploadFile';
import Results from './components/Results';
import axios from 'axios';

function App() {
  const [results, setResults] = useState('');

  const handleUpload = (formData) => {
    console.log("Uploading file...");  // Debugging output
    axios.post('http://127.0.0.1:5000/analyze', formData)
      .then((response) => {
        console.log("Received response:", response.data);  // Debugging output
        setResults(response.data);  // Store the entire response, not just `response.data.results`
      })
      .catch((error) => {
        console.error('There was an error analyzing the file!', error);  // Detailed error logging
      });
  };

  return (
    <div>
      <UploadFile onUpload={handleUpload} />
      {results && <Results results={results} />}
    </div>
  );
}

export default App;
