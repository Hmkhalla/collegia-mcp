"""Point d'entrée du serveur MCP du Collège de Bruxelles."""

from __future__ import annotations

import os

from collegia_mcp.server import mcp

__all__ = ["main", "mcp"]


def main() -> None:
    """Lance le serveur en HTTP local (streamable HTTP sur /mcp)."""
    mcp.run(
        transport="http",
        host=os.getenv("COLLEGIA_MCP_HOST", "127.0.0.1"),
        port=int(os.getenv("COLLEGIA_MCP_PORT", "8000")),
        path=os.getenv("COLLEGIA_MCP_PATH", "/mcp"),
    )
