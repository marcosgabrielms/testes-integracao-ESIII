# Testes de integração — ESIII

Dupla: **Marcos Gabriel e Nicole Almeida**.

Nesta atividade de Engenharia de Software III, usamos Python e pytest para
testar a integração entre as regras de negócio e o armazenamento dos dados.
O sistema de estoque usa SQLite em memória, com um banco independente por teste.

Como complemento, reconstruímos uma parte do Sistema de Reserva de Laboratórios
com base no projeto anterior de ESII. Essa versão usa arquivos JSON temporários
e não inclui a API. Em ambos os sistemas, os testes conferem os dados diretamente
no armazenamento, sem mocks.

## Testes implementados

Os testes de estoque começam com um produto de 10 unidades.

| Sistema | Teste | O que verifica |
| --- | --- | --- |
| Estoque | Adição de estoque | Adicionar 5 unidades deixa 15 no banco. |
| Estoque | Venda com estoque suficiente | Vender 4 unidades deixa saldo de 6. |
| Estoque | Venda com estoque insuficiente | Vender 11 gera uma exceção e mantém os dados do banco. |
| Estoque | Venda de zero unidades | Não gera exceção e mantém o estoque em 10. |
| Estoque | Venda de quantidade negativa | Vender -3 não gera exceção e aumenta o estoque para 13. |
| Estoque | Venda acima do estoque | Vender 11 gera uma exceção e não altera o banco. |
| Reservas | Reserva válida | Confirma a gravação no JSON e permite horários adjacentes. |
| Reservas | Reserva conflitante | Rejeita horários sobrepostos e mantém o JSON sem alterações. |

Os casos de venda com zero, quantidade negativa e valor acima do estoque fazem
parte do desafio com `@pytest.mark.parametrize`. Mantivemos as regras do roteiro:
somente vendas acima do estoque disponível são rejeitadas.

## Como executar

Com Python instalado, abra o PowerShell na pasta do projeto. Crie o ambiente
virtual, caso ainda não exista, e instale o pytest:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
```

Execute todos os testes com o Python da `.venv`, sem precisar ativá-la:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Na execução os **8 testes foram aprovados** sem falhas:
6 casos de estoque e 2 de reservas. O resultado foi `8 passed in 0.06s`.
