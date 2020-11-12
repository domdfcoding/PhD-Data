#!/bin/bash
# Script to copy results from OneDrive

declare -a arr=(
"191121"
"191126"
"191128"
"191206"
"191211"
"200124"
"200128"
"200129"
"200206"
"200218"
"200221"
"200227"
"200303"
)

for date in "${arr[@]}"; do
  output_folder=$(echo "${date}" | sed 's/.\{2\}/&-/g;s/-$//')
  declare output_folder
  echo "Copying results from ${output_folder}"
  mkdir -p "data/raw_results/${output_folder}"
  cp "/ownCloud/OneDrive2/LC-MS Results ${date}/CSV Results.csv" "data/raw_results/${output_folder}/" --no-clobber
  cp -r "/ownCloud/OneDrive2/LC-MS Results ${date}/CEF Exports" "data/raw_results/${output_folder}/" --no-clobber

done
