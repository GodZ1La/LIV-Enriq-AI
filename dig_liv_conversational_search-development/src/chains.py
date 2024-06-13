from src.model.model  import get_simple_call_chain, get_personal_shopper_chain

def _get_initial_router_model_call_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_simple_call_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

def get_hello_generator_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_simple_call_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

def get_farewell_generator_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_simple_call_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

def get_fallback_generator_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_simple_call_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

def get_recomendation_generator_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_personal_shopper_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )

def get_pregfrecuentes_chain(
    prompt_filename,
    model_name,
    max_output_tokens,
    temperature,
    top_p,
    top_k,
    project_id=None,
):
    return get_simple_call_chain(
        prompt_filename=prompt_filename,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        project_id=project_id,
    )