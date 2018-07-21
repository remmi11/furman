SELECT * FROM form_500 WHERE project_no = '1618114';
SELECT DISTINCT subdivision from form_500 ORDER BY subdivision;
SELECT COUNT(*) from form_500 WHERE subdivision IS NULL;
SELECT DISTINCT survey_type from form_500;
SELECT * FROM form_500 WHERE subdivision IS NULL;
UPDATE form_500 SET survey_type = 'rural' WHERE subdivision IS NULL;
UPDATE form_500 SET survey_type = 'prad' WHERE subdivision IS NOT NULL;

SELECT * FROM form_500 WHERE project_no = '1010860';
SELECT DISTINCT unit FROM form_500 WHERE survey_type = 'prad' ORDER BY unit;
UPDATE form_500 SET unit = 'prad' WHERE subdivision IS NOT NULL;
