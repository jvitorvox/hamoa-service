"""
MCP Server - Acesso a arquivos do repositório GitHub
Utiliza FastMCP para expor ferramentas que listam e leem arquivos da pasta /data
"""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Diretório onde os arquivos ficam armazenados
DATA_DIR = Path(__file__).parent / "data"

# Inicializa o servidor FastMCP
mcp = FastMCP("file-server")


@mcp.tool()
def list_files() -> str:
    """
    Lista todos os arquivos disponíveis na pasta /data.
    Retorna os nomes dos arquivos separados por linha.
    """
    if not DATA_DIR.exists():
        return "Pasta /data não encontrada."

    files = [f.name for f in DATA_DIR.iterdir() if f.is_file()]

    if not files:
        return "Nenhum arquivo encontrado na pasta /data."

    return "Arquivos disponíveis:\n" + "\n".join(f"- {f}" for f in sorted(files))


@mcp.tool()
def read_file(filename: str) -> str:
    """
    Lê e retorna o conteúdo de um arquivo da pasta /data.

    Args:
        filename: Nome do arquivo a ser lido (ex: 'exemplo.sql')
    """
    if not filename:
        return "Erro: nome do arquivo não informado."

    # Previne path traversal (ex: ../../etc/passwd)
    safe_name = Path(filename).name
    file_path = DATA_DIR / safe_name

    if not file_path.exists():
        available = [f.name for f in DATA_DIR.iterdir() if f.is_file()]
        hint = "\n".join(f"- {f}" for f in sorted(available)) if available else "Nenhum arquivo disponível."
        return f"Arquivo '{safe_name}' não encontrado.\n\nArquivos disponíveis:\n{hint}"

    if not file_path.is_file():
        return f"'{safe_name}' não é um arquivo válido."

    try:
        content = file_path.read_text(encoding="utf-8")
        return f"=== {safe_name} ===\n\n{content}"
    except UnicodeDecodeError:
        # Fallback para arquivos com encoding diferente
        try:
            content = file_path.read_text(encoding="latin-1")
            return f"=== {safe_name} ===\n\n{content}"
        except Exception as e:
            return f"Erro ao ler o arquivo '{safe_name}': {e}"
    except Exception as e:
        return f"Erro inesperado ao ler '{safe_name}': {e}"


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=port)
