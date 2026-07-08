# GGEMMA — Vitrine de Produtos

Site estático (GitHub Pages) que reúne os produtos e ferramentas Python desenvolvidos no ecossistema **GGEMMA**.

## Produtos na vitrine

| Produto | Página | Status |
|---------|--------|--------|
| **extrator_info_files** | [`docs/extrator.html`](docs/extrator.html) | Publicado no [GitHub](https://github.com/AndressaLF/extrator_info_files) |
| **batimetria_kml_shape** | [`docs/batimetria.html`](docs/batimetria.html) | Repositório local |

## Visualizar localmente

Abra `docs/index.html` no navegador ou sirva a pasta com um servidor estático:

```powershell
cd ggemma_projects\docs
python -m http.server 8080
# Acesse http://localhost:8080
```

## Publicar no GitHub Pages

1. Crie o repositório `ggemma_projects` no GitHub (se ainda não existir).
2. Envie este conteúdo para a branch `main`.
3. Em **Settings → Pages**, configure:
   - **Source:** Deploy from a branch
   - **Branch:** `main` / **`/docs`**
4. Aguarde alguns minutos. O site ficará em:

   `https://<seu-usuario>.github.io/ggemma_projects/`

O arquivo `.nojekyll` na pasta `docs/` evita que o GitHub Pages processe o site com Jekyll.

## Adicionar um novo produto

1. Crie `docs/<nome-do-produto>.html` seguindo o padrão das páginas existentes.
2. Adicione um card em `docs/index.html`.
3. Atualize a tabela neste README.

## Estrutura

```
ggemma_projects/
├── README.md
└── docs/
    ├── .nojekyll
    ├── index.html          # Página principal (vitrine)
    ├── extrator.html       # extrator_info_files
    ├── batimetria.html     # batimetria_kml_shape
    └── assets/
        └── style.css
```
