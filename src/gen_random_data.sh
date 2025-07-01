#!/bin/bash

output_file="rand_data.txt"
> "$output_file"  # Good practice to quote variables

# Writing headers
echo -e "Date\tGUID" > "$output_file"

# Function to generate a random date and GUID
gen_random_entry() {
    year=$((RANDOM % 35 + 1990))
    month=$((RANDOM % 12 + 1))
    day=$((RANDOM % 28 + 1))
    random_date=$(printf "%04d-%02d-%02d" "$year" "$month" "$day")
    guid=$(uuidgen) # More robust way to generate a GUID
    echo -e "$random_date\t$guid"
}

# Export the function so xargs subshells can see it
export -f gen_random_entry

# Generate 100,000 entries in parallel
seq 1 100000 | xargs -n 1 -P 0 bash -c 'gen_random_entry' >> "$output_file"
