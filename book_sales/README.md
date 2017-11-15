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

# Solution

The sql query can be found under `src/main/resources/sql`, in the aptly
named `query.sql`. The project can be built with Gradle in order to run
a basic test suite on the query, for example:

```bash
./gradlew test
```

and the output would be something like this:

```
BUILD SUCCESSFUL in 0s
4 actionable tasks: 4 up-to-date
```
