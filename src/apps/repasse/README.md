# App `repasse`

## Onde fica o quê
- `views/`: camada HTTP (auth, validação de input, serialização de output).
- `services/`: regras de negócio e orquestração.
- `selectors/`: consultas puras (filtros, agregações, lookup de vigência).
- `models/`: estrutura persistida e invariantes simples.
- `integrations/`: reservado para adapters utilitários de integração.

## Extensão de critérios de regra
1. Adicione novos campos na identidade em `RegraRepasse`.
2. Atualize filtros em `selectors/regra_repasse_selector.py`.
3. Ajuste desempate/prioridade em `services/regra_repasse_service.py`.

## Exemplo de payload Mirth
```json
[
  {
    "UNIDADE": "HOSPITAL A",
    "LEITURA": "PRIMEIRA",
    "DT_LAUDO": "2026-01-10",
    "DT_EXAME": "2026-01-09",
    "NR_PRESCRICAO": 12345,
    "NM_MEDICO_CORRIGIDO": "Dr. Fulano",
    "CRM_MEDICO_EXEC": "123456",
    "NM_PACIENTE": "Paciente 1",
    "DS_PROCED": "RM - Cranio",
    "DS_TIPO_PROCED": "RM",
    "ESCALA": "FORA_PLANTAO",
    "CONVENIO": "UNIMED",
    "QUANTIDADE": 1,
    "VALOR_EXAME": 350.00
  },
  {
    "UNIDADE": "HOSPITAL B",
    "LEITURA": "SEGUNDA",
    "DT_LAUDO": "2026-01-11",
    "DT_EXAME": "2026-01-11",
    "NR_PRESCRICAO": 12346,
    "NM_MEDICO_CORRIGIDO": "Dra. Beltrana",
    "CRM_MEDICO_EXEC": "789012",
    "NM_PACIENTE": "Paciente 2",
    "DS_PROCED": "TC Torax",
    "DS_TIPO_PROCED": "Tomografia",
    "ESCALA": "PLANTAO",
    "CONVENIO": "Particular Extra",
    "QUANTIDADE": 1,
    "VALOR_EXAME": 500.00
  }
]
```

## Exemplos de regras
- a) Fixo Tomografia fora do plantão:
  - `tipo_proced="Tomografia"`, `escala_categoria="FORA_PLANTAO"`, vigência `FIXO` `valor_fixo=30.00`.
- b) Fixo Tomografia em plantão:
  - `tipo_proced="Tomografia"`, `escala_categoria="PLANTAO"`, vigência `FIXO` `valor_fixo=40.00`.
- c) Percentual Particular Extra:
  - `convenio="Particular Extra"`, vigência `PERCENTUAL` `percentual=0.10`.
- d) Fixo por procedimento específico:
  - `procedimento="RM - Cranio"`, vigência `FIXO` `valor_fixo=50.00`.

## Exemplo de reajuste com histórico preservado
- Vigência antiga: `2026-01-01` até `2026-02-29` (`valor_fixo=50.00`).
- Nova vigência: inicia em `2026-03-01` (`valor_fixo=60.00`).
- O service fecha automaticamente a vigência aberta em `2026-02-28` e cria a nova sem sobrescrever histórico.

## Como rodar
1. Incluir `apps.repasse` em `INSTALLED_APPS`.
2. Executar migrações:
   - `python manage.py migrate`
3. Rodar testes do app:
   - `python manage.py test apps.repasse.tests`
