import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

logger = logging.getLogger("legalos.archive")

router = APIRouter(
    prefix="/archives",
    tags=["Gestion des Archives"]
)

class ArchivedCase(BaseModel):
    id: int
    ref: str
    title: str
    client: str
    category: str
    summary: str
    outcome: str  # "Gagné", "Perdu", "Transigé"
    key_arguments: str
    location: str  # Emplacement physique (ex: Armoire A, Carton 3)
    year: int

class SearchRequest(BaseModel):
    query: str
    semantic: bool = False
    category: str | None = None
    outcome: str | None = None

# Base de données d'archives (Simulation Real-World enrichie)
ARCHIVES_DB = [
    ArchivedCase(
        id=1,
        ref="2023-ARCH-01",
        title="Litige foncier Almadies - Famille Ndiaye c. SCI Horizon",
        client="Famille Ndiaye",
        category="Civil",
        summary="Conflit concernant la délimitation de propriété d'une parcelle de 500m² aux Almadies. Contestation d'un titre foncier suite à une vente superposée.",
        outcome="Gagné",
        key_arguments="Priorité de l'inscription au registre foncier (Article 381 du Code des obligations civiles et commerciales du Sénégal). Inopposabilité de la vente sous seing privé non enregistrée.",
        location="Armoire A, Carton 3",
        year=2023
    ),
    ArchivedCase(
        id=2,
        ref="2024-ARCH-02",
        title="Licenciement abusif - Diallo c. Banque Atlantique",
        client="Mamadou Diallo",
        category="Social",
        summary="Contestation du licenciement pour faute lourde d'un cadre bancaire sans procédure contradictoire ni préavis de licenciement.",
        outcome="Gagné",
        key_arguments="Non-respect de la procédure disciplinaire obligatoire prescrite par l'Article L.56 du Code du Travail sénégalais. Absence d'entretien préalable et défaut de notification écrite motivée.",
        location="Armoire B, Carton 8",
        year=2024
    ),
    ArchivedCase(
        id=3,
        ref="2022-ARCH-15",
        title="Injonction de payer - SOMACO c. Ets Bamba & Fils",
        client="SOMACO SARL",
        category="Commercial",
        summary="Recouvrement d'une créance de 8 500 000 FCFA issue de factures de livraison de marchandises restées impayées depuis plus de 6 mois.",
        outcome="Gagné",
        key_arguments="Application de l'Acte Uniforme OHADA portant organisation des procédures simplifiées de recouvrement (Articles 1 à 18). Présentation de bons de livraison signés et factures acceptées.",
        location="Armoire C, Carton 1",
        year=2022
    ),
    ArchivedCase(
        id=4,
        ref="2023-ARCH-44",
        title="Redressement Fiscal - Hydro-Dakar c. DGID",
        client="Hydro-Dakar SA",
        category="Fiscal",
        summary="Contestation d'un redressement sur l'impôt sur les sociétés suite à la réintégration par l'administration fiscale de charges de gestion jugées non déductibles.",
        outcome="Perdu",
        key_arguments="L'administration a prouvé avec succès l'absence de lien direct entre les charges exceptionnelles déduites et l'activité d'exploitation directe du contribuable (Article 8 du Code Général des Impôts).",
        location="Armoire D, Carton 2",
        year=2023
    ),
    ArchivedCase(
        id=5,
        ref="2024-ARCH-19",
        title="Bail commercial - Expulsion Locataire - SCI Keur Gui c. Bureau Services",
        client="SCI Keur Gui",
        category="Commercial",
        summary="Procédure d'expulsion d'un locataire commercial pour défaut de paiement de plus de 3 mois de loyers et charges contractuelles.",
        outcome="Gagné",
        key_arguments="Application stricte des règles du bail commercial de l'Acte Uniforme OHADA portant Droit Commercial Général. Mise en demeure préalable de 1 mois par exploit d'huissier restée infructueuse.",
        location="Armoire A, Carton 14",
        year=2024
    )
]

@router.get("/", response_model=list[ArchivedCase])
async def get_all_archives():
    return ARCHIVES_DB

@router.post("/search", response_model=list[ArchivedCase])
async def search_archives(request: SearchRequest):
    query = request.query.strip().lower()
    
    # 1. Filtrage traditionnel d'abord
    filtered_results = ARCHIVES_DB
    if request.category:
        filtered_results = [c for c in filtered_results if c.category.lower() == request.category.lower()]
    if request.outcome:
        filtered_results = [c for c in filtered_results if c.outcome.lower() == request.outcome.lower()]

    if not query:
        return filtered_results

    # 2. Si recherche sémantique avec clé OpenAI active
    openai_key = settings.OPENAI_API_KEY
    use_openai = request.semantic and openai_key and openai_key != "mock-key-for-now" and openai_key.startswith("sk-")

    if use_openai:
        try:
            from langchain_openai import OpenAIEmbeddings
            import numpy as np

            # Génération d'embeddings
            embeddings = OpenAIEmbeddings(api_key=openai_key)
            query_vector = embeddings.embed_query(query)

            scored_results = []
            for case in filtered_results:
                # Combiner titre + résumé + arguments clés pour l'embedding du dossier
                case_text = f"{case.title} {case.summary} {case.key_arguments}"
                case_vector = embeddings.embed_query(case_text)
                
                # Calcul de la similarité cosinus
                dot_product = np.dot(query_vector, case_vector)
                norm_q = np.linalg.norm(query_vector)
                norm_c = np.linalg.norm(case_vector)
                similarity = dot_product / (norm_q * norm_c) if (norm_q * norm_c) > 0 else 0.0

                scored_results.append((case, similarity))

            # Trier par similarité (seuil minimum facultatif de 0.6)
            scored_results.sort(key=lambda x: x[1], reverse=True)
            return [case for case, score in scored_results if score > 0.6]

        except Exception as e:
            logger.error(f"Erreur lors de la recherche sémantique OpenAI : {str(e)}. Fallback sur la recherche sémantique locale.")

    # 3. Fallback sur la recherche locale intelligente (Indexation conceptuelle locale / Mots-clés enrichis)
    # On définit des synonymes et concepts juridiques
    concept_map = {
        "licenciement": ["social", "travail", "faute", "procédure contradictoire", "préavis", "diallo"],
        "loyer": ["bail", "commercial", "expulsion", "keur", "impayer", "somaco", "bamba"],
        "terrain": ["foncier", "almadies", "ndiaye", "propriété", "titre"],
        "impot": ["fiscal", "dgid", "redressement", "déduction", "taxe", "hydro"],
        "argent": ["créance", "recouvrement", "facture", "injonction", "payer", "somaco"]
    }

    scored_results = []
    for case in filtered_results:
        score = 0
        text_to_search = f"{case.title} {case.summary} {case.key_arguments} {case.category} {case.client}".lower()
        
        # Match direct de mots
        words = query.split()
        for word in words:
            if word in text_to_search:
                score += 5
            
            # Recherche conceptuelle
            for concept, synonyms in concept_map.items():
                if word in concept or any(s in word for s in synonyms):
                    # Si le dossier correspond au concept, booster le score
                    if any(syn in text_to_search for syn in [concept] + synonyms):
                        score += 3
        
        if score > 0:
            scored_results.append((case, score))

    # Trier par score
    scored_results.sort(key=lambda x: x[1], reverse=True)
    return [case for case, score in scored_results]
