import streamlit as st
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ========================================
# 1. CONFIGURATION & INITIALISATION
# ========================================

# Configuration visuelle
st.set_page_config(
    page_title="Magic Pixel IA Catalog",
    page_icon="🎨",
    layout="wide"
)

# Chargement des variables d'environnement
load_dotenv()

# Initialisation du client Gemini
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Essayer depuis Streamlit secrets en fallback
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    if not api_key:
        st.error("⚠️ Clé API Gemini manquante. Configurez GEMINI_API_KEY dans .env ou Streamlit secrets.")
        st.stop()
    
    client = genai.Client(api_key=api_key)
    MODEL_ID = "gemini-2.0-flash-exp"  # Modèle rapide et performant
except Exception as e:
    st.error(f"Erreur d'initialisation de l'API Gemini : {e}")
    st.stop()

# Style personnalisé Magic Pixel
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #38bdf8, #818cf8);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
    }
    .catalog-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #38bdf8;
        margin-bottom: 20px;
    }
    .prompt-box {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 14px;
        margin: 10px 0;
    }
    .tag {
        display: inline-block;
        background: linear-gradient(45deg, #38bdf8, #818cf8);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        margin: 3px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# 2. SCHÉMA JSON DU CATALOGUE
# ========================================

catalog_schema: Dict[str, Any] = {
    "type": "array",
    "title": "MagicPixelCatalog",
    "items": {
        "type": "object",
        "required": ["id", "title", "prompt", "image_description"],
        "properties": {
            "id": {
                "type": "string",
                "description": "Identifiant unique de l'item."
            },
            "source_message_index": {
                "type": "integer",
                "description": "Index du message Gemini."
            },
            "title": {
                "type": "string",
                "description": "Titre lisible de l'item."
            },
            "prompt": {
                "type": "string",
                "description": "Prompt complet utilisé."
            },
            "short_prompt": {
                "type": "string",
                "description": "Résumé court du prompt (1-2 lignes)."
            },
            "image_description": {
                "type": "string",
                "description": "Description textuelle de l'image."
            },
            "style": {
                "type": "string",
                "description": "Style visuel (ex: photo restoration, vintage)."
            },
            "use_case": {
                "type": "string",
                "description": "Cas d'usage (ex: restauration photo de famille)."
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Tags pour filtrage."
            },
            "model_name": {
                "type": "string",
                "description": "Modèle utilisé si mentionné."
            },
            "rating": {
                "type": "integer",
                "description": "Note de 1 à 5 (optionnel)."
            },
            "notes": {
                "type": "string",
                "description": "Notes internes Magic Pixel IA."
            }
        }
    }
}

# ========================================
# 3. FONCTION DE GÉNÉRATION DU CATALOGUE
# ========================================

def generate_catalog_from_gemini(share_url: str) -> List[Dict[str, Any]]:
    """
    Utilise l'API Gemini avec URL Context pour extraire le catalogue
    depuis un lien de partage Gemini.
    """
    
    # Outil URL Context
    url_context_tool = types.Tool(url_context=types.UrlContext())
    
    # Prompt détaillé
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    f"""
Tu as accès au contenu de cette page de partage Gemini : {share_url}

Cette page contient une conversation où l'utilisateur crée un catalogue
d'images générées (prompts + images) pour Magic Pixel IA.

Tâche :
1. Parcours TOUTE la conversation.
2. Détecte chaque "item" du catalogue (un item = un prompt + une image associée ou décrite).
3. Pour chaque item, remplis STRICTEMENT le schéma JSON fourni.

Instructions sur les champs :
- "id" : génère un identifiant court et stable (ex: "portrait_vintage_001").
- "title" : titre court qui décrit l'image (langage humain).
- "prompt" : prompt COMPLET, prêt à être copié-collé.
- "short_prompt" : version courte, max ~120 caractères.
- "image_description" : description claire de l'image finale.
- "style" : un seul style principal (ex: "photo restoration", "vintage portrait").
- "use_case" : phrase courte décrivant le cas d'usage.
- "tags" : 3 à 10 tags utiles (couleurs, ambiance, type de sujet).
- "rating" : de 1 à 5 si estimable, sinon laisse vide.
- "notes" : commentaires utiles pour Magic Pixel IA, sinon chaîne vide.

IMPORTANT :
- Ne renvoie que du JSON valide, sans texte avant ni après.
- Respecte strictement les noms de champs et leurs types.
- Si une info n'est pas présente, laisse le champ vide ("") ou tableau vide ([]).
"""
                )
            ],
        )
    ]
    
    config = types.GenerateContentConfig(
        tools=[url_context_tool],
        response_mime_type="application/json",
        response_json_schema=catalog_schema,
    )
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=config,
        )
        
        # Parser la réponse JSON
        if hasattr(response, "parsed") and response.parsed is not None:
            catalog = response.parsed
        else:
            catalog = json.loads(response.text)
        
        if not isinstance(catalog, list):
            st.error("La réponse du modèle n'est pas une liste d'items.")
            return []
        
        return catalog
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction : {e}")
        return []

# ========================================
# 4. INTERFACE UTILISATEUR
# ========================================

st.title("🎨 Magic Pixel IA : Catalogue Automatique")
st.write("Collez le lien de partage Gemini pour extraire vos créations instantanément.")

# Barre de saisie
url_gemini = st.text_input(
    "Lien de partage Gemini",
    placeholder="https://gemini.google.com/share/..."
)

if st.button("🚀 GÉNÉRER LE CATALOGUE"):
    if url_gemini:
        with st.spinner("🔍 Analyse de la conversation Gemini et génération du catalogue..."):
            catalog = generate_catalog_from_gemini(url_gemini)
        
        if not catalog:
            st.warning("Aucun élément de catalogue détecté ou erreur lors de l'extraction.")
        else:
            st.success(f"✅ {len(catalog)} élément(s) extrait(s) !")
            
            # Affichage du catalogue
            for idx, item in enumerate(catalog, 1):
                st.markdown(f"<div class='catalog-card'>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"### 🖼️ Item #{idx}")
                    if item.get("image_description"):
                        st.info(item["image_description"])
                    
                    # Tags
                    if item.get("tags"):
                        tags_html = "".join([f"<span class='tag'>{tag}</span>" for tag in item["tags"]])
                        st.markdown(tags_html, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{item.get('title', 'Item sans titre')}**")
                    
                    # Style et use case
                    if item.get("style"):
                        st.caption(f"🎨 Style : {item['style']}")
                    if item.get("use_case"):
                        st.caption(f"💡 Cas d'usage : {item['use_case']}")
                    
                    # Prompt principal
                    st.markdown("**📝 Prompt complet :**")
                    st.code(item.get("prompt", ""), language="text")
                    
                    # Notes
                    if item.get("notes"):
                        st.info(f"📌 {item['notes']}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.divider()
            
            # Export JSON
            st.download_button(
                label="📥 Télécharger le catalogue (JSON)",
                data=json.dumps(catalog, indent=2, ensure_ascii=False),
                file_name="magic_pixel_catalog.json",
                mime="application/json"
            )
    else:
        st.error("Veuillez coller un lien de partage Gemini valide.")

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("Propriété de : Magic Pixel IA Community")
st.sidebar.markdown("""
### 🚀 Version 2.0
- ✅ API Gemini native
- ✅ Extraction JSON structurée
- ✅ Export catalogue
""")
