#!/usr/bin/env python3
"""
=============================================================================
Project:     ReviewToolKit
File:        aggregation.py
Authors:     Axel Masquelin, Kalysta Makimoto, Raul San Jose Estepar
Description: 
Modified:    2026-02-12
Version:     0.1
---------
NOTE: Should we use fuzzy logic with cleaning?
=============================================================================
"""

# ------------ Libraries & Modules ------------ #
import logging
# --------------------------------------------- #

logger = logging.getLogger(__name__)

def aggregate_data(df, config):

    group_by = config.get("group_by", [])
    metrics = config.get("metrics", {})

    if not group_by:
        logger.warning("Aggregation enabled but no group_by provided.")
        return df

    agg_dict = {}

    for metric_name, column in metrics.items():
        if metric_name.startswith("count"):
            agg_dict[column] = "count"

    aggregated_df = df.groupby(group_by).agg(agg_dict).reset_index()

    logger.info("Aggregation complete.")

    return aggregated_df
