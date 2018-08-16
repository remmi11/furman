--////////////////////////////////////
--// select within
--////////////////////////////////////

--// upload and reproject prad data
-- ALTER TABLE prad_2018 
-- ALTER COLUMN geom 
-- TYPE Geometry(Point, 4326) 
-- USING ST_Transform(geom, 4326);

ALTER TABLE pts_so_far 
ALTER COLUMN geom 
TYPE Geometry(Point, 2275) 
USING ST_Transform(geom, 2275);

ALTER TABLE master_geom
ALTER COLUMN geom TYPE geometry(Point,2275)
USING ST_SetSRID(geom,2275);

-- ALTER TABLE master_geom
-- ALTER COLUMN geom TYPE geometry(Point,4326)
-- USING ST_SetSRID(geom,4326);

-- ALTER TABLE prad_2018
-- ALTER COLUMN geom TYPE geometry(Point,4326)
-- USING ST_SetSRID(geom,4326);

CREATE INDEX prad_2018_idx on prad_2018 USING GIST (geom);

ALTER TABLE prad_2018_selected ALTER COLUMN lot_number TYPE varchar(20);

ALTER TABLE apex_pts_prad DROP COLUMN city;
ALTER TABLE apex_pts_prad DROP COLUMN state;
ALTER TABLE apex_pts_prad DROP COLUMN surveyor;

--// union
DROP TABLE IF EXISTS pts_so_far;
SELECT * 
INTO pts_so_far
FROM
apex_pts_prad
UNION ALL
SELECT * 
FROM 
golladay_pts_prad;

ALTER TABLE pts_so_far 
ALTER COLUMN geom 
TYPE Geometry(Point, 2275) 
USING ST_Transform(geom, 2275);

SELECT COUNT(*) 
FROM prad_2018 a INNER JOIN pts_so_far b
 ON ST_DWithin(a.geom, b.geom, 10) AND a.lot_number is null;

DROP TABLE IF EXISTS prad_2018_c;
SELECT 
a.account_nu, 
a.map_number, 
a.lot_number :: character varying(20), 
a.block_numb,
a.subdivisio,
a.unit_numbe,
a.address,
a.street,
a.street_pfx,
a.street_sfx,
a.zip,
a.county,
a.city,
a.geom, 
b.lot_number AS edited_lot
INTO prad_2018_c
FROM prad_2018 a INNER JOIN pts_so_far b
ON ST_DWithin(a.geom, b.geom, 10) AND a.lot_number is null;



--///////////////////////////////////////////////////////
--// Phase 1 (Selection) a + b = c
--///////////////////////////////////////////////////////

--// SELECT NEW RECORDS THAT OVERLAP MASTER AND ARE NULL
-- DROP TABLE IF EXISTS prad_2018_c;
-- SELECT 
-- a.id, 
-- a.account_nu, 
-- a.group_numb, 
-- a.addition_n, 
-- a.parcel_num, 
-- a.map_number, 
-- a.lot_number :: character varying(20), 
-- a.block_numb,
-- a.subdivisio,
-- a.unit_numbe,
-- a.address,
-- a.parcel_cou,
-- a.parcel_typ,
-- a.street,
-- a.street_pfx,
-- a.street_sfx,
-- a.zip,
-- a.county,
-- a.city,
-- a.edit_date,
-- a.edit_by,
-- a.geom, 
-- b.lot_number AS edited_lot
-- INTO prad_2018_c
-- FROM prad_2018 a INNER JOIN master_geom b
--  ON ST_DWithin(a.geom, ST_Transform(b.geom, 2275), 10) AND a.lot_number is null;

-- ALTER TABLE prad_2018_selected
-- ALTER COLUMN geom TYPE geometry(Point,4326)
-- USING ST_SetSRID(geom,4326);

CREATE INDEX prad_2018_c_idx ON prad_2018_c USING
gist(geom);

UPDATE prad_2018_c SET lot_number = edited_lot;

ALTER TABLE prad_2018_c DROP COLUMN edited_lot;



--///////////////////////////////////////////////////////
--// Phase 2 (append) c + a = d
--///////////////////////////////////////////////////////

-- ALTER TABLE prad_2018 DROP COLUMN m_country;
-- ALTER TABLE prad_2018 DROP COLUMN shape_leng;
-- ALTER TABLE prad_2018 DROP COLUMN shape_area;
-- ALTER TABLE prad_2018 DROP COLUMN m_zip;
-- ALTER TABLE prad_2018 DROP COLUMN m_state;
-- ALTER TABLE prad_2018 DROP COLUMN m_city;
-- ALTER TABLE prad_2018 DROP COLUMN m_addr_1;
-- ALTER TABLE prad_2018 DROP COLUMN m_addr_2;
-- ALTER TABLE prad_2018 DROP COLUMN owner1;
-- ALTER TABLE prad_2018 DROP COLUMN owner2;
-- ALTER TABLE prad_2018 DROP COLUMN owner3;
-- ALTER TABLE prad_2018 DROP COLUMN parcel_cou;
-- ALTER TABLE prad_2018 DROP COLUMN parcel_typ;
-- ALTER TABLE prad_2018 DROP COLUMN group_numb;
-- ALTER TABLE prad_2018 DROP COLUMN addition_n;
-- ALTER TABLE prad_2018 DROP COLUMN parcel_num;
-- ALTER TABLE prad_2018 DROP COLUMN parcel_add;

-- ALTER TABLE prad_2018 ALTER COLUMN address TYPE varchar(20);
-- 
-- ALTER TABLE prad_2018_C DROP COLUMN parcel_num;
-- ALTER TABLE prad_2018_c DROP COLUMN group_numb;
-- ALTER TABLE prad_2018_c DROP COLUMN addition_n;
-- ALTER TABLE prad_2018_c DROP COLUMN parcel_cou;
-- ALTER TABLE prad_2018_c DROP COLUMN parcel_typ;
-- 
-- ALTER TABLE prad_2018_c ALTER COLUMN address TYPE varchar(20);
-- 
-- ALTER TABLE prad_2018 ALTER COLUMN address TYPE varchar(20);

SELECT * FROM prad_2018_c LIMIT 100;

--// perform intersect in qgis delete from prad_2018 where lot number null

-- ALTER TABLE prad_2018 DROP COLUMN id;
-- ALTER TABLE prad_2018_c DROP COLUMN id;


--//rearrange prad_2018 colmns to prepare for union
CREATE TABLE prad_2018_insert
(
  account_nu character varying(13),
  map_number character varying(12),
  lot_number character varying(10),
  block_numb character varying(5),
  subdivisio character varying(33),
  unit_numbe character varying(10),
  address character varying(20),
  street character varying(22),
  street_pfx character varying(2),
  street_sfx character varying(6),
  zip character varying(5),
  county character varying(7),
  city character varying(18),
  geom geometry(Point,2275)
)
--// rearrange cont'd...
insert into prad_2018_insert(
account_nu,
map_number, 
lot_number, 
block_numb, 
subdivisio, 
unit_numbe, 
address, 
street, 
street_pfx, 
street_sfx, 
zip, 
county, 
city, 
geom
) 
select
account_nu,
map_number, 
lot_number, 
block_numb, 
subdivisio, 
unit_numbe, 
address, 
street, 
street_pfx, 
street_sfx, 
zip, 
county, 
city, 
geom
from prad_2018;

--//union prad_c with prad aggregate
SELECT *
INTO prad_2018_too_many
FROM
 prad_2018_insert
UNION ALL
SELECT *
FROM
 prad_2018_c;


--//////////////////////////////////////////////////////////////////////////////////
--// Phase 3 (remove) remove from d where a.acct = c.acct AND a.lot_number is null
--//////////////////////////////////////////////////////////////////////////////////

--// DELETE DUPLICATES SAVE WHERE LOT_NUMBER IS NOT NULL;
DELETE
FROM
    prad_2018_too_many a 
        USING prad_2018_too_many b
WHERE
    a.account_nu = b.account_nu
    AND a.lot_number is null AND b.lot_number IS NOT NULL;


--//////////////////////////////////////////////////////////////////////////////////
--// Phase 4 --// MERGE W/ master_geom;
--//////////////////////////////////////////////////////////////////////////////////

ALTER TABLE prad_2018_too_many ADD COLUMN meridian character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN township character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN _range character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN section character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN t_r character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN l1surnam character varying(32);
ALTER TABLE prad_2018_too_many ADD COLUMN l2block character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN l3surnum character varying(8);
ALTER TABLE prad_2018_too_many ADD COLUMN state character varying(10);
ALTER TABLE prad_2018_too_many ADD COLUMN join_type character varying(50);
ALTER TABLE prad_2018_too_many ADD COLUMN join_field character varying(200);
ALTER TABLE prad_2018_too_many ADD COLUMN mtrs character varying(20);

UPDATE master_geom SET join_type = 'prad' WHERE length(subdivisio) > 3;
UPDATE master_geom SET join_type = 'rural' WHERE subdivisio = '0' and length(mtrs) > 3;
UPDATE master_geom SET join_type = 'plss' WHERE length(mtrs) > 3; 

-- SELECT DISTINCT join_type FROM master_geom;
-- 
-- DELETE FROM master_geom where join_type = 'prad';
-- 
-- ALTER TABLE prad_2018_too_many ALTER COLUMN county TYPE varchar(50);
-- 


CREATE TABLE prad2many
(
  geom geometry(Point,4326),
  mtrs character varying(20),
  meridian character varying(10),
  township character varying(10),
  _range character varying(10),
  section character varying(10),
  t_r character varying(10),
  county character varying(50),
  l1surnam character varying(32),
  l2block character varying(10),
  l3surnum character varying(8),
  state character varying(10),
  join_type character varying(50),
  join_field character varying(200),
  account_nu character varying(20),
  map_number character varying(20),
  lot_number character varying(20),
  block_numb character varying(10),
  subdivisio character varying(50),
  unit_numbe character varying(10),
  address character varying(20),
  street character varying(50),
  street_pfx character varying(2),
  street_sfx character varying(10),
  zip character varying(10),
  city character varying(25)
)


--// reproject here
ALTER TABLE prad_2018_too_many 
ALTER COLUMN geom 
TYPE Geometry(Point, 4326) 
USING ST_Transform(geom, 4326);

INSERT INTO prad2many(
geom, 
mtrs, 
meridian, 
township, 
_range, 
section, 
t_r, 
county, 
l1surnam, 
l2block, 
l3surnum, 
state, 
join_type, 
join_field,
account_nu,
map_number,
lot_number,
block_numb,
subdivisio,
unit_numbe,
address,
street,
street_pfx,
street_sfx,
zip,
city
)
SELECT geom, 
mtrs, 
meridian, 
township, 
_range, 
section, 
t_r, 
county, 
l1surnam, 
l2block, 
l3surnum, 
state, 
join_type, 
join_field,
account_nu,
map_number,
lot_number,
block_numb,
subdivisio,
unit_numbe,
address,
street,
street_pfx,
street_sfx,
zip,
city
FROM prad_2018_too_many;

ALTER TABLE master_geom DROP COLUMN id; -- SERIAL PRIMARY KEY

SELECT DISTINCT subdivisio FROM prad2many ORDER BY subdivisio;
SELECT COUNT(*) FROM prad2many WHERE subdivisio is null;
DELETE FROM prad2many WHERE subdivisio is null;
SELECT COUNT(*) FROM prad2many WHERE subdivisio = '';

SELECT *
INTO master_geom_2
FROM
 master_geom
UNION ALL
SELECT *
FROM
 prad2many;

ALTER TABLE master_geom_2 ADD COLUMN id SERIAL PRIMARY KEY

DROP TABLE master_geom;

ALTER TABLE master_geom_2 RENAME TO master_geom;

-- ALTER TABLE master_geom
-- ALTER COLUMN geom 
-- TYPE Geometry(Point, 4326) 
-- USING ST_Transform(geom, 4326);

ALTER TABLE master_geom
ALTER COLUMN geom TYPE geometry(Point,4326)
USING ST_SetSRID(geom,4326);

CREATE INDEX master_geom_idx on master_geom USING GIST (geom);

DELETE FROM master_geom WHERE subdivisio LIKE 'SECT %';


--/////////////////////////////////////////////////////////////
--// UPDATE master_geom table with join_types and join_fields
--/////////////////////////////////////////////////////////////

SELECT DISTINCT join_type FROM master_geom;

UPDATE master_geom SET join_type = 'prad' WHERE length(subdivisio) > 3;
UPDATE master_geom SET join_type = 'rural' WHERE subdivisio = '0' and length(mtrs) > 3;
UPDATE master_geom SET join_type = 'plss' WHERE length(mtrs) > 3; 

SELECT * FROM master_geom WHERE join_type = 'prad' limit 200;
SELECT * FROM master_geom WHERE join_type = 'plss' limit 200;
SELECT * FROM master_geom WHERE join_type = 'rural' limit 200;

UPDATE master_geom SET block_numb = 'NO BLOCK' WHERE block_numb IS NULL AND join_type = 'prad';
UPDATE master_geom SET lot_number = 'NO LOT' WHERE lot_number IS NULL AND join_type = 'prad';
UPDATE master_geom SET unit_numbe = '1' WHERE unit_numbe IS NULL AND join_type = 'prad';

update master_geom set join_field = county || '\' || subdivisio || '\' || unit_numbe || '\' || block_numb || '\' || lot_number WHERE join_type = 'prad';
update master_geom set join_field = county || '\' || l1surnam || '\' || l2block || '\' || l3surnum WHERE join_type = 'rural';
update master_geom set join_field = county || '\' || meridian || '\' || t_r || '\' || section WHERE join_type = 'plss';

DROP TABLE prad2many;
DROP TABLE prad_2018_insert;
DROP TABLE prad_2018_c;
DROP TABLE prad_2018_too_many;

SELECT * FROM master_geom WHERE subdivisio LIKE 'UNIV%';