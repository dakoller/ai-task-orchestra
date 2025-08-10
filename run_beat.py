#!/usr/bin/env python
"""Run script for AI Task Orchestra Celery beat scheduler."""

import argparse
import logging
import sys

from src.ai_task_orchestra.config import settings
from src.ai_task_orchestra.worker import celery_app


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run AI Task Orchestra Celery beat scheduler")
    parser.add_argument(
        "--loglevel",
        type=str,
        default=settings.log_level.lower(),
        choices=["debug", "info", "warning", "error", "critical"],
        help=f"Log level (default: {settings.log_level.lower()})",
    )
    parser.add_argument(
        "--schedule",
        type=str,
        default="celerybeat-schedule",
        help="Path to the schedule database (default: celerybeat-schedule)",
    )
    return parser.parse_args()


def main():
    """Run the Celery beat scheduler."""
    args = parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run the beat scheduler
    beat_args = [
        "beat",
        f"--loglevel={args.loglevel}",
        f"--schedule={args.schedule}",
    ]
    
    celery_app.start(argv=beat_args)


if __name__ == "__main__":
    sys.exit(main())
