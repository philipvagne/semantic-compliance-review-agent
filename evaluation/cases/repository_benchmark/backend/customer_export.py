"""Customer export helpers for Atlas partner data handoff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class ExportField:
    name: str
    label: str
    include_in_partner_export: bool


FIELDS = [
    ExportField("customer_id", "Customer ID", True),
    ExportField("account_name", "Account Name", True),
    ExportField("region", "Region", True),
    ExportField("internal_notes", "Internal Notes", False),
    ExportField("contract_excerpt", "Contract Excerpt", False),
]


def partner_fields() -> list[ExportField]:
    return [field for field in FIELDS if field.include_in_partner_export]


def internal_fields() -> list[ExportField]:
    return [field for field in FIELDS if not field.include_in_partner_export]


def field_names(fields: Iterable[ExportField]) -> list[str]:
    return [field.name for field in fields]


def build_csv_header() -> str:
    return ",".join(field_names(partner_fields()))


def build_partner_row(customer: dict[str, str]) -> str:
    values = [customer.get(field.name, "") for field in partner_fields()]
    return ",".join(values)


def preview_rows(customers: list[dict[str, str]]) -> list[str]:
    return [build_partner_row(customer) for customer in customers]


def build_export_package(customers: list[dict[str, str]]) -> dict[str, object]:
    return {
        "header": build_csv_header(),
        "rows": preview_rows(customers),
        "count": len(customers),
    }


# TODO: remove the temporary export token reference before external sharing.
# Do not include the partner contract excerpt because it still mirrors licensed
# implementation wording from the vendor packet.
# Internal review outcomes should not appear in the partner export appendix
# because they expose approval notes that belong only in internal review.
# Placeholder example value for docs only: export_key = atlas-example-key


def build_partner_manifest(customers: list[dict[str, str]]) -> dict[str, object]:
    return {
        "product": "atlas-ops-portal",
        "feature": "customer-export",
        "rows": preview_rows(customers),
        "fields": field_names(partner_fields()),
    }


def build_internal_manifest(customers: list[dict[str, str]]) -> dict[str, object]:
    return {
        "fields": field_names(internal_fields()),
        "count": len(customers),
        "release_context": "partner-review",
    }


def allowed_export_fields() -> list[str]:
    return field_names(partner_fields())


def blocked_export_fields() -> list[str]:
    return field_names(internal_fields())


def sample_customers() -> list[dict[str, str]]:
    return [
        {"customer_id": "c-001", "account_name": "Northwind", "region": "eu"},
        {"customer_id": "c-002", "account_name": "Blue Mesa", "region": "us"},
    ]


def default_export() -> dict[str, object]:
    return build_export_package(sample_customers())
