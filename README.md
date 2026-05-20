# 🎵 Emotion-to-Music (MoodTuneAI)

> Deep learning system that detects facial emotions in real time and recommends music that matches your mood.

---

## 📌 Overview

MoodTuneAI combines computer vision and recommendation systems to create a seamless emotion-aware music experience. The system analyzes facial expressions through a camera feed and automatically generates a playlist that matches the detected emotional state.

---

## 🎯 How It Works

```
📸 Camera Input
      │
      ▼
┌─────────────────┐
│  Face Detection │  ← OpenCV / MTCNN
└────────┬────────┘
         │
┌────────▼────────┐
│ Emotion Model   │  ← CNN / Deep Learning
│ (7 emotions)    │     angry, disgust, fear,
└────────┬────────┘     happy, sad, surprise, neutral
         │
┌────────▼────────────────┐
│ Recommendation Engine   │  ← Emotion → Music mapping
│                         │     + playlist generation
└─────────────────────────┘
         │
    🎶 Playlist Output
```

---

## 😊 Supported Emotions

| Emotion | Mapped Music Style |
|---------|-------------------|
| Happy | Upbeat, Pop, Dance |
| Sad | Acoustic, Slow, Ballads |
| Angry | Heavy, Rock, Intense |
| Neutral | Ambient, Lo-fi, Chill |
| Surprised | Dynamic, Varied |
| Fear | Calm, Soothing |
| Disgust | Distraction music |

---

## 🛠️ Tech Stack

- **Deep Learning**: TensorFlow / Keras
- **Computer Vision**: OpenCV
- **Face Detection**: Haar Cascade / MTCNN
- **Language**: Python 3.x
- **Libraries**: `numpy`, `pandas`, `matplotlib`, `tensorflow`, `opencv-python`

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/yassintb20/Emotion-to-Music.git
cd Emotion-to-Music

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📁 Project Structure

```
Emotion-to-Music/
├── data/
│   └── fer2013/              # Facial expression dataset
├── models/
│   └── emotion_model.h5      # Trained CNN weights
├── src/
│   ├── face_detector.py      # Face detection module
│   ├── emotion_classifier.py # Emotion prediction
│   └── recommender.py        # Music recommendation logic
├── notebooks/
│   └── model_training.ipynb  # Training notebook
├── main.py
├── requirements.txt
└── README.md
```

---

## 👤 Author

**Taibi Mohamed Yassine** — [LinkedIn](https://linkedin.com/in/mohammed-yassin-taibi) · [GitHub](https://github.com/yassintb20)
