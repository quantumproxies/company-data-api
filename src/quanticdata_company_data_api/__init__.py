"""Company Data API: Company data API for Python and the command line: one structured company record from a domain, with name, legal name, description, industry, headquarters, office addresses, emails, phones, social profiles, logo and VAT number, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_company_data_api import CompanyData

    scraper = CompanyData()   # saved login (`company-data login`) or QUANTICDATA_API_KEY
    run = scraper.profile(...)   # one company record from a domain
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["CompanyData", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class CompanyData:
    """Company Data API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="company-data/0.1.0 (+https://github.com/quantumproxies/company-data-api)", timeout=timeout)

    def profile(
        self, domain: str,
        *,
        country: Optional[str] = None,
        use_ai: Optional[bool] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """One structured company record from a domain: name, description, industry, HQ, socials, contacts, logo.

        Args:
            domain: Company domain or site URL.
            country: ISO 3166-1 alpha-2 code — the site is read as a visitor from this country. Default us, in en-US, so a site that localizes by visitor answers in English.
            use_ai: Let an LLM fill description, industry, founding year and headquarters from the pages that were read (default on). --no-use-ai returns only the fields read directly from the pages.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 1 rows, one per profile: see ``types.CompanyProfileRow``.
        """
        payload = {
            "domain": domain,
            "country": country,
            "use_ai": use_ai,
        }
        return self.client.run_collector("company_profile", payload, wait=wait, timeout=timeout)
