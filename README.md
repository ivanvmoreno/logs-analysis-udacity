# Log-Analysis

### Project Overview
>This is a project built for the Udacity's Full Stack Web Developer Nanodegree Program

### Running the project

#### Prerequisites
  * [Python 3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Project Setup
  1. Install Vagrant and VirtualBox
  2. Download or clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository
  3. Download the [database script](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
  4. Unzip this file after downloading it. The file inside is called `newsdata.sql`
  
#### Launching the Virtual Machine:
  1. Launch the Vagrant VM inside Vagrant subdirectory in the downloaded `fullstack-nanodegree-vm` repository using:
  
  ```
    $ vagrant up
  ```
  2. Then login using command:
  
  ```
    $ vagrant ssh
  ```
  
#### Setting up the database and Creating Views:

  1. Load the data in the local database `news` using:
  
  ```
    psql -d news -f newsdata.sql
  ```
  The database includes three tables:
  * The `authors` table includes information about the authors of articles
  * The `articles` table includes the articles themselves
  * The `log` table includes one entry for each time a user has accessed the site
  
  2. Use `psql -d news` to connect to database.
  
  3. Create article_hits view using:
  ```sql
  -- Returns a list of articles with their id and visits
  create view article_hits as
    select articles.id as article_id, count(*) as total
    from articles, log
    where log.path LIKE CONCAT('%', articles.slug)
    group by articles.id;
  ```
  | Column  | Type    |
  | :-------| :-------|
  | article_id   | text    |
  | total  | integer    |
  
  4. Create log_formatted_date view using:
  ```sql
  -- Returns the log with a reformatted time column for each entry
  create view log_formatted_date as
    select path, ip, method, status, to_char(log.time, 'YYYY/MM/DD') as time, id 
    from log;
  ```
  | Column        | Type    |
  | :-------      | :-------|
  | path          | text    |
  | ip | inet   |
  | method | text   |
  | status | text   |
  | time | text   |
  | id | integer   |
  
  5. Create total_daily_requests view using:
  ```sql
  -- Returns a list of daily total requests
  create view total_daily_requests as
    select time as date,
      count(*) as total
    from log_formatted_date as log
    group by time;
  ```
  | Column        | Type    |
  | :-------      | :-------|
  | date          | timestamp with time zone    |
  | total | integer   |

  6. Create total_daily_errors view using:
  ```sql
  -- Returns a list of daily total errors
  create view total_daily_errors as
    select time as date,
      count(*) as total
    from log_formatted_date as log
    where status LIKE '%4__%'
      OR status LIKE '%5__%'
    group by time;
  ```
  | Column        | Type    |
  | :-------      | :-------|
  | date          | timestamp with time zone    |
  | total | integer   |

  7. Create total_daily_errors_percentage view using:
  ```sql
  -- Returns error a list of the daily error percentage
  create view total_daily_errors_percentage as
    select requests.date, errors.total/requests.total::float as error_percentage
    from total_daily_requests as requests,
      total_daily_errors as errors
    where requests.date = errors.date;
  ```
  | Column        | Type    |
  | :-------      | :-------|
  | date          | timestamp with time zone    |
  | error_percentage | float   |

#### Running the queries:
  1. From the vagrant directory inside the virtual machine,run `log_analysis.py` using:
  ```
    $ python log_analysis.py
  ```
