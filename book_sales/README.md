# Challenge directions 

Given the following tables

```sql
create table product
(
  product_id number primary key,
  name varchar2(128 byte) not null,
  rrp number not null,
  available_from date not null
);

create table orders
(
  order_id number primary key,
  product_id number not null,
  quantity number not null,
  order_price number not null,
  dispatch_date date not null,
  foreign key (product_id) references product(product_id)
);
```

Write an sql query to find books that have sold fewer than 10 copies in
the last year, excluding books that have been available for less than 1
month.
