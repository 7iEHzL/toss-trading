BIASED_RESEARCH_MODE = "BIASED_RESEARCH_MODE"
STATIC_FUNDAMENTALS_WARNING = (
    "BIASED_RESEARCH_MODE: ROE/PBR inputs are static and are not "
    "point-in-time fundamentals. Results may contain look-ahead bias."
)


def static_fundamentals_disclosure():
    return {
        "research_mode": BIASED_RESEARCH_MODE,
        "fundamentals_point_in_time": False,
        "warnings": [STATIC_FUNDAMENTALS_WARNING],
    }
