--
-- Copyright 2017 Gabriele Catania <gabriele.ctn@gmail.com>
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--    http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

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
