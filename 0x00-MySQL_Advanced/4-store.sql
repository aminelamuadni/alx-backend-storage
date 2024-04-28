-- Drop existing trigger to prevent errors
DROP TRIGGER IF EXISTS dec_quantity;

-- Create a simple trigger to decrement item quantity after a new order
CREATE TRIGGER dec_quantity
AFTER
INSERT
    ON orders FOR EACH ROW
UPDATE
    items
SET
    quantity = quantity - NEW.number
WHERE
    name = NEW.item_name;