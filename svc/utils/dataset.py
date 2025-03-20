from pydantic import BaseModel
import pandas as pd
import re

def read_csv(file_path):
    print('import dataset')
    df = pd.read_csv(file_path)
    df.columns = [re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower().replace(' ', '') for col in df.columns]
    return df

questions = [
    {
        "question": "Qual è il settore principale della tua azienda?",
        "options": [
            "a) Produzione e manifattura (es. meccanica, elettronica, ingegneria)",
            "b) Servizi finanziari o legali (es. banca, consulenza, contabilità)",
            "c) Tecnologia e innovazione (es. software, AI, digitalizzazione)",
            "d) Sanità e biotecnologie (es. cliniche, ricerca medica, farmaceutica)",
            "e) Commercio e retail (es. negozi, distribuzione, e-commerce)",
            "f) Altro (specificare)"
        ],
    },
    {
        "question": "Di quale servizio finanziario o legale hai più bisogno?",
        "options": [
            "a) Consulenza aziendale e strategica",
            "b) Contabilità, auditing e compliance",
            "c) Finanziamenti, investimenti e gestione del rischio",
            "d) Diritto commerciale e contrattuale",
            "e) Altro (specificare)"
        ],
    },
    {
        "question": "Qual è la tua priorità principale nei servizi finanziari?",
        "options": [
            "a) Ottenere finanziamenti o investimenti per la mia attività",
            "b) Ottimizzare la gestione finanziaria e il controllo di rischio",
            "c) Collaborare con esperti di mercati finanziari e corporate finance",
            "d) Sviluppare strategie di crescita per il mio business"
        ]
    }
]

todos = [
    {
        "id": 0,
        "project": "FastAPI",
        "description": "Create a new project",
        "steps": [
            "Create a new project using FastAPI",
            "Add a new endpoint to the project",
            "Test the new endpoint using the Swagger UI"
        ],
        "current_step": 0
    },
        {
        "id": 1,
        "project": "FastAPI",
        "description": "Create a new project",
        "steps": [
            "Create a new project using FastAPI",
            "Add a new endpoint to the project",
            "Test the new endpoint using the Swagger UI"
        ],
        "current_step": 0
    }
]

answers = []
