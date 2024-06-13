from src.router import get_initial_router_chain
from src.router import get_router


def get_parameters():
    # Consider loading this configuration from an external system, like Firebase or Cloud Storage
    return {
        "project_id": "crp-qas-poc-productoideal",
        # Initial Router
        "initial_router_prompt_filename": "chain_init.txt",
        "initial_router_model_name": "gemini-1.5-pro-001",  # text-bison@001
        "initial_router_max_output_tokens": "1024",
        "initial_router_temperature": 0.2,
        "initial_router_top_p": 0.8,
        "initial_router_top_k": 40,
         # Hello Generator
        "hello_generator_prompt_filename": "chain_saludo.txt",
        "hello_generator_model_name": "gemini-1.5-pro-001",  # "gemini-pro"
        "hello_generator_max_output_tokens": "1024",
        "hello_generator_temperature": 0.5,
        "hello_generator_top_p": 0.8,
        "hello_generator_top_k": 40,
        # Farewell Generator
        "farewell_generator_prompt_filename": "chain_despedida.txt",
        "farewell_generator_model_name": "gemini-1.5-pro-001",  # "gemini-pro"
        "farewell_generator_max_output_tokens": "1024",
        "farewell_generator_temperature": 0.5,
        "farewell_generator_top_p": 0.8,
        "farewell_generator_top_k": 40,
        # Fallback Generator
        "fallback_generator_prompt_filename": "chain_fallback.txt",
        "fallback_generator_model_name": "gemini-1.5-pro-001",  # "gemini-pro"
        "fallback_generator_max_output_tokens": "1024",
        "fallback_generator_temperature": 0.2,
        "fallback_generator_top_p": 0.8,
        "fallback_generator_top_k": 40,
        # recomendation Generator
        "recomendation_generator_prompt_filename": "chain_recomendacion.txt",
        "recomendation_generator_model_name": "gemini-1.5-pro-001",  # "gemini-pro"
        "recomendation_generator_max_output_tokens": "1024",
        "recomendation_generator_temperature": 0.2,
        "recomendation_generator_top_p": 0.95,
        "recomendation_generator_top_k": 40,
        # pregfrecuentes Generator
        "pregfrecuentes_generator_prompt_filename": "chain_pregfreq.txt",
        "pregfrecuentes_generator_model_name": "gemini-1.5-pro-001",  # "gemini-pro"
        "pregfrecuentes_generator_max_output_tokens": "1024",
        "pregfrecuentes_generator_temperature": 0.1,
        "pregfrecuentes_generator_top_p": 0.95,
        "pregfrecuentes_generator_top_k": 40,
    }


def buscar_promocion(fecha, fechas_promociones):
  """
  Función que busca a qué diccionario de la lista le corresponde la fecha dada y retorna el nombre de la promoción en una variable.

  Parámetros:
    fecha: La fecha a buscar en formato "yyyy-mm-dd".
    fechas_promociones: Una lista de diccionarios donde cada diccionario contiene la información de una promoción.

  Retorno:
    El nombre de la promoción correspondiente a la fecha dada, o "Ninguna promoción activa" si no se encuentra una coincidencia.
  """

  for promocion in fechas_promociones:
    fecha_inicial = promocion["Fecha_inicial"]
    fecha_final = promocion["Fecha_final"]

    if fecha >= fecha_inicial and fecha <= fecha_final:
      return promocion["Nombre_promocion"]

  return "Ninguna promoción activa"
# Ejemplo de uso

fecha = "2024-05-16"
fechas_promociones = [
  {
    "Nombre_promocion": "Venta Nocturna",
    "Fecha_inicial": "2024-05-29",
    "Fecha_final": "2024-06-30"
  },
  {
    "Nombre_promocion": "Dia de las madres",
    "Fecha_inicial": "2024-05-07",
    "Fecha_final": "2024-05-10"
  },
  {
    "Nombre_promocion": "Hot Sale ",
    "Fecha_inicial": "2024-05-12",
    "Fecha_final": "2024-05-24"
  }
]
def respond(parameters: dict,data:dict ,conversationHistory: str ):
    # query = data.get('query')
    # name = data.get('name')
    # conversationHistory = ["""
    # Usuario: Me gustan los perros
    # Iris: ¡Los perros son increíbles! ¿Estás buscando algo para consentir a tu mascota o te gustaría explorar productos inspirados en perros? 
    # Usuario: Me gustan los perros x2
    # Iris: ¡Entiendo! Te encantan los perros. ¿Buscas algo para tu amigo peludo o te gustaría ver productos con diseños de perritos? 
    # Usuario: No estoy seguro... Mi perrito se está haciendo viejito
    # Iris: Aww, entiendo! Quieres consentir a tu perrito en esta etapa. ¿Buscas algo para hacerlo sentir más cómodo, como una camita ortopédica, o quizás algo para consentirlo con sus sabores favoritos? 
    # Usuario: No estoy seguro, tambien me gustan los gatos
    # Iris:¡Los gatos también son adorables! ¿Quizás te gustaría ver algo para gatitos o prefieres seguir explorando opciones para tu perrito? 
    # """]
    query = data.get('user_query')
    name = data.get('user_name')
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    visitor_id = data.get('user_name')


    fecha = "2024-05-29"
    nombre_promocion = buscar_promocion(fecha, fechas_promociones)
    initial_router_chain = get_initial_router_chain(parameters=parameters)
    print(f'***Historial {conversationHistory}***')
    print(f'***Peticion usario {query}***')
    response = initial_router_chain.invoke({
       "conversationHistory":[conversationHistory] , 
       "query": f"{query} mi visitorId:{visitor_id}, mi loginId:{user_id} y mi sessionId {session_id} "  , 
       "name":name, 
       "nombre_promocion":nombre_promocion
    })
    intent_router=get_router(parameters=parameters)
    intent_response = intent_router.invoke({
       "conversationHistory":[conversationHistory] , 
       "query": f"{query} mi visitorId:{visitor_id}, mi loginId:{user_id} y mi sessionId {session_id} "  , 
       "name":name, 
       "nombre_promocion":nombre_promocion
    })
    return response,intent_response
    
    