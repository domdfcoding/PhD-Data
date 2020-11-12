#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  parse_raw_csv.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
import re

# this package
from mathematical.data_frames import set_display_options
from mathematical.utils import concatenate_csv
from mh_utils.csv_parser import ResultParser
from mh_utils.csv_parser.utils import concatenate_json


# Display options for numpy and pandas
set_display_options()


json_results_dir = pathlib.Path("data/json_results")
raw_results_dir = pathlib.Path("data/raw_results")
csv_results_dir = pathlib.Path("data/csv_results")

parser = ResultParser(raw_results_dir, json_results_dir, csv_results_dir)

dates = {
		"191121",
		"191126",
		"191128",
		"191206",
		"191211",
		"200124",
		"200128",
		"200129",
		"200206",
		"200218",
		"200221",
		"200227",
		"200303",
		}

dates = ["-".join(re.findall("..", date)) for date in dates]
parser.parse_directory_list(dates)

csv_files = []
json_files = []

for date in dates:
	csv_files.append(csv_results_dir / date / "CSV Results Parsed.csv")
	json_files.append(json_results_dir / date / "results.json")


combined_csv = concatenate_csv(*csv_files, outfile="data/All CSV Results.csv")
all_samples = concatenate_json(*json_files, outfile="data/All Results.json")

print(f"\nSaved complete set of results to -> data/All CSV Results.csv")
print(f"                                 -> data/All Results.json")


