#!/usr/bin/env python3
#
#  parse_raw_csv.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import pathlib
import re

# 3rd party
from mathematical.data_frames import set_display_options
from mathematical.utils import concatenate_csv
from mh_utils.csv_parser import ResultParser
from mh_utils.csv_parser.utils import concatenate_json

# Display options for numpy and pandas
set_display_options()

json_results_dir = pathlib.Path("../data/json_results")
raw_results_dir = pathlib.Path("../data/raw_results")
csv_results_dir = pathlib.Path("../data/csv_results")

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

dates = ['-'.join(re.findall("..", date)) for date in dates]
parser.parse_directory_list(dates)

csv_files = []
json_files = []

for date in dates:
	csv_files.append(csv_results_dir / date / "CSV Results Parsed.csv")
	json_files.append(json_results_dir / date / "results.json")

combined_csv = concatenate_csv(*csv_files, outfile="../data/All CSV Results.csv")
all_samples = concatenate_json(*json_files, outfile="../data/All Results.json")

print(f"\nSaved complete set of results to -> data/All CSV Results.csv")
print(f"                                 -> data/All Results.json")
