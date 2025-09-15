# calling-agent
# 🎙️ Voice Call AI Agent (Django + ElevenLabs + Twilio + Cloudflare Tunnel)

This project is a **Voice-enabled AI Agent** that converts text into natural speech using **ElevenLabs TTS**, hosts the audio via **Django + Cloudflare Tunnel**, and plays it during a **real phone call via Twilio**.  

---

## 🚀 Features
- 🔊 Text-to-Speech using **ElevenLabs** (realistic voices)  
- ☎️ Automated outbound phone calls via **Twilio**  
- 🌐 Public hosting of audio with **Cloudflare Tunnel**  
- 🔐 Token-protected media URLs for secure access  
- ⚡ Simple frontend (HTML/JS) + **Django REST API** backend  

---

## 🏗️ Architecture Flow

1. User provides **text + phone number + voice** via frontend.  
2. Backend calls **ElevenLabs API** → generates MP3.  
3. Audio converted → **8kHz mono WAV** (telephony format).  
4. Django saves file in `/media/tts/` with token protection.  
5. **Cloudflare Tunnel** exposes Django to the internet.  
6. **Twilio** fetches audio URL and plays it during the call.  


---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML + JavaScript  
- **APIs:** ElevenLabs (TTS), Twilio (Programmable Voice)  
- **Tools:** ffmpeg, Cloudflare Tunnel  
- **Security:** Token-based media access  

---

## ⚙️ Setup Instructions

### 1. Clone repo
```bash
git clone https://github.com/your-username/voice-ai-agent.git
cd voice-ai-agent
```
### 2. Create virtual environment & install dependencies
- python -m venv venv
- source venv/bin/activate   # (Linux/Mac)
- venv\Scripts\activate      # (Windows)

- pip install -r requirements.txt

### 3. Environment variables

**Create a .env file:**
- SECRET_KEY=your_django_secret
- DEBUG=True

- ELEVENLABS_API_KEY=your_elevenlabs_key

- TWILIO_ACCOUNT_SID=your_twilio_sid
- TWILIO_AUTH_TOKEN=your_twilio_auth
- TWILIO_NUMBER=+1xxxxxxx

- MEDIA_TOKEN=mysecret123
- TUNNEL_URL=https://your-tunnel.trycloudflare.com

## 4. Run Django server

 - python manage.py migrate 
 - python manage.py runserver 8000

## 5. Start Cloudflare Tunnel

- cloudflared tunnel --url http://localhost:8000

- Copy the public URL and update it in .env (TUNNEL_URL=).

## 6. Trigger a call

- Open index.html in browser.

- Enter Text + Phone Number + Voice.

- Click Generate & Call → Twilio will call your phone and play the audio! 🎉

## 🔒 Security Notes

Do not commit .env file to GitHub.

Use token-protected URLs (?token=mysecret123) to secure media access.

For production, consider AWS S3 presigned URLs instead of local tunnel.
