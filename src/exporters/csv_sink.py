#!/usr/bin/env python3
"""
Project:     ReviewToolKit
File:        csv_sink.py
Authors:     Axel Masquelin, Kalysta Makimoto, Raul San Jose Estepar
Description: Entrypoint for ReviewToolKit
Modified:    2026-02-12
Version:     0.1
---------
# NOTE: Need to build function registry
"""
# ------------ Libraries & Modules ------------ #
import logging
from pathlib import Path
# --------------------------------------------- #

logger = logging.getLogger(__name__)


def export_csv(df, output_path):

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    logger.info(f"File exported to: {output_path}")
