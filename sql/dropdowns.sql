SELECT * FROM master_geom LIMIT 100;

--// join_type (survey type) = prad
SELECT DISTINCT county FROM master_geom WHERE join_type = 'prad' ORDER BY county ASC;
SELECT DISTINCT subdivisio FROM master_geom WHERE join_type = 'prad' and county = 'Randall' ORDER BY subdivisio ASC;
SELECT DISTINCT unit_numbe FROM master_geom WHERE join_type = 'prad' and county = 'Randall' AND subdivisio = 'CANYON EAST' ORDER BY unit_numbe ASC;
SELECT DISTINCT block_numb FROM master_geom WHERE join_type = 'prad' and county = 'Randall' and subdivisio = 'CANYON EAST' AND unit_numbe = '1' ORDER BY block_numb ASC;
SELECT DISTINCT lot_number FROM master_geom WHERE join_type = 'prad' and county = 'Randall' and subdivisio = 'CANYON EAST' AND unit_numbe = '1' and block_numb = '0001' ORDER BY lot_number ASC;


--// join_type (survey type) = rural
SELECT DISTINCT county FROM master_geom WHERE join_type = 'rural' ORDER BY county ASC;
SELECT DISTINCT l1surnam FROM master_geom WHERE join_type = 'rural' and county = 'Tom Green' ORDER BY l1surnam ASC;
SELECT DISTINCT l2block FROM master_geom WHERE join_type = 'rural' and county = 'Tom Green' AND l1surnam = 'H&TC RR CO' ORDER BY l2block ASC;
SELECT DISTINCT l3surnum FROM master_geom WHERE join_type = 'rural' and county = 'Tom Green' AND l1surnam = 'H&TC RR CO' and l2block = '16' ORDER BY l3surnum ASC;

--// join_type (survey type) = plss
SELECT DISTINCT county FROM master_geom WHERE join_type = 'plss' ORDER BY county ASC;
SELECT DISTINCT meridian FROM master_geom WHERE join_type = 'plss' and county = 'Beaver' ORDER BY meridian ASC;
SELECT DISTINCT t_r FROM master_geom WHERE join_type = 'plss' and county = 'Beaver' AND meridian = '11' ORDER BY t_r ASC;
SELECT DISTINCT section FROM master_geom WHERE join_type = 'plss' and county = 'Beaver' AND meridian = '11' and t_r = '01-20' ORDER BY section ASC;
