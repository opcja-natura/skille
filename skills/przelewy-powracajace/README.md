# przelewy-powracajace

Agent Skill Opcja Natura: lista przelewów → wiersze do wklejenia w zakładce `payments_logs` arkusza „003_przelewy powracajace” + wątpliwości dla operatora + lista pominiętych.

- `SKILL.md` — reguły, słownik odbiorców (stan 10.2026), format wyniku,
- `agents/openai.yaml` — metadane interfejsu dla ChatGPT; inne implementacje Agent Skills mogą go zignorować.

Skill niczego nie zapisuje w arkuszu. Wymaga podłączonego Google Drive (odczyt `payments_list`, `payments_logs`, `payments_companies`) albo wklejenia tych zakładek.

**ChatGPT:** wgrać ZIP jako Skill. **Claude.ai:** wgrać ZIP jako custom Skill (albo paczkę `.skill`).

Master: repo `opcja-natura/skille`, `skills/przelewy-powracajace/`. Po zmianie: `scripts/pakuj.sh przelewy-powracajace` i wgrać ponownie.
