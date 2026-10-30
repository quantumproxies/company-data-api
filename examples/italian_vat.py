"""Partita IVA, codice fiscale and legal name of Italian companies, from their websites.

    python italian_vat.py @domini.txt --out partite_iva.csv

For each domain it reads the company record with AI completion off (the VAT
fields come straight from the pages and their structured data) and writes the
legal name, Partita IVA, codice fiscale and the VAT group flag. A Partita IVA
is returned only with its check digit verified; domains whose pages print
none are written with an empty vat_id.
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
    parser.add_argument("--out", default="vat_ids.csv")
    args = parser.parse_args()

    companies = CompanyData()
    rows = []
    for domain in read_domains(args.domains):
        try:
            run = companies.profile(domain, use_ai=False)
        except QuanticDataError as e:
            print(f"{domain}: {e}")
            continue
        p = run.rows[0] if len(run) else {}
        rows.append({"domain": p.get("domain") or domain, "name": p.get("name"), "legal_name": p.get("legal_name"),
                     "vat_id": p.get("vat_id"), "tax_id": p.get("tax_id"), "vat_group": p.get("vat_group"),
                     "addresses": p.get("addresses"), "pages_used": p.get("pages_used")})
        print(f"{domain}: {p.get('vat_id') or '-'}")

    write(rows, args.out)
    print(f"{sum(1 for r in rows if r['vat_id'])} of {len(rows)} companies with a Partita IVA, written to {args.out}")


if __name__ == "__main__":
    main()
