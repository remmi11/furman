import psycopg2
import shutil
import os
import re


# from PyPDF2 import PdfFileReader, PdfFileMerger

dir_path = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(dir_path, 'copies_100')

database="new"
user="postgres"
password="pass"
host="localhost"
port="5432"

conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

if conn:
    print "Opened database successfully"
    cur = conn.cursor()

else:
    print "[ ERROR ] Could not connect to database"

def commitQuery(query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return conn
    return cur

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def prepSrcUrl():

    # Creates well formatted table from previously generated form sample table
    # generated table contains columns "WTSToGDIUrl", "FormType", "YearJobCompleted", "JoinFieldWebMap", "JobNumber", "id(serial)", and job file src URL ("copyURL")

    query = """
                --// add primary key field
                DROP TABLE IF EXISTS copy_100;
                SELECT "WTSToGDIUrl", "FormType", "YearJobCompleted", "JoinFieldWebMap", "JobNumber" INTO copy_100 FROM form_100;
                ALTER TABLE copy_100 ADD COLUMN id SERIAL PRIMARY KEY;
                ALTER TABLE copy_100 ADD COLUMN "copyURL" character varying(300);
                UPDATE copy_100 set "copyURL" = 
                concat_ws('\\',
                "WTSToGDIUrl"::text,
                "FormType"::text,
                "YearJobCompleted"::text,
                "JoinFieldWebMap"::text,
                "JobNumber"::text )
            """

    commitQuery(query)
    #conn.close()


def createFolderPath():

    # This function copies job folders to local drive using copy table
    #

    query = """SELECT "id", "project_no", "map_no" FROM form_all"""

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    for row in cur:
        #do something with every single row here
        #optionally print the row

        if row[1] is not None and any(c.isalpha() for c in row[1]) == False:
            print row[1] + " is proper"
            src = row[1]
            if int(src[:2]) in range(15,20):
                yearfolder = 'dwg{0}' .format(src[:2])
                query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\\DWG\\', '{0}', '\\', '{1}', '\\', '{2}');""" .format(yearfolder, row[2], row[1])

            elif int(src[:2]) in range(0,15):
                yearfolder = '20{0} Scanned Documents' .format(src[:2])
                query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\\\IR 2008\\', '{0}', '\\', '{1}');""" .format(yearfolder, row[1])
           
            elif int(src[:2]) in range(50,100):
                yearfolder = '19{0} Scanned Documents' .format(src[:2])
                query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\\\IR 2008\\', '{0}', '\\', '{1}');""" .format(yearfolder, row[1])
            else:
                yearfolder= ""
            print src  + " " + yearfolder

        elif row[1] is not None:
            print row[1] + " is alphanumeric"


        else:
            str(row[0]) + " has none value"

        # if row[1] is not None and row[1][:1].upper() != 'D':
        #     src = row[1]
        #     if int(src[:2]) in range(15,20):
        #         yearfolder = 'dwg{0}' .format(src[:2])
        #         query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\DWG\', '{0}', '\\', '{1}', '\\', '{2}');""" .format(yearfolder, row[2], row[1])

        #     elif int(src[:2]) in range(0,15):
        #         yearfolder = '20{0} Scanned Documents' .format(src[:2])
        #         query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\IR 2008\', '{0}', '\\', '{1}');""" .format(yearfolder, row[1])
           
        #     elif int(src[:2]) in range(50,100):
        #         yearfolder = '19{0} Scanned Documents' .format(src[:2])
        #         query2 = """UPDATE form_all SET "folder_path" = concat('192.168.1.30:\\IR 2008\', '{0}', '\\', '{1}');""" .format(yearfolder, row[1])
        #     else:
        #         yearfolder= ""
        #     print src  + " " + yearfolder
        
        # else:
        #     print 'ID: ' + str(row[0]) + ' is not proper.'


        
        #dst = os.path.join(rootPath, os.path.basename(os.path.normpath(src)))
        commitQuery(query2)
        # try:
        #     print ""
        #     print src
        #     print dst
        #     shutil.copytree(src, dst)

        # except:
        #     pass

    conn.close()

    global rootPath


def updateFolderURL():

    # Update well formatted copy table before joining to points table
    #  ex. - https://s3.us-east-2.amazonaws.com/flsarchives/200046/

    query = """
                ALTER TABLE copy_100 ADD COLUMN "aws_link" character varying(300);
                UPDATE copy_100 SET "aws_link" =
                concat_ws('/',
                'https://s3.us-east-2.amazonaws.com/flsarchives', 
                "JobNumber"::text,
                "JobNumber"::text         
                );
            """

    query2 = """UPDATE copy_100 SET "aws_link" = concat("aws_link"::text, '_merged.pdf');"""
    commitQuery(query)
    commitQuery(query2)


def selectDuplicate():
    query = """
            --//check for duplicates in apex_pts
            select * from form ou
            where (select count(*) from form inr
            where inr."JobNumber" = ou."JobNumber") > 1
            """

            # ST_Y(apex_pts.geom) AS lat,
            # ST_X(apex_pts.geom) AS long


def mergePDF():

        rootPath = os.path.join(dir_path, 'copies_100')
        jobNumbers = []
        pdfList = []
        merger = PdfFileMerger()

        for jobNumber in os.listdir(rootPath):

            print '{' + jobNumber + '}'

            os.chdir(os.path.join(rootPath, jobNumber))

            #for root, dirs, files in os.walk(os.getcwd()):
            for dirpath, dirnames, filenames in os.walk(os.getcwd()):
                    print '########################################################'
                    current = os.getcwd()
                    print current
                    print '########################################################'
                    for filename in filenames:
                        # Search only pdfs
                        if filename.endswith(('.pdf','.PDF')):
                            pdf = os.path.abspath(filename)
                            mergedJob = "{0}_merged.pdf".format(jobNumber)
                            try:
                                ## merger.append(PdfFileReader(open(os.path.join('mypdfs', fname), 'rb')))
                                merger.append(PdfFileReader(pdf, "rb"))
                                merger.write(os.path.join(current,mergedJob))
                                pdfList.append(pdf)
                            except:
                                print jobNumber + '\n'

                    merger = PdfFileMerger()
                    print pdfList
                    pdfList = []
                    print ''
                    print ''
        count = 1

        # for row in cur:
        #     #do something with every single row here
        #     #optionally print the row
        #     rootPath = os.path.join(dir_path, 'copies_100')
        #     src = row[1]
        #     dst = os.path.join(rootPath, os.path.basename(os.path.normpath(src)))
            
        #     try:
        #         print dst
        #         shutil.copytree(src, dst)
        #     except:
        #         f.write(src + '\n')


createFolderPath()