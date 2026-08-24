"""Serveur MCP du Collège de Bruxelles — squelette de démonstration.

Ce module ne contient pour l'instant qu'un exemple de chaque primitive FastMCP
(outil, ressource, prompt), le temps de valider le transport HTTP local.
"""

from __future__ import annotations

from statistics import mean

from fastmcp import FastMCP

mcp = FastMCP(
    name="collegia",
    version="0.1.0",
    instructions=(
        "Serveur MCP du Collège de Bruxelles, destiné aux enseignants. "
        "Il donne accès aux données de l'école et à des aides à la préparation "
        "de cours, à la correction et aux tâches administratives. "
        "Réponds toujours en français."
    ),
)


@mcp.tool
def compute_class_average(grades: list[float], scale: float = 20.0) -> dict:
    """Calcule la moyenne d'une série de notes et la répartition réussite/échec.

    À utiliser quand un enseignant fournit les notes d'une interrogation ou d'un
    examen et veut une vue d'ensemble avant d'encoder les résultats.

    Args:
        grades: Les notes des élèves, dans l'ordre où elles ont été relevées.
        scale: Le total sur lequel l'évaluation est cotée (20 par défaut).

    Returns:
        La moyenne, la note minimale et maximale, le nombre d'élèves ayant
        atteint la moitié des points, et un commentaire en français.
    """
    if not grades:
        raise ValueError(
            "Aucune note fournie : indiquez au moins une note d'élève pour "
            "pouvoir calculer une moyenne."
        )
    if scale <= 0:
        raise ValueError(
            f"Le total de l'évaluation doit être strictement positif (reçu : {scale})."
        )
    out_of_range = [g for g in grades if g < 0 or g > scale]
    if out_of_range:
        raise ValueError(
            f"Ces notes sortent du barème /{scale:g} : {out_of_range}. "
            "Vérifiez le total de l'évaluation ou l'encodage des notes."
        )

    average = mean(grades)
    passing = [g for g in grades if g >= scale / 2]

    return {
        "effectif": len(grades),
        "moyenne": round(average, 2),
        "note_minimale": min(grades),
        "note_maximale": max(grades),
        "reussites": len(passing),
        "echecs": len(grades) - len(passing),
        "commentaire": (
            f"Moyenne de {average:.2f}/{scale:g} pour {len(grades)} élève(s) : "
            f"{len(passing)} ont atteint la moitié des points."
        ),
    }


@mcp.resource(
    "collegia://etablissement/infos",
    name="Informations sur l'établissement",
    description=(
        "Fiche d'identité du Collège de Bruxelles : coordonnées, niveaux "
        "organisés et horaire type. Données de démonstration."
    ),
    mime_type="text/markdown",
)
def school_info() -> str:
    """Fiche d'identité de l'établissement (données de démonstration)."""
    return """# Collège de Bruxelles

**Adresse** : rue de l'Exemple 1, 1000 Bruxelles
**Téléphone** : +32 2 000 00 00
**Langue d'enseignement** : français

## Niveaux organisés

- Degré inférieur : 1re à 3e année
- Degré supérieur : 4e à 6e année

## Horaire type

| Période | Horaire |
| --- | --- |
| 1re–2e | 08h30 – 10h10 |
| 3e–4e | 10h25 – 12h05 |
| 5e–6e | 13h00 – 14h40 |
| 7e–8e | 14h55 – 16h35 |

> Données de démonstration : à remplacer par les informations réelles de l'école.
"""


@mcp.prompt
def prepare_assessment(subject: str, year: str, chapter: str) -> str:
    """Prépare une évaluation écrite pour une classe.

    Args:
        subject: La matière concernée, par exemple « mathématiques ».
        year: L'année d'études, par exemple « 3e année ».
        chapter: Le chapitre ou la matière évaluée.
    """
    return f"""Tu aides un enseignant du Collège de Bruxelles à préparer une évaluation écrite.

- Matière : {subject}
- Année : {year}
- Chapitre évalué : {chapter}

Propose une évaluation d'une période (50 minutes) cotée sur 20, comprenant :

1. Les compétences visées, formulées en termes du référentiel.
2. Cinq à huit questions, de la restitution vers l'application et l'analyse.
3. Le barème détaillé, point par point.
4. Un corrigé succinct pour chaque question.

Rédige l'ensemble en français, dans un registre adapté à des élèves de {year}."""
