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

---

## To-Do

Fase 1: Interface e Usabilidade Local

 * [ ] Alternador de Visualização (Cards vs. Lista)
   * [ ] Adicionar botões seletores no topo da página com ícones do Tabler Icons (ti-layout-grid e ti-list).
   * [ ] Implementar a tabela do Bulma (<table class="table is-fullwidth">) para a visualização compacta.
   * [ ] Criar alternância via JavaScript persistindo a preferência no localStorage.
 * [ ] Paginação de Resultados
   * [ ] Tratar parâmetros de consulta (?page=1) no backend com Pandas.
   * [ ] Renderizar o componente nativo de navegação pagination do Bulma.
   * [ ] Permitir ajustar a quantidade de itens por página.

Fase 2: Automação e Busca de Metadados (APIs Externas)

 * [ ] Filmes e Séries (TMDB API)
   * [ ] Criar conta gratuita no TMDB e obter a chave de API.
   * [ ] Adicionar campo de busca por título no formulário de cadastro.
   * [ ] Preencher automaticamente título, sinopse, ano, diretor/criador e capa oficial.
 * [ ] Livros (Open Library API / Google Books API)
   * [ ] Implementar consulta aberta via Open Library (sem necessidade de chaves).
   * [ ] Extrair título, autor, ano de publicação e download automático de capa via ISBN/título.
 * [ ] Jogos (RAWG API / Steam API)
   * [ ] Obter chave de API gratuita no RAWG.
   * [ ] Buscar e autopreencher estúdio/desenvolvedor, gênero, plataformas e arte de capa.

Fase 3: Segurança e Controle de Acesso

 * [ ] Autenticação de Usuários
   * [ ] Avaliar método de proteção: tela de login nativa no Flask vs. autenticação no Cloudflare Access (Zero Trust).
   * [ ] Caso opte por login nativo: implementar Flask-Login ou controle por sessão com senhas criptografadas (hash).

Fase 4: Conteinerização e Deploy no Servidor

 * [ ] Ambiente de Produção (Podman)
   * [ ] Criar Containerfile com base Python e servidor WSGI (Gunicorn).
   * [ ] Criar compose.yaml com volumes nomeados para media-tracker.ods e static/covers/ usando o modificador :Z (SELinux).
   * [ ] Executar e validar contêiner em modo rootless no servidor Fedora.
 * [ ] Acesso Remoto (Cloudflare Tunnel)
   * [ ] Criar rota de serviço HTTP no Cloudflare Tunnel apontando para o contêiner interno (localhost:5050).
   * [ ] Configurar subdomínio próprio com certificado SSL automático 