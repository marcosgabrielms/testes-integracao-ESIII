from datetime import datetime

from .repository import ReservaRepository


class ReservaService:
    def __init__(self, repository: ReservaRepository):
        self.repository = repository

    def reservar(self, laboratorio: str, inicio: datetime, fim: datetime) -> dict:
        if inicio >= fim:
            raise ValueError("O início deve ser anterior ao fim da reserva.")

        reservas = self.repository.listar()
        for reserva in reservas:
            if (
                reserva["laboratorio"] == laboratorio
                and inicio < datetime.fromisoformat(reserva["fim"])
                and fim > datetime.fromisoformat(reserva["inicio"])
            ):
                raise ValueError("Horário conflitante com uma reserva existente.")

        reserva = {
            "laboratorio": laboratorio,
            "inicio": inicio.isoformat(),
            "fim": fim.isoformat(),
        }
        self.repository.salvar(reservas + [reserva])
        return reserva
