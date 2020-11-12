#!/usr/bin/env python3
#
#  _01_initial_propellant_std_charts.py
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
from charts_shared import all_samples, chdir, mass_calibration_ranges
from mathematical.data_frames import set_display_options

# this package
from lcms_results_processor.chart_tools import create_figure, plt, savefig
from lcms_results_processor.charts import (
		ChartItem,
		plot_areas,
		plot_retention_times,
		sort_n_filter_by_filename,
		tex_page,
		tex_page_landscape,
		update_all_labels_with_cal_range
		)
from lcms_results_processor.utils import _1mg_l, _1ug_l, _2ul, warn_if_all_filtered

# TODO injection volume: 1ug I think
chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1ug_+ve_191121-0003-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				vol=_2ul,
				esi=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_+ve_191121-0002-r001.d",
				new_name='',
				concentration=_1mg_l,
				sort_order=20,
				vol=_2ul,
				esi=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_-ve_191121-0006-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				vol=_2ul,
				esi=-1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_-ve_191121-0005-r001.d",
				new_name='',
				concentration=_1mg_l,
				sort_order=40,
				vol=_2ul,
				esi=-1,
				),
		]


def make_charts():
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	update_all_labels_with_cal_range(chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	target_samples = sort_n_filter_by_filename(all_samples, chart_items)
	all_identified_compounds = target_samples.get_compounds()

	# Remove nitrobenzene
	# all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	fig, ax = create_figure(tex_page_landscape, left=0.12)
	fig, ax = plot_areas(fig, ax, target_samples, all_identified_compounds, include_none=True, show_scores=True)
	fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	savefig(fig, "charts/first_4_propellant_pos_and_neg.png", dpi=300)
	savefig(fig, "charts/first_4_propellant_pos_and_neg.svg")
	# plt.show()

	# worklist = load_json_worklist("data/worklist.json")
	# print(worklist)
	#
	# print(worklist.loc["Methanol Blank"])
	# print(worklist.loc[worklist["Sample Name"] == "Methanol Blank"])
	# print(worklist.loc[worklist["Sample Name"].str.startswith("Methanol")])

	fig, ax = create_figure(tex_page, left=0.15, bottom=0.17)

	fig, ax = plot_retention_times(fig, ax, target_samples, target_samples.get_compounds(), legend_cols=3)
	fig.suptitle("Retention Times for Alliant Unique Propellant", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")

	plt.show()


if __name__ == "__main__":
	make_charts()
