# Padronização de Header/Footer - Vinculou

Este pacote contém:
- `original/` - cópia exata do repositório enviado (backup).
- `padronizado/` - versão com header/footer padronizados e `core/models_suggested.py` adicionado.
- `README_PR.md` - instruções para criar branch, aplicar mudanças e abrir PR no GitHub.
- `patch.diff` - diff que pode ser aplicado com `git apply`.


- Adicionado `core/models_suggested.py` com entidades Django sugeridas (User, Profile, Course, Professor, Subject, Evaluation, Community, Post, Message, Notification).
- Criado `core/templates/base.html` com header/footer padronizados (estilo "Vinculou").
- Atualizados templates HTML para extender `base.html` (remove duplicação de header/footer).



```bash

git checkout -b padronizacao/header-footer

git apply patch.diff
git add -A
git commit -m "Padroniza header/footer e adiciona core/models_suggested.py"
git push origin padronizacao/header-footer

```

s
- `core/models_suggested.py` é uma sugestão — se já existe `core/models.py`, revise conflitos antes de substituir.
- Teste localmente antes de mesclar a branch no `main`.
