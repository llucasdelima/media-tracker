function tratarErroCapa(img) {
  const nomeArquivo = img.dataset.capa;
  if (!img.dataset.tentouPng) {
    img.dataset.tentouPng = "true";
    img.src = `/static/covers/${nomeArquivo}.png`;
  } else {
    img.style.display = "none";
  }
}

function configurarChipsInput(wrapperId, inputId, hiddenId) {
  const wrapper = document.getElementById(wrapperId);
  const inputField = document.getElementById(inputId);
  const hiddenInput = document.getElementById(hiddenId);

  if (!wrapper || !inputField || !hiddenInput) return;

  const valorInicial = wrapper.dataset.initial || hiddenInput.value || "";
  const itens = valorInicial
    ? valorInicial
        .split(",")
        .map((i) => i.trim())
        .filter((i) => i.length > 0)
    : [];

  function atualizar() {
    // Remove apenas as tags geradas anteriormente
    const chipsExistentes = wrapper.querySelectorAll(".tags.has-addons");
    chipsExistentes.forEach((el) => el.remove());

    itens.forEach((item, index) => {
      // Contêiner principal agrupador do Bulma
      const tagGroup = document.createElement("div");
      tagGroup.className = "tags has-addons mb-2 mr-2 is-inline-flex";

      // Tag com o texto do item
      const tagText = document.createElement("span");
      tagText.className = "tag is-medium";
      tagText.textContent = item;

      // Botão 'X' de delete nativo do Bulma
      const tagDelete = document.createElement("a");
      tagDelete.className = "tag is-medium is-delete is-danger";
      tagDelete.setAttribute("role", "button");
      tagDelete.setAttribute("aria-label", `Remover ${item}`);

      tagDelete.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        removerItem(index);
      });

      // Monta a estrutura: <div class="tags has-addons"><span>...</span><a></a></div>
      tagGroup.appendChild(tagText);
      tagGroup.appendChild(tagDelete);

      wrapper.insertBefore(tagGroup, inputField);
    });

    hiddenInput.value = itens.join(", ");
  }

  function adicionarItem(texto) {
    const limpo = texto.replace(/,/g, "").trim();
    if (limpo && !itens.includes(limpo)) {
      itens.push(limpo);
      atualizar();
    }
    inputField.value = "";
  }

  function removerItem(index) {
    itens.splice(index, 1);
    atualizar();
  }

  inputField.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      adicionarItem(inputField.value);
    } else if (e.key === "Backspace" && inputField.value === "" && itens.length > 0) {
      removerItem(itens.length - 1);
    }
  });

  inputField.addEventListener("input", () => {
    if (inputField.value.includes(",")) {
      adicionarItem(inputField.value);
    }
  });

  inputField.addEventListener("change", () => {
    if (inputField.value.trim() !== "") {
      adicionarItem(inputField.value);
    }
  });

  atualizar();
}

document.addEventListener("DOMContentLoaded", () => {
  configurarChipsInput("criador-wrapper", "criador-input-field", "criador-hidden");
  configurarChipsInput("tags-wrapper", "tag-input-field", "tags-hidden");
});
