import json
import csv
import sys


def json_to_tsv(suppliers_filename, orders_filename):
    #  SUPPLIERS

    # read data file
    with open(suppliers_filename, 'r') as json_file:
        json_list = json.load(json_file)
        # counter = 0
        # for line in data:
        #     print(line)
        #     json_list = 

    # write to tsv files
    with open('suppliers.tsv', 'w', newline='') as sup_file, \
         open('suppliers_tel.tsv', 'w', newline='') as tel_file:
        sup_writer = csv.writer(sup_file, delimiter='\t')
        tel_writer = csv.writer(tel_file, delimiter='\t')


        # insert suppliers data into suppliers.tsv and suppliers_tel.tsv
        for supplier in json_list:
            # insert new record in suppliers.tsv
            sup_writer.writerow([supplier['_id'], supplier['name'], supplier['email']])
            # insert new record in suppliers_tel.tsv for each supplier telephone
            for tel in supplier['tel']:
                tel_writer.writerow([supplier['_id'], tel['number']])


    #  ORDERS

    # read data file
    with open(orders_filename, 'r') as json_file:
        json_list = [json.loads(line) for line in json_file]

    # write to tsv files
    with open('orders.tsv', 'w', newline='') as orders_file, \
         open('order_parts.tsv', 'w', newline='') as ord_parts_file:
        o_writer = csv.writer(orders_file, delimiter='\t')
        op_writer = csv.writer(ord_parts_file, delimiter='\t')

        counter = 1
        for order in json_list:
            # insert new record in orders.tsv
            o_writer.writerow([counter,order['when'],order['supp_id']])
            # insert new record in order_parts.tsv for each item
            for items in order['items']:
                op_writer.writerow([counter, items['part_id'], items['qty']])

            counter += 1

if __name__ == "__main__":
    filenames = sys.argv[1:]
    if (len(filenames) == 2):
        json_to_tsv(*filenames)
