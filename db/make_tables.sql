-- Suppliers Table
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255)
);

-- Telephone Numbers Table for Suppliers
CREATE TABLE IF NOT EXISTS suppliers_telephone (
    supplier_id INT,
    number VARCHAR(20),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Order Part Relationship Table
CREATE TABLE IF NOT EXISTS order_parts (
    order_id INT,
    part_id INT,
    quantity INT,
    PRIMARY KEY (order_id, part_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (part_id) REFERENCES parts(_id)
);
