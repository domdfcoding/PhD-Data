#!/usr/bin/env python3
#
#  get_acquisition_params.py
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

# 3rd party
import pandas
from domdf_python_tools.paths import PathPlus
from mathematical.data_frames import set_display_options

set_display_options()

worklist = pandas.read_json("../data/worklist.json")
worklist = worklist.set_index(["Data File"])

mass_calibration_ranges = PathPlus("../data/mass_calibration_ranges.json").load_json()
worklist["MZ Range"] = worklist.index.map(mass_calibration_ranges)


def set_default_value(df, column_name, value, dtype):
	df[column_name] = df[column_name].map({'': value}).fillna(value).astype(dtype)


set_default_value(worklist, "Drying Gas", 16, int)  # l/min
set_default_value(worklist, "Nebulizer", 40, int)  # psig
set_default_value(worklist, "Gas Temp", 250, int)  # C

print(worklist)
print(worklist.loc["Methanol_Blank_+ve_191121-0001-r001.d"]["Gas Temp"])

# Remove samples from 5th March that there aren't datafiles for
worklist = worklist.drop([
		"Unique_10ug_ml_diff_meth_v2_1_200303-0007.d",
		"MeOH_Blank_diff_method_200305-0001.d",
		"Column_Clean_200305-0002.d",
		])

print(worklist)
