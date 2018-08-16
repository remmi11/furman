--\\ prad
\copy form_all_furman(prad_acct, prad_acct_gis, date_entered,	date_needed, project_no, map_no, address_street, rural_section, rural_block, survey, county, clerksfile, book, page, sub_block, lot, subdivision, notes, contact, phone, city, state, zipcode, lender, gf_no, certify_to, client, cancelled, requested_by, filed, surveyor, title) FROM 'C:\Users\Noah\Desktop\django_form\sql\furman_landdatabase.csv' DELIMITER ',' CSV HEADER;
prad_acct, prad_acct_gis, date_entered,	date_needed, project_no, map_no, address_street, rural_section, rural_block, survey, county, clerksfile, book, page, sub_block, lot, subdivision, notes, contact, phone, city, state, zipcode, lender, gf_no, certify_to, client, cancelled, requested_by, filed, surveyor


--\\ canadian
\copy form_all_canadian(county, meridian, t_r, plss_section, subdivision, unit, sub_block, lot, survey, rural_block, rural_section, date_entered, project_no, address_street, requested_by, clerksfile, book, page, filed, surveyor, notes, well_name, well_number, contact, phone, city, state, zipcode, lender, gf_no, certify_to, title, client, date_needed, cancelled) FROM 'C:\Users\Noah\Desktop\django_form\sql\canadian_landdatabase.csv' DELIMITER ',' CSV HEADER;
county, meridian, t_r, plss_section, subdivision, unit, sub_block, lot, survey, rural_block, rural_section, date_entered, project_no, address_street, requested_by, clerksfile, book, page, filed, surveyor, notes, well_name, well_number, contact, phone, city, state, zipcode, lender, gf_no, certify_to, title, client, date_needed, cancelled

--// union 
SELECT * 
INTO form_all_both
FROM
form_all_furman
UNION ALL
SELECT * 
FROM 
form_all_canadian;

ALTER TABLE form_all DROP COLUMN id;
ALTER TABLE form_all_canadian DROP COLUMN id;

ALTER TABLE form_all DROP COLUMN user_id;
ALTER TABLE form_all_canadian DROP COLUMN user_id;

ALTER TABLE form_all DROP COLUMN updated_at;
ALTER TABLE form_all_canadian DROP COLUMN updated_at;

ALTER TABLE form_all DROP COLUMN created_at;
ALTER TABLE form_all_canadian DROP COLUMN created_at;

ALTER TABLE form_all_both ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE form_all_both ADD COLUMN updated_at timestamp;
ALTER TABLE form_all_both ADD COLUMN created_at timestamp;
ALTER TABLE form_all_both ADD COLUMN user_id integer;

ALTER TABLE form_all_both RENAME TO form_all;
ALTER TABLE form_all ADD COLUMN id SERIAL PRIMARY KEY;

UPDATE form_all SET title = 'GDI-CANADIAN' WHERE project_no LIKE '2%'

--// update join_type and join_field
SELECT DISTINCT survey_type FROM form_all;

UPDATE form_all SET survey_type = 'prad' WHERE title LIKE 'Furman%' AND length(subdivision) > 3;
UPDATE form_all SET join_type = 'prad' WHERE length(subdivisio) > 3;
UPDATE form_all SET survey_type = 'rural' WHERE length(survey) > 3;
UPDATE form_all SET survey_type = 'plss' WHERE length(t_r) > 3; 


UPDATE form_all SET survey_type = 'prad' WHERE title LIKE 'Furman%' AND subdivision is not null;
UPDATE form_all SET block_numb = 'NO BLOCK' WHERE block_numb IS NULL AND join_type = 'prad';
UPDATE form_all SET lot_number = 'NO LOT' WHERE lot_number IS NULL AND jnoin_type = 'prad';

ALTER TABLE form_all ADD COLUMN join_field character varying(255);

update form_all set join_field = county || '\' || subdivision || '\' || unit || '\' || sub_block || '\' || lot WHERE survey_type = 'prad';
update form_all set join_field = county || '\' || survey || '\' || rural_block || '\' || rural_section WHERE survey_type = 'rural';
update form_all set join_field = county || '\' || meridian || '\' || t_r || '\' || plss_section WHERE survey_type = 'plss';

UPDATE form_all SET project_no = LPAD(project_no::text, 7, '0') WHERE project_no = '180';
