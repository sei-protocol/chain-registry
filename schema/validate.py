import json
import sys
from pathlib import Path

from jsonschema import validate, ValidationError

REGISTRY_RAW_URL = (
    "https://raw.githubusercontent.com/"
    "sei-protocol/chain-registry/main/"
)


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def load_schema(schema_path):
    return load_json(schema_path)


def validate_file(schema_path, file_path):
    schema = load_schema(schema_path)
    data = load_json(file_path)

    try:
        validate(instance=data, schema=schema)
        print(f"{file_path} has valid schema.")
    except ValidationError as e:
        print(f"{file_path} has invalid schema: {e}")
        sys.exit(1)


def validate_wallet_references(chain_info_path, wallets_path):
    chain_info = load_json(chain_info_path)
    wallets = load_json(wallets_path)
    wallets_by_identifier = {
        wallet["identifier"]: wallet for wallet in wallets["extensions"]
    }
    missing_wallets = sorted(
        set(chain_info["supported_wallets"]) - wallets_by_identifier.keys()
    )

    if missing_wallets:
        print(
            f"{chain_info_path} references unknown wallets: "
            f"{', '.join(missing_wallets)}"
        )
        sys.exit(1)

    non_native_wallets = sorted(
        identifier
        for identifier in chain_info["supported_wallets"]
        if "native" not in wallets_by_identifier[identifier]["capabilities"]
    )

    if non_native_wallets:
        print(
            f"{chain_info_path} references wallets without native support: "
            f"{', '.join(non_native_wallets)}"
        )
        sys.exit(1)

    registry_root = Path(wallets_path).resolve().parent
    missing_icons = sorted(
        wallet["identifier"]
        for wallet in wallets["extensions"]
        if wallet["icon"].startswith(REGISTRY_RAW_URL)
        and not (
            registry_root / wallet["icon"].removeprefix(REGISTRY_RAW_URL)
        ).is_file()
    )

    if missing_icons:
        print(
            f"{wallets_path} references missing local icons for: "
            f"{', '.join(missing_icons)}"
        )
        sys.exit(1)

    print(
        f"{chain_info_path} has valid wallet references, "
        "capabilities, and icons."
    )


if __name__ == "__main__":
    validate_file('./schema/gas.json', './gas.json')
    validate_file('./schema/chains.json', './chains.json')
    validate_file('./schema/chain_info.json', './chain_info.json')
    validate_file('./schema/wallets.json', './wallets.json')
    validate_wallet_references('./chain_info.json', './wallets.json')
