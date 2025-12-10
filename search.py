import argparse
import json
from pathlib import Path
from typing import List, Dict


def load_conditions(data_path: Path) -> List[Dict[str, str]]:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text: str) -> str:
    return text.lower().strip()


def matches(query: str, record: Dict[str, str]) -> bool:
    q = normalize(query)
    searchable_fields = [
        record.get("dsm5_name", ""),
        record.get("icd11_name", ""),
        record.get("dsm5_code", ""),
        record.get("icd11_code", ""),
    ]
    return any(q in normalize(value) for value in searchable_fields)


def search_conditions(conditions: List[Dict[str, str]], query: str) -> List[Dict[str, str]]:
    return [record for record in conditions if matches(query, record)]


def format_record(record: Dict[str, str]) -> str:
    return (
        f"DSM-5-TR: {record.get('dsm5_name', 'N/A')} (code: {record.get('dsm5_code', 'N/A')})\n"
        f"ICD-11 : {record.get('icd11_name', 'N/A')} (code: {record.get('icd11_code', 'N/A')})\n"
        f"Summary: {record.get('summary', 'N/A')}\n"
        f"Notes  : {record.get('notes', 'N/A')}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Search a small sample crosswalk between DSM-5-TR and ICD-11 using names or codes. "
            "Entries are concise summaries; consult official manuals for full diagnostic criteria."
        )
    )
    parser.add_argument("query", help="Condition name or diagnostic code (DSM or ICD)")
    parser.add_argument(
        "--data",
        default=Path("data/conditions.json"),
        type=Path,
        help="Path to the JSON data file (default: data/conditions.json)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    conditions = load_conditions(args.data)
    results = search_conditions(conditions, args.query)

    if not results:
        print("No matches found. Try another term or code.")
        return

    for record in results:
        print(format_record(record))


if __name__ == "__main__":
    main()
