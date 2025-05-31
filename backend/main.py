import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from graphviz import Source
from prompts import DIAGRAM_PROMPTS

# Initialisation
load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_diagram_type(user_input: str) -> str:
    input_lower = user_input.lower()
    if any(w in input_lower for w in ["classe", "attribut", "méthode", "objet", "uml"]):
        return "class"
    elif any(w in input_lower for w in ["étapes", "processus", "flux", "organigramme"]):
        return "flowchart"
    elif any(w in input_lower for w in ["concept", "idée", "relation", "carte mentale", "mindmap"]):
        return "mindmap"
    else:
        return "graph"

def generate_diagram(diagram_type: str, user_request: str) -> str:
    if diagram_type not in DIAGRAM_PROMPTS:
        raise ValueError(f"Type de diagramme '{diagram_type}' non supporté.")
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

@app.route("/generate", methods=["POST"])
def generate_endpoint():
    try:
        data = request.get_json()
        user_input = data.get("input", "")
        if not user_input:
            return jsonify({"success": False, "error": "Texte de l'utilisateur manquant."}), 400

        diagram_type = detect_diagram_type(user_input)
        dot_code = generate_diagram(diagram_type, user_input)

        # Nettoyer markdown
        dot_clean = "\n".join(line for line in dot_code.strip().splitlines() if not line.strip().startswith("```"))
        dot_styled = apply_default_style(dot_clean)

        # Rendu SVG
        src = Source(dot_styled)
        svg_output = src.pipe(format="svg").decode("utf-8")

        return jsonify({"success": True, "svg": svg_output})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
