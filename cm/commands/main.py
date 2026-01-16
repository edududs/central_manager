"""Aplicação principal de comandos CLI."""

import typer

from ..services import ServicesContainer
from . import git

app = typer.Typer(
    help="Ferramenta central de comandos para gerenciamento de workspace.",
    no_args_is_help=True,
)
service_container = ServicesContainer()
console = service_container.console()


def _print_list(repos: list[str]) -> None:
    if not repos:
        console.print("[yellow]Nenhum repositório encontrado no workspace.[/]")
        raise typer.Exit(code=0)

    console.print(f"[cyan]Repositórios encontrados ({len(repos)}):[/]")
    for repo_path in repos:
        console.print(f"  • {repo_path}")


def _run_clone(url: str, branch: str | None, force: bool) -> None:
    repo_path = git.clone_repo(service_container, url, branch=branch, force=force)
    console.print(f"[green]✓ Repositório clonado com sucesso em: {repo_path}[/]")


def _run_delete(target: str) -> None:
    repo_path = git.delete_repo(service_container, target)
    console.print(f"[green]✓ Repositório removido com sucesso: {repo_path}[/]")


def _handle_cli_error(exc: Exception) -> None:
    console.print(f"[red bold]Erro: {exc!s}[/]")
    raise typer.Exit(code=1)


@app.command()
def clone(
    url: str = typer.Argument(..., help="URL do repositório GitHub"),
    branch: str | None = typer.Option(None, "--branch", "-b", help="Branch específico para clonar"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Sobrescreve repositório se já existir"
    ),
) -> None:
    """Clona um repositório GitHub no workspace."""
    try:
        _run_clone(url, branch=branch, force=force)
    except Exception as exc:
        _handle_cli_error(exc)


@app.command(name="list")
def list_command() -> None:
    """Lista todos os repositórios clonados no workspace."""
    try:
        repos = git.list_repos(service_container)
        _print_list(repos)
    except Exception as exc:
        _handle_cli_error(exc)


@app.command()
def delete(
    target: str = typer.Argument(..., help="Nome do repositório ou caminho"),
    force: bool = typer.Option(False, "--force", "-f", help="Remove sem confirmação"),
) -> None:
    """Remove um repositório do workspace."""
    try:
        if not force and not typer.confirm(
            f"Confirma remover '{target}' do workspace?", default=False
        ):
            raise typer.Exit(code=0)
        _run_delete(target)
    except Exception as exc:
        _handle_cli_error(exc)


def main() -> None:
    """Executa a aplicação Typer."""
    app()


__all__ = ["app", "main"]
