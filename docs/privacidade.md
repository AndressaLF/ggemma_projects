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
- README com placeholders `<OWNER>`
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
| Handle GitHub pessoal em links `*.github.io/...` | Identifica a conta |

---

<a id="urls-e-handles"></a>

## 🔗 URLs e handles

Nos docs versionados use:

```text
https://<OWNER>.github.io/ggemma_projects/
https://<OWNER>.github.io/extrator_info_files/
https://<OWNER>.github.io/SurveyAnchor/
https://<OWNER>.github.io/batimetria_kml_shape/
```

A URL real fica só em **Settings → Pages** / **About → Website** na interface do GitHub — não precisa estar hardcoded nos arquivos do site.

---

<a id="antes-do-push"></a>

## 🧹 Antes do push

```powershell
# Na pasta ggemma_projects
Select-String -Path docs\*.html,docs\assets\*.svg,README.md -Pattern "github\.io/[a-z0-9]+/|@gmail|C:\\Users|Y:\\|andressa" -CaseSensitive:$false
git status
git check-ignore -v cursor_ggemma_project_showcase.md
```

Se o `Select-String` achar handle pessoal ou path local: **corrija antes do commit**.
