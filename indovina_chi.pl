% --- Caricamento dinamico della KB ---
:- ['kb_importata'].

:- dynamic secret_personaggio/2.
:- use_module(library(random)).
:- use_module(library(readutil)).

% --- Menu di gioco ---
gioca :-
    writeln('==========================='),
    writeln('        INDOVINA CHI       '),
    writeln('==========================='),
    writeln('Un progetto di: Alberto Esposito, Carlo Falcone, Gabriele Terracciano'),
    writeln('Scegli la modalita:'),
    writeln('1 - Tu indovini il personaggio segreto'),
    writeln('2 - Io (Prolog) cerco di indovinare il tuo personaggio'),
    read(Scelta),
    ( Scelta = 1 -> gioca_utente
    ; Scelta = 2 -> gioca_prolog
    ; writeln('Scelta non valida.'), gioca
    ).

% --- Modalita 1: Utente indovina ---
gioca_utente :-
    scegli_personaggio,
    ciclo_gioco.

scegli_personaggio :-
    findall(Nome, personaggio(Nome, _), Lista),
    random_member(NomeSelezionato, Lista),
    personaggio(NomeSelezionato, Attributi),
    retractall(secret_personaggio(_, _)),
    assertz(secret_personaggio(NomeSelezionato, Attributi)),
    writeln('Personaggio segreto scelto. Inizia a fare delle domande.').

ciclo_gioco :-
    writeln('Scrivi una domanda nel formato: ha(attributo). oppure fai una ipotesi: e(nome) (la e senza accento).'),
    read(Input),
    ( Input = e(Nome) ->
        ( secret_personaggio(Nome, _) ->
            format('Esatto! Era ~w! Hai vinto!~n', [Nome])
        ; secret_personaggio(Secret, _),
          format('No, era ~w. Hai perso.~n', [Secret])
        )
    ; Input = ha(Attributo) ->
        ha(Attributo), ciclo_gioco
    ; writeln('Comando non valido. Usa ha(X). oppure e(nome).'), ciclo_gioco
    ).

ha(Attributo) :-
    secret_personaggio(_, Attributi),
    ( member(Attributo, Attributi) -> writeln('Si')
    ; writeln('No')
    ).

% --- Modalita 2: Prolog indovina ---
gioca_prolog :-
    writeln('Pensa a un personaggio tra quelli raffigurati e rispondi alle domande con si. o no.'),
    findall(P, personaggio(P, _), Lista),
    deduci(Lista).

deduci([Unico]) :-
    format('Il tuo personaggio e'' ~w?~n', [Unico]),
    read_line_to_string(user_input, RispStr),
    string_lower(RispStr, Lower),
    atom_string(Risp, Lower),
    ( Risp == si -> writeln('Ho indovinato!')
    ; writeln('Hai barato oppure ho sbagliato.')
    ).

deduci([]) :-
    writeln('Nessun candidato rimasto. Forse una risposta e'' errata.').

deduci(Candidati) :-
    scegli_attributo(Candidati, Attributo),
    format('Ha ~w?~n', [Attributo]),
    read_line_to_string(user_input, RispostaStr),
    string_lower(RispostaStr, Lower),
    atom_string(Risposta, Lower),
    ( (Risposta \= si, Risposta \= no) ->
        writeln('Rispondi solo con si. o no.'), deduci(Candidati)
    ; filtra(Candidati, Attributo, Risposta, Nuovi),
      length(Nuovi, N),
      format('Candidati rimasti: ~d~n', [N]),
      deduci(Nuovi)
    ).

scegli_attributo(Candidati, Attributo) :-
    findall(A, (member(P, Candidati), personaggio(P, Attrs), member(A, Attrs)), TuttiAttr),
    sort(TuttiAttr, Unici),
    random_member(Attributo, Unici).

filtra(Lista, Attributo, si, NuovaLista) :-
    include(has_attributo(Attributo), Lista, NuovaLista).
filtra(Lista, Attributo, no, NuovaLista) :-
    exclude(has_attributo(Attributo), Lista, NuovaLista).

has_attributo(Attr, Nome) :-
    personaggio(Nome, Attributi),
    member(Attr, Attributi).
