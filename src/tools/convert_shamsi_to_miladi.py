import json
from persiantools.jdatetime import JalaliDate


CONVERT_SHAMSI_TO_MILADI_SCHEMA = {
    "type": "function",
    "function": {
        "name": "convert_shamsi_to_miladi",
        "description": "Convert a Shamsi (Jalali/Persian) date to Miladi (Gregorian). Use this when the user provides a birthday in the Shamsi/Persian calendar. We store dates in Miladi.",
        "parameters": {
            "type": "object",
            "properties": {
                "shamsi_month": {
                    "type": "integer",
                    "description": "The Shamsi month (1-12). Farvardin=1, Ordibehesht=2, Khordad=3, Tir=4, Mordad=5, Shahrivar=6, Mehr=7, Aban=8, Azar=9, Dey=10, Bahman=11, Esfand=12",
                },
                "shamsi_day": {
                    "type": "integer",
                    "description": "The Shamsi day of the month (1-31)",
                },
            },
            "required": ["shamsi_month", "shamsi_day"],
        },
    },
}


def tool_convert_shamsi_to_miladi(mongodb_uri: str, arguments: dict) -> str:
    """Convert a Shamsi date to Miladi and return the Gregorian month and day."""
    shamsi_month = arguments["shamsi_month"]
    shamsi_day = arguments["shamsi_day"]

    try:
        # Use a reference year for conversion (we only care about month/day)
        # Using 1403 (2024-2025) as a reasonable reference year
        shamsi_date = JalaliDate(1403, shamsi_month, shamsi_day)
        gregorian_date = shamsi_date.to_gregorian()

        return json.dumps({
            "miladi_month": gregorian_date.month,
            "miladi_day": gregorian_date.day,
            "shamsi_input": f"{shamsi_month}/{shamsi_day}",
            "miladi_result": f"{gregorian_date.month}/{gregorian_date.day}",
        })
    except Exception as e:
        return json.dumps({"error": str(e)})
