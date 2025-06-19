import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


def meteo_settimanale(api_key=OPENWEATHERMAP_API_KEY, lat=46.0674, lon=11.1267):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    def estrai_info_giornaliere(giorno):
        data_str = datetime.utcfromtimestamp(giorno['dt']).strftime('%A %d %B %Y')
        return {
            'data': data_str,
            'summary': giorno.get('summary', 'N/A'),
            'descrizione': giorno['weather'][0]['description'],
            'temperatura': {
                'min': giorno['temp']['min'],
                'max': giorno['temp']['max'],
                'giorno': giorno['temp']['day']
            },
            'pioggia_mm': giorno.get('rain', 0),
            'umidità_%': giorno['humidity'],
            'vento_kmh': round(giorno['wind_speed'] * 3.6, 1),
            'indice_UV': giorno['uvi']
        }

    previsioni_giornaliere = data.get('daily', [])
    report = [estrai_info_giornaliere(g) for g in previsioni_giornaliere]

    output_lines = []
    for giorno in report:
        output_lines.append(f"{giorno['data']}")
        output_lines.append(f"Riassunto: {giorno['summary']}")
        output_lines.append(f"Meteo: {giorno['descrizione'].capitalize()}")
        output_lines.append(f"Temp: {giorno['temperatura']['min']}°C - {giorno['temperatura']['max']}°C (giorno: {giorno['temperatura']['giorno']}°C)")
        output_lines.append(f"Umidità: {giorno['umidità_%']}%")
        output_lines.append(f"Vento: {giorno['vento_kmh']} km/h")
        output_lines.append(f"Pioggia: {giorno['pioggia_mm']} mm")
        output_lines.append("")  # Riga vuota tra i giorni

    return '\n'.join(output_lines)
