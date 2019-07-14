#!/usr/bin/env python3
#
# Log Analysis project script

import psycopg2

DBNAME = 'news'

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# What are the most popular three articles of all time?
c.execute('''\
    select articles.title, total
    from articles, article_hits as visits
    where articles.id = visits.article_id
    order by total desc
    limit 3
''')
popular_articles = c.fetchall()
print('What are the most popular three articles of all time?')
for article in popular_articles:
    print('%s - %s views' % article)
print('')

# Who are the most popular article authors of all time?
c.execute('''\
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
    order by total desc
''')
popular_authors = c.fetchall()
print('Who are the most popular article authors of all time?')
for author in popular_authors:
    print('%s - %s views' % author)
print('')

# On which days did more than 1% of requests lead to errors?
c.execute('''\
    select * from total_daily_errors_percentage
    where error_percentage > 0.01
    order by error_percentage desc
''')
glitchy_days = c.fetchall()
print('On which days did more than 1% of requests lead to errors?')
for day in glitchy_days:
    print('%s - %5.2f%% errors' % (day[0], day[1] * 100))

c.close()
db.close()
