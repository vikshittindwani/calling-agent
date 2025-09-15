import os
import tempfile
import subprocess
import shutil
from pathlib import Path
from twilio.rest import Client

import boto3
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from urllib.parse import unquote
import os
from pathlib import Path
from django.conf import settings

def serve_tts(request, filename):
    """
    Serve TTS audio file only if correct ?token= provided
    """
    token = request.GET.get('token')
    if token != os.getenv("MEDIA_TOKEN"):
        return HttpResponseForbidden("Invalid token")

    path = Path(settings.MEDIA_ROOT) / 'tts' / unquote(filename)
    if not path.exists():
        return JsonResponse({"error": "Not found"}, status=404)

    return FileResponse(open(path, 'rb'), content_type='audio/wav')


# index page (serves frontend)
def index(request):
    return render(request, 'api/index.html')


@api_view(['GET'])
def get_voices(request):
    """
    Fetch available voices from ElevenLabs
    """
    try:
        url = "https://api.elevenlabs.io/v1/voices"
        r = requests.get(url, headers={"xi-api-key": settings.ELEVEN_API_KEY}, timeout=15)
        r.raise_for_status()
        return JsonResponse(r.json(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




@api_view(['POST'])
def generate_call(request):
    try:
        data = request.data
        text = data.get('text')
        voice_id = data.get('voiceId')
        to_number = data.get('to')

        if not all([text, voice_id, to_number]):
            return JsonResponse({"error": "Missing text, voiceId or to"}, status=400)

        # ----- Step 1: ElevenLabs TTS -----
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        tts_headers = {
            "xi-api-key": settings.ELEVEN_API_KEY,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json"
        }
        tts_resp = requests.post(tts_url, json={"text": text, "model_id": "eleven_multilingual_v2"}, headers=tts_headers)
        tts_resp.raise_for_status()

        # Save MP3 → convert to WAV
        tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_mp3.write(tts_resp.content)
        tmp_mp3.close()

        tmp_wav = tmp_mp3.name.replace(".mp3", ".wav")
        subprocess.run(['ffmpeg', '-y', '-i', tmp_mp3.name, '-ar', '8000', '-ac', '1', '-c:a', 'pcm_s16le', tmp_wav], check=True)

        # Move WAV file to media/tts/
        media_tts_dir = Path(settings.MEDIA_ROOT) / 'tts'
        media_tts_dir.mkdir(parents=True, exist_ok=True)
        dest_path = media_tts_dir / os.path.basename(tmp_wav)
        shutil.move(tmp_wav, dest_path)
        # after dest_path created
# prefer explicit TUNNEL_URL if set (set it after running localtunnel)
        tunnel_base = os.getenv("TUNNEL_URL") 
        if tunnel_base:
            audio_url = tunnel_base.rstrip('/') + settings.MEDIA_URL + f"tts/{dest_path.name}"
        else:
            audio_url = request.build_absolute_uri(settings.MEDIA_URL + f"tts/{dest_path.name}")

                            

        # Public URL via ngrok
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + "tts/" + dest_path.name)

        # ----- Step 2: Twilio call -----
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Create a TwiML Bin or inline TwiML
        twiml = f"<Response><Play>{audio_url}</Play></Response>"

        # Place call
        call = client.calls.create(
            twiml=twiml,
            to=to_number,
            from_=settings.TWILIO_NUMBER
        )

        return JsonResponse({
            "audioUrl": audio_url,
            "call_sid": call.sid,
            "status": "Call initiated"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
