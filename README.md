# QSkill Internship — Project Submissions

One-month internship at QSkill. This repository contains 3 completed mini-projects, each in its own folder with independent setup and dependencies.

## Table of Contents

- [Projects](#projects)
  - [1. Matrix Operations Tool](#1-matrix-operations-tool)
  - [2. Sentiment Analysis Web App](#2-sentiment-analysis-web-app)
  - [3. Voice-Activated Personal Assistant](#3-voice-activated-personal-assistant)
- [Repository Structure](#repository-structure)
- [General Setup](#general-setup)

---

## Projects

### 1. Matrix Operations Tool

A desktop GUI application for performing matrix operations, built with Tkinter and NumPy.

**Features**
- Addition, Subtraction, Multiplication
- Transpose, Determinant
- Dynamic input grid generation based on user-specified dimensions
- Real-time validation of matrix dimension compatibility per operation

**Tech Stack**
| Component | Library |
|---|---|
| GUI | `tkinter` |
| Computation | `numpy` |

**Setup & Run**
```bash
cd Matrix_operation_tool
python -m venv venv
venv\Scripts\activate          # Windows
pip install numpy
python MatrixOperationsTool.py
```

**Usage**
1. Select an operation via radio button (Addition, Subtraction, Multiplication, Transpose, Determinant)
2. Enter the row/column dimensions for the required matrix/matrices
3. Click **Next** to generate the input grid
4. Fill in matrix values and click **Calculate**
5. Result is displayed in the output panel

---

### 2. Sentiment Analysis Web App

A Flask web application that classifies user-submitted text as Positive, Negative, or Neutral using TextBlob, displaying polarity and subjectivity scores.

**Features**
- Text sentiment classification (Positive / Negative / Neutral)
- Polarity score (-1.0 to +1.0)
- Subjectivity score (0.0 to 1.0)
- Input validation with inline error display

**Tech Stack**
| Component | Library |
|---|---|
| Backend | `Flask` |
| NLP | `TextBlob` |
| Frontend | HTML, CSS, vanilla JS |
| Config | `python-dotenv` |

**Setup & Run**
```bash
cd Sentiment_analysis
python -m venv venv
venv\Scripts\activate           # Windows
pip install flask textblob python-dotenv
python -m textblob.download_corpora
python SentimentAnalysis.py
```

Visit `http://127.0.0.1:5000` in your browser.

**Environment Variables**
A `.env` file is auto-generated on first run if missing:
```
FLASK_API_KEY=
```

---

### 3. Voice-Activated Personal Assistant

A voice-controlled assistant that handles reminders, weather lookups, and news headlines using speech recognition and text-to-speech.

**Features**
- Voice input via microphone (Speech-to-Text, offline via Whisper)
- Spoken responses (Text-to-Speech)
- Real-time weather lookup (WeatherAPI) with locale-based country detection
- Latest news headlines (NewsAPI) with fallback on failed lookups
- Timed reminders via background multiprocessing (non-blocking)
- Spoken-number parsing ("five minutes" → `5`)
- Runtime microphone switching via keyboard shortcut

**Tech Stack**
| Component | Library |
|---|---|
| Speech-to-Text | `SpeechRecognition` + `openai-whisper` |
| Text-to-Speech | `pyttsx3` |
| Weather Data | [WeatherAPI](https://www.weatherapi.com/) |
| News Data | [NewsAPI](https://newsapi.org/) |
| Reminders | `multiprocessing` |
| Number parsing | `word2number` |
| Config | `python-dotenv` |

**Setup & Run**
```bash
cd VoiceActivatedPersonalAssistant
python -m venv venv
venv\Scripts\activate           # Windows
pip install SpeechRecognition[audio] pyttsx3 requests python-dotenv word2number openai-whisper keyboard
python VoiceAssistant.py
```

> **Note:** Use Python 3.11 or 3.12. `PyAudio` does not have precompiled wheels for Python 3.14 and will fail to build. If `pip install` fails, install via `pipwin install pyaudio` instead.

**Environment Variables**
Create a `.env` file in the project folder (auto-generated on first run if missing):
```
WEATHER_API_URL=https://api.weatherapi.com/v1
WEATHER_API=
NEWS_API_URL=https://newsapi.org/v2/everything
NEWS_API=
```

**Voice Commands**
| Say | Action |
|---|---|
| "weather" | Speaks current weather and forecast for your locale's country |
| "news" | Reads top headlines aloud for your locale's country |
| "reminder" | Prompts for a task name and duration, then sets a background reminder |
| "exit" / "quit" | Closes the assistant |

**Keyboard Shortcut**
| Key | Action |
|---|---|
| `m` | Switch active microphone device at runtime |

---

## Repository Structure

```
QSkill/
├── Matrix_operation_tool/
│   ├── MatrixOperationsTool.py
│   ├── Operations.py
│   └── question.txt
├── Sentiment_analysis/
│   ├── SentimentAnalysis.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── index.css
│   │   └── main.js
│   └── question.txt
├── VoiceActivatedPersonalAssistant/
│   ├── VoiceAssistant.py
│   └── question.txt
├── Questions.txt
└── README.md
```

Each project folder is self-contained with its own dependencies and `.env` configuration (where applicable). No shared state between projects.

---

## General Setup

**Prerequisites**
- Python 3.11 or 3.12 (Python 3.14 is **not** recommended — some dependencies like `PyAudio` lack precompiled wheels for it)
- pip

**Clone the repository**
```bash
git clone https://github.com/Azizshahiwala/QSkill.git
cd QSkill
```

Navigate into the relevant project folder and follow its individual setup instructions above. Each project uses its own virtual environment to avoid dependency conflicts.

---

## Author

**Aziz Shahiwala**
Final-year iMScIT, GLS University
[GitHub](https://github.com/Azizshahiwala)
