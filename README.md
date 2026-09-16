<img width="733" height="718" alt="Captura de pantalla 2026-09-16 235051" src="https://github.com/user-attachments/assets/fd5a4fc2-b377-40f4-a150-9d28e8af54d4" />
# 🇩🇪 German A2 Quiz & Vocabulary App

A custom desktop application built to combine **Multiplatform Application Development (DAM)** studies with language acquisition. Instead of traditional flashcard software, this tool allows me to test and improve my German A2 vocabulary and grammar interactively while sharpening my Python and SQLite skills.

## 🚀 Features

- **Multi-Tab Interface:** Separates the interactive quiz environment from the database management view.
- **Dynamic Lesson Filtering:** Filter questions by specific chapters (*Kapitel 1*, *Kapitel 2*) or run a mixed grammar session.
- **SQLite Integration:** Local relational database storing phrases, correct answers, and helpful hints.
- **Automated Schema Migration:** Includes logic to check table structures (`PRAGMA table_info`) and update columns dynamically.
- **Real-Time Timers & Feedback:** Countdown timers, instant visual feedback (correct/incorrect states), and score tracking.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** PyQt6
- **Database:** SQLite3

## 📁 Project Structure

```text
german-quiz-app/
│
├── main.py              # Entry point of the application
├── database.db          # SQLite local database
├── ui/                  # Qt Designer UI files / compiled modules
├── assets/              # Icons, styles, or supplementary media
└── requirements.txt     # Python dependencies
