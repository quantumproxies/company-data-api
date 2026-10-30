# Company Data API

[![ci](https://github.com/quantumproxies/company-data-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/company-data-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Turn a domain into a company record, from Python or the command line: name, legal name, tagline and description, industry, founding year, headquarters, office addresses, emails, phones, social profiles, logo, site language and, for Italian companies, the Partita IVA and codice fiscale, as JSON or CSV. The record is read from the company's own website; with AI completion on (the default) an LLM fills description, industry, founding year and headquarters from those pages. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/company-data-api
company-data login
company-data profile stripe.com -o stripe.json
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=company-data-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `company-data profile` | domain or site URL | Name, legal name, industry, HQ, addresses, socials, contacts, VAT id, 21 fields per row ([fields and price](https://quanticdata.io/collectors/company-data-api/?utm_source=github&utm_medium=readme&utm_campaign=company-data-api)) | up to 1 |

One call returns one record. The fields come from the company's own pages (the homepage and pages such as about and contact) and the structured data they carry; `pages_used` lists the pages that were read and `ai_used` says whether AI completion ran. For Italian companies `vat_id` is the 11-digit Partita IVA with its check digit verified, and `vat_group` flags a VAT group's number.

## Sample output

A real row from `company-data profile stripe.com --use-ai` (2026-10-23):

```json
{
  "url": "https://stripe.com/",
  "logo": "https://images.stripeassets.com/fzn2n1nzq965/1hgcBNd12BfT9VLgbId7By/01d91920114b124fb4cf6d448f9f06eb/favicon.svg",
  "name": "Stripe",
  "domain": "stripe.com",
  "emails": [],
  "phones": [],
  "tax_id": null,
  "vat_id": null,
  "ai_used": true,
  "founded": null,
  "socials": {
    "twitter": "https://twitter.com/stripe",
    "youtube": "https://youtube.com/@stripe",
    "facebook": "https://www.facebook.com/StripeHQ",
    "linkedin": "https://www.linkedin.com/company/stripe/",
    "instagram": "https://www.instagram.com/stripehq/"
  },
  "tagline": "Financial infrastructure to grow your revenue.",
  "industry": "Financial technology / payments",
  "language": "en-BR",
  "addresses": [
    "60 Anson Road #05-01, 079914, Singapore, SG",
    "920 5th Avenue, Suite 1900, 98104, Seattle, WA, US",
    "201 Bishopsgate, 5th Floor, EC2M 3AB, London, GB",
    "350 N. Orleans, Suite 5000S, 60654, Chicago, IL, US",
    "28 Liberty Street, 48th floor, 10005, New York, NY, US"
  ],
  "employees": null,
  "vat_group": null,
  "legal_name": "Stripe, LLC",
  "pages_used": [
    "https://stripe.com/",
    "https://stripe.com/en-br/contact/sales",
    "https://stripe.com/en-br/about"
  ],
  "description": "Stripe is a technology company that builds programmable financial infrastructure. It provides payments, financial services, and custom revenue models to help businesses start and scale.",
  "headquarters": null
}
```

## Python

```python
from quanticdata_company_data_api import CompanyData

companies = CompanyData()  # saved login, or QUANTICDATA_API_KEY

stripe = companies.profile("stripe.com").rows[0]
print(stripe["name"], stripe["legal_name"], stripe["industry"])
print(stripe["socials"]["linkedin"], stripe["addresses"][:2])

for domain in ["allbirds.com", "shopify.com"]:
    row = companies.profile(domain).rows[0]
    print(domain, row["name"], row["industry"], row["headquarters"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Enrich a list of domains**: Read a CSV with a column of domains and add name, legal name, industry, headquarters, LinkedIn page, emails and phones to every row, one call per domain. See [`examples/enrich_domains.py`](examples/enrich_domains.py).
- **Italian VAT numbers**: Get the Partita IVA, codice fiscale and legal name that Italian company sites print, with the VAT group flag, for invoicing or a business register check. See [`examples/italian_vat.py`](examples/italian_vat.py).
- **Company records as JSON Lines**: Write one JSON object per company, with every field kept as returned, for a CRM import, a search index or an LLM prompt. See [`examples/profiles_to_jsonl.py`](examples/profiles_to_jsonl.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `company-data run <id> -o out.csv` collects it later.

### `company-data profile`

One structured company record from a domain: name, description, industry, HQ, socials, contacts, logo.

```
company-data profile DOMAIN [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `DOMAIN` | string |  | Company domain or site URL. |
| `--country` | string |  | ISO 3166-1 alpha-2 code — the site is read as a visitor from this country. Default us, in en-US, so a site that localizes by visitor answers in English. |
| `--use-ai` | boolean | `True` | Let an LLM fill description, industry, founding year and headquarters from the pages that were read (default on). --no-use-ai returns only the fields read directly from the pages. |

## Output fields

<details><summary><code>company-data profile</code>: 21 fields</summary>

| Field | Type | Description |
|---|---|---|
| `domain` | string | Registrable host. |
| `url` | string | Homepage URL fetched. |
| `name` | string or null | Company / brand name. |
| `tagline` | string or null | Short positioning line. |
| `description` | string or null | What the company does (meta description or AI). |
| `logo` | string or null | Logo URL (JSON-LD / og:image). |
| `industry` | string or null | Industry / sector (AI). |
| `founded` | string or null | Founding year (JSON-LD / AI). |
| `headquarters` | string or null | HQ city/country (JSON-LD / AI). |
| `addresses` | string[] | Postal addresses found. |
| `emails` | string[] | Emails found. |
| `phones` | string[] | Phones found. |
| `socials` | object | { facebook, instagram, linkedin, twitter, youtube, tiktok } URLs. |
| `language` | string or null | Site language. |
| `pages_used` | string[] | Pages fetched. |
| `ai_used` | boolean | Whether AI completion ran. |
| `legal_name` | string or null | Registered company name, when the site states it in its structured data. |
| `vat_id` | string or null | VAT number: from the site's structured data (vatID), or the Italian Partita IVA printed on its pages, footer included. An Italian number is given as its 11 digits, check digit verified. For a member of an Italian VAT group, the group's number, which is the one valid on invoices and in VIES (see vat_group). |
| `tax_id` | string or null | Tax code: from the site's structured data (taxID), or the Italian codice fiscale printed on its pages, check digit verified. For a member of a VAT group it differs from vat_id and identifies the company in the business register. |
| `vat_group` | boolean or null | true when the site publishes vat_id as a VAT group's number ("Gruppo IVA …", "P.IVA Gruppo …"), false otherwise, null without an Italian vat_id. |
| `employees` | integer or null | Employee count, when the site states it in its structured data. |

</details>

## Sign-in and API keys

- `company-data login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `company-data login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `company-data login --api-key`.
- `company-data logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=company-data-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/company_profile/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"domain": "stripe.com", "use_ai": true}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=company-data-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=company-data-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this company data API free?**

The code is free and MIT-licensed. Lookups run on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a domain and get the company record back; the pages are read on QuanticData's side.

**Where does the data come from?**

From the company's own website: the homepage, pages such as about and contact, and the structured data they carry. With AI completion on, an LLM fills description, industry, founding year and headquarters from those same pages; ai_used says whether it ran.

**How many companies can one run return?**

One record per run, for one domain. For a list, call it once per domain, as examples/enrich_domains.py does.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Social profiles become socials.linkedin, socials.twitter and so on, and lists such as addresses and emails are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/enrich_domains.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Email Extractor](https://github.com/quantumproxies/email-extractor): Email extractor for Python and the command line.
- [Website Technology Checker](https://github.com/quantumproxies/website-technology-checker): Website technology checker for Python and the command line.
- [LinkedIn Scraper](https://github.com/quantumproxies/linkedin-scraper): LinkedIn scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=company-data-api).
