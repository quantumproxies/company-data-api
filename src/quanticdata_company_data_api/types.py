"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class CompanyProfileRow(TypedDict, total=False):
    """One row of `company-data profile` (company_profile v1.1.2)."""

    domain: str
    """Registrable host."""
    url: str
    """Homepage URL fetched."""
    name: Optional[str]
    """Company / brand name."""
    tagline: Optional[str]
    """Short positioning line."""
    description: Optional[str]
    """What the company does (meta description or AI)."""
    logo: Optional[str]
    """Logo URL (JSON-LD / og:image)."""
    industry: Optional[str]
    """Industry / sector (AI)."""
    founded: Optional[str]
    """Founding year (JSON-LD / AI)."""
    headquarters: Optional[str]
    """HQ city/country (JSON-LD / AI)."""
    addresses: List[str]
    """Postal addresses found."""
    emails: List[str]
    """Emails found."""
    phones: List[str]
    """Phones found."""
    socials: Dict[str, Any]
    """{ facebook, instagram, linkedin, twitter, youtube, tiktok } URLs."""
    language: Optional[str]
    """Site language."""
    pages_used: List[str]
    """Pages fetched."""
    ai_used: bool
    """Whether AI completion ran."""
    legal_name: Optional[str]
    """Registered company name, when the site states it in its structured data."""
    vat_id: Optional[str]
    """VAT number: from the site's structured data (vatID), or the Italian Partita IVA printed on its pages, footer included. An Italian number is given as its 11 digits, check digit verified. For a member of an Italian VAT group, the group's number, which is the one valid on invoices and in VIES (see vat_group)."""
    tax_id: Optional[str]
    """Tax code: from the site's structured data (taxID), or the Italian codice fiscale printed on its pages, check digit verified. For a member of a VAT group it differs from vat_id and identifies the company in the business register."""
    vat_group: Optional[bool]
    """true when the site publishes vat_id as a VAT group's number ("Gruppo IVA …", "P.IVA Gruppo …"), false otherwise, null without an Italian vat_id."""
    employees: Optional[int]
    """Employee count, when the site states it in its structured data."""
