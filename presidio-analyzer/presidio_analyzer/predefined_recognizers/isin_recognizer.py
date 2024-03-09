from typing import List, Optional, Tuple
from presidio_analyzer import Pattern, PatternRecognizer
from presidio_analyzer.analyzer_utils import PresidioAnalyzerUtils as Utils


class IsinRecognizer(PatternRecognizer):
    """
    Recognize ISIN codes using regex.

    Ref: https://en.wikipedia.org/wiki/International_Securities_Identification_Number

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    iso2a_countryname = ""
    utils = Utils()
    countries = utils.get_country_codes(iso_code="ISO3166-1-Alpha-2")
    for country in countries:
        iso2a_countryname += country + "|"
    pattern = "^" + "(" + iso2a_countryname.rstrip("|") + ")" + "[A-Z0-9]{9}[0-9]{1}$"

    PATTERNS = [
        Pattern(
            "ISIN (Medium)",
            r"\b[A-Z]{2}[A-Z0-9]{9}\d{1}\b",
            0.5,
        ),
        Pattern(
            "ISIN (Strong)",
            pattern,
            0.85,
        ),
    ]

    CONTEXT = ["ISIN", "ISIN_CODE"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ISIN_CODE",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = (
            replacement_pairs
            if replacement_pairs
            else [("-", ""), (" ", ""), (":", "")]
        )

        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
