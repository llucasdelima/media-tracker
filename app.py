import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, abort
import pandas as pd
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

ARQUIVO_ODS = os.path.join(BASE_DIR, "media-tracker.ods")
PASTA_CAPAS = os.path.join(BASE_DIR, "static", "covers")
os.makedirs(PASTA_CAPAS, exist_ok=True)

CONFIG_MIDIAS = {
    "livros": {
        "slug": "livros",
        "nome_aba": "Livros",
        "titulo_singular": "Livro",
        "campo_criador": "Autor",
        "rotulo_criador": "Autor(es)",
        "tem_editora": True,
        "tem_iniciado": True,
        "tem_temporada": False,
        "colunas": ["Título", "Autor", "Editora", "Ano", "Tags", "Status", "Iniciado", "Finalizado", "Nota", "Consideração", "Capa"],
        "status_opcoes": ["Quero ler", "Lendo", "Lido", "Abandonado"]
    },
    "jogos": {
        "slug": "jogos",
        "nome_aba": "Jogos",
        "titulo_singular": "Jogo",
        "campo_criador": "Desenvolvedora",
        "rotulo_criador": "Desenvolvedora",
        "tem_editora": False,
        "tem_iniciado": True,
        "tem_temporada": False,
        "colunas": ["Título", "Desenvolvedora", "Ano", "Tags", "Status", "Iniciado", "Finalizado", "Nota", "Consideração", "Capa"],
        "status_opcoes": ["Quero jogar", "Jogando", "Finalizado", "Abandonado"]
    },
    "filmes": {
        "slug": "filmes",
        "nome_aba": "Filmes",
        "titulo_singular": "Filme",
        "campo_criador": "Diretor",
        "rotulo_criador": "Diretor(es)",
        "tem_editora": False,
        "tem_iniciado": False,
        "tem_temporada": False,
        "colunas": ["Título", "Diretor", "Ano", "Tags", "Status", "Finalizado", "Nota", "Consideração", "Capa"],
        "status_opcoes": ["Quero ver", "Assistido", "Abandonado"]
    },
    "series": {
        "slug": "series",
        "nome_aba": "Séries",
        "titulo_singular": "Série",
        "campo_criador": None,
        "rotulo_criador": None,
        "tem_editora": False,
        "tem_iniciado": True,
        "tem_temporada": True,
        "colunas": ["Título", "Temporada", "Ano", "Tags", "Status", "Iniciado", "Finalizado", "Nota", "Consideração", "Capa"],
        "status_opcoes": ["Quero ver", "Assistindo", "Assistido", "Abandonado"]
    }
}

def sanitizar_nome_capa(nome_capa):
    if not nome_capa:
        return ""
    nome = str(nome_capa).strip().lower()
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        if nome.endswith(ext):
            nome = nome[:-len(ext)]
            break
    return nome

def processar_upload_capa(arquivo_storage):
    if not arquivo_storage or arquivo_storage.filename == "":
        return ""

    try:
        id_unico = uuid.uuid4().hex[:10]
        nome_arquivo = f"{id_unico}.jpg"
        caminho_final = os.path.join(PASTA_CAPAS, nome_arquivo)

        img = Image.open(arquivo_storage)

        if img.mode in ("RGBA", "LA", "P"):
            fundo_branco = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                fundo_branco.paste(img, mask=img.split()[3])
            else:
                img_conv = img.convert("RGBA")
                fundo_branco.paste(img_conv, mask=img_conv.split()[3])
            img = fundo_branco
        elif img.mode != "RGB":
            img = img.convert("RGB")

        largura_max = 400
        if img.width > largura_max:
            proporcao = largura_max / float(img.width)
            altura_calc = int(float(img.height) * float(proporcao))
            img = img.resize((largura_max, altura_calc), Image.Resampling.LANCZOS)

        img.save(caminho_final, "JPEG", quality=85, optimize=True)
        return id_unico

    except Exception as e:
        print(f"Erro ao processar imagem de capa: {e}")
        return ""

def ler_aba(slug_midia):
    if not os.path.exists(ARQUIVO_ODS):
        return []
    config = CONFIG_MIDIAS[slug_midia]
    try:
        df = pd.read_excel(ARQUIVO_ODS, sheet_name=config["nome_aba"], engine="odf", dtype=str)
        df = df.fillna("")
        registros = df.to_dict(orient="records")
        for r in registros:
            if "Capa" in r:
                r["Capa"] = sanitizar_nome_capa(r["Capa"])
        return registros
    except Exception as e:
        print(f"Erro ao ler a aba {config['nome_aba']}: {e}")
        return []

def salvar_aba_completa(slug_midia, df_aba):
    todas_as_abas = {}
    if os.path.exists(ARQUIVO_ODS):
        todas_as_abas = pd.read_excel(ARQUIVO_ODS, sheet_name=None, engine="odf", dtype=str)

    config = CONFIG_MIDIAS[slug_midia]
    for col in config["colunas"]:
        if col not in df_aba.columns:
            df_aba[col] = ""
    df_aba = df_aba[config["colunas"]].fillna("")

    todas_as_abas[config["nome_aba"]] = df_aba

    for nome, d in todas_as_abas.items():
        todas_as_abas[nome] = d.fillna("")

    with pd.ExcelWriter(ARQUIVO_ODS, engine="odf", mode="w") as writer:
        for nome, d in todas_as_abas.items():
            d.to_excel(writer, sheet_name=nome, index=False)

def extrair_metadados(itens, config):
    todas_tags = set()
    criadores = set()
    editoras = set()

    for item in itens:
        tags_raw = item.get("Tags", "")
        if tags_raw:
            lista_t = [t.strip() for t in str(tags_raw).split(",") if t.strip()]
            item["lista_tags"] = lista_t
            todas_tags.update(lista_t)
        else:
            item["lista_tags"] = []

        campo_c = config["campo_criador"]
        if campo_c and item.get(campo_c):
            c_raw = item[campo_c]
            lista_c = [c.strip() for c in str(c_raw).split(",") if c.strip()]
            criadores.update(lista_c)

        if config["tem_editora"] and item.get("Editora"):
            editoras.add(item["Editora"].strip())

    return {
        "tags_disponiveis": sorted(list(todas_tags)),
        "criadores_disponiveis": sorted(list(criadores)),
        "editoras_disponiveis": sorted(list(editoras))
    }

@app.route("/")
def raiz():
    return redirect(url_for("visao_todos"))

@app.route("/todos")
def visao_todos():
    todos_itens = []

    for slug, config in CONFIG_MIDIAS.items():
        itens = ler_aba(slug)
        for idx, item in enumerate(itens):
            tags_raw = item.get("Tags", "")
            item["lista_tags"] = (
                [t.strip() for t in str(tags_raw).split(",") if t.strip()]
                if tags_raw
                else []
            )

            criador_exibicao = ""
            if config["campo_criador"] and item.get(config["campo_criador"]):
                criador_exibicao = item[config["campo_criador"]]
            elif config["tem_temporada"] and item.get("Temporada"):
                criador_exibicao = f"Temporada {item['Temporada']}"

            todos_itens.append({
                "item": item,
                "categoria_slug": slug,
                "categoria_nome": config["titulo_singular"],
                "item_id": idx,
                "criador_exibicao": criador_exibicao
            })

    return render_template(
        "index.html",
        itens=todos_itens,
        categoria_atual="todos",
        config_todas=CONFIG_MIDIAS
    )

@app.route("/<categoria>")
def listar(categoria):
    if categoria not in CONFIG_MIDIAS:
        return redirect(url_for("visao_todos"))

    config = CONFIG_MIDIAS[categoria]
    itens = ler_aba(categoria)
    meta = extrair_metadados(itens, config)

    return render_template(
        "index.html",
        itens=itens,
        categoria_atual=categoria,
        config=config,
        config_todas=CONFIG_MIDIAS,
        **meta
    )

@app.route("/<categoria>/novo")
def novo_item(categoria):
    if categoria not in CONFIG_MIDIAS:
        abort(404)

    config = CONFIG_MIDIAS[categoria]
    itens = ler_aba(categoria)
    meta = extrair_metadados(itens, config)

    return render_template(
        "novo.html",
        categoria_atual=categoria,
        config=config,
        **meta
    )

@app.route("/<categoria>/adicionar", methods=["POST"])
def adicionar(categoria):
    if categoria not in CONFIG_MIDIAS:
        abort(404)

    config = CONFIG_MIDIAS[categoria]
    novo = {}

    arquivo_capa = request.files.get("arquivo_capa")
    nome_capa = processar_upload_capa(arquivo_capa)

    for col in config["colunas"]:
        if col == "Capa":
            novo[col] = nome_capa
        else:
            novo[col] = request.form.get(col, "").strip()

    itens = ler_aba(categoria)
    df_atual = pd.DataFrame(itens)
    df_novo = pd.DataFrame([novo])
    df_final = pd.concat([df_atual, df_novo], ignore_index=True)
    salvar_aba_completa(categoria, df_final)

    return redirect(url_for("listar", categoria=categoria))

@app.route("/<categoria>/item/<int:item_id>")
def ver_item(categoria, item_id):
    if categoria not in CONFIG_MIDIAS:
        abort(404)

    config = CONFIG_MIDIAS[categoria]
    itens = ler_aba(categoria)
    if item_id < 0 or item_id >= len(itens):
        abort(404)

    item = itens[item_id]
    meta = extrair_metadados(itens, config)

    return render_template(
        "item.html",
        item=item,
        item_id=item_id,
        categoria_atual=categoria,
        config=config,
        **meta
    )

@app.route("/<categoria>/editar/<int:item_id>", methods=["POST"])
def editar_item(categoria, item_id):
    if categoria not in CONFIG_MIDIAS:
        abort(404)

    config = CONFIG_MIDIAS[categoria]
    itens = ler_aba(categoria)
    if item_id < 0 or item_id >= len(itens):
        abort(404)

    arquivo_capa = request.files.get("arquivo_capa")
    nova_capa = processar_upload_capa(arquivo_capa)

    registro_atualizado = {}
    for col in config["colunas"]:
        if col == "Capa":
            registro_atualizado[col] = nova_capa if nova_capa else itens[item_id].get("Capa", "")
        else:
            registro_atualizado[col] = request.form.get(col, "").strip()

    itens[item_id] = registro_atualizado
    df_final = pd.DataFrame(itens)
    salvar_aba_completa(categoria, df_final)

    return redirect(url_for("ver_item", categoria=categoria, item_id=item_id))

@app.route("/<categoria>/deletar/<int:item_id>", methods=["POST"])
def deletar_item(categoria, item_id):
    if categoria not in CONFIG_MIDIAS:
        abort(404)

    itens = ler_aba(categoria)
    if item_id < 0 or item_id >= len(itens):
        abort(404)

    itens.pop(item_id)
    df_final = pd.DataFrame(itens)
    salvar_aba_completa(categoria, df_final)

    return redirect(url_for("listar", categoria=categoria))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
