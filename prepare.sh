grep -v '^#' ms_data_dirty.csv > ms_data_temp.csv
sed '/^[[:space:]]*$/d' ms_data_temp.csv > ms_data_temp2.csv
sed 's/,,*/,/g; s/,$//' ms_data_temp2.csv > ms_data_temp3.csv
head -n 1 ms_data_temp3.csv > ms_data.csv
cut -d',' -f1,2,4,5,6 ms_data_temp3.csv > ms_data_temp4.csv
awk -F',' '$5 >= 2.0 && $5 <= 8.0' ms_data_temp4.csv >> ms_data.csv

rm ms_data_temp.csv ms_data_temp2.csv ms_data_temp3.csv ms_data_temp4.csv

echo -e 'insurance_type\nBasic\nPremium\nPlatinum\nNoInsurance' > insurance.lst

echo -e "Total number of visits: $(wc -l < ms_data.csv)"
