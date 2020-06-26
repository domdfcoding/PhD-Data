from pprint import pprint

from charts_shared import all_samples
from lcms_processor import SampleList
from lcms_processor.utils import warn_if_all_filtered
from colorama import Fore

for sample in all_samples:
	sl = SampleList()
	sl.add_sample(sample)
	if warn_if_all_filtered(sl, ["Nitrobenzene"]):

		print(Fore.GREEN, sample, sample.filename, Fore.RESET)

	if not sl.get_compounds():
		print(f"No compounds detected for {sample.filename}")
		input(">")

