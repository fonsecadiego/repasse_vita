from django.db import transaction
from django.db.models import Model

from apps.repasse.selectors.catalog_selector import get_catalog_item_by_name_ci


@transaction.atomic
def upsert_catalog_value(model_class: type[Model], nome: str):
    nome_normalizado = (nome or "").strip()
    if not nome_normalizado:
        return None

    existente = get_catalog_item_by_name_ci(model_class, nome_normalizado)
    if existente:
        return existente

    return model_class.objects.create(nome=nome_normalizado)


@transaction.atomic
def create_catalog_item(model_class: type[Model], nome: str, ativo: bool = True):
    nome_normalizado = (nome or "").strip()
    if not nome_normalizado:
        raise ValueError("Nome é obrigatório")

    if get_catalog_item_by_name_ci(model_class, nome_normalizado):
        raise ValueError("Item já existe no catálogo")

    return model_class.objects.create(nome=nome_normalizado, ativo=ativo)


@transaction.atomic
def update_catalog_item(item, *, nome: str, ativo: bool):
    nome_normalizado = (nome or "").strip()
    if not nome_normalizado:
        raise ValueError("Nome é obrigatório")

    duplicate = item.__class__.objects.filter(nome__iexact=nome_normalizado).exclude(id=item.id).exists()
    if duplicate:
        raise ValueError("Já existe item com este nome")

    item.nome = nome_normalizado
    item.ativo = ativo
    item.save(update_fields=["nome", "ativo"])
    return item


@transaction.atomic
def toggle_catalog_item(item):
    item.ativo = not item.ativo
    item.save(update_fields=["ativo"])
    return item
