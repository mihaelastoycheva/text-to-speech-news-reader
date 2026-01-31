# Bulgarian News Text-to-Speech App (Streamlit + ElevenLabs)

This project converts Bulgarian text and articles into natural-sounding audio using the ElevenLabs Text-to-Speech API.  
The app provides three ways to generate audio:

1. Paste text directly  
2. Upload a DOCX file  
3. Enter a Lider.bg article URL (title and content are extracted automatically)

Built with Streamlit, optimized for simplicity and productivity.

---

## How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create a .env file and add your ElevenLabs API key
```bash
ELEVENLABS_API_KEY=your_api_key_here
```

### 3. Start the Streamlit app
```bash
streamlit run app.py
```

The app will open in your browser at:
http://localhost:8501

---

## Features

- High-quality Bulgarian speech generation
- DOCX article extraction and conversion
- Automatic extraction of title and article content from Lider.bg 
- Uses the ElevenLabs eleven_multilingual_v2 model 
- Clean and simple Streamlit interface
