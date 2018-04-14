use yelp_db

show tables

-- restauants 
-- filename=restaurants.csv
select * from business 
where id in (select business_id 
					from category 
					where category like 'Restaurants')

-- restaurants reviews
-- filename=reviews_html.html
select * from  review 
where business_id in (select business_id 
									from category 
									where category in ('Restaurants') )

-- restaurants reviews - Las Vegas
-- filename=reviews_vegas.html
select * from  review 
where business_id in (select business_id 
									from category , business
									where category.category in ('Restaurants')  and business.city in ('Las Vegas')) limit 1


-- city-wise restaurants counts
-- filename = restaurants_city_wise_count.csv
select city, count(city) 
from (select * 
		from business 
		where id in (select business_id 
							from category 
							where category like 'Restaurants')  
		) as res
group by city
order by count(city) desc

-- category counts
-- filename=category_counts.csv
select  category, count(category) 
from category 
group by category
order by  count(category) desc


select category, count(category)  from category  group by category order by  count(category) desc limit 5
