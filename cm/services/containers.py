from dependency_injector import containers, providers
from rich.console import Console

from .github import GithubConfig, GitService


class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Singleton(GithubConfig)
    console = providers.Singleton(Console)
    git = providers.Singleton(GitService, config=config, console=console)
