CREATE TABLE `customer` (
  `id` integer PRIMARY KEY,
  `f_name` string,
  `l_name` string,
  `email` string
);

CREATE TABLE `status` (
  `id` integer PRIMARY KEY,
  `name` string
);

CREATE TABLE `product` (
  `id` integer PRIMARY KEY,
  `name` string,
  `price` float
);

CREATE TABLE `order_` (
  `id` integer PRIMARY KEY,
  `customer_id` integer,
  `date_` string,
  `status_id` integer,
   FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
   FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
);

CREATE TABLE `product_order` (
  `order_id` integer,
  `product_id` integer,
  `quantity` integer,
   FOREIGN KEY (`order_id`) REFERENCES `order_` (`id`),
   FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
);

-- uzklausa 1 

SELECT 	order_.id as "order id", 
		order_.date_ as "date", 
		customer.l_name as "customer",
        sum(product_order.quantity * product.price) as "price"
FROM product_order
JOIN order_ on order_.id = product_order.order_id 
JOIN product on product.id = product_order.product_id
JOIN customer on customer.id = order_.customer_id
GROUP by order_id

-- SELECT 	order_.id as "order id", 
-- 		order_.date_ as "date", 
-- 		customer.l_name as "customer", 
-- 		sum(product_order.quantity * product.price) as price
-- FROM order_
-- JOIN product_order on order_.id = product_order.order_id 
-- JOIN product on product.id = product_order.product_id
-- JOIN customer on customer.id = order_.customer_id

-- uzklausa 2  

-- SELECT order_.id, product.name, product_order.quantity, product.price, product_order.quantity * product.price as "total"
-- FROM order_
-- JOIN product_order ON order_.id = product_order.order_id
-- JOIN product ON product.id = product_order.product_id 

-- uzklausa 3

-- SELECT product.name, sum(product_order.quantity) as quantity, product.price, sum(product_order.quantity) * product.price as "total"
-- FROM order_
-- JOIN product_order ON order_.id = product_order.order_id
-- JOIN product ON product.id = product_order.product_id 
-- GROUP BY product.name

SELECT my_order.id, my_order.date, customer.f_name, product.name, product.price, order_line.quantity, product.price * order_line.quantity as "sum"
FROM my_order
JOIN customer on my_order.customer_id = customer.id
JOIN status on my_order.status_id = status.id
JOIN order_line on order_line.order_id = my_order.id
JOIN product on order_line.product_id = product.id
