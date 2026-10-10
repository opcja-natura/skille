# Opcja Natura Creative Brand

Przenośny Agent Skill dla pracy kreatywnej Opcja Natura.

## Wersja źródła

Brandbook: **08.2026**.

Skill zawiera:

- `SKILL.md` - reguły aktywacji i workflow,
- `references/brand-guidelines-08-2026.md` - operacyjny ekstrakt zasad,
- `references/brandbook-agent.json` - dokładne tokeny i dane strukturalne,
- `assets/brandbook-agent.html` - pełny agent-friendly HTML z materiałem referencyjnym,
- `agents/openai.yaml` - metadane interfejsu dla ChatGPT; inne implementacje Agent Skills mogą ten plik zignorować.

## Kompatybilność

Paczka opiera się na otwartym formacie Agent Skills: katalog z `SKILL.md` i YAML frontmatter `name` + `description`, plus opcjonalne `references/` i `assets/`.

### ChatGPT

Wgrać ZIP jako Skill. `agents/openai.yaml` dostarcza nazwę wyświetlaną w interfejsie.

### Claude.ai

Wgrać ZIP jako custom Skill w ustawieniach funkcji Skills.

### Claude Code

Rozpakować katalog `opcja-natura-creative-brand` do jednego z miejsc:

- projektowo: `.claude/skills/opcja-natura-creative-brand/`
- użytkownik: `~/.claude/skills/opcja-natura-creative-brand/`

W obu przypadkach `SKILL.md` musi pozostać bezpośrednio w katalogu skilla.

## Aktualizacja brandbooka

Po pojawieniu się nowszego brandbooka nie nadpisywać po cichu snapshotu 08.2026. Zaktualizować pliki referencyjne, datę w `SKILL.md` i ponownie spakować cały skill.
