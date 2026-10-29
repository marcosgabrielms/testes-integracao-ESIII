# Testes de integração — ESIII

Equipe: **Marcos Gabriel e Nicole Almeida**.

## Sistema de Controle de Estoque

Implementação do roteiro em `produto.py`, `produto_repository.py` e
`estoque_service.py`, com testes em `tests/test_estoque_integracao.py`.
Cada teste, incluindo cada caso parametrizado, recebe uma conexão SQLite
independente com `:memory:`, a tabela `produtos` e um produto com 10 unidades.
A fixture fecha a conexão ao final. As operações passam pelo Service e pelo
Repository; as verificações consultam diretamente o SQLite, sem mocks.
SQLite faz parte da biblioteca padrão do Python; a única dependência de testes
a instalar é pytest, conforme os comandos de instalação abaixo.

| Teste obrigatório | Objetivo | Resultado |
| --- | --- | --- |
| `test_adicionar_estoque_atualiza_banco` | Adicionar 5 unidades e verificar 15 no banco. | PASSED |
| `test_vender_produto_com_estoque_suficiente` | Vender 4 unidades e verificar saldo 6. | PASSED |
| `test_vender_produto_com_estoque_insuficiente_nao_altera_banco` | Tentar vender 11 unidades, verificar `EstoqueInsuficienteError` e banco inalterado. | PASSED |

O desafio `test_vender_produto_quantidades_parametrizadas` utiliza
`@pytest.mark.parametrize` e preserva o comportamento original:

| Quantidade vendida | Comportamento com estoque inicial 10 | Resultado |
| --- | --- | --- |
| `0` | Sem exceção; estoque permanece 10. | PASSED |
| `-3` | Sem exceção; estoque aumenta para 13, pois o Service subtrai um valor negativo. | PASSED |
| `11` | Lança `EstoqueInsuficienteError`; os dados no banco permanecem iguais. | PASSED |

O roteiro rejeita somente vendas acima do estoque disponível. Não foram
adicionadas validações para zero ou valores negativos. Também foi preservada
a ausência de `commit` em `atualizar_quantidade`: os testes consultam a mesma
conexão em memória, sem afirmar persistência após seu fechamento.

Para executar as duas partes na raiz do repositório com `python` da `.venv`,
sem alterar a política de execução do PowerShell:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
python -m pytest -v
```

Execução conjunta real em 29/10/2026, na raiz do repositório, com Python 3.15.2
da `.venv` e pytest 9.2.0: `python -m pytest -v` → **8 passed in 0.07s**,
sem falhas. Foram executados os 3 testes obrigatórios de estoque, os 3 casos
do desafio parametrizado e os 2 testes de Reserva de Laboratórios.
Os arquivos de `reserva_laboratorios/` foram preservados, com hashes SHA-256
iguais aos anteriores à implementação do estoque. O registro abaixo de 2 testes
refere-se à execução anterior, exclusiva do complemento.

## Complemento: Reserva de Laboratórios

O exemplo em `reserva_laboratorios/` é uma reconstrução mínima a partir de um
projeto anterior de ESII, que utilizava Python, FastAPI, arquitetura em camadas
e persistência JSON. Não se afirma que este código seja idêntico ao original.
O recorte implementa somente Service → Repository → JSON, sem API ou endpoints.

O Service recebe o laboratório e o início/fim como `datetime`, rejeita início
igual ou posterior ao fim e sobreposições no mesmo laboratório, permitindo
horários adjacentes. O Repository lê e grava um arquivo JSON.
Os testes usam `tmp_path` do pytest para criar um JSON isolado por teste, sem mocks.

No PowerShell, na raiz do projeto, crie o ambiente caso ainda não exista:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
```

Para executar todos os testes, sem precisar ativar o ambiente:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

O VS Code está configurado em `.vscode/settings.json` para usar
`.venv\Scripts\python.exe`, descobrir testes com pytest e disponibilizar o
ambiente nos novos terminais integrados. `.venv/` está no `.gitignore`.
Após uma alteração do PATH do usuário, reabra o PowerShell ou o VS Code.

| Teste | Objetivo | Resultado |
| --- | --- | --- |
| `test_reserva_valida_persiste_no_json` | Reservar pelo Service e conferir diretamente o JSON, incluindo a aceitação de um horário adjacente. | PASSED |
| `test_reserva_conflitante_nao_altera_json` | Rejeitar um horário sobreposto e conferir que os bytes do JSON permanecem iguais. | PASSED |

Execução real após a configuração do ambiente em 29/10/2026, no Windows,
com Python 3.15.2 e pytest 9.2.0:
`.\.venv\Scripts\python.exe -m pytest -v` → **2 passed in 0.08s**.
A `.venv` reutiliza a instalação existente de Python gerenciada pelo uv.
A execução anterior usava Python 3.12.10 em uma pasta temporária, que não
configurava o Python no terminal do usuário.
