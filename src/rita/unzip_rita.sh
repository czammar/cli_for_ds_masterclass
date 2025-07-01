for zip in *.zip; do
    unzip -o "$zip" -d ./rita_unzipped/ &
done
