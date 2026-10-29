import sqlite3

import pytest

from estoque_service import EstoqueInsuficienteError, EstoqueService
from produto import Produto
from produto_repository import ProdutoRepository


@pytest.fixture
def ambiente_estoque():
    conexao = sqlite3.connect(":memory:")
    try:
        conexao.execute(
            """
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                quantidade INT NOT NULL
            );
            """
        )
        repositorio = ProdutoRepository(conexao)
        repositorio.salvar(Produto(1, "Caneta", 10))
        yield conexao, EstoqueService(repositorio)
    finally:
        conexao.close()


def test_adicionar_estoque_atualiza_banco(ambiente_estoque):
    conexao, service = ambiente_estoque

    service.adicionar_estoque(1, 5)

    linha = conexao.execute(
        "SELECT id, nome, quantidade FROM produtos WHERE id = ?", (1,)
    ).fetchone()
    assert linha == (1, "Caneta", 15)


def test_vender_produto_com_estoque_suficiente(ambiente_estoque):
    conexao, service = ambiente_estoque

    service.vender_produto(1, 4)

    linha = conexao.execute(
        "SELECT id, nome, quantidade FROM produtos WHERE id = ?", (1,)
    ).fetchone()
    assert linha == (1, "Caneta", 6)


def test_vender_produto_com_estoque_insuficiente_nao_altera_banco(ambiente_estoque):
    conexao, service = ambiente_estoque
    antes = conexao.execute("SELECT id, nome, quantidade FROM produtos").fetchall()

    with pytest.raises(
        EstoqueInsuficienteError, match="^Estoque insuficiente para o produto 1$"
    ):
        service.vender_produto(1, 11)

    depois = conexao.execute("SELECT id, nome, quantidade FROM produtos").fetchall()
    assert depois == antes == [(1, "Caneta", 10)]


@pytest.mark.parametrize(
    "quantidade, estoque_esperado, deve_falhar",
    [
        pytest.param(0, 10, False, id="zero"),
        pytest.param(-3, 13, False, id="negativa"),
        pytest.param(11, 10, True, id="maior-que-estoque"),
    ],
)
def test_vender_produto_quantidades_parametrizadas(
    ambiente_estoque, quantidade, estoque_esperado, deve_falhar
):
    conexao, service = ambiente_estoque
    antes = conexao.execute("SELECT id, nome, quantidade FROM produtos").fetchall()

    if deve_falhar:
        with pytest.raises(
            EstoqueInsuficienteError, match="^Estoque insuficiente para o produto 1$"
        ):
            service.vender_produto(1, quantidade)
    else:
        service.vender_produto(1, quantidade)

    depois = conexao.execute("SELECT id, nome, quantidade FROM produtos").fetchall()
    assert depois == [(1, "Caneta", estoque_esperado)]
    if deve_falhar:
        assert depois == antes
