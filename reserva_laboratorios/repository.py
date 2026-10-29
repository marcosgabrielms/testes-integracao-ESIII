import json
from pathlib import Path


class ReservaRepository:
    def __init__(self, arquivo: Path):
        self.arquivo = arquivo

    def listar(self) -> list[dict]:
        if not self.arquivo.exists():
            return []
        return json.loads(self.arquivo.read_text(encoding="utf-8"))

    def salvar(self, reservas: list[dict]) -> None:
        self.arquivo.write_text(
            json.dumps(reservas, ensure_ascii=False, indent=2), encoding="utf-8"
        )
