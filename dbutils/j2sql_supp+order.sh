#!/usr/bin/env bash

user="uXX"
pass="YourPass"
db="uXX"

echo "source make_tables.sql;" | mysql -u "$user" --password="$pass" "$db"
echo

python3 j2tsv_supp_order.py suppliers_100.json orders_4000.json

echo "load data local infile 'suppliers.tsv' into table suppliers" | mysql $db -u $user --password="$pass"
echo

echo "load data local infile 'suppliers_tel.tsv' into table suppliers_telephone" | mysql $db -u $user --password="$pass"
echo

echo "load data local infile 'orders.tsv' into table orders" | mysql $db -u $user --password="$pass"
echo

echo "load data local infile 'order_parts.tsv' into table order_parts" | mysql $db -u $user --password="$pass"
echo
