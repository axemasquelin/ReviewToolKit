#!/usr/bin/env python3
"""
=============================================================================
Project:     ReviewToolKit
File:        cleaning.py
Authors:     Axel Masquelin, Kalysta Makimoto, Raul San Jose Estepar
Description: Cleaning toolkit for dataframe
Modified:    2026-02-12
Version:     0.1
---------
NOTE: Should we use fuzzy logic with cleaning?
=============================================================================
"""

# ------------ Libraries & Modules ------------ #
import pandas as pd
import numpy as np
import unicodedata
import logging
import re
# --------------------------------------------- #

logger = logging.getLogger(__name__)

STANDARD_COLUMNS = [
    "Title",
    "Keywords",
    "Abstract",
    "Authors",
    "Publication Year",
    "Journal"
]

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_data(file_path, column_mapping=None):

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1")

    df.columns = [col.strip().lower() for col in df.columns]

    rename_dict = {}
    if column_mapping:
        for col in df.columns:
            if col in column_mapping:
                rename_dict[col] = column_mapping[col]

    df = df.rename(columns=rename_dict)

    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    df = df[STANDARD_COLUMNS]

    df["Publication Year"] = pd.to_numeric(
        df["Publication Year"], errors="coerce"
    )

    df["normalized_title"] = df["Title"].apply(normalize_text)

    logger.info(f"Cleaning complete: {file_path}")

    return df
