# 📝 MeetBrief: Government Meeting Summarizer

An automated meeting and summarization platform that allows users to upload meeting recordings (MP3/MP4). The backend processes the recording using WhisperX for transcription and a fine-tuned BART model for summarization. The frontend displays the transcript and summarized content in an intuitive user interface.

## 🚀 Features

- ✅ Upload meeting recordings in **MP3** or **MP4** format.
- 🎥 Automatic **video-to-audio** conversion using FFmpeg.
- 🎤 Accurate transcription using **WhisperX**.
- 📄 Summarization with a **fine-tuned BART** model.
- 🧑‍💻 User-friendly **UI** built with **React, TypeScript, and Tailwind CSS**.
- 📊 Display full **transcripts** and **summaries** for easy review.

## 🧰 Tech Stack

### Frontend
- ⚛️ React
- 🟦 TypeScript
- 🎨 Tailwind CSS

### Backend
- 🐍 Flask (Python)
- 🎤 WhisperX (for transcription)
- 📄 Fine-tuned BART (for summarization)
- 🎥 FFmpeg (for video-to-audio conversion)

## 📌 Installation

### Prerequisites

- 🐍 Python 3.10+
- 📦 Node.js 20+
- 🎥 FFmpeg installed on your system

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/nitesh-0/meetbrief.git
   cd meeting-summarization/backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:

   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend folder:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

## 📂 Directory Structure

```
meeting-summarization/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── models/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## 📡 API Endpoints

### 📤 POST `/upload`

- **Description:** Uploads a meeting recording for transcription and summarization.

- **Request:**

    ```json
    {
      "file": "meeting.mp4"
    }
    ```

- **Response:**

    ```json
    {
      "transcript": "Full meeting transcript",
      "summary": "Concise meeting summary"
    }
    ```

## 🤝 Contributing

Contributions are welcome! Feel free to **open an issue** or **submit a pull request**.

## 📜 License

This project is licensed under the **MIT License**.

## 🙌 Acknowledgements

- [OpenAI WhisperX](https://github.com/openai/whisper)
- [Hugging Face Transformers](https://huggingface.co/)
- [FFmpeg](https://ffmpeg.org/)