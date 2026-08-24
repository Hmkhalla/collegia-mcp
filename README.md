# collegia-mcp

Serveur MCP du **Collège de Bruxelles**, destiné aux enseignants : il expose des outils,
des ressources et des prompts qui rendent les agents IA plus utiles pour la préparation
de cours, la correction et les tâches administratives.

> État actuel : squelette de démonstration. Un exemple de chaque primitive MCP,
> servi en HTTP en local.

## Démarrer

```bash
uv sync
uv run collegia-mcp
```

Le serveur écoute sur `http://127.0.0.1:8000/mcp` (streamable HTTP).
Variables d'environnement : `COLLEGIA_MCP_HOST`, `COLLEGIA_MCP_PORT`, `COLLEGIA_MCP_PATH`.

Autres commandes utiles :

```bash
uv run fastmcp dev src/collegia_mcp/server.py      # MCP Inspector
uv run fastmcp inspect src/collegia_mcp/server.py  # lister les composants
```

## Composants exposés

| Type | Nom | Rôle |
| --- | --- | --- |
| Outil | `compute_class_average` | Moyenne, extrêmes et taux de réussite d'une série de notes. |
| Ressource | `collegia://etablissement/infos` | Fiche d'identité de l'école (coordonnées, niveaux, horaire type). |
| Prompt | `prepare_assessment` | Prépare une évaluation écrite pour une matière, une année et un chapitre. |

## Brancher un client MCP

```json
{
  "mcpServers": {
    "collegia": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```
