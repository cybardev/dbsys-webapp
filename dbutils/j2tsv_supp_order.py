#!/usr/bin/env python3
# -*- coding: utf8 -*-

import csv
import json
import sys


def json_to_tsv(suppliers_filename: str, orders_filename: str):
    s_list = suppliers_list(suppliers_filename)
    suppliers_to_tsv(s_list)

    o_list = orders_list(orders_filename)
    orders_to_tsv(o_list)


def suppliers_list(fname: str) -> list:
    with open(fname) as f:
        return json.load(f)


def suppliers_to_tsv(s_list: list):
    with open("suppliers.tsv", "w", newline="") as sup_file, open(
        "suppliers_tel.tsv", "w", newline=""
    ) as tel_file:
        sup_writer = csv.writer(sup_file, delimiter="\t")
        tel_writer = csv.writer(tel_file, delimiter="\t")

        for supplier in s_list:
            sup_writer.writerow([supplier["_id"], supplier["name"], supplier["email"]])
            for tel in supplier["tel"]:
                tel_writer.writerow([supplier["_id"], tel["number"]])


def orders_list(fname: str) -> list:
    with open(fname) as json_file:
        return [json.loads(line) for line in json_file]


def orders_to_tsv(o_list: list):
    with open("orders.tsv", "w", newline="") as orders_file, open(
        "order_parts.tsv", "w", newline=""
    ) as ord_parts_file:
        o_writer = csv.writer(orders_file, delimiter="\t")
        op_writer = csv.writer(ord_parts_file, delimiter="\t")

        for counter, order in enumerate(o_list, 1):
            o_writer.writerow([counter, order["when"], order["supp_id"]])
            for items in order["items"]:
                op_writer.writerow([counter, items["part_id"], items["qty"]])


if __name__ == "__main__":
    s_fname, o_fname = sys.argv[1], sys.argv[2]
    json_to_tsv(s_fname, o_fname)
