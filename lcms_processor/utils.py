#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  utils.py
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
from numbers import Number

# 3rd party
from typing import Iterable

import numpy
import pandas
import sdjson

# this package
from .classes import Sample, SampleList


def set_display_options(desired_width=400, max_columns=15, max_rows=20):
	pandas.set_option('display.width', desired_width)
	numpy.set_printoptions(linewidth=desired_width)
	pandas.options.display.max_columns = max_columns
	pandas.options.display.max_rows = max_rows


def concatenate_csv(csv_files, csv_outfile):
	"""
	
	:param csv_files:
	:type csv_files: list of str or list of pathlib.Path
	
	:return: A :class:`pandas.DataFrame` containing the concatenated CSV data
	:rtype: pandas.DataFrame
	"""
	
	data_frames = []
	
	for csv_file in csv_files:
		
		# Read CSV file to data frame
		results_df = pandas.read_csv(csv_file, header=0, index_col=False, dtype=str)
		
		data_frames.append(results_df)
	
	concat_df = pandas.concat(data_frames)
	concat_df.to_csv(csv_outfile, index=False)
	
	return concat_df


def concatenate_json(json_files, output_file):
	"""

	:param json_files:
	:type json_files: list of str or list of pathlib.Path
	:param output_file:
	:type output_file:

	:return: a list of the :class:`Sample` objects in the concatenated json output
	:rtype:
	"""
	
	all_samples = SampleList()
	
	for json_file in json_files:
		with open(json_file) as fp:
			samples = sdjson.load(fp)

		for sample in samples:
			all_samples.append(Sample(**sample))
	
	with open(output_file, "w") as fp:
		sdjson.dump(all_samples, fp, indent=2)
	
	return all_samples


def load_sample_list(json_file):
	"""

	:param json_file:
	:type json_file: str or pathlib.Path
	:return:
	:rtype:
	"""

	all_samples = SampleList()

	with open(json_file) as fp:
		samples = sdjson.load(fp)

	for sample in samples:
		all_samples.append(Sample(**sample))

	return all_samples


def load_json_worklist(filename):
	worklist = pandas.read_json(filename)
	return worklist


neg_esi = "\u2212ESI"
pos_esi = "+ESI"
m_math_space = "\u205F"
sup_1 = "$^{1}$"  # "\u00B9"
sup_2 = "$^{2}$"  # "\u00B2"
sup_3 = "$^{3}$"  # "\u00B3"
sup_4 = "$^{4}$"  # "\u00B3"


def format_si_units(value, *units):
	return "".join([str(value), m_math_space, *units]).rstrip(m_math_space)


def make_conditions_label(
		sample_name, concentration,
		esi=1, dgt=None, dgf=None, neb=None,
		vol=format_si_units(5, 'µL'), **kwargs):

	if esi in {"1", "+"} or (isinstance(esi, Number) and esi > 0):
		conditions = [pos_esi]
	elif esi in {"-1", "-"} or (isinstance(esi, Number) and esi < 0):
		conditions = [neg_esi]
	else:
		conditions = []

	if dgt is not None:
		conditions.append(f"DGT: {dgt}")
	if dgf is not None:
		conditions.append(f"DGF: {dgf}")
	if neb is not None:
		conditions.append(f"NEB: {neb}")

	output_string = f"{sample_name} {concentration}"

	if vol is not None:
		output_string += f"\n{vol} injection"
	if conditions:
		output_string += f"\n({', '.join(conditions)})"
	for key, val in kwargs.items():
		output_string += f"\n{key}: {val}"
	return output_string


_0_1ug_l = format_si_units(0.1, 'µg', '/', 'L')
_1ug_l = format_si_units(1, 'µg', '/', 'L')
_10ug_l = format_si_units(10, 'µg', '/', 'L')
_100ug_l = format_si_units(100, 'µg', '/', 'L')
_1mg_l = format_si_units(1, 'mg', '/', 'L')
_10mg_l = format_si_units(10, 'mg', '/', 'L')

_1ul = format_si_units(1, 'µL')
_2ul = format_si_units(2, 'µL')


def warn_if_all_filtered(sample_list: SampleList, filtered_compounds: Iterable[str]) -> bool:
	identified_compounds = sample_list.get_compounds()

	warned = False

	for sample, areas in sample_list.get_areas_for_compounds(identified_compounds).items():
		if set({k for k, v in areas.items() if v is not None}) == set(filtered_compounds):
			sample_name = sample.replace('\n', '\\n')
			print(f"Attention: All compounds detected for '{sample_name}' were filtered out.")

			warned = True

	return warned

