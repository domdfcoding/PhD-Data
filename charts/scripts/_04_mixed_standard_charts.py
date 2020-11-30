#!/usr/bin/env python3
#
#  _04_mixed_standard_charts.py
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
from charts_shared import all_samples, chdir
from domplotlib import create_figure
from mathematical.data_frames import set_display_options

# this package
from lcms_results_processor.chart_tools import savefig
from lcms_results_processor.charts import (
		ChartItem,
		plot_areas,
		plot_retention_times,
		sort_n_filter_by_filename,
		tex_page,
		tex_page_landscape
		)
from lcms_results_processor.utils import _0_1ug_l, _1ug_l, _10ug_l, _100ug_l, warn_if_all_filtered

chart_items = [
		ChartItem.from_conditions(
				current_name=None,
				sort_order=2,
				new_name='',
				vol=None,
				esi=None,
				Repeat=1,
				filename="Propellant_Std_0.1ug_1_200128-0006.d",
				concentration=_0_1ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=3,
				new_name='',
				vol=None,
				esi=None,
				Repeat=2,
				filename="Propellant_Std_0.1ug_2_200128-0007.d",
				concentration=_0_1ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=10,
				new_name='',
				vol=None,
				esi=None,
				Repeat=1,
				filename="Propellant_Std_1ug_1_200124-0002.d",
				concentration=_1ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=20,
				new_name='',
				vol=None,
				esi=None,
				Repeat=2,
				filename="Propellant_Std_1ug_2_200124-0003.d",
				concentration=_1ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=30,
				new_name='',
				vol=None,
				esi=None,
				Repeat=1,
				filename="Propellant_Std_10ug_1_200124-0004.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=40,
				new_name='',
				vol=None,
				esi=None,
				Repeat=2,
				filename="Propellant_Std_10ug_2_200124-0005.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=50,
				new_name='',
				vol=None,
				esi=None,
				Repeat=3,
				filename="Propellant_Std_10ug_normal_200128-0002.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=60,
				new_name='',
				dgf=14,
				vol=None,
				esi=None,
				filename="Propellant_Std_10ug_DG14_200128-0003.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=70,
				new_name='',
				dgt=200,
				vol=None,
				esi=None,
				filename="Propellant_Std_10ug_GT200_200128-0004.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=80,
				new_name='',
				neb=35,
				vol=None,
				esi=None,
				filename="Propellant_Std_10ug_NEB35_200128-0005.d",
				concentration=_10ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=90,
				new_name='',
				vol=None,
				esi=None,
				Repeat=1,
				filename="Propellant_Std_100ug_1_200124-0006.d",
				concentration=_100ug_l,
				),
		ChartItem.from_conditions(
				current_name=None,
				sort_order=100,
				new_name='',
				vol=None,
				esi=None,
				Repeat=2,
				filename="Propellant_Std_100ug_2_200124-0007.d",
				concentration=_100ug_l,
				),
		# ChartItem.from_conditions(
		# 		current_name="None, sort_order=100,
		# 		new_name=make_conditions_label(f"{sup_1} MS/MS", _10ug_l, vol=None, esi=None),
		# 		# TODO: MSMS
		# 		filename="Propellant_Std_10ug_ms_ms_1_200124-0008.d",
		#		concentration=_10ug_l,
		# 		),

		# No compounds detected in this sample
		# ChartItem.from_conditions(
		# 		current_name="None, sort_order=110,
		# 		new_name=make_conditions_label(f"{sup_2} MS/MS", _10ug_l, vol=None, esi=None),
		# 		# TODO: MSMS
		# 		filename="Propellant_Std_10ug_ms_ms_2_200124-0008.d	(ms/ms)",
		#		concentration=_10ug_l,
		# 		),
		]


def make_charts():
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	# update_all_labels_with_cal_range(chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	target_samples = sort_n_filter_by_filename(all_samples, chart_items)
	all_identified_compounds = target_samples.get_compounds()

	# Remove nitrobenzene
	all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	# fig, ax = create_figure(tex_page_landscape, left=0.2)  # With m/z Range indicated
	fig, ax = create_figure(tex_page_landscape, left=0.125, top=0.09)  # Without m/z Range indicated
	fig, ax = plot_areas(fig, ax, target_samples, all_identified_compounds, show_scores=True, mz_range=(100, 3200))  # , include_none=True, legend_cols=3)
	# fig.suptitle("Peak Areas and Scores for Mixed Standard", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")

	savefig(fig, "charts/mixed_standards.png", dpi=600)
	savefig(fig, "charts/mixed_standards.svg")

	# plt.show()

	fig, ax = create_figure(tex_page, left=0.15, bottom=0.17)

	fig, ax = plot_retention_times(fig, ax, target_samples, target_samples.get_compounds(), legend_cols=3)
	ax.set_ylabel("Concentration and Conditions")

	# plt.show()


if __name__ == "__main__":
	make_charts()
