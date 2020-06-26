import pathlib
import os
from lcms_processor.utils import load_sample_list
import json

oldwd = os.getcwd()


def chdir():
	root = pathlib.Path(__file__).parent.parent.parent.absolute()
	os.chdir(root)


chdir()


all_samples = load_sample_list("All Results.json")
all_samples.sort_samples("sample_name")

with open("data/mass_calibration_ranges.json") as fp:
	mass_calibration_ranges = json.load(fp)


__all__ = [
		"all_samples",
		"mass_calibration_ranges",
		]

os.chdir(oldwd)
