# Logs Analysis
This is a project built for the Udacity's Full Stack Web Developer Nanodegree Program

## Database information

There are three tables in the "news" database:

1. articles
   1. author `integer`
   2. title `text`
   3. slug `text`
   4. lead `text`
   5. body `text`
   6. time [timestamp with time zone]
   7. id `integer`
2. authors
   1. name `text`
   2. bio `text`
   3. id `integer`
3. log
   1. path `text`
   2. ip `inet`
   3. method `text`
   4. status `text`
   5. time [timestamp with time zone]
   6. id `integer`

## Questions to answer

1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?

---

## Queries

### What are the most popular three articles of all time?

```sql
-- Returns a list of 3 most popular articles
select articles.title, total
from articles, article_hits as visits
where articles.id = visits.article_id
order by total desc
limit 3;
```

```sql
-- Returns a list of top articles with their id and visits
create view article_hits as
  select articles.id as article_id, 
		count(*) as total
  from articles, log
  where log.path LIKE CONCAT('%', articles.slug, '%')
  group by articles.id;
```

### Who are the most popular authors of all time?

```sql
-- Returns a list of all visits received by each author
select authors.name as author_name,
	sum(total)::integer as total
from authors, 
	(select article_id, authors.id as author_id, total
	 from article_hits, articles, authors
	 where article_hits.article_id = articles.id
	 	and articles.author = authors.id
   ) as articles_list
where authors.id = articles_list.author_id
group by authors.id
order by total desc;
```

### On which days did more than 1% of requests lead to errors?

```sql
-- Returns a list of days in which the error percentage is over 0.01
select * from total_daily_errors_percentage
where error_percentage > 0.01
order by error_percentage desc;
```

```sql
-- Returns error a list of the error percentage per day
create view total_daily_errors_percentage as
  select requests.date, errors.total/requests.total::float as error_percentage
  from total_daily_requests as requests,
    total_daily_errors as errors
  where requests.date = errors.date;
```

```sql
-- Returns a list of total errors per day
create view total_daily_errors as
  select time as date,
    count(*) as total
  from log_formatted_date as log
  where status LIKE '%4__%'
    OR status LIKE '%5__%'
  group by time;
```

```sql
-- Returns a list of total requests per day
create view total_daily_requests as
  select time as date,
    count(*) as total
  from log_formatted_date as log
  group by time;
```

```sql
-- Returns the log with a reformatted time column for each row
create view log_formatted_date as
  select path, ip, method, status, to_char(log.time, 'YYYY/MM/DD') as time, id 
  from log;
```