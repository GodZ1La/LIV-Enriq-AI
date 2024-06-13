from langchain_google_vertexai import VertexAI
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional
#import  src.Prompt_Galery
from typing import Union, Optional
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser

from functools import partial

from src.getter import get_prompt_from_local_filename


from vertexai.preview import reasoning_engines

import json 
import logging
import time
import re

AVAILABLE_MODELS = {
    "gemini-1.5-pro-001": VertexAI,
}

def get_model_class(model_name: str) -> BaseLanguageModel:
    return AVAILABLE_MODELS[model_name]

def get_initialized_model(
    model_name: str,
    max_output_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    location: str = "us-central1",
    project_id: Optional[str] = None,
):
    model_class = AVAILABLE_MODELS[model_name]
    return model_class(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        location=location,
        project=project_id,
    )

#def get_prompt_from_local_filename(filename: str):
#    if filename =='chain_init':
#       return  src.Prompt_Galery.chain_init()
#    elif filename =='chain_saludo':
#       return  src.Prompt_Galery.chain_saludo()
#    elif filename =='chain_despedida':
#       return  src.Prompt_Galery.chain_despedida()
#    elif filename =='chain_fallback':
#       return  src.Prompt_Galery.chain_fallback()
#    elif filename =='chain_recomendacion':
#       return  src.Prompt_Galery.chain_recomendacion()
#    else: print('No hay prompt')


def get_simple_call_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id: str = None,
) -> Union[BaseLanguageModel]:
    prompt_template_str = get_prompt_from_local_filename(prompt_filename)
    model = get_initialized_model(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

    #from langchain.output_parsers import CommaSeparatedListOutputParser

    #output_parser = CommaSeparatedListOutputParser()

    #format_instructions = output_parser.get_format_instructions()

    return PromptTemplate.from_template(prompt_template_str) | model | StrOutputParser()


def retry_function(func, max_retries=2, retry_interval=1, allowed_exceptions=(Exception,)):
    """Retries a function call up to max_retries times if an allowed exception occurs.

    Args:
        func: The function to call.
        max_retries: The maximum number of retry attempts (default: 2).
        retry_interval: The delay in seconds between retry attempts (default: 1).
        allowed_exceptions: A tuple of exception classes to retry on (default: Exception).
    """

    retries = 0

    while retries <= max_retries:
        try:
            result = func()  # Call the function
            return result     # If successful, return the result
        except allowed_exceptions as e:
            retries += 1
            logging.warning(f"Exception occurred: {e}. Retrying... (attempt {retries})")
            if retries <= max_retries:  # Check if we should retry again
                time.sleep(retry_interval)
            else:
                logging.error(f"Max retries reached. Giving up on function {func.__name__}")
                raise  # Re-raise the original exception


def handleRecommendation(result):
    print(f"Funcion handleRecommendation {result}")
    result_map = result.get('result')
    if result_map.get('type') == 'TERMINO_DE_BUSQUEDA':
       ##print(f"Funcion {result_map.get('type')}")
       remote_app = reasoning_engines.ReasoningEngine("projects/937376174852/locations/us-central1/reasoningEngines/5232092051469762560")
       #print(f'remote_app {remote_app}')
       prompt =  get_prompt_from_local_filename('reasoning_eng.txt')
       prompt_val = prompt.replace("{consulta}", result_map.get('text'))
       result_text = remote_app.query(
           input= prompt_val
           #input = """Cuantos niveles tiene este producto 9944370691?"""
       )
       # Extraer la respuesta JSON formateada como cadena y eliminar los delimitadores de Markdown
       output_str = result_text['output'].strip().strip('```json').strip().strip('```')
      # Reemplazar caracteres de escape no válidos
       output_str = output_str.replace('\\n', '').replace('\\"', '"')
       #print(f'output_str {output_str}')

       # Parsear la cadena JSON
       output_data = json.loads(output_str)




       basepath = "https://www.liverpool.com.mx/tienda/pdp/"

       for record in output_data["output"]["records"]:
           title = record["title"].replace(" ", "-")
           productId = record["productId"]
           record["productUrl"] = f"{basepath}{title}/{productId}"

       #print(f'resultado {output_data}')
       ##result_text.get('output')
       return output_data 
    else: return result_map.get('text')

#def handleRecommendation(result):
#    result = retry_function(handleRecommendation_2)
#    return result

class PromptMessage(BaseModel):
    type: str = Field(description="La siguiente accion que el flujo debe tomar")
    text: str = Field(description="Valor de la siguiente accion")

def get_personal_shopper_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id: str = None,):
   
   prompt_template_str = get_prompt_from_local_filename(prompt_filename)
   model = get_initialized_model(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )
   parser = JsonOutputParser(pydantic_object=PromptMessage)
   personal_shopper_chain = (PromptTemplate.from_template(prompt_template_str) | model | parser)
  
   composite_chain = {
      "result" : personal_shopper_chain,
      "conversation": lambda x: x["conversationHistory"],
      "user_query": lambda x: x["query"]
   } | RunnableLambda(partial(handleRecommendation))

   return composite_chain




   