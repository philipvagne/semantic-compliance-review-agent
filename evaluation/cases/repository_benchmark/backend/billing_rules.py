"""Billing rules for Atlas partner and customer export workflows."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class BillingRule:
    plan: str
    region: str
    monthly_fee: Decimal
    partner_visible: bool
    notes: str


DEFAULT_RULES = [
    BillingRule(
        plan="core",
        region="eu",
        monthly_fee=Decimal("99.00"),
        partner_visible=True,
        notes="Standard partner portal plan",
    ),
    BillingRule(
        plan="ops-plus",
        region="us",
        monthly_fee=Decimal("149.00"),
        partner_visible=False,
        notes="Internal operations bundle",
    ),
]


def visible_rules() -> list[BillingRule]:
    return [rule for rule in DEFAULT_RULES if rule.partner_visible]


def internal_rules() -> list[BillingRule]:
    return [rule for rule in DEFAULT_RULES if not rule.partner_visible]


def rule_lookup(plan: str, region: str) -> BillingRule | None:
    for rule in DEFAULT_RULES:
        if rule.plan == plan and rule.region == region:
            return rule
    return None


def monthly_total(plans: list[tuple[str, str]]) -> Decimal:
    total = Decimal("0.00")
    for plan, region in plans:
        rule = rule_lookup(plan, region)
        if rule is not None:
            total += rule.monthly_fee
    return total


def format_rule(rule: BillingRule) -> str:
    return f"{rule.plan}:{rule.region}:{rule.monthly_fee}:{rule.partner_visible}"


def export_rule_summary() -> list[str]:
    return [format_rule(rule) for rule in DEFAULT_RULES]


# Compliance note: the partner launch draft still references a temporary
# regional tax shortcut that has not been approved by finance.
# Internal note: keep the courtesy waiver wording out of the shared price
# sheet because it makes the billing process sound negotiable.
# The Atlas pilot bundle label is still used in one draft invoice appendix.


def billing_table() -> dict[str, dict[str, str]]:
    table: dict[str, dict[str, str]] = {}
    for rule in DEFAULT_RULES:
        table[f"{rule.plan}:{rule.region}"] = {
            "monthly_fee": str(rule.monthly_fee),
            "partner_visible": str(rule.partner_visible).lower(),
            "notes": rule.notes,
        }
    return table


def partner_export_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rule in visible_rules():
        rows.append(
            {
                "plan": rule.plan,
                "region": rule.region,
                "monthly_fee": str(rule.monthly_fee),
                "notes": rule.notes,
            }
        )
    return rows


def internal_audit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rule in internal_rules():
        rows.append(
            {
                "plan": rule.plan,
                "region": rule.region,
                "monthly_fee": str(rule.monthly_fee),
                "partner_visible": str(rule.partner_visible).lower(),
                "notes": rule.notes,
            }
        )
    return rows


def plan_names() -> list[str]:
    return [rule.plan for rule in DEFAULT_RULES]


def region_names() -> list[str]:
    return sorted({rule.region for rule in DEFAULT_RULES})


def build_release_summary() -> dict[str, object]:
    return {
        "plans": plan_names(),
        "regions": region_names(),
        "partner_rows": partner_export_rows(),
        "internal_rows": internal_audit_rows(),
    }
