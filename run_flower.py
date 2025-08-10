#!/usr/bin/env python
"""Run script for AI Task Orchestra Celery flower monitoring tool."""

import argparse
import logging
import sys

from celery.bin import flower

from src.ai_task_orchestra.config import settings
from src.ai_task_orchestra.worker import celery_app


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run AI Task Orchestra Celery flower monitoring tool")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="Port to bind to (default: 5555)",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default=settings.log_level.lower(),
        choices=["debug", "info", "warning", "error", "critical"],
        help=f"Log level (default: {settings.log_level.lower()})",
    )
    return parser.parse_args()


def main():
    """Run the Celery flower monitoring tool."""
    args = parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run the flower monitoring tool
    flower_args = [
        "flower",
        f"--address={args.host}",
        f"--port={args.port}",
        f"--broker={settings.redis_url}",
        "--broker_api=",  # No broker API
    ]
    
    flower.FlowerCommand(app=celery_app).run_from_argv(
        argv=["flower"] + flower_args,
        prog_name="flower",
    )


if __name__ == "__main__":
    sys.exit(main())
