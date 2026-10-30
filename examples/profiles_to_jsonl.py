"""Company records for a list of domains, one JSON object per line.

    python profiles_to_jsonl.py stripe.com shopify.com allbirds.com --out companies.jsonl

Each line is the full record as the API returns it (nested socials and lists
kept), ready for a CRM import, a search index or an LLM prompt. Domains can
also come from a file: python profiles_to_jsonl.py @domains.txt
"""

import argparse

from quanticdata_company_data_api import CompanyData, QuanticDataError, write


def read_domains(values):
    domains = []
    for v in values:
        if v.startswith("@"):
            with open(v[1:], encoding="utf-8") as fh:
                domains += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        else:
            domains.append(v)
    return domains


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domains", nargs="+", help="domains, URLs or @file.txt")
    parser.add_argument("--out", default="companies.jsonl")
    args = parser.parse_args()

    companies = CompanyData()
    records = []
    for domain in read_domains(args.domains):
        try:
            records.extend(companies.profile(domain))
        except QuanticDataError as e:
            print(f"{domain}: {e}")
            continue
        print(f"{domain}: {records[-1].get('name') if records else '-'}")

    write(records, args.out, "jsonl")
    print(f"{len(records)} company records written to {args.out}")


if __name__ == "__main__":
    main()
