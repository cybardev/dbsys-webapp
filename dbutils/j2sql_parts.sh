#!/usr/bin/env bash

# import environment secrets (user, pass, db)
source ../.env

echo

mongoimport -d "$db" -c parts -u "$user" --password="$pass" --type="json" --file="parts_100.json"
mongoexport -d "$db" -c parts -u "$user" -p "$pass" --type=csv --fields "_id,price,description" | tail -n +2 >parts.csv

echo "source parts_table.sql;" | mysql -u "$user" --password="$pass" "$db"
cat parts.csv | tr "," "\t" >parts.tsv
echo "load data local infile 'parts.tsv' into table parts" | mysql $db -u $user --password="$pass"
rm parts.csv parts.tsv
echo
