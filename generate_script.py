import os, datetime
from dotenv import load_dotenv
from openai import OpenAI

# === CONFIG ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
clientOpenAI = OpenAI(api_key=OPENAI_API_KEY)


# === GENERAZIONE TESTO CON OPENAI ===
def generate_script(weather_summary, city_name):
    mese = datetime.datetime.now().month
    day = datetime.datetime.now().day
    prompt = (
        f"Sei un presentatore TV. Genera solamente un discorso di 140 parole, descrivi il meteo settimanale a {city_name} in maniera discorsiva e fluida. Ricordati che oggi è giorno {day} del mese {mese}."
        f"Queste sono le informazioni per il meteo della settimana: {weather_summary}"
        f"Concludi con un simpatico proverbio folkloristico sui friulani, specificando che è un proverbio sui friulani"
    )
    print(f"[generate_script] Prompt:\n{prompt}")
    resp = clientOpenAI.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    result = resp.choices[0].message.content
    print(f"[generate_script] Risultato:\n{result}")
    return result
