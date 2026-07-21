:- consult('conhecimento_ms.pl').

% ----------------------------------------------------------
% peso/3 — pontos de cada sintoma
% peso(TipoAcidente, Sintoma, Pontos)
%
% Derivação automática do grau na tabela sintoma_grau/3.
% ----------------------------------------------------------

% Exceção: coagulacao_proxy(alterada) vale 2 pontos em qualquer
% tipo, apesar de graduar como 'leve' no botrópico.
% Justificativa: MS trata coagulopatia como possibilidade em
% todos os graus (checkpoint, Decisão de peso).
peso(_, coagulacao_proxy(alterada), 2).

% Regras gerais (derivadas de sintoma_grau/3)
peso(Tipo, Sintoma, 3) :-
    sintoma_grau(Tipo, Sintoma, grave).

peso(Tipo, Sintoma, 2) :-
    Sintoma \= coagulacao_proxy(alterada),
    sintoma_grau(Tipo, Sintoma, moderado).

peso(Tipo, Sintoma, 1) :-
    Sintoma \= coagulacao_proxy(alterada),
    sintoma_grau(Tipo, Sintoma, leve).