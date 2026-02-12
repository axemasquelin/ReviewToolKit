#!/usr/bin/env python3
"""
=============================================================================
Project:     ReviewToolKit
File:        run_validations.py
Authors:     Axel Masquelin, Kalysta Makimoto, Raul San Jose Estepar
Description: Entrypoint for ReviewToolKit
Modified:    2026-02-12
Version:     0.1
---------
# NOTE: Need to build function registry
=============================================================================
"""

# ------------ Libraries & Modules ------------ #
import argparse
import logging
import yaml
import pandas as pd
from pathlib import Path

from src.transforms.cleaning import clean_data
from src.transforms.aggregation import aggregate_data
from src.transforms.deduplicate import deduplicate_entries
from src.exporters.csv_sink import export_csv
# --------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_pipeline(config_path: str):

    config = load_config(config_path)

    logger.info(f"Running project: {config['project']['name']}")

    # Loading CSV Files 
    frames = []
    for file_path in config["input_files"]:
        logger.info(f"Loading file: {file_path}")

        if config["steps"]["cleaning"]["enabled"]:
            df = clean_data(file_path, config.get("column_mapping"))
        else:
            df = pd.read_csv(file_path)

        frames.append(df)

    merged_df = pd.concat(frames, ignore_index=True)
    logger.info(f"Total rows after merge: {len(merged_df)}")

    # Aggregation Steps (User-Controlled)
    if config["steps"]["aggregation"]["enabled"]:
        merged_df = aggregate_data(
            merged_df,
            config["steps"]["aggregation"]
        )

    # Deduplication (User-Controlled)
    if config["steps"]["deduplication"]["enabled"]:
        threshold = config["steps"]["deduplication"]["fuzzy_threshold"]
        merged_df = deduplicate_entries(merged_df, threshold)

    # Exporter Functionality (User-Controlled)
    if config["steps"]["export"]["enabled"]:
        export_path = config["steps"]["export"]["output_path"]
        export_csv(merged_df, export_path)

    logger.info("Pipeline completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Review Toolkit Validation Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML configuration file"
    )

    args = parser.parse_args()

    run_pipeline(args.config)
