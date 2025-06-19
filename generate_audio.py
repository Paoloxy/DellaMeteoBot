# === CONVERSIONE AUDIO IN MESSAGGIO VOCALE ===
import os
import tempfile
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "0uuAbiObbJtLqLtrmdck"  # inserisci la tua voice_id

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
import tempfile


def generate_audio(text: str) -> str:
    print("[generate_audio] Invio richiesta a ElevenLabs...")
    # Genera audio con il modello v2 e voice_settings
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Salva temporaneamente l'MP3
    mp3_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    with open(mp3_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    print(f"[generate_audio] Audio MP3 salvato in {mp3_path}")

    # Converti l'MP3 in OGG Opus per Telegram
    ogg_path = mp3_path.replace(".mp3", ".ogg")
    AudioSegment.from_mp3(mp3_path).export(ogg_path, format="ogg", codec="libopus")
    print(f"[generate_audio] Audio convertito in formato OGG per Telegram: {ogg_path}")

    return ogg_path