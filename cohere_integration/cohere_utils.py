from config.settings import COHERE_TOKEN
from config.constants import EVENT_FORMAT_PROMPT
import cohere, datetime, json, dateparser

co = cohere.Client(COHERE_TOKEN)

def get_event(userinput: str):
    today = datetime.datetime.today()
    today_str = today.strftime("%d/%m/%Y")

    prompt = EVENT_FORMAT_PROMPT.format(
        today=today_str,
        userinput=userinput,
    )
    print(f"[Hoy es] {today_str}")
    
    # Posible error en fechas: "domingo que viene" da una fecha 1 día después, verlo mas adelante
    # De momento uso el formato '(fecha relativa o no),(evento)' el mensaje de telegram.
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=100,
            temperature=0.3
        )
        
        text = response.generations[0].text.strip()
        print("Prompt enviado:", prompt)
        print("Respuesta bruta:", text)

        json_response = json.loads(text)

        fecha_raw = json_response.get("fecha", "")
        fecha_parseada = dateparser.parse(
            fecha_raw,
            settings={'RELATIVE_BASE': today}
        )

        if fecha_parseada:
            json_response["fecha"] = fecha_parseada.strftime("%d/%m")
        else:
            json_response["fecha"] = "??/??"

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
