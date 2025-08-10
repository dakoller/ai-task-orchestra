#!/usr/bin/env python
"""Run script for AI Task Orchestra Celery worker."""

import argparse
import logging
import sys

from src.ai_task_orchestra.config import settings
from src.ai_task_orchestra.worker import celery_app


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run AI Task Orchestra Celery worker")
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default=settings.log_level.lower(),
        choices=["debug", "info", "warning", "error", "critical"],
        help=f"Log level (default: {settings.log_level.lower()})",
    )
    parser.add_argument(
        "--queues",
        type=str,
        default="celery",
        help="Comma-separated list of queues to consume from (default: celery)",
    )
    return parser.parse_args()


def main():
    """Run the Celery worker."""
    args = parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run the worker
    worker_args = [
        "worker",
        f"--concurrency={args.concurrency}",
        f"--loglevel={args.loglevel}",
        f"--queues={args.queues}",
    ]
    
    celery_app.worker_main(argv=worker_args)


if __name__ == "__main__":
    sys.exit(main())
