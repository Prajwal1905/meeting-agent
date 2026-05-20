import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = "http://127.0.0.1:8001";

export default function Upload() {
  const [mode, setMode] = useState("audio");
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAudioUpload = async () => {
    if (!file) return setError("Please select an audio file");
    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post(`${API}/api/upload`, formData);
      navigate(`/results/${res.data.meeting_id}`, { state: res.data });
    } catch (e) {
      setError("Upload failed. Make sure backend is running.");
    }
    setLoading(false);
  };

  const handleTranscriptUpload = async () => {
    if (!transcript.trim()) return setError("Please paste a transcript");
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(`${API}/api/upload-transcript`, {
        transcript,
      });
      navigate(`/results/${res.data.meeting_id}`, { state: res.data });
    } catch (e) {
      setError("Failed. Make sure backend is running.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-16">
      <h1 className="text-4xl font-bold mb-2">Meeting Intelligence</h1>
      <p className="text-gray-400 mb-10">
        Upload a recording or paste a transcript. AI handles the rest.
      </p>

      <div className="flex gap-4 mb-8">
        <button
          onClick={() => setMode("audio")}
          className={`px-5 py-2 rounded-full text-sm font-medium transition ${mode === "audio" ? "bg-violet-600 text-white" : "bg-gray-800 text-gray-400 hover:text-white"}`}
        >
          Audio Upload
        </button>
        <button
          onClick={() => setMode("transcript")}
          className={`px-5 py-2 rounded-full text-sm font-medium transition ${mode === "transcript" ? "bg-violet-600 text-white" : "bg-gray-800 text-gray-400 hover:text-white"}`}
        >
          Paste Transcript
        </button>
      </div>

      {mode === "audio" ? (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 text-center">
          <div className="text-5xl mb-4">🎙️</div>
          <p className="text-gray-400 mb-6">Supports mp3, mp4, wav, m4a</p>
          <input
            type="file"
            accept="audio/*,video/mp4"
            onChange={(e) => setFile(e.target.files[0])}
            className="hidden"
            id="fileInput"
          />
          <label
            htmlFor="fileInput"
            className="cursor-pointer bg-gray-800 hover:bg-gray-700 px-6 py-3 rounded-xl text-sm transition"
          >
            {file ? file.name : "Choose File"}
          </label>
          {file && (
            <button
              onClick={handleAudioUpload}
              disabled={loading}
              className="mt-6 w-full bg-violet-600 hover:bg-violet-700 py-3 rounded-xl font-medium transition disabled:opacity-50"
            >
              {loading
                ? "Processing... this may take a minute"
                : "Process Meeting"}
            </button>
          )}
        </div>
      ) : (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8">
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Paste your meeting transcript here..."
            className="w-full bg-gray-800 text-white rounded-xl p-4 h-48 resize-none outline-none text-sm"
          />
          <button
            onClick={handleTranscriptUpload}
            disabled={loading}
            className="mt-4 w-full bg-violet-600 hover:bg-violet-700 py-3 rounded-xl font-medium transition disabled:opacity-50"
          >
            {loading ? "Processing... please wait" : "Process Transcript"}
          </button>
        </div>
      )}

      {error && <p className="mt-4 text-red-400 text-sm">{error}</p>}
    </div>
  );
}
