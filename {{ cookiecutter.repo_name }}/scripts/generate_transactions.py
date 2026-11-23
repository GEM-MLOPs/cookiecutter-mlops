"""Generador incremental de compras sintéticas para el laboratorio MLOps.

Solo datos OBSERVABLES en raw/: customers.csv y transacciones particionadas.
Los parámetros LATENTES del simulador viven en simulation/customer_profiles.csv
(no deben utilizarse como features del modelo).

Desde la raíz del repositorio:
    uv run python scripts/generate_transactions.py --init --months 12 --customers 1000
    uv run python scripts/generate_transactions.py --advance
    uv run python scripts/generate_transactions.py --advance --scenario seasonal
    uv run python scripts/generate_transactions.py --advance --scenario drift

Por defecto escribe en data/synthetic/. Requiere Python 3.10+; sin librerías externas.
"""

import argparse
import csv
import hashlib
import json
import math
import os
import random
from datetime import date, timedelta
from pathlib import Path

ROOT_DEFAULT = Path("data/synthetic")
CUSTOMER_FIELDS = ["customer_id", "created_at", "birth_date"]
PROFILE_FIELDS = [
    "customer_id", "segment", "preferred_category", "avg_ticket",
    "base_purchase_rate", "activity_factor", "preferred_sales_channel",
    "preferred_payment_method", "discount_sensitivity",
]
TRANSACTION_FIELDS = [
    "transaction_id", "customer_id", "transaction_date", "category", "amount",
    "currency", "payment_method", "sales_channel", "discount_amount", "items_count",
]
SEGMENTS = {"frequent": (2.5, 120.0), "occasional": (0.7, 230.0), "at_risk": (0.25, 170.0)}
CATEGORIES = ("grocery", "home", "electronics", "fashion")
CHANNELS = ("app", "web", "store")
PAYMENTS = ("credit_card", "debit_card", "digital_wallet", "cash")
CHANNEL_PAYMENT_WEIGHTS = {
    "app": (0.20, 0.26, 0.52, 0.02),
    "web": (0.50, 0.34, 0.15, 0.01),
    "store": (0.20, 0.28, 0.16, 0.36),
}


def add_month(value: date, months: int = 1) -> date:
    index = value.year * 12 + value.month - 1 + months
    return date(index // 12, index % 12 + 1, 1)


def stable_rng(seed: int, key: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}:{key}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def poisson(lam: float, rng: random.Random) -> int:
    # Knuth: eficiente para las tasas pequeñas de este laboratorio.
    cutoff, product, count = math.exp(-lam), 1.0, 0
    while product > cutoff:
        count += 1
        product *= rng.random()
    return count - 1


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_csv(path: Path, fields: list[str]) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != fields:
            raise ValueError(f"Esquema incompatible en {path}. Se esperaba {fields}")
        return list(reader)


def save_json(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temporary, path)


def transaction_path(root: Path, month: date) -> Path:
    return root / "raw" / "transactions" / f"year={month.year}" / f"month={month.month:02d}" / "transactions.csv"


def sample_birth_date(created_at: date, rng: random.Random) -> date:
    # Una fecha realista; edad entre 18 y 75 años a la fecha de alta.
    age = rng.randint(18, 75)
    year = created_at.year - age
    # Rechazo sencillo del 29/02 para evitar fechas imposibles.
    while True:
        month = rng.randint(1, 12)
        day = rng.randint(1, 28)  # válido en cualquier año y mes
        born = date(year, month, day)
        actual_age = created_at.year - born.year - ((created_at.month, created_at.day) < (born.month, born.day))
        if 18 <= actual_age <= 75:
            return born


def make_customer(customer_number: int, created_at: date, rng: random.Random, seed: int) -> tuple[dict, dict]:
    customer_id = f"C{customer_number:06d}"
    segment = rng.choices(list(SEGMENTS), weights=[0.3, 0.5, 0.2])[0]
    rate, ticket = SEGMENTS[segment]
    pref_rng = stable_rng(seed, f"preferences:{customer_id}")
    channel = pref_rng.choices(CHANNELS, weights=[0.38, 0.32, 0.30])[0]
    payment = pref_rng.choices(PAYMENTS, weights=CHANNEL_PAYMENT_WEIGHTS[channel])[0]
    customer = {
        "customer_id": customer_id,
        "created_at": created_at.isoformat(),
        "birth_date": sample_birth_date(created_at, rng).isoformat(),
    }
    profile = {
        "customer_id": customer_id,
        "segment": segment,
        "preferred_category": rng.choice(CATEGORIES),
        "avg_ticket": round(ticket * rng.uniform(0.7, 1.3), 2),
        "base_purchase_rate": round(rate * rng.uniform(0.8, 1.2), 3),
        "activity_factor": 1.0,
        "preferred_sales_channel": channel,
        "preferred_payment_method": payment,
        "discount_sensitivity": round(pref_rng.betavariate(2, 3), 3),
    }
    return customer, profile


def make_transaction(profile: dict, period: date, ordinal: int, scenario: str, rng: random.Random) -> dict:
    channel = (profile["preferred_sales_channel"] if rng.random() < 0.75
               else rng.choice(CHANNELS))
    payment = (profile["preferred_payment_method"] if rng.random() < 0.60
               else rng.choices(PAYMENTS, weights=CHANNEL_PAYMENT_WEIGHTS[channel])[0])
    items = rng.choices([1, 2, 3, 4, 5], weights=[42, 29, 16, 9, 4])[0]
    ticket = float(profile["avg_ticket"]) * (1.2 if scenario == "drift" else 1.0)
    gross = max(1.0, rng.lognormvariate(math.log(ticket) - 0.5 * 0.35**2, 0.35))
    gross = round(gross * (1 + 0.22 * (items - 1)), 2)
    discount_chance = min(0.85, 0.08 + 0.42 * float(profile["discount_sensitivity"])
                          + (0.20 if scenario == "seasonal" else 0.0))
    discount_rate = rng.uniform(0.05, 0.25) if rng.random() < discount_chance else 0.0
    discount = round(gross * discount_rate, 2)
    days = (add_month(period) - period).days
    purchase_date = period + timedelta(days=rng.randrange(days))
    category = (profile["preferred_category"] if rng.random() < 0.75
                else rng.choice(CATEGORIES))
    return {
        "transaction_id": f"T{period:%Y%m}-{profile['customer_id']}-{ordinal:03d}",
        "customer_id": profile["customer_id"],
        "transaction_date": purchase_date.isoformat(),
        "category": category,
        "amount": round(gross - discount, 2),
        "currency": "PEN",
        "payment_method": payment,
        "sales_channel": channel,
        "discount_amount": discount,
        "items_count": items,
    }


def generate_month(customers: list[dict], profiles: list[dict], state: dict,
                   period: date, scenario: str) -> tuple[list[dict], list[dict], list[dict]]:
    rng = stable_rng(state["seed"], period.strftime("period:%Y-%m"))
    # Incorporar ~1% de clientes nuevos (al inicio del periodo).
    new_count = max(1, round(len(customers) * 0.01))
    for _ in range(new_count):
        state["next_customer_num"] += 1
        customer, profile = make_customer(state["next_customer_num"], period, rng, state["seed"])
        customers.append(customer)
        profiles.append(profile)

    rows = []
    for profile in profiles:
        # Estado persistente: puede desactivarse o reactivarse en meses sucesivos.
        if rng.random() < 0.025:
            profile["activity_factor"] = (0.15 if float(profile["activity_factor"]) > 0.5 else 1.0)
        lam = (float(profile["base_purchase_rate"]) * float(profile["activity_factor"])
               * (1.5 if scenario == "seasonal" else 1.0)
               * (0.45 if scenario == "drift" else 1.0))
        for ordinal in range(1, poisson(lam, rng) + 1):
            rows.append(make_transaction(profile, period, ordinal, scenario, rng))

    rows.sort(key=lambda row: (row["transaction_date"], row["transaction_id"]))
    return customers, profiles, rows


def run_period(root: Path, state: dict, customers: list[dict], profiles: list[dict],
               period: date, scenario: str) -> tuple[list[dict], list[dict]]:
    output = transaction_path(root, period)
    if output.exists():
        raise FileExistsError(f"Periodo ya generado: {output}")
    customers, profiles, rows = generate_month(customers, profiles, state, period, scenario)
    write_csv(output, rows, TRANSACTION_FIELDS)
    write_csv(root / "raw" / "customers.csv", customers, CUSTOMER_FIELDS)
    write_csv(root / "simulation" / "customer_profiles.csv", profiles, PROFILE_FIELDS)
    state.update({
        "last_generated_month": period.strftime("%Y-%m"),
        "total_customers": len(customers),
        "total_transactions": state["total_transactions"] + len(rows),
    })
    save_json(root / "simulation" / "state.json", state)
    print(f"{period:%Y-%m} | escenario={scenario} | +{len(rows)} transacciones | "
          f"{len(customers)} clientes | total={state['total_transactions']}")
    return customers, profiles


def main() -> None:
    parser = argparse.ArgumentParser(description="Generación sintética incremental para MLOps")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--init", action="store_true", help="Crear historial inicial")
    mode.add_argument("--advance", action="store_true", help="Generar el siguiente mes")
    parser.add_argument("--root", type=Path, default=ROOT_DEFAULT)
    parser.add_argument("--start", default="2025-01", help="Periodo inicial YYYY-MM")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--customers", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--scenario", choices=["normal", "seasonal", "drift"], default="normal")
    args = parser.parse_args()
    root = args.root
    state_file = root / "simulation" / "state.json"
    customer_file = root / "raw" / "customers.csv"
    profile_file = root / "simulation" / "customer_profiles.csv"

    if args.init:
        if any(path.exists() for path in (state_file, customer_file, profile_file,
                                            root / "raw" / "transactions")):
            parser.error("Ya hay una simulación en --root. No se sobrescriben datos. "
                         "Use --advance o seleccione una ruta vacía con --root.")
        if args.months < 1 or args.customers < 1:
            parser.error("--months y --customers deben ser positivos")
        try:
            first = date.fromisoformat(args.start + "-01")
            if first.strftime("%Y-%m") != args.start:
                raise ValueError("Formato inválido")
        except ValueError:
            parser.error("--start debe tener formato YYYY-MM válido")

        rng = random.Random(args.seed)
        customers, profiles = [], []
        for number in range(1, args.customers + 1):
            customer, profile = make_customer(number, first, rng, args.seed)
            customers.append(customer)
            profiles.append(profile)
        state = {"schema_version": 2, "seed": args.seed, "last_generated_month": None,
                 "next_customer_num": args.customers, "total_customers": args.customers,
                 "total_transactions": 0}
        for i in range(args.months):
            customers, profiles = run_period(root, state, customers, profiles,
                                             add_month(first, i), args.scenario)
    else:
        if not (state_file.exists() and customer_file.exists() and profile_file.exists()):
            parser.error("No existe una simulación compatible. Ejecute --init en un --root vacío.")
        state = json.loads(state_file.read_text(encoding="utf-8"))
        if state.get("schema_version") != 2:
            parser.error("El esquema previo no es compatible; inicialice en un --root vacío.")
        customers = read_csv(customer_file, CUSTOMER_FIELDS)
        profiles = read_csv(profile_file, PROFILE_FIELDS)
        if len(customers) != len(profiles) or {c["customer_id"] for c in customers} != {p["customer_id"] for p in profiles}:
            parser.error("Inconsistencia entre clientes observables y perfiles del simulador")
        last = date.fromisoformat(state["last_generated_month"] + "-01")
        run_period(root, state, customers, profiles, add_month(last), args.scenario)


if __name__ == "__main__":
    main()
