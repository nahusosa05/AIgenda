from config.settings import COHERE_TOKEN
import cohere, datetime, json

co = cohere.Client(COHERE_TOKEN)

def get_event(userinput: str):
    prompt = f"""
    Extraé el evento, la fecha y la hora del siguiente mensaje. Respondé solamente en formato JSON, con los siguientes campos:
    - "evento": qué hay que hacer.
    - "fecha": en formato DD/MM (día/mes).
    - "hora": en formato HH:MM (hora:minuto). Si no se menciona la hora, poné "Sin hora".

    Si la fecha está escrita en forma relativa (por ejemplo "este domingo", "mañana", "el viernes que viene"), calculá la fecha correspondiente basándote en el día de hoy.

    Hoy es {datetime.date.today().strftime('%A %d/%m')}. Usá esa fecha para calcular los días relativos.

    Mensaje: "{userinput}"
    Respuesta:
    """
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=100,
            temperature=0.3
        )
        text = response.generations[0].text.strip()
        json_response = json.loads(text)
        return json_response
    
    except json.JSONDecodeError:
        return {
            "evento": "Formato no reconocido",
            "fecha": "??/??",
            "hora": "Sin hora"
        }

    except cohere.CohereAPIError as e:
        if e.status_code == 429:
            return "⚠️ Límite de uso alcanzado. Esperá un minuto e intentá de nuevo."
        else:
            raise