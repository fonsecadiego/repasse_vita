from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DashboardFiltrosDTO:
    ano: int
    mes: int
    unidade: str = ""
    convenio: str = ""
    escala: str = ""
    leitura: str = ""
    tipo_proced: str = ""
    procedimento: str = ""

    @classmethod
    def from_querydict(cls, querydict, *, hoje: date | None = None) -> "DashboardFiltrosDTO":
        referencia = hoje or date.today()
        ano_raw = querydict.get("ano")
        mes_raw = querydict.get("mes")

        ano = int(ano_raw) if ano_raw else referencia.year
        mes = int(mes_raw) if mes_raw else referencia.month

        if not (1 <= mes <= 12):
            raise ValueError("Parâmetro 'mes' deve estar entre 1 e 12")

        return cls(
            ano=ano,
            mes=mes,
            unidade=(querydict.get("unidade") or "").strip(),
            convenio=(querydict.get("convenio") or "").strip(),
            escala=(querydict.get("escala") or "").strip(),
            leitura=(querydict.get("leitura") or "").strip(),
            tipo_proced=(querydict.get("tipo_proced") or "").strip(),
            procedimento=(querydict.get("procedimento") or "").strip(),
        )

    def to_apuracao_filtros(self) -> dict:
        return {
            "unidade": self.unidade,
            "convenio": self.convenio,
            "escala": self.escala,
            "leitura": self.leitura,
            "ds_tipo_proced": self.tipo_proced,
            "ds_proced": self.procedimento,
        }

    def to_query_params(self) -> dict:
        return {
            "ano": self.ano,
            "mes": self.mes,
            "unidade": self.unidade,
            "convenio": self.convenio,
            "escala": self.escala,
            "leitura": self.leitura,
            "tipo_proced": self.tipo_proced,
            "procedimento": self.procedimento,
        }
