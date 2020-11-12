#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  standards_low_flow.py
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
	create_figure, plot_areas,
	sort_n_filter_by_filename,
	tex_page_landscape, update_all_labels_with_cal_range,
	)
from lcms_processor.tkagg_pyplot import plt, savefig
from lcms_processor.utils import _0_1ug_l, _1ug_l, set_display_options, sup_1, sup_2, warn_if_all_filtered

chart_items = [
		ChartItem.from_conditions(
				sort_order=10,
				new_name=f"Mixed Standard{sup_1}",
				filename="Propellant_Std_0.1ug_1_200129-0002.d",
				concentration=_0_1ug_l,
				vol=None, esi=None,
				),

		ChartItem.from_conditions(
				sort_order=20,
				new_name=f"Mixed Standard{sup_2}",
				filename="Propellant_Std_0.1ug_2_200129-0003.d",
				concentration=_0_1ug_l,
				vol=None, esi=None,
				),
		ChartItem.from_conditions(
				sort_order=30,
				new_name=f"Mixed Standard{sup_1}",
				filename="Propellant_Std_1ug_1_200129-0005.d",
				concentration=_1ug_l,
				vol=None, esi=None,
				),
		ChartItem.from_conditions(
				sort_order=40,
				new_name=f"Mixed Standard{sup_2}",
				filename="Propellant_Std_1ug_2_200129-0007.d",
				concentration=_1ug_l,
				vol=None, esi=None,
				),

		ChartItem.from_conditions(
				sort_order=50,
				new_name=f"DPA{sup_1} low flow",
				filename="DPA_1ug_ml_1_200206-0002.d",
				concentration=_1ug_l,
				vol=None, esi=None,
				),

		ChartItem.from_conditions(
				sort_order=60,
				new_name=f"DPA{sup_2} low flow",
				filename="DPA_1ug_ml_2_200206-0004.d",
				concentration=_1ug_l, vol=None, esi=None
				),

		ChartItem.from_conditions(
				sort_order=70,
				new_name=f"EC{sup_1} low flow",
				filename="EC_1ug_ml_1_200206-0006.d",
				concentration=_1ug_l,
				vol=None, esi=None,
				),

		ChartItem.from_conditions(
				sort_order=80,
				new_name=f"EC{sup_2} low flow",
				filename="EC_1ug_ml_2_200206-0008.d",
				concentration=_1ug_l, vol=None, esi=None
				),

		]

def make_charts():
	from charts_shared import all_samples, mass_calibration_ranges, chdir
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
	fig.suptitle("Peak Areas and Scores for Standards with Reduced Flow Rate", fontsize=14, y=0.985)  # Put actual number
	ax.set_ylabel("Concentration and Conditions")
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	# fig.set_size_inches(to_inch(A4_landscape))
	# fig.tight_layout()
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	savefig(fig, "charts/standards_low_flow.png", dpi=300)
	savefig(fig, "charts/standards_low_flow.svg")

	# plt.show()


if __name__ == '__main__':
	make_charts()
