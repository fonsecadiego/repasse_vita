import hashlib
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from django.db import transaction

from apps.repasse.models import Medico, ProducaoLaudo


REQUIRED_FIELDS = {
    "UNIDADE",
    "LEITURA",
    "DT_LAUDO",
    "DT_EXAME",
    "NR_PRESCRICAO",
    "NM_MEDICO_CORRIGIDO",
    "CRM_MEDICO_EXEC",
    "NM_PACIENTE",
    "DS_PROCED",
    "DS_TIPO_PROCED",
    "ESCALA",
    "CONVENIO",
    "QUANTIDADE",
    "VALOR_EXAME",
}


@dataclass
class IngestaoResultado:
    recebidos: int
    inseridos: int
    ignorados_por_duplicidade: int
    atualizados: int



def _normalize_str(value: str | None) -> str:
    return (value or "").strip()


def _normalize_row(row: dict) -> dict:
    missing = REQUIRED_FIELDS.difference(row.keys())
    if missing:
        raise ValueError(f"Campos obrigatórios ausentes: {sorted(missing)}")

    return {
        "unidade": _normalize_str(row["UNIDADE"]),
        "leitura": _normalize_str(row["LEITURA"]).upper(),
        "dt_laudo": row["DT_LAUDO"],
        "dt_exame": row["DT_EXAME"],
        "nr_prescricao": int(row["NR_PRESCRICAO"]),
        "nome_medico": _normalize_str(row["NM_MEDICO_CORRIGIDO"]),
        "crm_medico": _normalize_str(row["CRM_MEDICO_EXEC"]),
        "nome_paciente": _normalize_str(row["NM_PACIENTE"]),
        "ds_proced": _normalize_str(row["DS_PROCED"]),
        "ds_tipo_proced": _normalize_str(row["DS_TIPO_PROCED"]),
        "escala": _normalize_str(row["ESCALA"]).upper(),
        "convenio": _normalize_str(row["CONVENIO"]),
        "quantidade": Decimal(str(row["QUANTIDADE"])),
        "valor_exame": Decimal(str(row["VALOR_EXAME"])),
    }


def _hash_idempotencia(row: dict) -> str:
    identity_fields = [
        str(row["nr_prescricao"]),
        row["crm_medico"],
        row["leitura"],
        str(row["dt_laudo"]),
        row["ds_proced"],
        row["unidade"],
    ]
    raw = "|".join(identity_fields)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@transaction.atomic
def ingest_from_mirth(payload: list[dict]) -> IngestaoResultado:
    normalized = [_normalize_row(item) for item in payload]

    crms = sorted({item["crm_medico"] for item in normalized if item["crm_medico"]})
    medicos_by_crm = {m.crm: m for m in Medico.objects.filter(crm__in=crms)}
    novos_medicos = []
    for item in normalized:
        crm = item["crm_medico"]
        if crm and crm not in medicos_by_crm:
            medico = Medico(nome=item["nome_medico"] or crm, crm=crm)
            novos_medicos.append(medico)
            medicos_by_crm[crm] = medico

    if novos_medicos:
        Medico.objects.bulk_create(novos_medicos, ignore_conflicts=True)
        medicos_by_crm = {m.crm: m for m in Medico.objects.filter(crm__in=crms)}

    hashes = []
    for item in normalized:
        item["hash_idempotencia"] = _hash_idempotencia(item)
        hashes.append(item["hash_idempotencia"])

    existing_by_hash = {p.hash_idempotencia: p for p in ProducaoLaudo.objects.filter(hash_idempotencia__in=hashes)}

    to_create = []
    to_update = []
    for item in normalized:
        medico = medicos_by_crm[item["crm_medico"]]
        existing = existing_by_hash.get(item["hash_idempotencia"])
        if existing:
            changed = False
            for field in [
                "unidade",
                "leitura",
                "dt_laudo",
                "dt_exame",
                "nr_prescricao",
                "nome_paciente",
                "ds_proced",
                "ds_tipo_proced",
                "escala",
                "convenio",
                "quantidade",
                "valor_exame",
            ]:
                new_value = item[field]
                if getattr(existing, field) != new_value:
                    setattr(existing, field, new_value)
                    changed = True
            if existing.medico_id != medico.id:
                existing.medico = medico
                changed = True
            if changed:
                to_update.append(existing)
            continue

        to_create.append(
            ProducaoLaudo(
                unidade=item["unidade"],
                leitura=item["leitura"],
                dt_laudo=item["dt_laudo"],
                dt_exame=item["dt_exame"],
                nr_prescricao=item["nr_prescricao"],
                nome_paciente=item["nome_paciente"],
                ds_proced=item["ds_proced"],
                ds_tipo_proced=item["ds_tipo_proced"],
                escala=item["escala"],
                convenio=item["convenio"],
                quantidade=item["quantidade"],
                valor_exame=item["valor_exame"],
                medico=medico,
                hash_idempotencia=item["hash_idempotencia"],
            )
        )

    if to_create:
        ProducaoLaudo.objects.bulk_create(to_create, ignore_conflicts=True)

    if to_update:
        ProducaoLaudo.objects.bulk_update(
            to_update,
            fields=[
                "unidade",
                "leitura",
                "dt_laudo",
                "dt_exame",
                "nr_prescricao",
                "nome_paciente",
                "ds_proced",
                "ds_tipo_proced",
                "escala",
                "convenio",
                "quantidade",
                "valor_exame",
                "medico",
            ],
        )

    return IngestaoResultado(
        recebidos=len(payload),
        inseridos=len(to_create),
        ignorados_por_duplicidade=max(len(payload) - len(to_create) - len(to_update), 0),
        atualizados=len(to_update),
    )
