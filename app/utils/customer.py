from pathlib import Path
from app.db.database import SessionLocal
from app.db.models import Customer
from openpyxl import load_workbook
from typing import Tuple
import csv

REQUIRED_COLUMNS = {"name", "email", "amount"}


def validate_file_columns(path: Path) -> None:
    ext = path.suffix.lower()
    if ext == ".csv":
        header = get_csv_header(path)
    elif ext in (".xls", ".xlsx"):
        header = get_excel_header(path)
    else:
        raise ValueError("Unsupported file type")

    validate_header(header)


def get_csv_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or []


def get_excel_header(path: Path) -> list[str]:
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    return list(next(rows, []))


def validate_header(header: list[str] | tuple[str, ...]) -> None:
    if not header:
        raise ValueError("File has no header")

    normalized = {str(col).strip().lower() for col in header if col}
    missing = REQUIRED_COLUMNS - normalized

    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def stream_and_insert(path: Path, user_id: int) -> Tuple[int, int, int]:
    ext = path.suffix.lower()

    if ext == ".csv":
        return stream_csv(path, user_id)
    elif ext in (".xls", ".xlsx"):
        return stream_excel(path, user_id)
    else:
        raise ValueError("Unsupported file type")


def stream_csv(path: Path, user_id: int) -> Tuple[int, int, int]:
    total = failed = success = 0

    with SessionLocal() as db, path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1

            customer = Customer(
                name=row["name"],
                email=row["email"],
                amount=int(row["amount"]),
                user_id=user_id,
            )
            db.add(customer)

            try:
                db.commit()
                success += 1
            except Exception:
                db.rollback()
                failed += 1

    return total, failed, success


def stream_excel(path: Path, user_id: int) -> Tuple[int, int, int]:
    total = failed = success = 0

    wb = load_workbook(path, read_only=True)
    ws = wb.active

    rows = ws.iter_rows(values_only=True)
    header = [h.strip().lower() for h in next(rows)]

    with SessionLocal() as db:
        for row in rows:
            total += 1
            data = dict(zip(header, row))

            try:
                customer = Customer(
                    name=data["name"],
                    email=data["email"],
                    amount=int(data["amount"]),
                    user_id=user_id,
                )

                db.add(customer)
                db.commit()
                success += 1
            except Exception:
                db.rollback()
                failed += 1

    return total, failed, success
