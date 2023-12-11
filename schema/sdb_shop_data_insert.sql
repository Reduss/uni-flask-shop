use sdb_shop;

INSERT INTO customer (first_name, last_name, phone_num, address) VALUES
('Bob', 'Odenkirk', '+00000000000', 'address1'),
('Jimmy', 'Page', '+00000000001', 'address2'),
('Robby', 'Williams', '+00000000002', 'address3'),
('Jack', 'Sparrow', '+00000000003', 'address4');

INSERT INTO category (title) VALUES
('Table'),
('Chair'),
('Wardrobe'),
('None');

INSERT INTO order_status (title) VALUES
('New'),
('Confirmed'),
('Complete'),
('Canceled');

INSERT INTO product (title, price, category_id, amount_in_stock) VALUES
('Dining Table', 299.99, 1, 10),
('Coffee Table', 149.99, 1, 20),
('Office Desk', 199.99, 1, 15),
('Dining Chair (Set of 2)', 99.99, 2, 30),
('Armchair', 129.99, 2, 25),
('Study Chair', 79.99, 2, 40),
('Wardrobe with Mirrors', 499.99, 3, 8),
('Wooden Wardrobe', 399.99, 3, 12),
('Kids Table', 89.99, 1, 20),
('Bar Stool (Set of 4)', 199.99, 2, 15),
('Bookshelf', 129.99, 3, 18),
('Foldable Table', 119.99, 1, 25),
('Accent Chair', 149.99, 2, 20),
('Sliding Wardrobe', 599.99, 3, 10),
('Outdoor Dining Table', 249.99, 1, 15);
