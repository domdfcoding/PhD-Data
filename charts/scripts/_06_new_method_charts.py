#!/usr/bin/env python3
#
#  _06_new_method_charts.py
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
from mathematical.data_frames import set_display_options

# this package
from lcms_results_processor.chart_tools import savefig
from lcms_results_processor.charts import (
		ChartItem,
		plot_areas,
		sort_n_filter_by_filename,
		tex_page_landscape,
		update_all_labels_with_cal_range
		)
from lcms_results_processor.utils import _1ug_l, _10ug_l, sup_1, sup_2, sup_3, warn_if_all_filtered

ec_dpa_chart_items = [
		ChartItem.from_conditions(
				sort_order=10,
				filename="DPA_1ug_ml_diff_method_200206-0010.d",
				new_name=f"DPA{sup_1}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=20,
				filename="DPA_1ug_ml_diff_method_1_200218-0002.d",
				new_name=f"DPA{sup_2}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=30,
				filename="DPA_1ug_ml_diff_method_2_200218-0003.d",
				new_name=f"DPA{sup_3}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=40,
				filename="EC_1ug_ml_diff_method_200206-0011.d",
				new_name=f"EC{sup_1}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		# ChartItem.from_conditions(
		# 		sort_order=50,
		# 		filename="EC_1ug_ml_diff_method_1_200218-0005.d",  # This is actually DPA
		# 		new_name=f"EC{sup_2}",
		# 		concentration=_1ug_l, vol=None, esi=None,
		# 		),
		ChartItem.from_conditions(
				sort_order=60,
				filename="EC_1ug_ml_diff_method_2_200218-0006.d",
				new_name=f"EC{sup_2}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=70,
				filename="EC_1ug_ml_diff_method_3_200218-0006.d",
				new_name=f"EC{sup_3}",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		]

# ---

std_mix_chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_1_200221-0002.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				vol=None,
				esi=None,
				Repeat=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_2_200221-0004.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=20,
				vol=None,
				esi=None,
				Repeat=2,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_2_200221-0006.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				vol=None,
				esi=None,
				Repeat=3,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_10ug_diff_meth_1_200221-0011.d",
				new_name='',
				concentration=_10ug_l,
				sort_order=40,
				vol=None,
				esi=None,
				Repeat=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_10ug_diff_meth_2_200221-0012.d",
				new_name='',
				concentration=_10ug_l,
				sort_order=50,
				vol=None,
				esi=None,
				Repeat=2,
				),
		# ChartItem.from_conditions(
		# 		filename="Unique_10ug_ml_diff_method_1_200303-0005.d",
		# 		new_name='Alliant Unique',
		# 		concentration=_10ug_l,
		# 		sort_order=0,
		# 		vol=None, esi=None,
		# 		Repeat=1,
		# 		),
		# ChartItem.from_conditions(
		# 		filename="Unique_10ug_ml_diff_method_2_200303-0006.d",
		# 		new_name='Alliant Unique',
		# 		concentration=_10ug_l,
		# 		sort_order=0,
		# 		vol=None, esi=None,
		# 		Repeat=2,
		# 		),
		]


def make_charts():

	chdir()

	# Display options for numpy and pandas
	set_display_options()

	update_all_labels_with_cal_range(ec_dpa_chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	ec_dpa_target_samples = sort_n_filter_by_filename(all_samples, ec_dpa_chart_items)
	ec_dpa_identified_compounds = ec_dpa_target_samples.get_compounds()

	# Remove nitrobenzene
	ec_dpa_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(ec_dpa_target_samples, ["Nitrobenzene"])

	fig, ax = create_figure(tex_page_landscape, left=0.15, bottom=0.17, top=0.1)
	fig, ax = plot_areas(
		fig,
		ax,
		ec_dpa_target_samples,
		ec_dpa_identified_compounds,
		include_none=True,
		show_scores=True,
		legend_cols=4,
		show_score_in_legend=True,
		)
	# fig.suptitle("Peak Areas and Scores with Method 3", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")
	fig.text(0.739, 0.026, "¹²³", fontsize=9, zorder=20)
	fig.text(0.762, 0.026, "Repeat analyses", fontsize=9, zorder=20)

	savefig(fig, "charts/new_method_standards.png", dpi=600)
	savefig(fig, "charts/new_method_standards.svg")

	# update_all_labels_with_cal_range(std_mix_chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	std_mix_target_samples = sort_n_filter_by_filename(all_samples, std_mix_chart_items)
	std_mix_identified_compounds = std_mix_target_samples.get_compounds()

	# Remove nitrobenzene
	std_mix_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(std_mix_target_samples, ["Nitrobenzene"])

	# fig, ax = create_figure(tex_page_landscape, left=0.2, bottom=0.2)  # With mz range
	fig, ax = create_figure(tex_page_landscape, left=0.11, bottom=0.2, top=0.1)  # Without mz range
	fig, ax = plot_areas(
		fig,
		ax,
		std_mix_target_samples,
		std_mix_identified_compounds,
		include_none=True,
		show_scores=True,
		legend_cols=4,
		# mz_range=(100, 3200)
		show_score_in_legend=True,
		)
	# fig.suptitle("Peak Areas and Scores for Mixed Standard with Method 3", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration")  #  and Conditions
	fig.text(0.637, 0.026, "Calibration Range: $100-3200~m/z$", fontsize=9, zorder=20)

	savefig(fig, "charts/new_method_mixed_standard.png", dpi=600)
	savefig(fig, "charts/new_method_mixed_standard.svg")

	# plt.show()


if __name__ == "__main__":
	make_charts()
