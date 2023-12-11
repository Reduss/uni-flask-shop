use sdb_shop

DELIMITER //
CREATE PROCEDURE PlaceOrder(
    IN customer_fname VARCHAR(45),
    IN customer_lname VARCHAR(45),
    IN customer_phone VARCHAR(13),
    IN customer_address VARCHAR(100),
    
    IN product_ids_list VARCHAR(255),  
    IN product_amounts_list VARCHAR(255) 
)
BEGIN
    DECLARE order_id INT;
	DECLARE customer_id INT;
    
	-- create customer entry
     INSERT INTO customer (first_name, last_name, phone_num, address) 
     VALUES (customer_fname, customer_lname, customer_phone, customer_address);

    SET @customer_id = LAST_INSERT_ID();
    
    -- create order entry
    INSERT INTO customer_order (customer_order.customer_id, status_id, order_date, total_price)
    VALUES (@customer_id, (SELECT id FROM order_status WHERE title = 'New'), NOW(), 0);
    
    SET order_id = LAST_INSERT_ID();

    SET @product_ids = product_ids_list;
    SET @amounts = product_amounts_list;

    WHILE LENGTH(@product_ids) > 0 DO
        SET @comma_pos = LOCATE(',', @product_ids);
        SET @product_id = IF(@comma_pos > 0, SUBSTRING(@product_ids, 1, @comma_pos - 1), @product_ids);
        SET @product_ids = IF(@comma_pos > 0, SUBSTRING(@product_ids, @comma_pos + 1), '');

        SET @comma_pos = LOCATE(',', @amounts);
        SET @amount = IF(@comma_pos > 0, SUBSTRING(@amounts, 1, @comma_pos - 1), @amounts);
        SET @amounts = IF(@comma_pos > 0, SUBSTRING(@amounts, @comma_pos + 1), '');
		
        SET @stock_amount = (SELECT amount_in_stock FROM product WHERE id = @product_id);
        
        IF @amount <= @stock_amount THEN
			-- update total_price
			SET @price = (SELECT price FROM product WHERE id = @product_id);
			UPDATE customer_order SET total_price = total_price + @price * @amount WHERE customer_order.id = order_id;
			
            
			-- Insert the order item
			INSERT INTO order_item (customer_order_id, product_id, amount, price)
			VALUES (order_id, @product_id, @amount, @price);
			UPDATE product SET amount_in_stock = amount_in_stock - @amount WHERE id = @product_id;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Invalid product amount';
        END IF;
    END WHILE;
END //
DELIMITER ;

use sdb_shop;
CALL PlaceOrder('fname', 'lname', '+99999999', 'addr', '1, 2', '2, 1');

