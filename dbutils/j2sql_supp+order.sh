#!/usr/bin/env bash

user="uXY"
pass="XYZ"
db="uXY"

# create tables in database
echo "source make_tables.sql;" | mysql -u "$user" --password="$pass" "$db"
echo

# convert json to tsv files
python3 j2tsv_supp+order.py suppliers_100.json orders_4000.json

# load data into database
declare -a tables=("suppliers" "suppliers_telephone" "orders" "order_parts")
for table in "${tables[@]}"; do
    echo "load data local infile '$table.tsv' into table $table" | mysql $db -u $user --password="$pass"
    rm "$table.tsv" # remove tsv file after loading data into database
    echo
done
