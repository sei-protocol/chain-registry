import json
import sys
from jsonschema import validate, ValidationError


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
    wallet_identifiers = {
        wallet["identifier"] for wallet in wallets["extensions"]
    }
    missing_wallets = sorted(
        set(chain_info["supported_wallets"]) - wallet_identifiers
    )

    if missing_wallets:
        print(
            f"{chain_info_path} references unknown wallets: "
            f"{', '.join(missing_wallets)}"
        )
        sys.exit(1)

    print(f"{chain_info_path} has valid wallet references.")


if __name__ == "__main__":
    validate_file('./schema/gas.json', './gas.json')
    validate_file('./schema/chains.json', './chains.json')
    validate_file('./schema/chain_info.json', './chain_info.json')
    validate_file('./schema/wallets.json', './wallets.json')
    validate_wallet_references('./chain_info.json', './wallets.json')
