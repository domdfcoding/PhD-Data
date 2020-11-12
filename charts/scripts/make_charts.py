#!/usr/bin/env python3
#
#  make_charts.py
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
import json
import os
import pathlib

# 3rd party
from mathematical.data_frames import set_display_options
from mh_utils.csv_parser import SampleList

root = pathlib.Path(__file__).parent.parent.parent.absolute()
os.chdir(root)

# Display options for numpy and pandas
set_display_options()

all_samples = SampleList.from_json_file("All Results.json")
all_samples.sort_samples("sample_name")
with open("data/mass_calibration_ranges.json") as fp:
	mass_calibration_ranges = json.load(fp)

# pprint(all_samples.sample_names)

target_samples = all_samples.filter([
		# 'DPA 10ug/mL  - different method (1)',
		# 'DPA 10ug/mL  - different method (2)',
		# 'DPA 10ug/mL - new mix  - different method (2)',
		# 'DPA 10ug/mL - new mix - different method (1)',
		# 'DPA 1ug/mL  - different method',
		# 'DPA 1ug/mL  - different method (1)',
		# 'DPA 1ug/mL  - different method (2)',
		# 'DPA 1ug/mL (1)',
		# 'DPA 1ug/mL (2)',
		# 'EC 1ug/mL  - different method',
		# 'EC 1ug/mL  - different method (1)',
		# 'EC 1ug/mL  - different method (2)',
		# 'EC 1ug/mL  - different method (3)',
		# 'EC 1ug/mL (1)',
		# 'EC 1ug/mL (2)',

		# 'Flask Cleaning Test',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method',
		# 'MeOH Blank - different method - 1700mz',
		# 'Methanol Blank',
		# 'Methanol Blank',
		# 'Methanol Blank',
		# 'Methanol Blank',
		# 'Methanol Blank (2)',
		# 'Methanol Blank (2)',
		# 'Methanol Blank DG14 Neb 40',
		# 'Propellant 100mg',
		# 'Propellant 10mg',
		# 'Propellant 10mg',
		# 'Propellant 10mg (1) rerun',
		# 'Propellant 10mg (2)',
		# 'Propellant 10mg (2) DG14 Neb 40',
		# 'Propellant 10mg (2) GF 14 Neb 35',
		# 'Propellant 1mg',
		# 'Propellant 1mg (2)',
		# 'Propellant 1mg (2) DG14 Neb 40',
		# 'Propellant 1mg (2) GF 14',
		# 'Propellant 1mg (2) GF 14 Neb 35',
		# 'Propellant 1mg (2) GT 200',
		# 'Propellant 1mg (2) Neb 50',
		# 'Propellant 1mg (2) Repeat DG14 Neb 40',
		# 'Propellant 1ug',
		# 'Propellant 1ug',
		# 'Propellant 1ug (2)',
		# 'Propellant 1ug (2) DG14 Neb 40',
		# 'Propellant 1ug (2) Repeat DG14 Neb 40',
		# 'Propellant Standard 0.1ug/mL (1)',
		# 'Propellant Standard 0.1ug/mL (1)',
		# 'Propellant Standard 0.1ug/mL (2)',
		# 'Propellant Standard 0.1ug/mL (2)',
		# 'Propellant Standard 100ug/mL (1)',
		# 'Propellant Standard 100ug/mL (1)',
		# 'Propellant Standard 10ug/mL',
		# 'Propellant Standard 10ug/mL (1)',
		# 'Propellant Standard 10ug/mL (2)',
		# 'Propellant Standard 10ug/mL - different method (1)',
		# 'Propellant Standard 10ug/mL - different method (2)',
		"Propellant Standard 10ug/mL DG 14",
		"Propellant Standard 10ug/mL GT 200",
		"Propellant Standard 10ug/mL NEB 35",
		# 'Propellant Standard 10ug/mL ms/ms (1)',
		# 'Propellant Standard 10ug/mL ms/ms (2)',
		# 'Propellant Standard 1ug/mL (1)',
		# 'Propellant Standard 1ug/mL (1)',
		# 'Propellant Standard 1ug/mL (2)',
		# 'Propellant Standard 1ug/mL (2)',
		# 'Propellant Standard 1ug/mL - different method (1)',
		# 'Propellant Standard 1ug/mL - different method (2)',
		# 'Propellant Standard 1ug/mL - different method (3)',

		# 'Unique 10ug/mL - different method (1)',
		# 'Unique 10ug/mL - different method (2)',
		])

# plot_area_and_score(all_samples, "Diphenylamine")
# plt.savefig("charts/dpa.png")
#
# plot_areas(target_samples, ["Diphenylamine", "Ethyl Centralite", "Nitrobenzene"])
# plt.savefig("charts/areas.png")
#
# # plot_area_and_score(all_samples, "Nitrobenzene")
# # plt.show()
#
#
# worklist = load_json_worklist("data/worklist.json")
# print(worklist)
#
# # print(worklist.loc["Methanol Blank"])
# print(worklist.loc[worklist["Sample Name"] == "Methanol Blank"])
# print(worklist.loc[worklist["Sample Name"].str.startswith("Methanol")])
#
#
samples = """
Sample Name,Method,Data File

# Alliant Unique pos and neg
Propellant 1mg +ve,Maitre Gunshot Residue Positive.m,Propellant_1mg_+ve_191121-0002-r001.d
Propellant 1ug +ve,Maitre Gunshot Residue Positive.m,Propellant_1ug_+ve_191121-0003-r001.d
Propellant 1mg -ve,Maitre Gunshot Residue Negative.m,Propellant_1mg_-ve_191121-0005-r001.d
Propellant 1ug -ve,Maitre Gunshot Residue Negative.m,Propellant_1ug_-ve_191121-0006-r001.d

# Increased injection volume from 1ug to 5ug
Propellant 1mg +ve 5ul,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_+ve_5ul_191121-0008-r001.d
Propellant 1ug +ve 5ul,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_+ve_5ul_191121-0009-r001.d

# method permutations	(standard conditions GT 250)
Propellant 1mg gas 200,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_gas_200_191121-0011-r001.d
Propellant 1ug gas 200,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_gas_200_191121-0012-r001.d
Propellant 1mg gas 280,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_gas_280_191121-0013-r001.d
Propellant 1ug gas 280,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_gas_280_191121-0014-r001.d
Propellant 1mg drying 14,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_drying_14_191121-0015-r001.d
Propellant 1ug drying 14,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_drying_14_191121-0016-r001.d
Propellant 1mg drying 16,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_drying_16_191121-0017-r001.d
Propellant 1ug drying 16,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_drying_16_191121-0018-r001.d
Propellant 1mg drying 18,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_drying_18_191121-0019-r001.d
Propellant 1ug drying 18,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_drying_18_191121-0020-r001.d
Propellant 1mg nebul 40,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_nebul_40_191121-0021-r001.d
Propellant 1ug nebul 40,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_nebul_40_191121-0022-r001.d
Propellant 1mg nebul 50,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_nebul_50_191121-0023-r001.d
Propellant 1ug nebul 50,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_nebul_50_191121-0024-r001.d
Propellant 1mg nebul 60,Maitre Gunshot Residue Positive 5ul.m,Propellant_1mg_nebul_60_191121-0025-r001.d
Propellant 1ug nebul 60,Maitre Gunshot Residue Positive 5ul.m,Propellant_1ug_nebul_60_191121-0026-r001.d

# Benito method
Propellant 1mg,Benito Gunshot Residue Positive.m,Propellant_1mg_191126-0002-r001.d
Propellant 1ug,Benito Gunshot Residue Positive.m,Propellant_1ug_191126-0003-r001.d
Propellant 10mg,Benito Gunshot Residue UV.m,Propellant_10mg_191128-0002-r001.d
Propellant 10mg,Benito Gunshot Residue Positive.m,Propellant_10mg_191128-0004-r001.d
Propellant 100mg,Benito Gunshot Residue Positive + UV.m,Propellant_100mg_191128-0005-r001.d

# C18 Extend
Propellant 1ug,C18 Extend Gunshot Residue Positive + UV.m,Propellant_1ug_191128-0005-r001.d
Propellant 1mg,C18 Extend Gunshot Residue Positive + UV.m,Propellant_1mg_191128-0006-r001.d

Propellant 1ug (2),Benito Gunshot Residue Positive.m,Propellant 1ug (2)_191206-0002.d
Propellant 1mg (2),Benito Gunshot Residue Positive.m,Propellant 1mg (2)_191206-0003.d
Propellant 10mg (2),Benito Gunshot Residue Positive.m,Propellant 10mg (2)_191206-0004.d

# method permutations	(standard conditions GT 250)
Propellant 1mg (2) GT 200,Benito Gunshot Residue Positive.m,Propellant 1mg (2)_191206-0006.d
Propellant 1mg (2) GF 14,Benito Gunshot Residue Positive.m,Propellant 1mg (2)_191206-0007.d
Propellant 1mg (2) Neb 50,Benito Gunshot Residue Positive.m,Propellant 1mg (2)_191206-0008.d
Propellant 1mg (2) GF 14 Neb 35,Benito Gunshot Residue Positive.m,Propellant 1mg (2)_191206-0009.d
Propellant 10mg (2) GF 14 Neb 35,Benito Gunshot Residue Positive.m,Propellant 10mg (2)_191206-00010.d
Propellant 10mg (1) rerun,Benito Gunshot Residue Positive.m,Propellant 10mg (1)_191206-00011.d
Propellant 1ug (2) DG14 Neb 40,Maitre Gunshot Residue Positive 5ul.m,Propellant 1ug (2)_191211-0002.d
Propellant 1mg (2) DG14 Neb 40,Maitre Gunshot Residue Positive 5ul.m,Propellant 1mg (2)_191211-0003.d
Propellant 10mg (2) DG14 Neb 40,Maitre Gunshot Residue Positive 5ul.m,Propellant 10mg (2)_191211-0004.d
Propellant 1ug (2) Repeat DG14 Neb 40,Maitre Gunshot Residue Positive 5ul.m,Propellant 1ug (2)_repeat_191211-0004.d
Propellant 1mg (2) Repeat DG14 Neb 40,Maitre Gunshot Residue Positive 5ul.m,Propellant 1mg (2)_repeat_191211-0005.d

# Standard mixture
Propellant Standard 1ug/mL (1),Benito Gunshot Residue Positive.m,Propellant_Std_1ug_1_200124-0002.d
Propellant Standard 1ug/mL (2),Benito Gunshot Residue Positive.m,Propellant_Std_1ug_2_200124-0003.d
Propellant Standard 10ug/mL (1),Benito Gunshot Residue Positive.m,Propellant_Std_10ug_1_200124-0004.d
Propellant Standard 10ug/mL (2),Benito Gunshot Residue Positive.m,Propellant_Std_10ug_2_200124-0005.d
Propellant Standard 100ug/mL (1),Benito Gunshot Residue Positive.m,Propellant_Std_100ug_1_200124-0006.d
Propellant Standard 100ug/mL (1),Benito Gunshot Residue Positive.m,Propellant_Std_100ug_2_200124-0007.d
Propellant Standard 10ug/mL ms/ms (1),Benito Gunshot Residue Positive ms-ms.m,Propellant_Std_10ug_ms_ms_1_200124-0008.d
Propellant Standard 10ug/mL ms/ms (2),Benito Gunshot Residue Positive ms-ms.m,Propellant_Std_10ug_ms_ms_2_200124-0008.d
Propellant Standard 10ug/mL,Benito Gunshot Residue Positive.m,Propellant_Std_10ug_normal_200128-0002.d
Propellant Standard 10ug/mL DG 14,Benito Gunshot Residue Positive.m,Propellant_Std_10ug_DG14_200128-0003.d
Propellant Standard 10ug/mL GT 200,Benito Gunshot Residue Positive.m,Propellant_Std_10ug_GT200_200128-0004.d
Propellant Standard 10ug/mL NEB 35,Benito Gunshot Residue Positive.m,Propellant_Std_10ug_NEB35_200128-0005.d
Propellant Standard 0.1ug/mL (1),Benito Gunshot Residue Positive.m,Propellant_Std_0.1ug_1_200128-0006.d
Propellant Standard 0.1ug/mL (2),Benito Gunshot Residue Positive.m,Propellant_Std_0.1ug_2_200128-0007.d
Propellant Standard 0.1ug/mL (1),Benito Gunshot Residue Positive low flow.m,Propellant_Std_0.1ug_1_200129-0002.d
Propellant Standard 0.1ug/mL (2),Benito Gunshot Residue Positive low flow.m,Propellant_Std_0.1ug_2_200129-0003.d
Propellant Standard 1ug/mL (1),Benito Gunshot Residue Positive low flow.m,Propellant_Std_1ug_1_200129-0005.d
Propellant Standard 1ug/mL (2),Benito Gunshot Residue Positive low flow.m,Propellant_Std_1ug_2_200129-0007.d

Flask Cleaning Test,Benito Gunshot Residue Positive.m,Flask_Cleaning_Test_200129-0009.d

DPA 1ug/mL (1),Benito Gunshot Residue Positive low flow.m,DPA_1ug_ml_1_200206-0002.d
DPA 1ug/mL (2),Benito Gunshot Residue Positive low flow.m,DPA_1ug_ml_2_200206-0004.d
EC 1ug/mL (1),Benito Gunshot Residue Positive low flow.m,EC_1ug_ml_1_200206-0006.d
EC 1ug/mL (2),Benito Gunshot Residue Positive low flow.m,EC_1ug_ml_2_200206-0008.d

# New eluent
DPA 1ug/mL  - different method,Based on Cannabinoids in Urine.m,DPA_1ug_ml_diff_method_200206-0010.d
EC 1ug/mL  - different method,Based on Cannabinoids in Urine.m,EC_1ug_ml_diff_method_200206-0011.d
MeOH Blank - different method,Based on Cannabinoids in Urine.m,MeOH_Blank_diff_method_200218-0001.d
DPA 1ug/mL  - different method (1),Based on Cannabinoids in Urine.m,DPA_1ug_ml_diff_method_1_200218-0002.d
DPA 1ug/mL  - different method (2),Based on Cannabinoids in Urine.m,DPA_1ug_ml_diff_method_2_200218-0003.d
MeOH Blank - different method,Based on Cannabinoids in Urine.m,MeOH_Blank_diff_method_200218-0004.d
EC 1ug/mL  - different method (1),Based on Cannabinoids in Urine.m,EC_1ug_ml_diff_method_1_200218-0005.d
EC 1ug/mL  - different method (2),Based on Cannabinoids in Urine.m,EC_1ug_ml_diff_method_2_200218-0006.d
EC 1ug/mL  - different method (3),Based on Cannabinoids in Urine.m,EC_1ug_ml_diff_method_3_200218-0006.d

"""

# 3rd party
import _01_initial_propellant_std_charts
import _02_propellant_method_permutations_charts
import _03_benito_prop_method_permutations_charts
import _04_mixed_standard_charts
import _05_standards_low_flow_charts
import _06_new_method_charts

_01_initial_propellant_std_charts.make_charts()
_02_propellant_method_permutations_charts.make_charts()
_03_benito_prop_method_permutations_charts.make_charts()
_04_mixed_standard_charts.make_charts()
_05_standards_low_flow_charts.make_charts()
_06_new_method_charts.make_charts()
