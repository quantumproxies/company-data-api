"""Add company name, industry, headquarters and contacts to a CSV of domains.

    python enrich_domains.py accounts.csv --column website --out accounts_enriched.csv

Calls the company profile once per distinct domain in the column and writes
the input rows back with name, legal name, industry, founding year,
headquarters, LinkedIn page, emails, phones and VAT number added. Domains
that fail are reported and left blank, the rest of the file is still written.
"""

import argparse
import csv
from urllib.parse import urlparse

from quanticdata_company_data_api import CompanyData, QuanticDataError, write

ADDED = ["name", "legal_name", "industry", "founded", "headquarters", "emails", "phones", "vat_id"]


def domain_of(value: str) -> str:
    value = value.strip()
    host = urlparse(value if "://" in value else "https://" + value).hostname or ""
    return host[4:] if host.startswith("www.") else host


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_in")
    parser.add_argument("--column", default="domain", help="column with the domain or website URL")
    parser.add_argument("--no-ai", action="store_true", help="only the fields read directly from the pages")
    parser.add_argument("--out", default="enriched.csv")
    args = parser.parse_args()

    with open(args.csv_in, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    domains = sorted({domain_of(r.get(args.column) or "") for r in rows} - {""})

    companies = CompanyData()
    profiles = {}
    for i, domain in enumerate(domains, 1):
        try:
            run = companies.profile(domain, use_ai=not args.no_ai)
            profiles[domain] = run.rows[0] if len(run) else {}
        except QuanticDataError as e:
            print(f"  {domain}: {e}")
            profiles[domain] = {}
        print(f"{i}/{len(domains)} {domain}: {profiles[domain].get('name') or '-'}")

    out = []
    for r in rows:
        p = profiles.get(domain_of(r.get(args.column) or ""), {})
        out.append({**r, **{f"company_{k}": p.get(k) for k in ADDED},
                    "company_linkedin": (p.get("socials") or {}).get("linkedin")})
    write(out, args.out)
    print(f"{len(out)} rows written to {args.out}")


if __name__ == "__main__":
    main()
