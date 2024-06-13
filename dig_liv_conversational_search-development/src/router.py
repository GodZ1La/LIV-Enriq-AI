
from src.chains  import _get_initial_router_model_call_chain
from src.chains  import get_hello_generator_chain
from src.chains  import get_farewell_generator_chain
from src.chains  import get_fallback_generator_chain
from src.chains  import get_recomendation_generator_chain
from src.chains  import get_pregfrecuentes_chain
from langchain_core.runnables import RunnableLambda


def handleRecommendation(result):
    print(f'Result from Recommendation Prompt {result}')

def get_initial_router_chain(parameters):
    initial_router_model_call_chain = _get_initial_router_model_call_chain(
        prompt_filename=parameters.get("initial_router_prompt_filename"),
        model_name=parameters.get("initial_router_model_name"),
        max_output_tokens=parameters.get("initial_router_max_output_tokens"),
        temperature=parameters.get("initial_router_temperature"),
        top_p=parameters.get("initial_router_top_p"),
        top_k=parameters.get("initial_router_top_k"),
        project_id=parameters.get("project_id")   
    )
        # Define Hello Chain
    hello_intent_chain = get_hello_generator_chain(
        prompt_filename=parameters.get("hello_generator_prompt_filename"),
        model_name=parameters.get("hello_generator_model_name"),
        max_output_tokens=parameters.get("hello_generator_max_output_tokens"),
        temperature=parameters.get("hello_generator_temperature"),
        top_p=parameters.get("hello_generator_top_p"),
        top_k=parameters.get("hello_generator_top_k"),
        project_id=parameters.get("project_id")
    )

    # Define Farewell Chain
    farewell_intent_chain = get_farewell_generator_chain(
        prompt_filename=parameters.get("farewell_generator_prompt_filename"),
        model_name=parameters.get("farewell_generator_model_name"),
        max_output_tokens=parameters.get("farewell_generator_max_output_tokens"),
        temperature=parameters.get("farewell_generator_temperature"),
        top_p=parameters.get("farewell_generator_top_p"),
        top_k=parameters.get("farewell_generator_top_k"),
        project_id=parameters.get("project_id")
    )

    # Define Fallback Chain
    fallback_intent_chain = get_fallback_generator_chain(
        prompt_filename=parameters.get("fallback_generator_prompt_filename"),
        model_name=parameters.get("fallback_generator_model_name"),
        max_output_tokens=parameters.get("fallback_generator_max_output_tokens"),
        temperature=parameters.get("fallback_generator_temperature"),
        top_p=parameters.get("fallback_generator_top_p"),
        top_k=parameters.get("fallback_generator_top_k"),
        project_id=parameters.get("project_id")
    )
    # Define recomendation chain
    recomendation_intent_chain = get_recomendation_generator_chain(
        prompt_filename=parameters.get("recomendation_generator_prompt_filename"),
        model_name=parameters.get("recomendation_generator_model_name"),
        max_output_tokens=parameters.get("recomendation_generator_max_output_tokens"),
        temperature=parameters.get("recomendation_generator_temperature"),
        top_p=parameters.get("recomendation_generator_top_p"),
        top_k=parameters.get("recomendation_generator_top_k"),
        project_id=parameters.get("project_id")
    )
     # Define recomendation pregfrec
    pregfrecuentes_chain = get_pregfrecuentes_chain(
        prompt_filename=parameters.get("pregfrecuentes_generator_prompt_filename"),
        model_name=parameters.get("pregfrecuentes_generator_model_name"),
        max_output_tokens=parameters.get("pregfrecuentes_generator_max_output_tokens"),
        temperature=parameters.get("pregfrecuentes_generator_temperature"),
        top_p=parameters.get("pregfrecuentes_generator_top_p"),
        top_k=parameters.get("pregfrecuentes_generator_top_k"),
        project_id=parameters.get("project_id")
    )


    def route(info):
        print(f'***ROUTER INVOKED*** {info["topic"]}')
        if "INTENCION_SALUDO" in info["topic"].upper():
            return hello_intent_chain
        elif "INTENCION_DESPEDIDA" in info["topic"].upper():
            return farewell_intent_chain
        elif "INTENCION_RECOMENDACION_PRODUCTO" in info["topic"].upper():
            return recomendation_intent_chain
        elif "INTENCION_FALLBACK" in info["topic"].upper():
            return fallback_intent_chain
        elif "INTENCION_PREGUNTAS_FRECUENTES" in info["topic"].upper():
            return pregfrecuentes_chain
        else:
            return fallback_intent_chain
    
    full_chain = {"topic": initial_router_model_call_chain,
                  "name" : lambda x: x["name"],
                  "query": lambda x: x["query"],
                  "conversationHistory" : lambda x: x["conversationHistory"],
                  "nombre_promocion" : lambda x: x["nombre_promocion"]} | RunnableLambda(route)
    ##print(full_chain)   
    return full_chain

def get_router(parameters):
    initial_router_model_call_chain = _get_initial_router_model_call_chain(
        prompt_filename=parameters.get("initial_router_prompt_filename"),
        model_name=parameters.get("initial_router_model_name"),
        max_output_tokens=parameters.get("initial_router_max_output_tokens"),
        temperature=parameters.get("initial_router_temperature"),
        top_p=parameters.get("initial_router_top_p"),
        top_k=parameters.get("initial_router_top_k"),
        project_id=parameters.get("project_id")   
    )
    return initial_router_model_call_chain