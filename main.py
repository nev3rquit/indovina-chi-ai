import subprocess
from interfaccia_mongo import scrivi_fatti_prolog, salva_partita, popola_personaggi

popola_personaggi() #Caricamento dei 10 personaggi di esempio

def gioca_utente():
    scrivi_fatti_prolog()
    subprocess.run(["swipl", "-s", "indovina_chi.pl", "-g", "gioca_utente", "-t", "halt"], check=True)
    nome = input("[MAIN] Inserisci il nome del personaggio che era stato scelto (per salvarlo nel DB): ")
    esito = input("[MAIN] Hai indovinato? Scrivi (vittoria/sconfitta): ")
    tentativi = int(input("[MAIN] Quanti tentativi hai fatto?: "))
    salva_partita("utente_indovina", nome, esito, tentativi)

def gioca_prolog():
    scrivi_fatti_prolog()
    subprocess.run(["swipl", "-s", "indovina_chi.pl", "-g", "gioca_prolog", "-t", "halt"], check=True)
    nome = input("[MAIN] Qual era il personaggio che avevi pensato (per salvarlo nel DB)?: ")
    esito = input("[MAIN] Ha indovinato? Scrivi (vittoria/sconfitta): ")
    tentativi = int(input("[MAIN] Quante domande ti ha fatto?: "))
    salva_partita("prolog_indovina", nome, esito, tentativi)

if __name__ == "__main__":
    print("Benvenuto in INDOVINA CHI")
    print("Un progetto di: Alberto Esposito, Carlo Falcone, Gabriele Terracciano")
    print("1 - Tu indovini il personaggio segreto")
    print("2 - Il computer prova a indovinare il tuo personaggio")
    scelta = input("Scegli una modalita (1/2): ")

    if scelta == "1":
        gioca_utente()
    elif scelta == "2":
        gioca_prolog()
    else:
        print("Scelta non valida.")