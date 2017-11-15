create table product (
  product_id number primary key,
  name varchar(128) not null,
  rrp number not null,
  available_from date not null
);

create table orders (
  order_id number primary key,
  product_id number not null,
  quantity number not null,
  order_price number not null,
  dispatch_date date not null,
  foreign key (product_id) references product(product_id)
);
