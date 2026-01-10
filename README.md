# 🎨 Magic Pixel IA : Catalogue Automatique

**Version 2.0** - Extraction intelligente de catalogues depuis les conversations Gemini

## 🚀 Fonctionnalités

- ✅ **Extraction via API Gemini native** : Plus besoin de scraping fragile !
- ✅ **JSON structuré** : Schéma précis pour vos items de catalogue
- ✅ **Export catalogue** : Téléchargement JSON direct
- ✅ **Interface élégante** : Design Magic Pixel avec gradients bleus

## 📋 Prérequis

1. **Clé API Gemini** : Obtenez-la sur [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Python 3.8+
3. Les dépendances dans `requirements.txt`

## 🛠️ Installation locale

```bash
# Cloner le repo
git clone https://github.com/filucate-prog/magic-pixel-catalog.git
cd magic-pixel-catalog

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
cp .env.example .env
# Éditer .env et ajouter votre GEMINI_API_KEY

# Lancer l'app
streamlit run app.py
```

## ☁️ Déploiement sur Streamlit Cloud

1. Forkez ce repo
2. Connectez-vous à [Streamlit Cloud](https://share.streamlit.io/)
3. Créez une nouvelle app et sélectionnez ce repo
4. **Important** : Dans les Settings → Secrets, ajoutez :

```toml
GEMINI_API_KEY = "votre_clé_api_ici"
```

5. Déployez ! 🎉

## 📖 Utilisation

1. Ouvrez l'app Magic Pixel Catalog
2. Collez un **lien de partage Gemini** (format : `https://gemini.google.com/share/...`)
3. Cliquez sur **🚀 GÉNÉRER LE CATALOGUE**
4. Attendez l'extraction intelligente
5. Visualisez votre catalogue structuré
6. Téléchargez en JSON si besoin

## 🎯 Schéma du catalogue

Chaque item extrait contient :

- `id` : Identifiant unique
- `title` : Titre lisible
- `prompt` : Prompt complet (copiable)
- `short_prompt` : Résumé court
- `image_description` : Description de l'image
- `style` : Style visuel (ex: "photo restoration")
- `use_case` : Cas d'usage
- `tags` : Liste de tags pour filtrage
- `rating` : Note de 1 à 5 (optionnel)
- `notes` : Notes internes

## 🔧 Architecture technique

**Avant (v1.0)** : Playwright → Scraping DOM → Fragile

**Maintenant (v2.0)** : API Gemini + URL Context → JSON structuré → Robuste ✨

L'app utilise :
- `google.genai` : SDK officiel Python
- `types.Tool(url_context=...)` : Outil URL Context pour analyser les pages Gemini
- `response_json_schema` : Force un JSON valide conforme au schéma

## 🐛 Dépannage

### "Clé API manquante"
→ Vérifiez que `GEMINI_API_KEY` est bien configurée dans `.env` ou Streamlit Secrets

### "Aucun élément de catalogue détecté"
→ Vérifiez que le lien Gemini contient bien une conversation avec des prompts/images
→ Assurez-vous que le lien est bien **public** (pas en mode privé)

### Erreur de quota API
→ Vérifiez vos limites sur [Google AI Studio](https://aistudio.google.com/)

## 📝 Licence

Propriété de **Magic Pixel IA Community**

## 🙏 Remerciements

Merci à la communauté Magic Pixel IA pour le feedback et les tests ! 💙

---

**Créé avec ❤️ par Magic Pixel IA**
