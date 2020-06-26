#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  charts.py
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
from typing import Dict, List, Optional, Sequence, Tuple, Union

# 3rd party
import matplotlib.ticker as plticker
import numpy
from domdf_python_tools import pagesizes
# from domdf_python_tools.pagesizes import
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# this package
from lcms_processor.tkagg_pyplot import plt
from lcms_processor.utils import set_display_options
from .utils import format_si_units, make_conditions_label

# Display options for numpy and pandas
set_display_options()

A4_portrait = pagesizes.A4.inch
A5_portrait = pagesizes.A5.inch
A4_landscape = A4_portrait.landscape()
A5_landscape = A5_portrait.landscape()


def plot_area_and_score(samples, compound_name, include_none=False):
	"""
	Plot the peak area and score for the compound with the given name

	:param samples: A list of samples to plot on the chart
	:type samples: :class:`SampleList`
	:param compound_name:
	:type compound_name: str
	:param include_none: Whether samples where the compound was not found
		should be plotted. Default False
	:type include_none: bool, optional

	:return:
	:rtype:
	"""
	
	peak_areas, scores = samples.get_areas_and_scores(compound_name, include_none)
	
	fig, ax1 = plt.subplots()
	y_positions = numpy.arange(len(peak_areas))
	y_positions = [x * 1.5 for x in y_positions]
	
	bar_width = 0.5
	offset = bar_width / 2
	area_y_pos = [x + offset for x in y_positions]
	
	area_bar = ax1.barh(area_y_pos, list(peak_areas.values()), label="Peak Area", color="tab:orange", height=bar_width)
	ax1.set_xscale("log")
	ax1.set_xlabel("Log10(Peak Area)")
	
	ax2 = ax1.twiny()
	score_scatter = ax2.scatter(list(scores.values()), area_y_pos, label="Score", color="tab:blue")
	ax2.set_xlabel("Score")
	ax1.barh([], [], label="Score", color="tab:blue", height=bar_width)
	
	ax1.set_yticks(y_positions)
	ax1.set_yticklabels(list(peak_areas.keys()))
	fig.suptitle(f"Peak Area and Score for {compound_name}\n")
	
	fig.set_size_inches(A4_landscape)
	plt.tight_layout()
	plt.subplots_adjust(top=0.9)
	ax1.legend()
	
	return fig, ax1, ax2


def plot_areas(samples, compound_names, include_none=False, show_scores=False, legend_cols=6) -> Tuple[Figure, Axes]:
	"""
	Plot the peak area and score for the compound with the given name

	:param samples: A list of samples to plot on the chart
	:type samples: SampleList
	:param compound_names: A list of compounds to plot
	:type compound_names: list of str
	:param include_none: Whether samples where the compound was not found
		should be plotted. Default ``False``
	:type include_none: bool, optional
	:param show_scores: Whether the scores should be shown on the chart. Default ``False``
	:type show_scores: bool, optional
	:param legend_cols:
	:type legend_cols:

	:return:
	:rtype:
	"""

	areas_dict, scores_dict = samples.get_areas_and_scores_for_compounds(compound_names, include_none)

	fig, ax = plt.subplots(ncols=1)

	if show_scores:
		ax2 = ax.twiny()

	y_positions = numpy.arange(len(areas_dict))
	y_positions = [x * 1.5 for x in y_positions]
	
	# n_samples = areas_dict.n_samples
	n_compounds = len(compound_names)
	
	bar_width = 1.5 / (n_compounds + 1)

	# TODO: bar_spacing = bar_width / (n_samples + 1)
	
	bar_offsets = list(numpy.arange(
			(0 - ((bar_width / 2) * (n_compounds - 1))),
			(0 + ((bar_width / 2) * n_compounds)),
			bar_width
			))[::-1]  # Reverse order

	sample_names = areas_dict.sample_names

	divider_positions = set()

	for cpd_idx, compound_name in enumerate(compound_names):
		compound_y_positions = []
		compound_areas = areas_dict.get_compound_areas(compound_name)
		compound_scores = scores_dict.get_compound_scores(compound_name)

		for sample_idx, sample_name in enumerate(sample_names):
			compound_y_positions.append(y_positions[sample_idx] + bar_offsets[cpd_idx])
			divider_positions.add((y_positions[sample_idx] + bar_offsets)[0] + bar_width)
			divider_positions.add((y_positions[sample_idx] + bar_offsets)[-1] - bar_width)

		ax.barh(compound_y_positions, compound_areas, label=compound_name, height=bar_width, edgecolor="black", linewidth=0.25)

		if show_scores:
			score_scatter = ax2.scatter([x if x else None for x in compound_scores], compound_y_positions, color="black", s=bar_width*50)
			# for area, ypos in zip(compound_areas, compound_y_positions):
			# 	score_text = ax.text(area, ypos, "Score", va='center')

	for pos in divider_positions:
		ax.axhline(pos, color="black", linewidth=0.5, xmin=-0.01, clip_on=False)

	loc = plticker.MultipleLocator(base=bar_width)
	ax.yaxis.set_minor_locator(loc)
	ax.grid(which='minor', axis='y', linestyle='-')
	ax.set_ylim(bottom=min(divider_positions), top=max(divider_positions))
	ax.set_yticks(y_positions)
	ax.set_xscale("log")
	ax.set_xlabel("Log$_{10}$(Peak Area)", fontsize=11, labelpad=0)
	ax.set_yticklabels(sample_names)

	if show_scores:
		min_score = 40
		ax2.set_xlim(left=min_score, right=100)  # Compounds with scores below 50 were excluded by MassHunter
		ax2.grid(False)
		ax2.set_xlabel("Score", fontsize=11, ha="center")
		ax2.set_xticks(numpy.arange(min_score, 110, 10))
		# ax2.set_xticks([0, 10, 20, 30, 40, 60, 70, 80, 90, 100])
		ax.scatter([], [], label="Score", color="black")
		fig.suptitle("Peak Areas and Scores", fontsize=14, y=0.985)
	else:
		fig.suptitle("Peak Areas", fontsize=14, y=0.985)

	fig.set_size_inches(A4_landscape)
	fig.legend(loc="lower center", ncol=legend_cols)
	fig.tight_layout()

	if show_scores:
		fig.subplots_adjust(bottom=0.11, top=0.90)
	else:
		fig.subplots_adjust(bottom=0.11, top=0.95)

	return fig, ax


class ChartItem:
	def __init__(
			self, new_name, filename, sort_order, current_name=None):

		self.new_name = new_name
		self.filename = filename
		self.sort_order = sort_order
		self.current_name = current_name

	__slots__ = ["new_name", "filename", "sort_order", "current_name"]

	@classmethod
	def from_conditions(
			cls, new_name, filename, sort_order, current_name=None, *,
			concentration, esi=1, dgt=None, dgf=None, neb=None,
			vol=format_si_units(5, 'µL'), **kwargs):

		new_name = make_conditions_label(
				new_name,
				concentration=concentration,
				esi=esi, dgt=dgt, dgf=dgf, neb=neb, vol=vol, **kwargs
				)

		return cls(new_name, filename, sort_order, current_name)

	def rename(self, new_name):
		return self.__class__(
				new_name=new_name,
				filename=self.filename,
				sort_order=self.sort_order,
				current_name=self.current_name,
				)


def sort_n_filter_by_filename(all_samples, chart_items):
	# Filter samples, reorder and rename
	target_samples = all_samples.filter([s.filename for s in chart_items], key="filename")

	ug_sample_order = {s.filename: s.sort_order for s in chart_items}
	target_samples.reorder_samples(ug_sample_order, key="filename")

	sample_labels = {s.filename: s.new_name for s in chart_items}
	target_samples.rename_samples(sample_labels, key="filename")

	return target_samples


raw_mz_type = Union[str, float]


def update_label_with_cal_range(
		item: ChartItem,
		mass_calibration_ranges: Dict[str, Sequence[raw_mz_type]],
		):
	# print(item.filename)
	# print(item.new_name)
	# print(mass_calibration_ranges[item.filename])

	item.new_name += "\nMZ Range: {}-{}".format(*mass_calibration_ranges[item.filename])

	return item


def cast_cal_range(cal_range: Sequence[raw_mz_type]) -> Tuple[float, float]:
	min_val, max_val = cal_range
	return float(min_val), float(max_val)


def update_all_labels_with_cal_range(
		item_list: List[ChartItem],
		mass_calibration_ranges: Dict[str, Sequence[raw_mz_type]],
		default_cal_range: Optional[Sequence[raw_mz_type]],
		):

	if default_cal_range:

		default_cal_range = cast_cal_range(default_cal_range)

		if not any(
				cast_cal_range(mass_calibration_ranges[item.filename]) != default_cal_range
				for item in item_list
				):

			return

	for item in item_list:
		update_label_with_cal_range(item, mass_calibration_ranges)
