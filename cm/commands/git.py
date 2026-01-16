"""Casos de uso de Git para CLI/TGUI."""

from pathlib import Path

from ..services import ServicesContainer


def list_repos(container: ServicesContainer) -> list[str]:
    """Lista repositórios clonados no workspace."""
    service = container.git()
    return service.list_repos()


def clone_repo(
    container: ServicesContainer,
    url: str,
    branch: str | None = None,
    force: bool = False,
) -> Path:
    """Clona um repositório no workspace."""
    service = container.git()
    return service.clone_url(url, branch=branch, force=force)


def delete_repo(container: ServicesContainer, target: str) -> Path:
    """Remove um repositório do workspace."""
    service = container.git()
    return service.delete_repo(target)
