import streamlit as st
import os
import subprocess
from playwright.sync_api import sync_playwright

# 1. Configuration visuelle de l'application
st.set_page_config(page_title="Magic Pixel IA Catalog", page_icon="🎨", layout="wide")

# 2. Installation automatique du navigateur (nécessaire pour le serveur)
@st.cache_resource
def install_browser():
    subprocess.run(["playwright", "install", "chromium"])

install_browser()

# 3. Style personnalisé (Couleurs Magic Pixel)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background: linear-gradient(45deg, #38bdf8, #818cf8); 
        color: white; 
        font-weight: bold; 
        border: none;
        padding: 15px;
    }
    .prompt-box { 
        background-color: #1e293b; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #38bdf8; 
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 Magic Pixel IA : Catalogue Automatique")
st.write("Collez le lien de partage Gemini pour extraire vos créations instantanément.")

# 4. Barre de saisie du lien
url_gemini = st.text_input("Lien de partage Gemini", placeholder="https://gemini.google.com/share/...")

if st.button("🚀 GÉNÉRER LE CATALOGUE"):
    if url_gemini:
        with st.spinner("Extraction en cours depuis l'écosystème Gemini..."):
            try:
                with sync_playwright() as p:
                    # Lancement du navigateur invisible
                    browser = p.chromium.launch(headless=True,
                    args=['--disable-blink-features=AutomationControlled', '--no-sandbox'])
                    page = browser.new_page()
                    page.goto(url_gemini,  wait_until="domcontentloaded", timeout=60000)
                    
                    # Extraction des textes (Prompts) et des images
                # Extraction de tous les conteneurs de prompts utilisateur
            prompts_containers = page.query_selector_all('[id^="user-query-content-"]')
                    if not prompts_containers:
                        st.warning("Aucun contenu trouvé. Vérifiez que le lien est bien un lien de partage public.")
                    
                    # 5. Affichage des résultats dans une grille
                for i, container in enumerate(prompts_containers):                        
                    # Extraire le texte du prompt
                    p_text = container.inner_text()                        
                        st.divider()
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            if img_element:
                                img_url = img_element.get_attribute("src")
                                st.image(img_url, caption=f"Création #{i+1}", use_container_width=True)
                            else:
                                st.info("Pas d'image détectée pour cette étape.")
                        
                        with col2:
                            st.markdown("### 📝 Prompt utilisé")
                            st.code(p_text, language="text")
                            st.success("Vous pouvez copier le prompt ci-dessus pour le réutiliser !")
                            
                    browser.close()
            except Exception as e:
                st.error(f"Erreur lors de l'extraction : {e}")
    else:
        st.error("Veuillez coller un lien de partage Gemini valide.")

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("Propriété de : Magic Pixel IA Community")
