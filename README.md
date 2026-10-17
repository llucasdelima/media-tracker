# Media Tracker

Aplicação web minimalista para catalogação e acompanhamento de consumo de mídia (livros, jogos, filmes e séries), utilizando planilhas locais no formato OpenDocument (`.ods`) como banco de dados.

Construído com foco em simplicidade, soberania de dados e sem dependências pesadas de bancos de dados relacionais.

---

## Recursos

- **Persistência em `.ods`**: Gravação e leitura direta em planilhas locais via Pandas e ODFpy.
- **Categorização Personalizada**: Abas separadas com campos específicos para livros, jogos, filmes e séries.
- **Visão Unificada e Filtrada**: Listagem agregada de todas as mídias ou navegação por categorias individuais.
- **Entrada Dinâmica de Tags e Criadores**: Componente de chips nativos baseado em componentes do Bulma com seleção via `datalist`.
- **Avaliação Numérica**: Seletor simplificado de notas de 1 a 10.
- **Gestão de Capas**: Upload, tratamento de dimensões e limpeza de arquivos de capa órfãos em disco.

---

## Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)
- [ODFpy](https://pypi.org/project/odfpy/)
- [Pillow (PIL)](https://python-pillow.org/)
- [Bulma CSS](https://bulma.io/)
- [Tabler Icons](https://tabler.io/icons)

---

## Estrutura do Projeto

```text
media-tracker/
├── app.py                  # Rotas e regras de negócio da aplicação Flask
├── media-tracker.ods       # Planilha de dados (mídias catalogadas)
├── requirements.txt        # Dependências do Python
├── static/
│   ├── covers/             # Armazenamento local de capas (.jpg / .png)
│   ├── css/                # Folhas de estilo adicionais
│   ├── img/                # Pasta para imagens dos site
│   └── js/
│       └── main.js         # Lógica dos componentes dinâmicos (tags/chips)
└── templates/
    ├── base.html           # Layout base Jinja2
    ├── index.html          # Listagem unificada e filtrada de itens
    ├── item.html           # Edição e exclusão de registro
    └── novo.html           # Formulário de cadastro de novo item
```

## Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- Gerenciador de pacotes `pip`

### 1. Clonar o repositório

```bash
git clone [https://github.com/SEU_USUARIO/media-tracker.git](https://github.com/SEU_USUARIO/media-tracker.git)
cd media-tracker
```

### 2. Configurar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

_(Caso não tenha um `requirements.txt` gerado, as dependências base são: `flask`, `pandas`, `odfpy` e `pillow`)._

### 4. Executar o servidor de desenvolvimento

```bash
flask run --debug
```

Acesse a interface no navegador através de `http://127.0.0.1:5000`.

---

## Licença

Este projeto é disponibilizado para fins de estudo e uso pessoal.

### Referências oficiais

- [Documentação do Flask — Estrutura de Projetos e Instalação](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Documentação do GitHub — Criando e formatando READMEs](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
