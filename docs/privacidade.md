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

- HTML/CSS em `docs/` (descrição genérica das ferramentas)
- README e docs com links Pages em `andressalf.github.io`
- `.gitignore`

---

<a id="nunca-versionar"></a>

## ⛔ Nunca versionar

| Item | Motivo |
|------|--------|
| `cursor_*.md` / transcripts | E-mail, paths, handles, histórico de setup |
| `scripts/` | Manutenção local |
| `.env`, `*.local.toml` | Segredos / overrides |
| Nomes de campanha, cliente, rota, embarcação | Identificação de projeto interno |
| `C:\Users\…`, `Y:\…` | Paths pessoais |
| E-mails, PATs, chaves SSH | Credenciais |

---

<a id="urls-e-handles"></a>

## 🔗 URLs e handles

Nos docs versionados use o handle público `andressalf`:

```text
https://andressalf.github.io/ggemma_projects/
https://andressalf.github.io/extrator_info_files/
https://andressalf.github.io/SurveyAnchor/
https://andressalf.github.io/batimetria_kml_shape/
```

Ainda **não** versionar e-mails, paths locais (`C:\Users\…`, `Y:\…`) nem nomes de campanha.

---

<a id="antes-do-push"></a>

## 🧹 Antes do push

```powershell
# Na pasta ggemma_projects
Select-String -Path docs\*.html,docs\assets\*.svg,README.md -Pattern "@gmail|C:\\Users|Y:\\" -CaseSensitive:$false
git status
git check-ignore -v cursor_ggemma_project_showcase.md
```

Se o `Select-String` achar e-mail ou path local: **corrija antes do commit**.
