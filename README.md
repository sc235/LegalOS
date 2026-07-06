# LegalOS - Plateforme de gestion pour cabinets d'avocats en Afrique de l'Ouest

**LegalOS** est une application web moderne conçue pour automatiser et optimiser la gestion quotidienne des cabinets d'avocats opérant dans la zone OHADA (Sénégal, Côte d'Ivoire, Mali, etc.). Elle propose des fonctionnalités d'automatisation intelligente basées sur l'Intelligence Artificielle et la recherche sémantique appliquée au droit ouest-africain.

---

## 🚀 Fonctionnalités Clés

1. **Tableau de Bord Multi-Rôles**
   - **Avocat / Associé** : Accès complet à l'agenda, à la base de données clients, à la rédaction d'actes IA et aux archives.
   - **Secrétaire** : Gestion administrative (dossiers, calendrier des audiences, etc.).
   - **Comptable** : Accès dédié à la facturation et aux états financiers du cabinet.

2. **Assistant Juridique IA (Génération d'Actes & Chat)**
   - **Chat Juridique** : Posez des questions de droit ouest-africain. L'IA (via GPT-4o-mini ou le moteur de secours local) répond en citant les articles pertinents (Codes du travail locaux, Actes Uniformes OHADA, etc.).
   - **Générateur d'Actes** : Génération automatisée de brouillons de contrats, requêtes et mises en demeure basés sur un prompt utilisateur.

3. **Gestion & Recherche Sémantique d'Archives**
   - Base de données d'archives de dossiers passés du cabinet.
   - Recherche classique par mot-clé et filtrage par catégorie/issue judiciaire.
   - **Recherche Sémantique Avancée** : Recherche par concepts et arguments juridiques (avec OpenAI Embeddings ou par fallback intelligent sur un graphe conceptuel local).

4. **Agenda & Suivi des Audiences**
   - Visualisation des audiences à venir, des délibérés et des rendez-vous clients.

---

## 🛠️ Architecture du Projet

Le projet adopte une séparation stricte des préoccupations (Clean Architecture) :

```
LegalOS/
├── backend/                  # API REST (FastAPI)
│   ├── app/
│   │   ├── application/     # Cas d'utilisation et logique métier
│   │   ├── domain/          # Entités et règles métier fondamentales
│   │   ├── infrastructure/  # Routeurs API, configuration de la base de données
│   │   ├── config.py        # Gestion de la configuration globale
│   │   └── main.py          # Point d'entrée de l'application FastAPI
│   └── requirements.txt     # Dépendances Python
└── frontend/                 # Application web SPA (Angular 19)
    ├── src/
    │   ├── app/
    │   │   ├── core/        # Services partagés, intercepteurs, guards (ex: AuthService, AiService)
    │   │   └── features/    # Modules fonctionnels (landing page, auth/login, dashboard)
    │   └── styles.css       # Système de styles
    └── package.json         # Dépendances et scripts npm
```

---

## ⚙️ Installation & Démarrage

### 1. Prérequis
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### 2. Configuration & Lancement du Backend (FastAPI)

1. Rendez-vous dans le dossier backend :
   ```bash
   cd backend
   ```

2. Créez et activez un environnement virtuel :
   - **Sur Windows (PowerShell) :**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Sur macOS/Linux :**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créez et configurez le fichier `.env` à la racine de `/backend` :
   ```ini
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/legalos
   SECRET_KEY=votre_cle_secrete_ici
   OPENAI_API_KEY=sk-proj-... # Ajoutez votre clé API OpenAI réelle pour la sémantique & chat
   ```

5. Démarrez le serveur uvicorn :
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   L'API sera disponible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000) (Documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)).

---

### 3. Configuration & Lancement du Frontend (Angular)

1. Rendez-vous dans le dossier frontend :
   ```bash
   cd ../frontend
   ```

2. Installez les paquets npm :
   ```bash
   npm install
   ```

3. Lancez le serveur de développement :
   ```bash
   npm run start
   ```

4. Ouvrez votre navigateur et naviguez sur : [http://localhost:4200](http://localhost:4200)

---

## 🧪 Simulation de Connexion de Test

Pour tester le prototype sans base de données d'utilisateurs persistante, vous pouvez utiliser les boutons d'accès rapide sur l'écran de connexion ou saisir n'importe quel email se terminant par `@cabinet.com` ou `@legalos.com` avec le mot de passe `admin`.

Exemples de rôles préconfigurés :
- **Avocat** : `associe@cabinet-diallo.com` (Accès complet)
- **Secrétaire** : `secretaire@cabinet-diallo.com` (Accès limité aux dossiers, calendrier et archives)
- **Comptable** : `compta@cabinet-diallo.com` (Accès limité à la facturation)
