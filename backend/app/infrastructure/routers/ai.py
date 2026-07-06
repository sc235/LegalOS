import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

# Configuration du logging
logger = logging.getLogger("legalos.ai")

router = APIRouter(
    prefix="/ia",
    tags=["Intelligence Artificielle"]
)

# Requêtes / Réponses Pydantic
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    reply: str
    is_mocked: bool
    details: str | None = None

class DocumentRequest(BaseModel):
    prompt: str
    doc_type: str  # e.g., "mise_en_demeure", "contrat", "requete"

class DocumentResponse(BaseModel):
    document_content: str
    is_mocked: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_legal(request: ChatRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="La requête ne peut pas être vide.")

    # Vérifier si la clé OpenAI est configurée
    use_mock = True
    openai_key = settings.OPENAI_API_KEY

    if openai_key and openai_key != "mock-key-for-now" and openai_key.startswith("sk-"):
        use_mock = False

    if not use_mock:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage

            chat = ChatOpenAI(
                api_key=openai_key,
                model="gpt-4o-mini",
                temperature=0.2
            )

            messages = [
                SystemMessage(content=(
                    "Tu es un assistant juridique expert en droit ouest-africain (traité OHADA, codes nationaux Sénégal, Côte d'Ivoire, etc.). "
                    "Donne des réponses précises, cite les articles de lois pertinents quand c'est possible, et utilise un ton formel et professionnel. "
                    "Si tu n'es pas sûr, mentionne-le."
                )),
                HumanMessage(content=query)
            ]

            response = chat.invoke(messages)
            return ChatResponse(
                reply=response.content,
                is_mocked=False,
                details="Généré en direct par GPT-4o-mini"
            )

        except Exception as e:
            logger.error(f"Erreur d'appel OpenAI : {str(e)}. Utilisation du fallback.")
            # Continuer vers le fallback en cas d'erreur réseau/clé

    # Fallback / Générateur de démo local intelligent
    reply = ""
    query_lower = query.lower()

    if "ohada" in query_lower or "injonction" in query_lower:
        reply = (
            "**[Mode Démo - Réponse Locale]**\n\n"
            "Selon l'Acte Uniforme OHADA portant organisation des procédures simplifiées de recouvrement (Articles 1 à 18) :\n\n"
            "1. **Créance admissible** : Elle doit être certaine, liquide et exigible.\n"
            "2. **Juridiction compétente** : Le Président du Tribunal du domicile du débiteur.\n"
            "3. **Pièces justificatives requises** : Tout document prouvant la créance (contrat, facture impayée, bon de livraison signé, reconnaissance de dette).\n"
            "4. **Procédure** : Dépôt d'une requête au greffe. Si le juge accepte, il rend une ordonnance portant injonction de payer, qui doit être signifiée au débiteur sous 3 mois par huissier."
        )
    elif "bail" in query_lower or "loyer" in query_lower:
        reply = (
            "**[Mode Démo - Réponse Locale]**\n\n"
            "En matière de bail d'habitation sous la législation sénégalaise :\n\n"
            "1. **Expulsion pour impayés** : Une mise en demeure de payer de 30 jours (par exploit d'huissier ou lettre recommandée avec AR) est obligatoire.\n"
            "2. **Délai** : Si le locataire ne règle pas sa dette dans ce délai de 30 jours, le bailleur peut saisir le Tribunal d'Instance pour demander la résiliation du bail et l'expulsion.\n"
            "3. **Tribunal compétent** : Le Tribunal d'Instance du lieu de situation de l'immeuble."
        )
    else:
        reply = (
            f"**[Mode Démo - Réponse Locale]**\n\n"
            f"J'ai bien reçu votre question : \"{query}\".\n\n"
            "Pour que je puisse répondre dynamiquement via l'IA de production, veuillez renseigner une clé API OpenAI valide dans le fichier `backend/.env` du projet.\n\n"
            "En attendant, sachez que pour toute procédure en Afrique de l'Ouest (CEDEAO / UEMOA), la mise en demeure écrite reste un préambule indispensable avant d'intenter une action au fond devant les tribunaux civils ou de commerce."
        )

    return ChatResponse(
        reply=reply,
        is_mocked=True,
        details="Généré par le moteur de secours local (Clé API OpenAI non configurée)"
    )

@router.post("/generate-document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Le prompt ne peut pas être vide.")

    use_mock = True
    openai_key = settings.OPENAI_API_KEY

    if openai_key and openai_key != "mock-key-for-now" and openai_key.startswith("sk-"):
        use_mock = False

    if not use_mock:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage

            chat = ChatOpenAI(
                api_key=openai_key,
                model="gpt-4o-mini",
                temperature=0.3
            )

            system_prompt = (
                f"Tu es un avocat sénégalais et ivoirien expert. Rédige un projet d'acte de type '{request.doc_type}' "
                "basé sur les instructions de l'utilisateur. Le style doit être hautement solennel, précis, et utiliser les formules juridiques requises en Afrique de l'Ouest."
            )

            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ])

            return DocumentResponse(
                document_content=response.content,
                is_mocked=False
            )
        except Exception as e:
            logger.error(f"Erreur génération OpenAI : {str(e)}")

    # Fallback document generator
    doc = (
        f"=== PROJET D'ACTE JURIDIQUE GENERÉ EN MODE DEMO ===\n"
        f"TYPE : {request.doc_type.upper()}\n"
        f"DATE : 03 Juillet 2026\n"
        f"PAYS : Zone OHADA\n\n"
        f"CONTEXTE : {prompt}\n\n"
        f"----------------------------------------------------\n"
        f"À [Destinataire],\n\n"
        f"Par la présente, nous vous notifions formellement que notre cabinet a été saisi par [Client] afin de faire valoir ses droits concernant la situation décrite ci-dessus.\n\n"
        f"S'agissant d'un manquement flagrant à vos obligations contractuelles, nous vous mettons en demeure par cette notification de régulariser la situation sous un délai de huit (8) jours francs.\n\n"
        f"À défaut de quoi, nous serons contraints d'engager toutes procédures judiciaires utiles, notamment par voie de requête aux fins d'injonction devant la juridiction compétente.\n\n"
        f"Veuillez agréer, Monsieur, l'expression de nos sentiments distingués.\n\n"
        f"Pour le Cabinet,\n"
        f"Me. Diallo & Associés"
    )

    return DocumentResponse(
        document_content=doc,
        is_mocked=True
    )
