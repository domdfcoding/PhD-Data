#!/usr/bin/env python3
#
#  _02_propellant_method_permutations_charts.py
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
from domplotlib import create_figure
from domplotlib.styles.domdf import plt
from mathematical.data_frames import set_display_options

# this package
from lcms_results_processor.chart_tools import savefig
from lcms_results_processor.charts import (
		ChartItem,
		plot_areas,
		plot_retention_times,
		sort_n_filter_by_filename,
		tex_page,
		update_all_labels_with_cal_range
		)
from lcms_results_processor.utils import _1ug_l, warn_if_all_filtered

# Filter samples, reorder and rename
ug_chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1ug_+ve_5ul_191121-0009-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				esi=None,
				vol=None,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_gas_200_191121-0012-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=20,
				esi=None,
				vol=None,
				dgt=200,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_gas_280_191121-0014-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				esi=None,
				vol=None,
				dgt=280,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_drying_14_191121-0016-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=40,
				esi=None,
				vol=None,
				dgf=14,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_drying_16_191121-0018-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=50,
				esi=None,
				vol=None,
				dgf=16,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_drying_18_191121-0020-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=60,
				esi=None,
				vol=None,
				dgf=18,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_nebul_40_191121-0022-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=70,
				esi=None,
				vol=None,
				neb=40,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_nebul_50_191121-0024-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=80,
				esi=None,
				vol=None,
				neb=50,
				),
		# TODO: missing datafile
		# ChartItem.from_conditions(
		# 		filename="Propellant_1ug_nebul_60_191121-0026-r001.d",
		# 		new_name="",
		# 		concentration=_1ug_l,
		# 		sort_order=90,
		# 		esi=None,
		# 		vol=None,
		# 		neb=60,
		# 		),
		]

mg_chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1mg_+ve_5ul_191121-0008-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				esi=None,
				vol=None,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_gas_200_191121-0011-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=20,
				esi=None,
				vol=None,
				dgt=200,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_gas_280_191121-0013-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				esi=None,
				vol=None,
				dgt=280,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_drying_14_191121-0015-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=40,
				esi=None,
				vol=None,
				dgf=14,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_drying_16_191121-0017-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=50,
				esi=None,
				vol=None,
				dgf=16,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_drying_18_191121-0019-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=60,
				esi=None,
				vol=None,
				dgf=18,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_nebul_40_191121-0021-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=70,
				esi=None,
				vol=None,
				neb=40,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_nebul_50_191121-0023-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=80,
				esi=None,
				vol=None,
				neb=50,
				),

		# TODO: have datafile but no results
		ChartItem.from_conditions(
				filename="Propellant_1mg_nebul_60_191121-0025-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=90,
				esi=None,
				vol=None,
				neb=60,
				),
		]


def make_charts():
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	update_all_labels_with_cal_range(ug_chart_items, mass_calibration_ranges, ["50", "1700"])
	update_all_labels_with_cal_range(mg_chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	ug_target_samples = sort_n_filter_by_filename(all_samples, ug_chart_items)
	ug_identified_compounds = ug_target_samples.get_compounds()

	# Filter samples, reorder and rename
	mg_target_samples = sort_n_filter_by_filename(all_samples, mg_chart_items)
	mg_identified_compounds = mg_target_samples.get_compounds()

	all_identified_compounds = sorted({*ug_identified_compounds, *mg_identified_compounds})

	# Remove nitrobenzene
	all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(ug_target_samples, ["Nitrobenzene"])
	warn_if_all_filtered(mg_target_samples, ["Nitrobenzene"])

	fig, ax = create_figure(tex_page, left=0.155, top=0.09)

	fig, ax = plot_areas(fig, ax, ug_target_samples, all_identified_compounds, include_none=True, show_scores=True, legend_cols=3)
	fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)

	# fig.set_size_inches(A4_portrait)
	# fig.tight_layout()
	# fig.subplots_adjust(bottom=0.13, top=0.91)

	savefig(fig, "charts/propellant_5ul_injection_micro.png", dpi=300)
	savefig(fig, "charts/propellant_5ul_injection_micro.svg")

	fig, ax = create_figure(tex_page, left=0.155, top=0.09)

	fig, ax = plot_areas(fig, ax, mg_target_samples, all_identified_compounds, include_none=True, show_scores=True, legend_cols=3)
	fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)

	# fig.set_size_inches(A4_portrait)
	# fig.tight_layout()
	# fig.subplots_adjust(bottom=0.13, top=0.91)

	savefig(fig, "charts/propellant_5ul_injection_milli.png", dpi=300)
	savefig(fig, "charts/propellant_5ul_injection_milli.svg")

	# plt.show()

	fig, ax = create_figure(tex_page, left=0.15, bottom=0.17)

	fig, ax = plot_retention_times(fig, ax, ug_target_samples, ug_target_samples.get_compounds(), legend_cols=3)
	ax.set_ylabel("Concentration and Conditions")

	fig, ax = create_figure(tex_page, left=0.15, bottom=0.17)
	fig, ax = plot_retention_times(fig, ax, mg_target_samples, mg_target_samples.get_compounds(), legend_cols=3)
	ax.set_ylabel("Concentration and Conditions")

	plt.show()


if __name__ == "__main__":
	make_charts()
