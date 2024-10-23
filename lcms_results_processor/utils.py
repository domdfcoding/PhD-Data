#!/usr/bin/env python3
#
#  charts.py
"""

"""
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
from numbers import Number
from typing import Iterable, List, Optional

# 3rd party
import pandas  # type: ignore[import]
import sdjson
from chemistry_tools.units import format_si_units, m_math_space
from domdf_python_tools.typing import PathLike
from mh_utils.csv_parser import Sample, SampleList

__all__ = ["load_json_worklist", "make_conditions_label", "warn_if_all_filtered", "concatenate_json"]


def load_json_worklist(filename: PathLike) -> pandas.DataFrame:
	"""
	Load a worklist from a JSON file as a pandas DataFrame.

	:param filename:
	"""

	worklist = pandas.read_json(filename)
	return worklist


def make_conditions_label(
		sample_name: str,
		concentration: float,
		esi: int = 1,
		dgt: Optional[float] = None,
		dgf: Optional[float] = None,
		neb: Optional[float] = None,
		vol: str = format_si_units(5, "µL"),
		**kwargs,
		) -> str:
	r"""

	:param sample_name:
	:param concentration:
	:param esi:
	:param dgt:
	:param dgf:
	:param neb:
	:param vol:
	:param \*\*kwargs: Additional keyword values to add to the label.
	"""

	if esi in {'1', '+'} or (isinstance(esi, Number) and esi > 0):
		conditions = [pos_esi]
	elif esi in {"-1", '-'} or (isinstance(esi, Number) and esi < 0):
		conditions = [neg_esi]
	else:
		conditions = []

	if dgt is not None:
		conditions.append(f"DGT: {dgt}{m_math_space}℃")
	if dgf is not None:
		conditions.append(f"DGF: {dgf}{m_math_space}L/min")
	if neb is not None:
		conditions.append(f"NEB: {neb}{m_math_space}psig")

	output_string = f"{sample_name} {concentration}"

	if vol is not None:
		output_string += f"\n{vol} injection"
	if conditions:
		# output_string += f"\n({', '.join(conditions)})"
		output_string += f"\n".join(('', *conditions))
	for key, val in kwargs.items():
		output_string += f"\n{key}: {val}"

	return output_string


neg_esi: str = "−ESI"
pos_esi: str = "+ESI"
sup_1: str = "$^{1}$"  # "\u00B9"
sup_2: str = "$^{2}$"  # "\u00B2"
sup_3: str = "$^{3}$"  # "\u00B3"
sup_4: str = "$^{4}$"  # "\u00B3"

_0_1ug_l: str = format_si_units(0.1, "µg", '/', 'L')
_1ug_l: str = format_si_units(1, "µg", '/', 'L')
_10ug_l: str = format_si_units(10, "µg", '/', 'L')
_100ug_l: str = format_si_units(100, "µg", '/', 'L')
_1mg_l: str = format_si_units(1, "mg", '/', 'L')
_10mg_l: str = format_si_units(10, "mg", '/', 'L')

_1ul: str = format_si_units(1, "µL")
_2ul: str = format_si_units(2, "µL")


def warn_if_all_filtered(sample_list: SampleList, filtered_compounds: Iterable[str]) -> List[str]:
	"""
	Emits a warning if all compounds have been filtered out for a sample.

	:param sample_list:
	:param filtered_compounds:

	:return: A list of samples for which all compounds were filtered out.
	"""

	identified_compounds = sample_list.get_compounds()

	warned = []

	for sample, areas in sample_list.get_areas_for_compounds(identified_compounds).items():
		if {k for k, v in areas.items() if v is not None} == set(filtered_compounds):
			sample_name = sample.replace('\n', '\\n')
			print(f"Attention: All compounds detected for '{sample_name}' were filtered out.")
			warned.append(sample_name)

	return warned


def concatenate_json(*files: PathLike, outfile: Optional[PathLike] = None) -> SampleList:
	r"""
	Concatenate multiple JSON files together and return a list of :class:`Sample`
	objects in the concatenated json output.

	:param \*files: The files to concatenate.
	:param outfile: The file to save the output as. If :py:obj:`None` no file will be saved.

	.. versionadded:: 0.2.0
	"""  # noqa: D400

	all_samples = SampleList()

	for json_file in files:
		with open(json_file, encoding="UTF-8") as fp:
			samples = sdjson.load(fp)

		for sample in samples:
			all_samples.append(Sample(**sample))

	if outfile is not None:
		with open(outfile, 'w', encoding="UTF-8") as fp:
			sdjson.dump(all_samples, fp, indent=2)

	return all_samples
