from abc import ABC
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings, ABC):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class GithubConfig(BaseConfig):
    github_token: str = Field(default="", description="Token do usuário do GitHub")
    git_email: str = Field(default="", description="Email do usuário do GitHub")
    root_dir: Path | str = Field(default=Path.cwd(), description="Diretório raiz do workspace")
    workspace_dir: Path | str = Field(
        default=Path.cwd() / "projects", description="Diretório do workspace"
    )

    @field_validator("workspace_dir")
    @classmethod
    def validate_workspace_dir(cls, v: Path | str) -> Path:
        if isinstance(v, Path):
            if not v.exists():
                v.mkdir(parents=True, exist_ok=True)
            return v
        if not Path(v).exists():
            Path(v).mkdir(parents=True, exist_ok=True)
        return Path(v).resolve()
