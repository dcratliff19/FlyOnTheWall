# FlyOnTheWall Audio Collection and Analyzation
```
|-- FLYONTHEWALL --| 
|        __        |
|   -. (#)(#) .-   |
|    '\.';;'./'    |
| .-\.'  ;;  './-. |
|   ;    ;;    ;   | 
|   ;   .''.   ;   |
|    '''    '''    |
|-- FLYONTHEWALL --|
```
FlyOnTheWall is an open source software that collects audio records from client nodes, uses [Google's MediaPipe](https://developers.google.com/mediapipe/solutions/audio/audio_classifier) machine learning library to classify the sounds into one of [yamnet's classes](https://storage.googleapis.com/mediapipe-tasks/audio_classifier/yamnet_label_list.txt), and stores that data into a MySQL Database for later analysis.
### Report for detecting dog sounds.

```sql
with class_1_tbl as (
    SELECT 
    class_1, 1 as 'class', avg(decibel_reading), count(*)
    from raw_sounds 
    group by 1,2  
    ORDER BY `count(*)` DESC
),

class_2_tbl as 
(
    SELECT 
    class_2, 2 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by 1,2  
    ORDER BY `count(*)` DESC
),

class_3_tbl as 
(
    SELECT 
    class_3, 3 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by class_3  
    ORDER BY `count(*)` DESC
),

class_4_tbl as 
(
    SELECT 
    class_4, 4 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by class_4  
    ORDER BY `count(*)` DESC
),

class_5_tbl as 
(
    SELECT 
    class_5, 5 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by class_5  
    ORDER BY `count(*)` DESC
),

final_table as 
(
    select * 
    from class_1_tbl 
    UNION ALL 
    select * from class_2_tbl
    UNION ALL
    select * from class_3_tbl
    UNION ALL
    select * from class_4_tbl
    UNION ALL
    select * from class_5_tbl
    order by 4 desc
 )
select * from final_table
where class_1 in ('Domestic animals, pets', 'Dog', 'Bark', 'Yip', 'Howl', 'Bow-wow', 'Growling', 'Whimper (dog)');

```