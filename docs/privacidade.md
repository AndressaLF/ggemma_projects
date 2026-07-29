# Privacidade na vitrine (o que pode e o que não pode ir ao Git)

Checklist antes de cada `git push` deste repositório.

---

## 📑 Sumário

- [✅ Pode versionar](#pode-versionar)
- [⛔ Nunca versionar](#nunca-versionar)
- [🔗 URLs e handles](#urls-e-handles)
- [🧹 Antes do push](#antes-do-push)

---

<a id="pode-versionar"></a>

## ✅ Pode versionar

- HTML/CSS/imagens em `docs/` (descrição genérica das ferramentas)
- README, LICENSE, `tools/sync_versions.py`, `tools/versions.toml`
- Links Pages em `andressalf.github.io` e site público do lab (`ggemma-ufrn.com`)
- `.gitignore`

---

<a id="nunca-versionar"></a>

## ⛔ Nunca versionar

| Item | Motivo |
|------|--------|
| `cursor_*.md` / `cursor_ggemma*` / transcripts | E-mail, paths, handles, histórico de setup |
| `scripts/` e `tools/_*.py` | Manutenção / patches locais |
| `.venv/`, caches Python | Ambiente local |
| `.env`, `*.local.toml`, `*.pem`, `*.key` | Segredos / overrides |
| Nomes de campanha, cliente, rota, embarcação | Identificação de projeto interno |
| `C:\Users\…`, `Y:\…`, `D:\Campanha` etc. | Paths pessoais / de disco local |
| E-mails, PATs, chaves SSH | Credenciais |
| Favicons experimentais obsoletos (`favicon.svg`, `favicon_ggemma_16x16.png`) | Substituídos por `favicon.ico` / `favicon.png` |

---

<a id="urls-e-handles"></a>

## 🔗 URLs e handles

Nos docs versionados use o handle público `andressalf` e o site institucional:

```text
https://andressalf.github.io/ggemma_projects/
https://www.ggemma-ufrn.com/
```

Ainda **não** versionar e-mails, paths locais (`C:\Users\…`, `Y:\…`, `D:\…`) nem nomes de campanha.
Em exemplos de comando, use caminhos relativos (`./pasta_campanha`).

---

<a id="antes-do-push"></a>

## 🧹 Antes do push

```powershell
# Na pasta ggemma_projects
Select-String -Path docs\*.html,docs\assets\*.svg,README.md -Pattern "@gmail|C:\\Users|Y:\\|[A-Z]:\\" -CaseSensitive:$false
git status
git check-ignore -v cursor_ggemma_project_showcase.md scripts/
```

Se o `Select-String` achar e-mail ou path de disco (`C:\…`, `D:\…`): **corrija antes do commit**.
