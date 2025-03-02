import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState<string>('');
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const { data } = await axios.post('http://127.0.0.1:5000/upload', formData);
      setTranscript(data.transcript);
      setSummary(data.summary);
    } catch (error) {
      console.error('Error uploading file', error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-blue-300 to-blue-300 p-6">
      <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-20">Government Meeting Summarizer</h1>

      {/* Upload Section */}
      <div className="flex items-center justify-center mb-6 h-[20vh]">
        <div className="flex flex-col items-center bg-white p-6 rounded-2xl shadow-lg w-1/2">
          <input
            type="file"
            accept="audio/*,video/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="mb-4 border border-gray-300 p-2 rounded-lg"
          />
          <button
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            onClick={handleUpload}
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Upload & Transcribe'}
          </button>
        </div>
      </div>

      {/* Summary & Transcript Section */}
      <div className="grid grid-cols-2 gap-6 flex-1 p-4">
        {/* Summary Box */}
        <div className="bg-white ml-6 p-6 rounded-2xl shadow-lg h-[40vh] overflow-y-auto">
          <h2 className="text-xl text-center font-semibold mb-4">Summary</h2>
          {loading ? <p className="text-gray-500">Loading summary...</p> : <p className="text-gray-800">{summary || 'Summary will appear here'}</p>}
        </div>

        {/* Transcript Box */}
        <div className="bg-white mr-6 p-6 rounded-2xl shadow-lg h-[40vh] overflow-y-auto">
          <h2 className="text-xl text-center font-semibold mb-4">Transcript</h2>
          {loading ? <p className="text-gray-500">Loading transcript...</p> : <p className="text-gray-800">{transcript || 'Transcript will appear here'}</p>}
        </div>
      </div>
    </div>
  );
};

export default App;
