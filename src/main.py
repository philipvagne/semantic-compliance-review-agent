import argparse
import asyncio
import logging
import warnings

from src.adk_spike import format_result
from src.adk_spike import run_spike


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the minimal ADK feasibility spike."
    )
    parser.add_argument("review_text", help="Single review input string.")
    return parser.parse_args()


def main() -> None:
    logging.getLogger("google_adk").setLevel(logging.ERROR)
    warnings.filterwarnings(
        "ignore",
        message=r"\[EXPERIMENTAL\] feature FeatureName\.JSON_SCHEMA_FOR_FUNC_DECL is enabled\.",
        category=UserWarning,
    )
    args = parse_args()
    result = asyncio.run(run_spike(args.review_text))
    print(format_result(result))


if __name__ == "__main__":
    main()
