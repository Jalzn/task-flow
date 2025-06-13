# TaskFlow - Sistema de Gerenciamento de Tarefas Empresariais

Um sistema CLI moderno para gerenciamento de tarefas em ambientes empresariais com múltiplos times e funcionários.

## Membros do Grupo

- Jalmir de Jesus Ferreira da Silva Junior
- Pedro Henrique de Mattos Gomes
- ...

## Explicação do Sistema

O TaskFlow é um sistema de linha de comando desenvolvido para empresas que precisam gerenciar tarefas entre diferentes times e funcionários. O sistema oferece funcionalidades para:

- **Gerenciamento de Times**: Criação, listagem e remoção de times
- **Gerenciamento de Funcionários**: Cadastro de funcionários em times específicos
- **Gerenciamento de Tarefas**: Criação, atribuição, atualização de status e listagem de tarefas
- **Relatórios**: Visualização de estatísticas por time e funcionário
- **Priorização**: Sistema de prioridades (Alta, Média, Baixa)
- **Status Tracking**: Acompanhamento do progresso das tarefas (Pendente, Em Progresso, Concluída)

O sistema utiliza uma interface de linha de comando intuitiva com comandos organizados por contexto (teams, employees, tasks) e oferece saída formatada com cores e tabelas para melhor experiência do usuário.

## Tecnologias Utilizadas

- **Python 3.11+**: Linguagem de programação principal
- **SQLModel**: ORM moderno para definição de modelos e interação com banco de dados
- **SQLite**: Banco de dados relacional leve para armazenamento
- **Typer**: Framework para criação de CLIs modernas e intuitivas
- **Rich**: Biblioteca para formatação rica de saída no terminal (cores, tabelas, progress bars)
- **Pydantic**: Validação de dados e serialização
- **Pytest**: Framework de testes unitários
- **Coverage.py**: Ferramenta de medição de cobertura de testes
- **GitHub Actions**: CI/CD para automação de testes
- **Codecov**: Plataforma para relatórios de cobertura online

### Estrutura do Projeto

```
taskflow/
├── README.md
├── requirements.txt
├── main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── employees/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   │   └── utils.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   │   └── utils.py
│   ├── teams/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   │   └── utils.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_models/
    ├── test_services/
    └── test_cli/
```

## Instalação e Uso

```bash
# Clonar o repositório
git clone https://github.com/Jalzn/taskflow.git
cd taskflow

# Instalar dependências
pip install -r requirements.txt

```

## Comandos Principais

```bash
# Gerenciar times
python main.py teams create --name "Desenvolvimento"  --description "Time de desenvolvimento de software"
python main.py teams list
python main.py teams delete 1

# Gerenciar funcionários
python main.py employees create --name "João Silva" --email "joao@empresa.com" --team 1
python main.py employees list
python main.py employees list-by-team 1

# Gerenciar tarefas
python main.py tasks create --name "Implementar feature X" --description "Descrição detalhada" --team 1 --status 1 --priority high
python main.py tasks list
python main.py tasks update-status 1 in_progress
python main.py tasks assign 1 2

# Relatórios
python main.py tasks stats
python main.py tasks by-team 1
```

## Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=taskflow --cov-report=html --cov-report=xml

# Ver relatório de cobertura
open htmlcov/index.html
```
