def get_prompt_from_local_filename(filename: str):
    with open(f"src/prompts/{filename}", "r") as f:
        prompt = f.read()
    return prompt

