import os
from dotenv import load_dotenv
from openai import OpenAI
from graphviz import Source
from prompts import DIAGRAM_PROMPTS

# Charger la clé API depuis .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_diagram_type(user_input: str) -> str:
    input_lower = user_input.lower()

    if any(word in input_lower for word in ["classe", "attribut", "méthode", "objet", "uml"]):
        return "class"
    elif any(word in input_lower for word in ["étapes", "processus", "flux", "organigramme"]):
        return "flowchart"
    elif any(word in input_lower for word in ["concept", "idée", "relation", "risque", "actif", "carte mentale", "mindmap"]):
        return "mindmap"
    else:
        return "graph"

def generate_diagram(diagram_type: str, user_request: str) -> str:
    if diagram_type not in DIAGRAM_PROMPTS:
        raise ValueError(f"Diagram type '{diagram_type}' not supported.")
    
    system_prompt = DIAGRAM_PROMPTS[diagram_type]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

def apply_default_style(dot_code: str, dpi: int = 300) -> str:
    if "digraph" not in dot_code:
        return dot_code

    style_block = f'''
    graph [bgcolor="#f9f9f9", style=filled, dpi={dpi}];

    node [
        shape=box,
        style="rounded,filled",
        color="#4A90E2",
        fillcolor="#E3F2FD",
        fontname="Helvetica",
        fontsize=14,
        fontcolor="#0D47A1"
    ];

    edge [
        color="#64B5F6",
        arrowhead=vee,
        penwidth=1.5
    ];
    '''

    if "node [" not in dot_code and "edge [" not in dot_code:
        dot_code = dot_code.replace("digraph", f'digraph')
        dot_code = dot_code.replace("{", "{\n" + style_block.strip(), 1)

    return dot_code

def save_and_render_dot(dot_code: str, filename: str = "diagram", dpi: int = 300, format: str = "png"):
    cleaned = dot_code.strip()

    # Nettoyer les balises Markdown s'il y en a
    if cleaned.startswith("```"):
        cleaned = "\n".join(line for line in cleaned.splitlines() if not line.strip().startswith("```"))

    # Appliquer le style visuel par défaut
    styled_code = apply_default_style(cleaned, dpi)

    # Génération de l'image (svg ou png)
    src = Source(styled_code)
    src.render(filename, format=format, cleanup=True)
    print(f" Image générée : {filename}.{format}")


if __name__ == "__main__":
    user_input = input("Entrez votre demande pour générer un diagramme :\n> ")
    diagram_type = detect_diagram_type(user_input)
    print(f" Type détecté : {diagram_type}")

    diagram_code = generate_diagram(diagram_type, user_input)
    print("Code DOT généré :\n", diagram_code)

    #save_and_render_dot(diagram_code)
    save_and_render_dot(diagram_code, format="svg")



