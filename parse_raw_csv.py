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

# 3rd party
from domdf_python_tools.paths import maybe_make

# this package
from lcms_processor.core import parse_masshunter_csv
from lcms_processor.utils import concatenate_csv, concatenate_json, set_display_options

# Display options for numpy and pandas
set_display_options()


class ResultParser:
	def __init__(self, raw_results_dir, json_results_dir, csv_results_dir):
		"""
		Take a directory of CSV results exported from MassHunter and parse them to CSV and JSON.

		:param raw_results_dir: The directory in which the raw exports from MassHunter are stored.
		:type raw_results_dir: str or pathlib.Path
		:param json_results_dir: The directory to store the output json files in
		:type json_results_dir: str or pathlib.Path
		:param csv_results_dir: The directory to store the output csvfiles in
		:type csv_results_dir: str or pathlib.Path
		"""
		
		self.raw_results_dir = pathlib.Path(raw_results_dir)
		
		self.json_results_dir = pathlib.Path(json_results_dir)
		maybe_make(self.json_results_dir, parents=True)
		
		self.csv_results_dir = pathlib.Path(csv_results_dir)
		maybe_make(self.csv_results_dir, parents=True)

	def parse_for_directory(self, directory):
		"""
		Convert the "CSV Results.csv" file in the given directory to CSV and JSON

		:param directory:
		:type directory: pathlib.Path

		:return:
		:rtype:
		"""

		maybe_make(self.json_results_dir / directory)
		maybe_make(self.csv_results_dir / directory)
		
		infile = raw_results_dir / directory / "CSV Results.csv"
		csv_outfile = csv_results_dir / directory / "CSV Results Parsed.csv"
		json_outfile = json_results_dir / directory / "results.json"
		print(f"{infile} -> {csv_outfile}")
		print(f"{' ' * len(str(infile))} -> {json_outfile}")
		
		parse_masshunter_csv(infile, csv_outfile, json_outfile)
	
	def parse_directory_list(self, directory_list):
		"""
		Runs :meth:`ResultsParser.parse_for_directory` for each directory in ``directory_list``
		
		:param directory_list: A list of directorys to process
		:type directory_list:
		"""
		
		for directory in directory_list:
			print(f"Processing directory {directory}")
			self.parse_for_directory(directory)


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


combined_csv = concatenate_csv(csv_files, "data/All CSV Results.csv")
all_samples = concatenate_json(json_files, "data/All Results.json")

print(f"\nSaved complete set of results to -> data/All CSV Results.csv")
print(f"                                 -> data/All Results.json")


