#!/usr/bin/env python
"""Run script for AI Task Orchestra."""

import argparse
import logging
import sys

import uvicorn

from src.ai_task_orchestra.config import settings


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run AI Task Orchestra")
    parser.add_argument(
        "--host",
        type=str,
        default=settings.api_host,
        help=f"Host to bind to (default: {settings.api_host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.api_port,
        help=f"Port to bind to (default: {settings.api_port})",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=settings.api_reload,
        help="Enable auto-reload (default: {})".format("enabled" if settings.api_reload else "disabled"),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=settings.api_debug,
        help="Enable debug mode (default: {})".format("enabled" if settings.api_debug else "disabled"),
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=settings.log_level,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help=f"Log level (default: {settings.log_level})",
    )
    return parser.parse_args()


def main():
    """Run the application."""
    args = parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run the application
    uvicorn.run(
        "src.ai_task_orchestra.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower(),
    )


if __name__ == "__main__":
    sys.exit(main())
