-- Suppliers Table
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Telephone Numbers Table for Suppliers
CREATE TABLE IF NOT EXISTS suppliers_telephone (
    supplier_id INT NOT NULL,
    number VARCHAR(20) PRIMARY KEY NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY NOT NULL,
    order_date DATE NOT NULL,
    supplier_id INT NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Order Part Relationship Table
CREATE TABLE IF NOT EXISTS order_parts (
    order_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, part_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (part_id) REFERENCES parts(_id)
);
