---
name: analyser-resultats
description: Analyse une série de notes d'interrogation ou d'examen et rédige un
  commentaire exploitable en conseil de classe. À utiliser dès qu'un enseignant
  fournit des notes, parle de résultats d'évaluation, de moyenne de classe ou de
  délibération.
allowed-tools: mcp__plugin_collegia_collegia__compute_class_average
---

# Analyser les résultats d'une évaluation

## Étapes

1. **Rassembler les données.** Relève les notes fournies et le barème. Si le
   barème n'est pas précisé, suppose /20 et signale-le dans ta réponse.

2. **Calculer.** Appelle `compute_class_average` avec les notes et le barème.
   N'estime jamais la moyenne toi-même : l'outil renvoie aussi la répartition
   réussite/échec, dont tu as besoin pour l'étape suivante.

3. **Interpréter avant de juger les élèves.** Une moyenne basse n'est pas
   automatiquement un problème de classe :
   - Moyenne sous 10/20 **et** plus de deux tiers d'échecs : évoque d'abord un
     problème de calibrage de l'épreuve ou de couverture de la matière.
   - Écart important entre la note minimale et maximale : signale une classe
     hétérogène, qui appelle une remédiation ciblée plutôt qu'une reprise
     collective.
   - Moyenne élevée avec peu de dispersion : l'épreuve n'a probablement pas
     discriminé les niveaux.

4. **Rédiger.** Trois à cinq lignes en français, dans un registre utilisable tel
   quel en conseil de classe. Termine par une action concrète proposée à
   l'enseignant.

## À éviter

- Ne nomme jamais d'élève : tu ne reçois que des notes, pas des identités.
- Ne conclus pas sur un effectif inférieur à cinq élèves ; dis que
  l'échantillon est trop petit pour être interprété.
