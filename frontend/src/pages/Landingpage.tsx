import { useState } from "react";

export default function Landing() {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      setSummary("This is the generated summary of your meeting. It provides key points and insights.");
      setLoading(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen w-full flex flex-col bg-gradient-to-r from-blue-100 to-purple-200">
      {/* Main Title */}
      <h1 className="text-5xl font-bold text-gray-900 text-center py-8">Meeting Summarizer</h1>

      <div className="flex flex-1 w-full">
        {/* Left Section: Upload */}
        <div className="w-1/2 h-screen flex flex-col items-center justify-center bg-white shadow-lg p-10">
          <p className="text-lg text-gray-700 mb-8">Upload your meeting video or audio file to generate a concise summary.</p>
          <input
            type="file"
            accept="video/*,audio/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-700 file:mr-4 file:py-3 file:px-6 file:border-0 file:bg-indigo-500 file:text-white file:rounded-lg hover:file:bg-indigo-600"
          />
          <button
            onClick={handleUpload}
            className="mt-6 w-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-3 rounded-xl hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50"
            disabled={!file || loading}
          >
            {loading ? "Processing..." : "Upload & Summarize"}
          </button>
        </div>

        {/* Right Section: Summary */}
        <div className="w-1/2 h-screen bg-white shadow-lg p-10 overflow-y-auto">
          <h2 className="text-3xl font-semibold text-gray-900 mb-6">Summary</h2>
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {summary || "Your meeting summary will appear here once it's generated."}
          </p>
        </div>
      </div>
    </div>
  );
}