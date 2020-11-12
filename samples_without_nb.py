from charts_shared import all_samples

for sample in all_samples:
	# print(sample.results_list)
	# print(sample.filename)
	# print("Nitrobenzene" in sample.results_list)
	# print("Diethyl Phthalate" in sample.results_list)

	if "Nitrobenzene" not in sample.results_list:
		print(sample.filename)

	# input(">")
