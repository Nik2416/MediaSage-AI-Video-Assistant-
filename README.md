AI Meeting Assistant 🎙️
An AI-powered meeting and video intelligence application built with Python. It converts YouTube videos and local audio/video recordings into structured, searchable meeting insights.

The application transcribes speech, generates summaries, extracts action items and decisions, and lets users ask questions about the transcript through a Retrieval-Augmented Generation (RAG) chatbot.
✨ Features
- YouTube and local media input: Process a YouTube URL or upload an audio/video file.
- English transcription: Transcribe audio locally using OpenAI Whisper.
- Hindi and Hinglish transcription: Use Sarvam AI for Hindi/Hinglish speech transcription.
- Meeting summaries: Generate concise, structured summaries in bullet points.
- Action-item extraction: Identify tasks, assigned owners, and deadlines when mentioned.
- Decision extraction: Highlight important decisions made during the meeting.
- Open questions: Identify unresolved questions and follow-up points.
- Chat with your meeting: Ask questions about the transcript using RAG, LangChain, and ChromaDB.
- Report export: Export meeting results as PDF or TXT files.
🧰 Tech Stack
Component	Technology
Programming language	Python
English speech-to-text	OpenAI Whisper (local)
Hindi/Hinglish speech-to-text	Sarvam AI
LLM	Mistral AI
LLM orchestration	LangChain (LCEL)
Embeddings	Hugging Face Sentence Transformers
Vector database	ChromaDB
Audio/video processing	FFmpeg, pydub, yt-dlp
User interface	Streamlit


⚙️ Prerequisites
Before running the project, install:
- Python 3.10–3.12 (recommended)
- FFmpeg
- Git
- A Mistral AI API key
- A Sarvam AI API key (needed for Hindi/Hinglish transcription)
Whisper and Hugging Face embedding models run locally. Their model files may be downloaded the first time you use them. Mistral AI and Sarvam AI require internet access and valid API keys.

🚀 Installation
1. Clone the repository
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
Replace the URL and folder name with your GitHub repository details.
2. Create a virtual environment
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
** macOS / Linux:**
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
4. Install FFmpeg
FFmpeg is a system dependency and is not installed by pip.
- Windows: Download FFmpeg from ffmpeg.org, extract it, and add its bin folder to your system PATH.
- macOS: brew install ffmpeg
- Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg
Verify the installation:
ffmpeg -version
5. Configure API keys
Create a file named .env in the project's root directory:
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key

# Optional configuration (use the names/defaults expected by your code)
WHISPER_MODEL=small
Get your API keys:
- Mistral AI: https://console.mistral.ai/
- Sarvam AI: https://dashboard.sarvam.ai/
Do not upload your .env file or expose your API keys on GitHub.
6. Run the application
Start the Streamlit interface:
streamlit run app.py
Streamlit will display a local URL in the terminal (usually http://localhost:8501). Open it in your browser.

If your project also includes a command-line workflow, run:
python main.py
🧭 How It Works
YouTube URL / Audio / Video File
              |
              v
       Audio Extraction
       (yt-dlp / FFmpeg)
              |
              v
       Audio Processing
        (pydub / chunks)
              |
              v
        Speech-to-Text
     Whisper / Sarvam AI
              |
              v
       Transcript Cleanup
              |
              v
       Mistral AI + LangChain
       /        |          \
  Summary   Action Items   Decisions &
                         Open Questions
              |
              v
       Hugging Face Embeddings
              |
              v
           ChromaDB
              |
              v
        RAG Chat with Meeting
              |
              v
         PDF / TXT Report
📁 Project Structure
The exact filenames can vary depending on your implementation. A typical structure for this project is:
AI-Meeting-Assistant/
│
├── app.py                    # Streamlit user interface
├── main.py                   # Main pipeline / application entry point
├── requirements.txt          # Python dependencies
├── .env                      # API keys (do not commit)
├── .gitignore
│
├── core/
│   ├── transcriber.py        # Whisper and Sarvam transcription
│   ├── translator.py         # Transcript translation/cleanup
│   ├── summarise.py          # Meeting summary generation
│   ├── extractor.py          # Action items, decisions, questions
│   ├── vector_store.py       # Embeddings and ChromaDB storage
│   └── rag_engine.py         # Retrieval and question answering
│
└── utils/
    └── audio_processor.py    # Download, extract, convert, chunk audio
Keep the structure in this section aligned with the actual files in your repository.
💬 Example Questions
After processing a meeting, you can ask:
- What were the main topics discussed?
- What tasks were assigned, and to whom?
- Which deadlines were mentioned?
- What decisions were finalized?
- Which questions are still unresolved?
The assistant should answer using the processed meeting transcript. If a detail was not mentioned, it should say so rather than inventing an answer.
🔐 Privacy and API Notes
- English transcription with Whisper is performed locally on your machine.
- Hindi/Hinglish transcription uses the Sarvam AI service.
- Summarization, extraction, and RAG responses use the configured Mistral AI service.
- Do not process confidential recordings unless you have permission and are comfortable with the services used.
- Never commit .env, API keys, private recordings, transcripts, or generated reports to a public repository.
🛠️ Troubleshooting
FFmpeg not found

Make sure FFmpeg is installed and its bin directory is added to PATH. Restart the terminal after changing PATH.

API authentication error

Check that the API key is correct, active, and loaded from the .env file. Confirm that the variable names match the ones used in your Python code.

Whisper is slow or runs out of memory

Try a smaller model such as tiny or base. Model size affects transcription speed, memory usage, and accuracy.

ChromaDB or embedding model download fails

Check your internet connection for the first model download and ensure that enough disk space is available.

A Python import is missing

Activate the project's virtual environment and reinstall the dependencies:
pip install -r requirements.txt
🔮 Possible Future Improvements
- Speaker diarization and speaker-wise summaries
- Timestamped action items and transcript search
- Support for additional languages
- Compare insights across multiple meetings
- Calendar and meeting-platform integrations
- Real-time meeting transcription
🙌 Acknowledgements
Built with the help of open-source tools and AI platforms, including OpenAI Whisper, LangChain, ChromaDB, Hugging Face, Streamlit, Mistral AI, and Sarvam AI.
Note: This README describes the intended project workflow. Update the repository URL, folder structure, environment-variable names, and run commands to match your final implementation.
