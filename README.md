
# Verifier — A Smart Link & Image Verification Tool with Discord Bot & Web Interface


 
A security-focused web application and Discord bot built with Django, REST Framework, and Discord.py that verifies suspicious URLs and images. It checks for malicious or unsafe links using Google Safe Browsing API, fetches site previews using BeautifulSoup, and performs smart image verification based on EXIF metadata and resolution. The project includes a responsive frontend and seamless Discord command integration for real-time verification.




---

## 🎥 Demo Video

Watch the demo here

[![Demo GIF](https://your-image-link.com/demo.gif)](https://github.com/user-attachments/assets/bf08e149-b684-4b25-8268-eccd79ada378)

https://github.com/user-attachments/assets/1ba6d37b-82d3-4127-9f8a-bf4666a8c18e



---


## 🎥 Features


## ✅ Link Verification

- Accepts any URL and resolves its final destination.
- Uses **Google Safe Browsing API** to check for:
  - Malware, phishing, or unsafe content
- Shows:
  - ✅ Safety verdict (`Safe` / `Unsafe` / `Unable to verify`)
  - 📝 Page title & meta description
- Ideal for shortened or suspicious links.

---

## 🖼️ Image Verification (Web Only)

- Upload an image to check for:
  - **EXIF metadata** (software used, capture time)
  - **Resolution & format-based analysis**
- Gives a verdict:
  - `Original`, `Screenshot`, `Edited`, or `AI-generated`
- Helps spot fake, edited, or AI-created images.

---

## 🤖 Discord Bot

- Use `!verifylink <url>` inside Discord to:
  - 🔗 Get final URL
  - ⚠️ Safety check
  - 📝 Site info

> Note: Image verification not supported in Discord (due to metadata stripping).

---

## 🌐 Web Interface

- Built with **HTML + CSS** (no JavaScript)
- Fast, lightweight UI with two pages:
  - Link verification
  - Image verification
- Simple and accessible for all users.

---

## 🔒 Security & Extensibility

- Input validation & edge-case handling
- Modular design for future features:
  - Domain blacklists
  - Screenshot analysis
  - AI-based forgery detection

---







## Technologies
---

## 🛠️ Tech Stack & Tools

- **Python** – Core backend logic and integrations.
- **Django** – Web framework for serving HTML templates and building API endpoints.
- **Django REST Framework** – For creating RESTful APIs used by the frontend and Discord bot.
- **Discord.py** – Python library for interacting with the Discord API and building the bot.
- **HTML & CSS** – Simple, lightweight frontend (no JavaScript used).
- **Pillow (PIL)** – Processes images and extracts EXIF metadata.
- **BeautifulSoup** – Parses and extracts webpage previews (title and meta description).
- **Google Safe Browsing API** – Checks URL safety to detect malware and phishing.
- **Requests** – Handles HTTP calls for web scraping and API communication.
- **re (Regular Expressions)** – Used in the Discord bot to parse and validate user input.







## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/project-name.git
   cd project-name




