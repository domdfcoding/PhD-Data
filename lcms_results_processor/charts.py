#!/usr/bin/env python3
#
#  charts.py
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
import itertools
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

# 3rd party
import matplotlib.ticker as plticker
import numpy
import pandas
from domdf_python_tools import pagesizes
from domdf_python_tools.iterative import chunks
from domdf_python_tools.typing import PathLike
from domplotlib.styles.domdf import plt
from mathematical.data_frames import set_display_options
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from mh_utils.csv_parser import SampleList

# this package
from lcms_results_processor.utils import format_si_units, make_conditions_label

__all__ = [
		"plot_area_and_score",
		"plot_areas",
		"plot_retention_times",
		"make_rt_dataframe",
		"ChartItem",
		"sort_n_filter_by_filename",
		"update_label_with_cal_range",
		"cast_cal_range",
		"legend",
		"update_all_labels_with_cal_range"
		]

# Display options for numpy and pandas
set_display_options()

A4_portrait = pagesizes.A4.inch
A5_portrait = pagesizes.A5.inch
A4_landscape = A4_portrait.landscape()
A5_landscape = A5_portrait.landscape()
tex_page = pagesizes.PageSize(426, 674 * 0.9).inch
tex_page_landscape = pagesizes.PageSize(426 * 0.9, 674).inch.landscape()


def plot_area_and_score(samples: SampleList, compound_name: str, include_none: bool = False):
	"""
	Plot the peak area and score for the compound with the given name

	:param samples: A list of samples to plot on the chart
	:param compound_name:
	:param include_none: Whether samples where the compound was not found
		should be plotted.
	"""

	peak_areas, scores = samples.get_areas_and_scores(compound_name, include_none)

	fig, ax1 = plt.subplots()
	y_positions = numpy.arange(len(peak_areas))
	y_positions = [x * 1.5 for x in y_positions]

	bar_width = 0.5
	offset = bar_width / 2
	area_y_pos = [x + offset for x in y_positions]

	area_bar = ax1.barh(
			area_y_pos,
			list(peak_areas.values()),
			label="Peak Area",
			color="tab:orange",
			height=bar_width,
			)
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


def plot_areas(
		fig: Figure,
		ax: Axes,
		samples: SampleList,
		compound_names: List[str],
		include_none: bool = False,
		show_scores: bool = False,
		legend_cols: int = 6,
		mz_range=None,
		show_score_in_legend: bool = False,
		) -> Tuple[Figure, Axes]:
	"""
	Plot the peak area and score for the compounds with the given names

	:param fig:
	:param ax:
	:param samples: A list of samples to plot on the chart
	:param compound_names: A list of compounds to plot
	:param include_none: Whether samples where the compound was not found should be plotted.
	:param show_scores: Whether the scores should be shown on the chart.
	:param legend_cols:
	:param mz_range:
	:param show_score_in_legend:
	"""

	areas_dict, scores_dict = samples.get_areas_and_scores_for_compounds(compound_names, include_none)

	if show_scores:
		ax2 = ax.twiny()

	y_positions = numpy.arange(len(areas_dict))
	y_positions = [x * 1.5 for x in y_positions]

	# n_samples = areas_dict.n_samples
	n_compounds = len(compound_names)

	bar_width = 1.5 / (n_compounds + 1)

	# TODO: bar_spacing = bar_width / (n_samples + 1)

	bar_offsets = list(
			numpy.arange((0 - ((bar_width / 2) * (n_compounds - 1))), (0 + ((bar_width / 2) * n_compounds)),
							bar_width)
			)[::-1]  # Reverse order

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

		ax.barh(
				compound_y_positions,
				compound_areas,
				label=compound_name,
				height=bar_width,
				edgecolor="black",
				linewidth=0.25
				)

		if show_scores:
			score_scatter = ax2.scatter([x if x else None for x in compound_scores],
										compound_y_positions,
										color=["black" if s >= 75 else "orange" for s in compound_scores],
										s=bar_width * 50)
		# for area, ypos in zip(compound_areas, compound_y_positions):
		# 	score_text = ax.text(area, ypos, "Score", va='center')

	for pos in divider_positions:
		ax.axhline(pos, color="black", linewidth=0.5, xmin=-0.01, clip_on=False)

	loc = plticker.MultipleLocator(base=bar_width)
	ax.yaxis.set_minor_locator(loc)
	ax.grid(which="minor", axis='y', linestyle='-')
	ax.set_ylim(bottom=min(divider_positions), top=max(divider_positions))
	ax.set_yticks(y_positions)
	ax.set_xscale("log")
	ax.set_xlabel("Log$_{10}$(Peak Area)", labelpad=0)
	ax.set_yticklabels(sample_names)

	if show_scores:
		min_score = 40
		ax2.set_xlim(left=min_score, right=100)  # Compounds with scores below 50 were excluded by MassHunter
		ax2.grid(False)
		ax2.set_xlabel("Score", ha="center")
		ax2.set_xticks(numpy.arange(min_score, 110, 10))
		# ax2.set_xticks([0, 10, 20, 30, 40, 60, 70, 80, 90, 100])
		ax.scatter([], [], label="Score", color="black")

	legend(fig, loc="lower center", ncol=legend_cols, mz_range=mz_range, show_score=show_score_in_legend)

	return fig, ax


def plot_retention_times(
		fig: Figure,
		ax: Axes,
		samples: SampleList,
		compound_names: List[str],
		include_none: bool = False,
		legend_cols: int = 6,
		mz_range=None,
		) -> Tuple[Figure, Axes]:
	"""
	Plot the retention times for the compounds with the given names

	:param fig:
	:param ax:
	:param samples: A list of samples to plot on the chart
	:param compound_names: A list of compounds to plot
	:param include_none: Whether samples where the compound was not found should be plotted.
	:param legend_cols:
	:param mz_range:
	"""

	rt_data = make_rt_dataframe(compound_names, samples, include_none=include_none)

	label_strings = numpy.array(rt_data.index, dtype=str)
	label_indices = numpy.arange(len(label_strings))

	divider_positions = set()
	for idx in label_indices:
		divider_positions.add(idx - 0.5)
		divider_positions.add(idx + 0.5)

	for compound, times in rt_data.iteritems():
		rt_values = numpy.array(times, dtype=numpy.float64)
		mask = numpy.isfinite(rt_values)
		ax.plot(
				rt_values[mask],
				label_indices[mask],
				linestyle="--",
				marker='o',
				label=compound,
				linewidth=1,
				)

	ax.set_ylim(bottom=min(divider_positions), top=max(divider_positions))
	ax.set_xlabel("Retention Time (mins)", labelpad=0)
	ax.set_yticks(label_indices)
	ax.set_yticklabels(label_strings)
	ax.set_xlim(left=0)

	legend(fig, loc="lower center", ncol=legend_cols, mz_range=mz_range, show_score=False)

	return fig, ax


def make_rt_dataframe(
		compound_names: List[str],
		samples: SampleList,
		include_none: bool = False,
		) -> pandas.DataFrame:
	"""

	:param compound_names:
	:param samples:
	:param include_none:
	"""

	rt_data = pandas.DataFrame(columns=compound_names, index=[x.sample_name for x in samples])

	for compound in compound_names:
		rt_dict = samples.get_retention_times(compound, include_none=True)
		rt_data[compound] = rt_data.index.map(rt_dict)

	if not include_none:
		rt_data.dropna(axis=0, how="all", inplace=True)
		rt_data.dropna(axis=1, how="any", inplace=True, thresh=2)

	return rt_data


class ChartItem:
	"""

	:param new_name:
	:param filename:
	:param sort_order:
	:param current_name:
	"""

	def __init__(self, new_name: str, filename: PathLike, sort_order, current_name: Optional[str] = None):
		self.new_name: str = new_name
		self.filename: PathLike = filename
		self.sort_order = sort_order
		self.current_name: Optional[str] = current_name

	__slots__ = ("new_name", "filename", "sort_order", "current_name")

	@classmethod
	def from_conditions(
			cls,
			new_name: str,
			filename: PathLike,
			sort_order,
			current_name: Optional[str] = None,
			*,
			concentration,
			esi: Optional[int] = 1,
			dgt=None,
			dgf=None,
			neb=None,
			vol=format_si_units(5, "µL"),
			**kwargs
			) -> "ChartItem":
		"""
		Construct a :class:`~.ChartItem`.

		:param new_name:
		:param filename:
		:param sort_order:
		:param current_name:
		:param concentration:
		:param esi:
		:param dgt:
		:param dgf:
		:param neb:
		:param vol:
		:param kwargs:
		"""

		new_name = make_conditions_label(
				new_name,
				concentration=concentration,
				esi=esi,
				dgt=dgt,
				dgf=dgf,
				neb=neb,
				vol=vol,
				**kwargs,
				)

		return cls(new_name, filename, sort_order, current_name)

	def rename(self, new_name: str) -> "ChartItem":
		"""
		Create a new :class:`~.ChartItem` with a different name.

		:param new_name:
		"""

		return self.__class__(
				new_name=new_name,
				filename=self.filename,
				sort_order=self.sort_order,
				current_name=self.current_name,
				)


def sort_n_filter_by_filename(all_samples: SampleList, chart_items: Iterable[ChartItem]) -> SampleList:
	"""

	:param all_samples:
	:param chart_items:
	"""

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
	"""

	:param item:
	:param mass_calibration_ranges:
	"""

	item.new_name += "\n${}-{}~m/z$".format(*mass_calibration_ranges[item.filename])
	return item


def cast_cal_range(cal_range: Sequence[raw_mz_type]) -> Tuple[float, float]:
	"""

	:param cal_range:
	"""

	min_val, max_val = cal_range
	return float(min_val), float(max_val)


def legend(
		fig: Figure,
		*,
		ncol: int = 1,
		mz_range: Optional[Tuple[int, int]] = None,
		show_score: bool = False,
		**kwargs,
		):
	"""
	Place a legend on the figure.
	"""

	handles, labels = fig.axes[0].get_legend_handles_labels()

	if show_score:
		if isinstance(handles[0], PathCollection):
			handles = [*handles[1:], handles[0]]
			labels = [*labels[1:], labels[0]]
	else:
		if isinstance(handles[0], PathCollection):
			handles = [*handles[1:]]
			labels = [*labels[1:]]

	# Rearrange legend items to read right to left rather than top to bottom.
	handles = list(filter(None, itertools.chain.from_iterable(itertools.zip_longest(*chunks(handles, ncol)))))
	labels = list(filter(None, itertools.chain.from_iterable(itertools.zip_longest(*chunks(labels, ncol)))))

	if mz_range:
		rect = Rectangle((0, 0), 1, 1, fc='w', fill=False, edgecolor="none", linewidth=0)
		handles.append(rect)
		labels.append("Calibration Range: ${}-{}~m/z$ ".format(*mz_range))

	return fig.legend(handles, labels, ncol=ncol, **kwargs)


def update_all_labels_with_cal_range(
		item_list: List[ChartItem],
		mass_calibration_ranges: Dict[str, Sequence[raw_mz_type]],
		default_cal_range: Optional[Sequence[raw_mz_type]],
		) -> None:
	"""

	:param item_list:
	:param mass_calibration_ranges:
	:param default_cal_range:
	"""

	if default_cal_range:

		default_cal_range = cast_cal_range(default_cal_range)

		if not any(
				cast_cal_range(mass_calibration_ranges[item.filename]) != default_cal_range for item in item_list
				):
			return

	for item in item_list:
		update_label_with_cal_range(item, mass_calibration_ranges)
