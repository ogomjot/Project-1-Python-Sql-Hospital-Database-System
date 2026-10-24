"""Hospital Management System: a small CLI app backed by MySQL.

Configuration is read from environment variables (see .env.example):
    DB_HOST (default: localhost)   DB_USER (default: root)
    DB_PASSWORD (required)         DB_NAME (default: hospital)
"""

import os
import re
import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Callable, NamedTuple, Optional

import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError

PAYMENT_STATUSES = ("Paid", "Pending", "Partial")


# ---------------------------------------------------------------- parsers --
# Each parser takes the raw string and returns a clean value, or raises
# ValueError with a message that is shown to the user.

def text(max_len: int) -> Callable[[str], str]:
    def parse(raw: str) -> str:
        if not raw:
            raise ValueError("This field cannot be empty.")
        if len(raw) > max_len:
            raise ValueError(f"Maximum {max_len} characters.")
        return raw
    return parse


def integer(low: int, high: int) -> Callable[[str], int]:
    def parse(raw: str) -> int:
        try:
            value = int(raw)
        except ValueError:
            raise ValueError("Enter a whole number.") from None
        if not low <= value <= high:
            raise ValueError(f"Enter a number between {low} and {high}.")
        return value
    return parse


def phone(raw: str) -> int:
    digits = re.sub(r"[\s\-+]", "", raw)
    if not digits.isdigit() or not 10 <= len(digits) <= 15:
        raise ValueError("Enter a valid phone number (10-15 digits).")
    return int(digits)


def iso_date(raw: str) -> date:
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Use the format YYYY-MM-DD (e.g. 2024-03-15).") from None


def money(raw: str) -> Decimal:
    try:
        value = Decimal(raw).quantize(Decimal("0.01"))
    except InvalidOperation:
        raise ValueError("Enter an amount like 2500 or 2500.50.") from None
    if value < 0 or value > Decimal("99999999.99"):
        raise ValueError("Amount is out of range.")
    return value


def payment_status(raw: str) -> str:
    for option in PAYMENT_STATUSES:
        if raw.lower() == option.lower():
            return option
    raise ValueError(f"Choose one of: {', '.join(PAYMENT_STATUSES)}.")


# ----------------------------------------------------------------- fields --
class Field(NamedTuple):
    label: str
    parser: Callable[[str], object]
    optional: bool = False


# Single source of truth: drives both "add" and "update".
FIELDS = {
    "patient_name": Field("Patient name", text(40)),
    "age": Field("Age", integer(0, 130)),
    "contact_number": Field("Contact number", phone),
    "diagnosis": Field("Diagnosis", text(50)),
    "doctor_treating": Field("Doctor's name", text(50)),
    "department": Field("Department", text(50)),
    "date_of_admission": Field("Admission date (YYYY-MM-DD)", iso_date),
    "date_of_discharging": Field(
        "Discharge date (YYYY-MM-DD, blank if still admitted)", iso_date, optional=True
    ),
    "fees": Field("Fees", money),
    "payment_status": Field(f"Payment status ({'/'.join(PAYMENT_STATUSES)})", payment_status),
}

SUMMARY_COLUMNS = (
    "patient_id", "patient_name", "age", "doctor_treating",
    "department", "date_of_admission", "date_of_discharging", "fees", "payment_status",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS hospital (
    patient_id          INT           PRIMARY KEY,
    patient_name        VARCHAR(40)   NOT NULL,
    age                 INT           NOT NULL,
    contact_number      BIGINT        NOT NULL,
    diagnosis           VARCHAR(50)   NOT NULL,
    doctor_treating     VARCHAR(50)   NOT NULL,
    department          VARCHAR(50)   NOT NULL,
    date_of_admission   DATE          NOT NULL,
    date_of_discharging DATE          NULL,
    fees                DECIMAL(10,2) NOT NULL,
    payment_status      VARCHAR(20)   NOT NULL
)
"""


# --------------------------------------------------------------- UI helpers --
def ask(label: str, parser: Callable[[str], object], optional: bool = False):
    """Prompt until the input passes the parser. Blank returns None if optional."""
    while True:
        raw = input(f"{label}: ").strip()
        if optional and not raw:
            return None
        try:
            return parser(raw)
        except ValueError as err:
            print(f"  x {err}")


def confirm(question: str) -> bool:
    return input(f"{question} (y/n): ").strip().lower() == "y"


def print_table(rows: list, columns: tuple = SUMMARY_COLUMNS) -> None:
    if not rows:
        print("No records found.")
        return
    cells = [[("-" if r[c] is None else str(r[c])) for c in columns] for r in rows]
    widths = [max(len(c), *(len(row[i]) for row in cells)) for i, c in enumerate(columns)]
    header = " | ".join(c.replace("_", " ").title().ljust(w) for c, w in zip(columns, widths))
    print(header)
    print("-+-".join("-" * w for w in widths))
    for row in cells:
        print(" | ".join(v.ljust(w) for v, w in zip(row, widths)))
    print(f"\n{len(rows)} record(s).")


def print_patient(row: dict) -> None:
    print(f"\nPatient #{row['patient_id']}")
    for column, field in FIELDS.items():
        value = row[column]
        print(f"  {field.label.split(' (')[0]:<16}: {'-' if value is None else value}")


def check_dates(admitted: date, discharged: Optional[date]) -> None:
    if discharged is not None and discharged < admitted:
        raise ValueError("Discharge date cannot be before the admission date.")


# --------------------------------------------------------------- database --
def get_connection():
    password = os.getenv("DB_PASSWORD")
    if password is None:
        sys.exit("DB_PASSWORD is not set. Copy .env.example and export the variables first.")
    db_name = os.getenv("DB_NAME", "hospital")
    if not db_name.isidentifier():
        sys.exit("DB_NAME may only contain letters, digits and underscores.")
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=password,
            cursorclass=DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            cur.execute(f"USE `{db_name}`")
            cur.execute(SCHEMA)
        conn.commit()
        return conn
    except MySQLError as err:
        sys.exit(f"Could not connect to MySQL: {err}")


def fetch_patient(conn, patient_id: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hospital WHERE patient_id = %s", (patient_id,))
        return cur.fetchone()


# --------------------------------------------------------------- actions --
def add_patient(conn) -> None:
    patient_id = ask("Patient ID", integer(1, 2_147_483_647))
    if fetch_patient(conn, patient_id):
        print(f"A patient with ID {patient_id} already exists.")
        return

    record = {col: ask(f.label, f.parser, f.optional) for col, f in FIELDS.items()}
    while True:
        try:
            check_dates(record["date_of_admission"], record["date_of_discharging"])
            break
        except ValueError as err:
            print(f"  x {err}")
            record["date_of_discharging"] = ask(
                FIELDS["date_of_discharging"].label, iso_date, optional=True
            )

    columns = ", ".join(["patient_id", *record])
    placeholders = ", ".join(["%s"] * (len(record) + 1))
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO hospital ({columns}) VALUES ({placeholders})",
            (patient_id, *record.values()),
        )
    conn.commit()
    print("Patient added.")


def view_patients(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hospital ORDER BY patient_id")
        print_table(cur.fetchall())


def search_patients(conn) -> None:
    query = input("Enter a patient ID or part of a name: ").strip()
    if not query:
        return
    with conn.cursor() as cur:
        if query.isdigit():
            cur.execute("SELECT * FROM hospital WHERE patient_id = %s", (int(query),))
        else:
            cur.execute(
                "SELECT * FROM hospital WHERE patient_name LIKE %s ORDER BY patient_name",
                (f"%{query}%",),
            )
        rows = cur.fetchall()
    if len(rows) == 1:
        print_patient(rows[0])
    else:
        print_table(rows)


def update_patient(conn) -> None:
    patient_id = ask("Patient ID", integer(1, 2_147_483_647))
    row = fetch_patient(conn, patient_id)
    if row is None:
        print("Patient not found.")
        return

    columns = list(FIELDS)
    print("\nWhich field do you want to update?")
    for number, column in enumerate(columns, start=1):
        print(f"  {number:>2}. {FIELDS[column].label.split(' (')[0]}")
    column = columns[ask("Choice", integer(1, len(columns))) - 1]
    field = FIELDS[column]

    while True:
        value = ask(f"New value for {field.label}", field.parser, field.optional)
        merged = {**row, column: value}
        try:
            check_dates(merged["date_of_admission"], merged["date_of_discharging"])
            break
        except ValueError as err:
            print(f"  x {err}")

    # `column` comes from the FIELDS whitelist, never from raw user input.
    with conn.cursor() as cur:
        cur.execute(f"UPDATE hospital SET {column} = %s WHERE patient_id = %s", (value, patient_id))
    conn.commit()
    print("Record updated.")


def delete_patient(conn) -> None:
    patient_id = ask("Patient ID to delete", integer(1, 2_147_483_647))
    row = fetch_patient(conn, patient_id)
    if row is None:
        print("Patient not found.")
        return
    print_patient(row)
    if not confirm("Delete this record permanently?"):
        print("Cancelled.")
        return
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hospital WHERE patient_id = %s", (patient_id,))
    conn.commit()
    print("Record deleted.")


# ------------------------------------------------------------------- main --
MENU = {
    "1": ("Add patient", add_patient),
    "2": ("View all patients", view_patients),
    "3": ("Search patient", search_patients),
    "4": ("Update patient", update_patient),
    "5": ("Delete patient", delete_patient),
    "6": ("Exit", None),
}


def main() -> None:
    conn = get_connection()
    try:
        while True:
            print("\n=== Hospital Management System ===")
            for key, (label, _) in MENU.items():
                print(f"  {key}. {label}")
            choice = input("Choose an option: ").strip()
            if choice not in MENU:
                print("Please pick a number from the menu.")
                continue
            action = MENU[choice][1]
            if action is None:
                print("Thank you for visiting.")
                break
            try:
                action(conn)
            except MySQLError as err:
                conn.rollback()
                print(f"Database error: {err}")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
