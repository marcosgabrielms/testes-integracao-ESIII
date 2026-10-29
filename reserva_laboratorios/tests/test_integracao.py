import json
from datetime import datetime

import pytest

from reserva_laboratorios.repository import ReservaRepository
from reserva_laboratorios.service import ReservaService


def test_reserva_valida_persiste_no_json(tmp_path):
    arquivo = tmp_path / "reservas.json"
    service = ReservaService(ReservaRepository(arquivo))

    service.reservar(
        "Lab 1", datetime(2026, 10, 29, 8), datetime(2026, 10, 29, 9)
    )

    esperado = [
        {
            "laboratorio": "Lab 1",
            "inicio": "2026-10-29T08:00:00",
            "fim": "2026-10-29T09:00:00",
        }
    ]
    assert json.loads(arquivo.read_text(encoding="utf-8")) == esperado

    # O início igual ao fim da reserva anterior é permitido.
    service.reservar(
        "Lab 1", datetime(2026, 10, 29, 9), datetime(2026, 10, 29, 10)
    )
    esperado.append(
        {
            "laboratorio": "Lab 1",
            "inicio": "2026-10-29T09:00:00",
            "fim": "2026-10-29T10:00:00",
        }
    )
    assert json.loads(arquivo.read_text(encoding="utf-8")) == esperado


def test_reserva_conflitante_nao_altera_json(tmp_path):
    arquivo = tmp_path / "reservas.json"
    service = ReservaService(ReservaRepository(arquivo))
    service.reservar(
        "Lab 1", datetime(2026, 10, 29, 8), datetime(2026, 10, 29, 10)
    )
    conteudo_anterior = arquivo.read_bytes()

    with pytest.raises(ValueError, match="Horário conflitante"):
        service.reservar(
            "Lab 1", datetime(2026, 10, 29, 9), datetime(2026, 10, 29, 11)
        )

    assert arquivo.read_bytes() == conteudo_anterior
