#!/usr/bin/env python3
#
#  _05_standards_low_flow_charts.py
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
from lcms_results_processor.utils import _0_1ug_l, _1ug_l, sup_1, sup_2, warn_if_all_filtered

chart_items = [
		ChartItem.from_conditions(
				sort_order=10,
				new_name=f"Mixed Standard{sup_1}",
				filename="Propellant_Std_0.1ug_1_200129-0002.d",
				concentration=_0_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=20,
				new_name=f"Mixed Standard{sup_2}",
				filename="Propellant_Std_0.1ug_2_200129-0003.d",
				concentration=_0_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=30,
				new_name=f"Mixed Standard{sup_1}",
				filename="Propellant_Std_1ug_1_200129-0005.d",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=40,
				new_name=f"Mixed Standard{sup_2}",
				filename="Propellant_Std_1ug_2_200129-0007.d",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=50,
				new_name=f"DPA{sup_1} low flow",
				filename="DPA_1ug_ml_1_200206-0002.d",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=60,
				new_name=f"DPA{sup_2} low flow",
				filename="DPA_1ug_ml_2_200206-0004.d",
				concentration=_1ug_l,
				vol=None,
				esi=None
				),
		ChartItem.from_conditions(
				sort_order=70,
				new_name=f"EC{sup_1} low flow",
				filename="EC_1ug_ml_1_200206-0006.d",
				concentration=_1ug_l,
				vol=None,
				esi=None,
				),
		ChartItem.from_conditions(
				sort_order=80,
				new_name=f"EC{sup_2} low flow",
				filename="EC_1ug_ml_2_200206-0008.d",
				concentration=_1ug_l,
				vol=None,
				esi=None
				),
		]


def make_charts():
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	# for item in chart_items:
	# 	print(mass_calibration_ranges[item.filename])
	# 	print(item.new_name)

	update_all_labels_with_cal_range(chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	target_samples = sort_n_filter_by_filename(all_samples, chart_items)

	all_identified_compounds = target_samples.get_compounds()

	# Remove nitrobenzene
	all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	fig, ax = create_figure(tex_page_landscape, left=0.23)
	fig, ax = plot_areas(fig, ax, target_samples, all_identified_compounds, include_none=True, show_scores=True)
	fig.suptitle(
			"Peak Areas and Scores for Standards with Reduced Flow Rate",
			fontsize=14,
			y=0.985,
			)  # Put actual number
	ax.set_ylabel("Concentration and Conditions")
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	# fig.set_size_inches(to_inch(A4_landscape))
	# fig.tight_layout()
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	savefig(fig, "charts/standards_low_flow.png", dpi=300)
	savefig(fig, "charts/standards_low_flow.svg")

	# plt.show()


if __name__ == "__main__":
	make_charts()
