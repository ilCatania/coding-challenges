select product_id, name
from product
where
    available_from < dateadd('month', -1, current_date)
    and product_id not in (
		select product_id from orders
		where dispatch_date between dateadd('year', -1, current_date) and current_date
		group by product_id having sum(quantity) >= 10
	)
