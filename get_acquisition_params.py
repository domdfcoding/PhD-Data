import json

import pandas

from lcms_processor.utils import (
	set_display_options,
	)

# Display options for numpy and pandas
set_display_options()

worklist = pandas.read_json("data/worklist.json")
with open("data/mass_calibration_ranges.json") as fp:
	mass_calibration_ranges = json.load(fp)

worklist = worklist.set_index(["Data File"])

worklist['MZ Range'] = worklist.index.map(mass_calibration_ranges)


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


