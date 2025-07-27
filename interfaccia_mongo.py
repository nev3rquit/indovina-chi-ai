from pymongo import MongoClient
from datetime import datetime
import random

# --- CONNESSIONE DB ---
def get_database():
    client = MongoClient("localhost", 27017)
    return client["indovinachi"]

# --- RACCOLTE ---
db = get_database()
col_personaggi = db["personaggi"]
col_partite = db["partite"]

# --- PERSONAGGI ---
def get_personaggi():
    """Restituisce tutti i personaggi dal DB come lista di dict"""
    risposta = list(col_personaggi.find({}, {'_id': 0}))
    return risposta

def get_personaggi_prolog():
    """Restituisce i personaggi come fatti Prolog"""
    lista = get_personaggi()
    fatti = []
    for p in lista:
        attr_str = ', '.join(p['attributi'])
        fatto = f"personaggio({p['nome']}, [{attr_str}])."
        fatti.append(fatto)
    return fatti

def scrivi_fatti_prolog(filename='kb_importata.pl'):
    fatti = get_personaggi_prolog()
    with open(filename, 'w') as f:
        for riga in fatti:
            f.write(riga + '\n')

# --- POPOLA DB CON ESEMPI ---
def popola_personaggi():
    esempio = [
        {"nome": "mario", "attributi": ["baffi", "occhiali", "cappello"]},
        {"nome": "giulia", "attributi": ["capelli_lunghi", "sorriso", "occhiali"]},
        {"nome": "pietro", "attributi": ["barba", "calvizie"]},
        {"nome": "luca", "attributi": ["capelli_neri", "cappello"]},
        {"nome": "anna", "attributi": ["capelli_biondi", "tatuaggi", "occhiali"]},
        {"nome": "marco", "attributi": ["baffi", "sorriso"]},
        {"nome": "elena", "attributi": ["capelli_rossi", "occhiali"]},
        {"nome": "giorgio", "attributi": ["barba", "cappello"]},
        {"nome": "sofia", "attributi": ["capelli_biondi", "capelli_lunghi"]},
        {"nome": "franco", "attributi": ["calvizie", "occhiali", "tatuaggi"]}
    ]
    col_personaggi.delete_many({})
    col_personaggi.insert_many(esempio)
    print("[INTERFACCIA] Personaggi caricati.")

# --- PARTITE ---
def salva_partita(modalita, personaggio_segreto, esito, tentativi):
    partita = {
        'modalita': modalita,
        'personaggio_segreto': personaggio_segreto,
        'esito': esito,
        'tentativi': tentativi,
        'data': datetime.now()
    }
    col_partite.insert_one(partita)

# --- UTILITY ---
def scegli_personaggio_casuale():
    personaggi = get_personaggi()
    return random.choice(personaggi) if personaggi else None
