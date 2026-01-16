import shutil
from pathlib import Path
from urllib.parse import urlparse

import git
from git.exc import GitCommandError
from rich.console import Console

from .config import GithubConfig


def extract_repo_name(url: str) -> str:
    """Extrai o nome do repositório de uma URL.

    Args:
        url: URL do repositório (com ou sem .git).

    Returns:
        Nome do repositório sem .git.

    """
    parsed = urlparse(url.strip())
    path = parsed.path.strip("/")
    repo_name = path.split("/")[-1] if path else ""
    return repo_name.removesuffix(".git")


def normalize_clone_url(url: str) -> str:
    """Normaliza a URL para clone adicionando .git se necessário.

    Args:
        url: URL do repositório (com ou sem .git).

    Returns:
        URL normalizada com .git no final.

    """
    parsed = urlparse(url.strip())
    if not parsed.path.endswith(".git"):
        new_path = f"{parsed.path}.git" if parsed.path else ".git"
        return parsed._replace(path=new_path).geturl()
    return url.strip()


class GitService:
    def __init__(self, config: GithubConfig, console: Console) -> None:
        self.config = config
        self.console = console

    def list_repos(self) -> list[str]:
        """Lista repositórios git no workspace."""
        workspace = Path(self.config.workspace_dir)
        return [str(path.parent) for path in workspace.rglob(".git") if path.is_dir()]

    def _try_clone(self, url: str, repo_path: Path, branch: str | None = None) -> bool:
        """Tenta clonar o repositório com o branch especificado."""

        def _cleanup() -> None:
            """Remove diretório parcialmente criado em caso de erro."""
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)

        try:
            if branch:
                git.Repo.clone_from(url, str(repo_path), branch=branch)
            else:
                git.Repo.clone_from(url, str(repo_path))

            is_valid = repo_path.exists() and (repo_path / ".git").exists()
            if is_valid:
                self.console.print(
                    f"[green bold]Repositório {url} clonado com sucesso em: {repo_path}[/]"
                )
            else:
                self.console.print(
                    f"[red bold]Falha ao clonar repositório: {url} não foi criado[/]"
                )
                _cleanup()
            return is_valid
        except GitCommandError:
            self.console.print(f"[red bold]Falha ao clonar repositório: {url}[/]")
            _cleanup()
            return False
        except Exception as e:
            self.console.print(f"[red bold]Erro ao clonar repositório: {e}[/]")
            _cleanup()
            return False

    def clone_url(self, url: str, branch: str | None = None, force: bool = False) -> Path:
        """Clona um repositório a partir de uma URL.

        Args:
            url: URL do repositório (com ou sem .git).
            branch: Branch específico para clonar. Se None, tenta main/master ou padrão.
            force: Se True, sobrescreve o repositório se já existir.

        Returns:
            Path: Caminho do repositório clonado.

        Raises:
            ValueError: Se a URL for inválida ou o repositório já existir.
            RuntimeError: Se o clone falhar após todas as tentativas.

        """
        if not url or not url.strip():
            raise ValueError("URL do repositório não pode ser vazia")

        clone_url, repo_name = normalize_clone_url(url), extract_repo_name(url)
        repo_path = Path(self.config.workspace_dir) / repo_name

        if repo_path.exists():
            if not force:
                msg = (
                    f"Repositório {repo_name} já existe em {repo_path}. "
                    "Use force=True para sobrescrever."
                )
                raise ValueError(msg)
            shutil.rmtree(repo_path, ignore_errors=True)

        # Se branch especificado e diferente de main/master, clona com esse branch
        # Caso contrário, clona sem especificar branch (usa o padrão do repositório)
        branch_to_clone = branch if branch and branch not in {"main", "master"} else None

        if self._try_clone(clone_url, repo_path, branch_to_clone):
            return repo_path

        msg = f"Falha ao clonar repositório: {repo_path} não foi criado"
        raise RuntimeError(msg)

    def delete_repo(self, target: str) -> Path:
        """Remove um repositório do workspace.

        Args:
            target: Nome do repositório ou caminho para o diretório.

        Returns:
            Path: Caminho removido.

        Raises:
            ValueError: Se o target for inválido ou fora do workspace.
            FileNotFoundError: Se o target não existir.

        """
        if not target or not target.strip():
            raise ValueError("Nome ou caminho do repositório não pode ser vazio")

        workspace = Path(self.config.workspace_dir).resolve()
        target_path = Path(target)

        if not target_path.is_absolute():
            target_path = workspace / target_path

        target_path = target_path.resolve()

        if target_path == workspace:
            raise ValueError("Não é permitido remover o diretório raiz do workspace")

        if not target_path.is_relative_to(workspace):
            raise ValueError("O repositório precisa estar dentro do workspace")

        if not target_path.exists():
            msg = f"Repositório não encontrado: {target_path}"
            raise FileNotFoundError(msg)

        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()

        self.console.print(f"[green]Repositório removido: {target_path}[/green]")
        return target_path
