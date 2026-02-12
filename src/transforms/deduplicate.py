#!/usr/bin/env python3
"""
=============================================================================
Project:     ReviewToolKit
File:        deduplicate.py
Authors:     Axel Masquelin, Kalysta Makimoto, Raul San Jose Estepar
Description: Check  for Matches and Ensure that no duplicate manuscripts exist
Modified:    2026-02-12
Version:     0.1
---------
NOTE: Should we use fuzzy logic with cleaning?
=============================================================================
"""

# ------------ Libraries & Modules ------------ #
from thefuzz import fuzz
import logging
# --------------------------------------------- #

logger = logging.getLogger(__name__)


def deduplicate_entries(df, fuzzy_threshold=92):

    df = df.reset_index(drop=True)
    to_drop = set()

    for year, group in df.groupby("Publication Year"):
        indices = group.index.tolist()

        for i in range(len(indices)):
            if indices[i] in to_drop:
                continue

            title_i = df.loc[indices[i], "normalized_title"]

            for j in range(i + 1, len(indices)):
                if indices[j] in to_drop:
                    continue

                title_j = df.loc[indices[j], "normalized_title"]

                score = fuzz.token_set_ratio(title_i, title_j)

                if score >= fuzzy_threshold:
                    to_drop.add(indices[j])

    logger.info(f"Duplicates identified: {len(to_drop)}")

    return df.drop(index=to_drop).drop(columns=["normalized_title"])
