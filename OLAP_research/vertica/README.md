*Выполнение запросов во время записи данных*

Executing query

    SELECT COUNT(*) FROM views

[420000]

Query execution took: 
0.02783513069152832


Executing query
    
    SELECT count(DISTINCT movie_id) FROM views

[10000]
Query execution took: 
0.2515218257904053


Executing query

    SELECT count(DISTINCT user_id) FROM views

[10000]
Query execution took: 
0.22393584251403809


Executing query

    SELECT 
        user_id, 
        count(distinct movie_id) 
    FROM views
    GROUP by user_id
    
Query execution took: 
2.4797160625457764


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    GROUP by user_id
    
Query execution took: 
0.4341411590576172


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    WHERE event_time > '2021-04-13 23:09:02'
    GROUP by user_id
    
Query execution took: 
0.4405517578125


Executing insert query. Rows: 10

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

0.24517130851745605


Executing insert query. Rows: 100

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

1.9224703311920166


Executing insert query. Rows: 1000

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

19.16924285888672


Executing query

    SELECT COUNT(*) FROM views

[426110]
Query execution took: 
0.020767927169799805