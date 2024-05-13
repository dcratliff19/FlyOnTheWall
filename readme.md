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

## Setup
1. Set the environment variables in .env
2. Run the migration (`migrations/migration.sql`) in whatever the database you have set in the .env
3. Install the requirements (`pip install -r requirements.txt`)
4. Fly!

## CLI Tool

Options:
```bash
--query: Use the database row ID to search for the audio file.     
    -Args: 1 = database ID, 2 = seconds before, 3 = seconds after 
    -Example: --id 64 2 2
--client: runs the FlyOnTheWall Client.
--server: Runs the FlyOnTheWall server.
```
Example: The command `./FlyOnTheWall --query 64 2 2` will output a `audio.wav` file of the audio generated from the database row with ID 64 with 2 seconds (2 rows) before and 2 seconds (2 rows) after. An additional `audio.csv` file will be output containing the raw data.

Note: the MySQL database must be running first.

# Raw Data and Metadata Points:

1. **raw_audio_bytes** - The audio stored as in it's raw byte format.
2. **class_1 to class_5** - The 5 most likely classes found by the neural network. 	
3. **class_1_percent to class_5_percent** - The 5 confidence levels for the corresponding classes. 	
4. **decibel_reading** - The estimated decibel reading using:
```python 
rms = audioop.rms(audio, 1) / 32767
db = 20 * log10(rms)
```
5. **record_datetime** - Time and Date the sound occurred.	
6. **device_id** - The device ID that recorded the sound.	
7. **created_at** - The timestamp the record was created at.

# Data Table Structure
```sql
CREATE TABLE `raw_sounds` (
  `id` int NOT NULL,
  `raw_audio_bytes` longblob NOT NULL,
  `class_1` text NOT NULL,
  `class_2` text NOT NULL,
  `class_3` text NOT NULL,
  `class_4` text NOT NULL,
  `class_5` text NOT NULL,
  `class_1_percent` float NOT NULL,
  `class_2_percent` float NOT NULL,
  `class_3_percent` float NOT NULL,
  `class_4_percent` float NOT NULL,
  `class_5_percent` float NOT NULL,
  `decibel_reading` float NOT NULL,
  `record_datetime` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

# Reporting using the Raw Data
The following SQL script can be used to run a report on the occurrence of dog barks in the data.
### Dataset Example:
```
sound	                   class avg(decibel_reading) count(*)	
--------------------------------------------------------------
"Domestic animals, pets",  4,	 -32.06690931320190,  2	
"Domestic animals, pets",  3,	 -38.41637420654297,  1	
Dog,	                   5,	 -44.81098556518555,  1	

```
### SQL
```sql
with class_1_tbl as (
    SELECT 
    class_1 as 'sound', 1 as 'class', avg(decibel_reading), count(*)
    from raw_sounds 
    group by 1,2  
    ORDER BY `count(*)` DESC
),

class_2_tbl as 
(
    SELECT 
    class_2 as 'sound', 2 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by 1,2  
    ORDER BY `count(*)` DESC
),

class_3_tbl as 
(
    SELECT 
    class_3 as 'sound', 3 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by class_3  
    ORDER BY `count(*)` DESC
),

class_4_tbl as 
(
    SELECT 
    class_4 as 'sound', 4 as 'class',avg(decibel_reading), count(*)
    from raw_sounds 
    group by class_4  
    ORDER BY `count(*)` DESC
),

class_5_tbl as 
(
    SELECT 
    class_5 as 'sound', 5 as 'class',avg(decibel_reading), count(*)
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
where sound in ('Domestic animals, pets', 'Dog', 'Bark', 'Yip', 'Howl', 'Bow-wow', 'Growling', 'Whimper (dog)');

```


TODO:
- Add indexes to the database table.
- Move the user's to the database.