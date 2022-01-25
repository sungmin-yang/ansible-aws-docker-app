 CREATE TABLE random1m (
 	uuid UUID, 			-- 16 bytes
     date DATE,			--  4 bytes
 	numb  REAL,			--  4 bytes
     text VARCHAR(10)	-- 10 bytes
 );

INSERT INTO random1m (uuid, date, numb, text)

	SELECT 
		gen_random_uuid(),
		time,
		round((random() * 200)::NUMERIC, 3),
		substr(md5(random()::text), 0, 10)
	FROM
		generate_series(now() + interval '1 day',
						now() + interval '1000000 day',
						interval '1 day') AS time
;