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
-- kad rezultate matytųsi užsakymo id, pozicijos su kiekiais, kainomis ir bendra pozicijos suma:

SELECT product_order.order_id, product.name, product_order.qty, product.price, product_order.qty * product.price as "Total" 
FROM product_order
JOIN product ON product_order.product_id = product.id

ARBA:

-- SELECT 
-- 	order_.id, 
-- 	product.name, 
-- 	product_order.quantity, 
-- 	product.price, 
-- 	product_order.quantity * product.price as "total"
-- FROM order_
-- JOIN product_order ON order_.id = product_order.order_id
-- JOIN product ON product.id = product_order.product_id 

-- uzklausa 1 
-- kad rezultate matytųsi užsakymo id, užsakovo pavardė, data, bendra užsakymo suma

SELECT 	order_.id as "order id", 
		order_.date_ as "date", 
		customer.l_name as "customer",
        sum(product_order.quantity * product.price) as "price"
FROM product_order
JOIN order_ on order_.id = product_order.order_id 
JOIN product on product.id = product_order.product_id
JOIN customer on customer.id = order_.customer_id
GROUP by order_id


-- uzklausa 2
-- prieš tai buvusios užklausos pagrindu sukurkite užklausą, kurioje matytųsi, kiek ir kokio produkto buvo užsakyta:

-- SELECT 
-- 	order_.id, 
-- 	product.name, 
-- 	sum(product_order.quantity) as "QTY", 
-- 	product.price, 
-- 	sum(product_order.quantity) * product.price as "total"
-- FROM order_
-- JOIN product_order ON order_.id = product_order.order_id
-- JOIN product ON product.id = product_order.product_id
-- group by product_order.product_id
