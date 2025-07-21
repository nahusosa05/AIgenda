WELCOME_MESSAGE = "¡Hola soy AIgenda! ¿En qué te puedo ayudar?"

EVENT_FORMAT_PROMPT = """
    Extraé el evento, la fecha y la hora del siguiente mensaje. Respondé solamente en formato JSON, con los siguientes campos:
    - "evento": qué hay que hacer.
    - "fecha": en formato DD/MM (día/mes).
    - "hora": en formato HH:MM (hora:minuto). Si no se menciona la hora, poné "Sin hora".

    Si la fecha está escrita en forma relativa (por ejemplo "este domingo", "mañana", "el viernes que viene"), calculá la fecha correspondiente basándote en el día de hoy.

    Hoy es {today}. Usá esa fecha para calcular los días relativos.

    Mensaje: "{userinput}"
    """
    
FECHA_ERROR = "Error en fecha, ingrese nuevamente"