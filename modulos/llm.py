import re
from typing import List
from openai import OpenAI

SUPPORTED_MODELS = [
    "deepseek/deepseek-v4-flash-0731",
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct",
]

CONVERSATIONAL_MARKERS = [
    "aquí", "aqui", "here", "espero", "saludos", "nota:", "note:",
    "recuerda", "cualquier", "let me know", "feel free", "hope this",
    "atentamente", "dork", "dorks:", "lista de", "buena", "¡buena",
    "exito", "¡exito", "suerte", "¡suerte"
]

COMMON_DORK_OPERATORS = [
    ":", "filetype", "inurl", "intitle", "site", "ext", "allinurl",
    "allintext", "index of", "index.of", "cache", "intext"
]


def clean_dork_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    if line.startswith("```") or line.endswith("```"):
        line = line.replace("```", "").strip()
    line = re.sub(r"^\s*(\d+[\.\)]|\-|\*)\s*", "", line).strip()

    if (line.startswith('"') and line.endswith('"')) or \
       (line.startswith("'") and line.endswith("'")) or \
       (line.startswith('`') and line.endswith('`')):
        line = line[1:-1].strip()

    if " #" in line:
        line = line.split(" #")[0].strip()
    return line

def is_valid_dork_candidate(cleaned_line: str) -> bool:
    if not cleaned_line:
        return False
    lower = cleaned_line.lower().strip()

    for marker in CONVERSATIONAL_MARKERS:
        if lower.startswith(marker):
            return False

    has_operator = (
        ":" in lower
        or any(op in lower for op in COMMON_DORK_OPERATORS)
        or '"' in cleaned_line
    )
    if not has_operator:
        return False

    if lower.endswith(("!", "?", "¡", "¿")):
        return False

    if lower.endswith(".") and ":" not in lower:
        return False

    return True

def parse_llm_response(raw_text: str) -> List[str]:
    lines = raw_text.splitlines()
    cleaned_dorks: List[str] = []
    seen = set()

    for raw_line in lines:
        cleaned = clean_dork_line(raw_line)
        if not cleaned:
            continue
        if not is_valid_dork_candidate(cleaned):
            continue
        if cleaned not in seen:
            seen.add(cleaned)
            cleaned_dorks.append(cleaned)

    return cleaned_dorks

def generate_dorks_with_llm(
    target_or_prompt: str,
    api_key: str,
    model: str = "deepseek/deepseek-v4-flash-0731",
    timeout: float = 30.0,
) -> List[str]:
    
    if not api_key or not api_key.strip():
        raise ValueError("La clave de API de OpenRouter no fue proporcionada.")
    
    if not target_or_prompt or not target_or_prompt.strip():
        raise ValueError("El objetivo o prompt para la IA está vacío.")

    system_prompt = (
        "Eres DorkGPT, un asistente experto en ciberseguridad, OSINT y Google Dorking avanzado. "
        "Tu función es interpretar cualquier solicitud del usuario (ya sea un objetivo o empresa, un tipo de archivo expuesto, "
        "un escenario de vulnerabilidad o una instrucción libre en lenguaje natural como 'Crea dorks para buscar logins en ciertos tld' "
        "o 'Exposed .env files') y generar exactamente 10 Google Dorks potentes, precisos y listos para ejecutar.\n\n"
        "Reglas obligatorias:\n"
        "1. Interpreta la intención técnica de la petición y diseña dorks específicos usando operadores de búsqueda avanzados "
        "(filetype:, ext:, intitle:, inurl:, site:, intext:, allinurl:, allintext:, 'index of', etc.).\n"
        "2. Si la petición menciona TLDs específicos, tecnologías, credenciales o extensiones, incorpóralos en la sintaxis de cada dork.\n"
        "3. Devuelve EXACTAMENTE 10 dorks, un dork por línea.\n"
        "4. NO agregues introducciones, comentarios, numeración (1., 2.), viñetas ni bloques markdown. Solo las cadenas de búsqueda ejecutables."
    )

    user_prompt = (
        f"Interpreta la siguiente instrucción/objetivo y genera exactamente 10 Google Dorks:\n"
        f"\"{target_or_prompt.strip()}\""
    )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key.strip(),
        timeout=timeout,
    )

    response = client.chat.completions.create(
        model=model.strip() or "deepseek/deepseek-v4-flash-0731",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    content = ""
    if response and response.choices and len(response.choices) > 0:
        content = response.choices[0].message.content or ""

    dorks = parse_llm_response(content)
    if not dorks:
        raise RuntimeError("El modelo no devolvió dorks válidos en su respuesta.")

    return dorks