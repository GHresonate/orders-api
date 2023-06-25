DROP TRIGGER IF EXISTS update_timestamp ON order_status;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Creation of product table
CREATE TABLE IF NOT EXISTS public.product (
  product_id INT NOT NULL,
  name varchar(250) NOT NULL,
  PRIMARY KEY (product_id)
);

-- Creation of country table
CREATE TABLE IF NOT EXISTS public.country (
  country_id INT NOT NULL,
  country_name varchar(450) NOT NULL,
  PRIMARY KEY (country_id)
);

-- Creation of city table
CREATE TABLE IF NOT EXISTS public.city (
  city_id INT NOT NULL,
  city_name varchar(450) NOT NULL,
  country_id INT NOT NULL,
  PRIMARY KEY (city_id),
  CONSTRAINT fk_country
      FOREIGN KEY(country_id)
    REFERENCES country(country_id)
);

-- Creation of store table
CREATE TABLE IF NOT EXISTS public.store (
  store_id INT NOT NULL,
  name varchar(250) NOT NULL,
  city_id INT NOT NULL,
  PRIMARY KEY (store_id),
  CONSTRAINT fk_city
      FOREIGN KEY(city_id)
    REFERENCES city(city_id)
);

-- Creation of user table
CREATE TABLE IF NOT EXISTS public.users (
  user_id INT NOT NULL,
  name varchar(250) NOT NULL,
  PRIMARY KEY (user_id)
);

-- Creation of status_name table
CREATE TABLE IF NOT EXISTS public.status_name (
  status_name_id INT NOT NULL,
  status_name varchar(450) NOT NULL,
  PRIMARY KEY (status_name_id)
);

-- Creation of sale table
CREATE TABLE IF NOT EXISTS public.sale (
  sale_id uuid DEFAULT uuid_generate_v4() NOT NULL,
  amount DECIMAL(20,3) NOT NULL,
  date_sale TIMESTAMP,
  product_id INT NOT NULL,
  user_id INT NOT NULL,
  store_id INT NOT NULL,
  PRIMARY KEY (sale_id),
  CONSTRAINT fk_product
      FOREIGN KEY(product_id)
    REFERENCES product(product_id),
  CONSTRAINT fk_user
      FOREIGN KEY(user_id)
    REFERENCES users(user_id),
  CONSTRAINT fk_store
      FOREIGN KEY(store_id)
    REFERENCES store(store_id)
);
CREATE OR REPLACE FUNCTION set_updated_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TABLE IF NOT EXISTS public.order_status (
  order_status_id uuid DEFAULT uuid_generate_v4() NOT NULL,
  update_at TIMESTAMP NOT NULL DEFAULT NOW(),
  sale_id uuid NOT NULL UNIQUE,
  status_name_id INT NOT NULL,
  PRIMARY KEY (order_status_id),
  CONSTRAINT fk_sale
      FOREIGN KEY(sale_id)
	  REFERENCES sale(sale_id),
  CONSTRAINT fk_status_name
      FOREIGN KEY(status_name_id)
	  REFERENCES status_name(status_name_id)
);

CREATE trigger update_timestamp BEFORE UPDATE ON order_status FOR EACH ROW EXECUTE PROCEDURE set_updated_time();

-- Creation of order_status_stats table
CREATE TABLE IF NOT EXISTS order_status_stats (
    dt DATE NOT NULL,
    order_status_name VARCHAR(100) NOT NULL,
    orders_count INT NOT NULL
);

--clear datas if it does`t empty
TRUNCATE store CASCADE;
TRUNCATE users CASCADE;
TRUNCATE status_name CASCADE;
TRUNCATE sale CASCADE;
TRUNCATE order_status CASCADE;
TRUNCATE product CASCADE;
TRUNCATE city CASCADE;
TRUNCATE country CASCADE;
TRUNCATE order_status_stats CASCADE;
