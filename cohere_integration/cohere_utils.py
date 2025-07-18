from config.settings import COHERE_TOKEN
import cohere

co = cohere.Client(COHERE_TOKEN)

def get_event(userinput):
    prompt = f"""
    Extraé el evento, la fecha y la hora del siguiente mensaje con el formato fecha (Dia/Mes) y hora (Hora:Minuto), 
    
    Mensaje:"{userinput}"
    
    Respuesta en JSON:
    """
    
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )
    
    return response.generations[0].text.strip()