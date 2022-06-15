#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 14:34:43 2022

@author: charliehenry
"""

import pandas as pd
from sodapy import Socrata
import os

df = pd.read_csv("split_failures.csv")
# df = df[df["Time"] == "PM"]
# df = df[df["Month"] == "Apr"]
# df = df[df["Year"] == 2022]

df["start_dt"] = pd.to_datetime(df["startDate"])
df["month_no"] = df["start_dt"].dt.month
df["year_no"] = df["start_dt"].dt.year


def get_crash_count(lat, long, radius, month, year):

    print(f"intersction at {lat},{long} on {month}-{year}")

    res = client.get(
        "y2wy-tgr5",
        select="count(crash_id)",
        where=f"within_circle(point, {lat},{long}, {radius}) AND date_extract_m(crash_date) = {month} AND date_extract_y(crash_date) = {year}",
        limit=2,
    )

    return int(res[0]["count_crash_id"])


client = Socrata("data.austintexas.gov", timeout=10)


# df['crash_count'] = df.apply()

df["crash_count"] = df.apply(
    lambda x: get_crash_count(
        x["lat"], x["lon"], 91.44 / 3, x["month_no"], x["year_no"]
    ),
    axis=1,
)

df["crashes per 1000 veh"] = df["crash_count"] / df["totalVehicleVolume"]

df.to_csv("crashes_intx.csv")
