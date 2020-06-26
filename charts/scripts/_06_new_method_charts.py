#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  mixed_standard_charts.py.py
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

# this package
from lcms_processor.charts import (
	A4_portrait,
	ChartItem,
	plot_areas,
	sort_n_filter_by_filename,
	update_all_labels_with_cal_range
)
from lcms_processor.tkagg_pyplot import plt, savefig
from lcms_processor.utils import (
	_1mg_l, _1ug_l, _1ul, _10ug_l, set_display_options, sup_1, sup_2, sup_3,
	warn_if_all_filtered,
	)

ec_dpa_chart_items = [

		ChartItem.from_conditions(
				sort_order=10,
				filename="DPA_1ug_ml_diff_method_200206-0010.d",
				new_name=f"DPA{sup_1}",
				concentration=_1ug_l, vol=None, esi=None,
				),
		ChartItem.from_conditions(
				sort_order=20,
				filename="DPA_1ug_ml_diff_method_1_200218-0002.d",
				new_name=f"DPA{sup_2}",
				concentration=_1ug_l, vol=None, esi=None,
				),
		ChartItem.from_conditions(
				sort_order=30,
				filename="DPA_1ug_ml_diff_method_2_200218-0003.d",
				new_name=f"DPA{sup_3}",
				concentration=_1ug_l, vol=None, esi=None,
				),

		ChartItem.from_conditions(
				sort_order=40,
				filename="EC_1ug_ml_diff_method_200206-0011.d",
				new_name=f"EC{sup_1}",
				concentration=_1ug_l, vol=None, esi=None,
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
				concentration=_1ug_l, vol=None, esi=None,
				),
		ChartItem.from_conditions(
				sort_order=70,
				filename="EC_1ug_ml_diff_method_3_200218-0006.d",
				new_name=f"EC{sup_3}",
				concentration=_1ug_l, vol=None, esi=None,
				),

		]

# ---

std_mix_chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_1_200221-0002.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				vol=None, esi=None,
				Repeat=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_2_200221-0004.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=20,
				vol=None, esi=None,
				Repeat=2,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_1ug_diff_meth_2_200221-0006.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				vol=None, esi=None,
				Repeat=3,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_10ug_diff_meth_1_200221-0011.d",
				new_name='',
				concentration=_10ug_l,
				sort_order=40,
				vol=None, esi=None,
				Repeat=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_Std_10ug_diff_meth_2_200221-0012.d",
				new_name='',
				concentration=_10ug_l,
				sort_order=50,
				vol=None, esi=None,
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
	from charts_shared import all_samples, mass_calibration_ranges, chdir
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

	fig, ax = plot_areas(ec_dpa_target_samples, ec_dpa_identified_compounds, include_none=True, show_scores=True, legend_cols=3)
	fig.suptitle("Peak Areas and Scores with Method 3", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	fig.set_size_inches(A4_portrait)
	fig.tight_layout()
	fig.subplots_adjust(bottom=0.13, top=0.91)

	savefig(fig, "charts/new_method_standards.png", dpi=300)
	savefig(fig, "charts/new_method_standards.svg")

	update_all_labels_with_cal_range(std_mix_chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	std_mix_target_samples = sort_n_filter_by_filename(all_samples, std_mix_chart_items)
	std_mix_identified_compounds = std_mix_target_samples.get_compounds()

	# Remove nitrobenzene
	std_mix_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(std_mix_target_samples, ["Nitrobenzene"])

	fig, ax = plot_areas(std_mix_target_samples, std_mix_identified_compounds, include_none=True, show_scores=True, legend_cols=3)
	fig.suptitle("Peak Areas and Scores for Mixed Standard with Method 3", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	fig.set_size_inches(A4_portrait)
	fig.tight_layout()
	fig.subplots_adjust(bottom=0.13, top=0.91)
	#
	savefig(fig, "charts/new_method_mixed_standard.png", dpi=300)
	savefig(fig, "charts/new_method_mixed_standard.svg")

	# plt.show()


if __name__ == '__main__':
	make_charts()
