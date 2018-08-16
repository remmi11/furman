-- SELECT substring(project_no,1,3) FROM form_all WHERE project_no = '1720117';
UPDATE form_all SET project_no = LPAD(project_no::text, 7, '0') 
UPDATE form_all SET "folder_path" = concat(
'192.168.1.30:\\DWG\', 'DWG', 
substring(project_no,1,2), 
'\', 
map_no, 
'\', 
project_no
) 
WHERE 
substring(project_no,1,2) = '15' 
or 
substring(project_no,1,2) = '16' 
or 
substring(project_no,1,2) = '17' 
or 
substring(project_no,1,2) = '18';



UPDATE form_all SET "folder_path" = concat(
'192.168.1.30:\\IR 2008\', 
'20', 
substring(project_no,1,2), 
' Scanned Documents\', 
map_no, 
'\', 
project_no
)
WHERE 
substring(project_no,1,2) = '00'
OR 
substring(project_no,1,2) = '01'
OR 
substring(project_no,1,2) = '02'
OR 
substring(project_no,1,2) = '03'
OR 
substring(project_no,1,2) = '04'
OR 
substring(project_no,1,2) = '05'
OR 
substring(project_no,1,2) = '06'
OR 
substring(project_no,1,2) = '07'
OR 
substring(project_no,1,2) = '08'
OR 
substring(project_no,1,2) = '09'
OR 
substring(project_no,1,2) = '10'
OR 
substring(project_no,1,2) = '11'
OR 
substring(project_no,1,2) = '12'
OR 
substring(project_no,1,2) = '13'
OR 
substring(project_no,1,2) = '14';


UPDATE form_all SET "folder_path" = concat(
'192.168.1.30:\\IR 2008\', 
'19', 
substring(project_no,1,2), 
' Scanned Documents\',
map_no,
'\',
project_no
)
WHERE
substring(project_no,1,2) = '45'
 OR
substring(project_no,1,2) = '46'
 OR
substring(project_no,1,2) = '47'
 OR
substring(project_no,1,2) = '48'
 OR
substring(project_no,1,2) = '49'
 OR
substring(project_no,1,2) = '50'
 OR
substring(project_no,1,2) = '51'
 OR
substring(project_no,1,2) = '52'
 OR
substring(project_no,1,2) = '53'
 OR
substring(project_no,1,2) = '54'
 OR
substring(project_no,1,2) = '55'
 OR
substring(project_no,1,2) = '56'
 OR
substring(project_no,1,2) = '57'
 OR
substring(project_no,1,2) = '58'
 OR
substring(project_no,1,2) = '59'
 OR
substring(project_no,1,2) = '60'
 OR
substring(project_no,1,2) = '61'
 OR
substring(project_no,1,2) = '62'
 OR
substring(project_no,1,2) = '63'
 OR
substring(project_no,1,2) = '64'
 OR
substring(project_no,1,2) = '65'
 OR
substring(project_no,1,2) = '66'
 OR
substring(project_no,1,2) = '67'
 OR
substring(project_no,1,2) = '68'
 OR
substring(project_no,1,2) = '69'
 OR
substring(project_no,1,2) = '70'
 OR
substring(project_no,1,2) = '71'
 OR
substring(project_no,1,2) = '72'
 OR
substring(project_no,1,2) = '73'
 OR
substring(project_no,1,2) = '74'
 OR
substring(project_no,1,2) = '75'
 OR
substring(project_no,1,2) = '76'
 OR
substring(project_no,1,2) = '77'
 OR
substring(project_no,1,2) = '78'
 OR
substring(project_no,1,2) = '79'
 OR
substring(project_no,1,2) = '80'
 OR
substring(project_no,1,2) = '81'
 OR
substring(project_no,1,2) = '82'
 OR
substring(project_no,1,2) = '83'
 OR
substring(project_no,1,2) = '84'
 OR
substring(project_no,1,2) = '85'
 OR
substring(project_no,1,2) = '86'
 OR
substring(project_no,1,2) = '87'
 OR
substring(project_no,1,2) = '88'
 OR
substring(project_no,1,2) = '89'
 OR
substring(project_no,1,2) = '90'
 OR
substring(project_no,1,2) = '91'
 OR
substring(project_no,1,2) = '92'
 OR
substring(project_no,1,2) = '93'
 OR
substring(project_no,1,2) = '94'
 OR
substring(project_no,1,2) = '95'
 OR
substring(project_no,1,2) = '96'
 OR
substring(project_no,1,2) = '97'
 OR
substring(project_no,1,2) = '98'
 OR
substring(project_no,1,2) = '99';