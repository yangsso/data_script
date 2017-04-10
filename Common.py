# -*- coding: utf-8 -*-
import datetime
import re
import csv

import xlrd
import openpyxl

class Common():
        
        def dictall(self,cursor):

                columns = cursor.description
                result = []
                for row in cursor.fetchall():
                        result.append({columns[i][0]:value for (i,value) in enumerate(row)})

                return result

        def dictone(self, cursor):

                columns = cursor.description
                return {columns[i][0]:value for (i,value) in enumerate(cursor.fetchone())}
        
        def get_removed_emoji_str(self,text):

                try:
                # Wide UCS-4 build
                        myre = re.compile(u'['
                                u'\U0001F300-\U0001F64F'
                                u'\U0001F680-\U0001F6FF'
                                u'\u2600-\u26FF\u2700-\u27BF]+', 
                                re.UNICODE)
                except re.error:
                # Narrow UCS-2 build
                        myre = re.compile(u'('
                                u'\ud83c[\udf00-\udfff]|'
                                u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                                u'[\u2600-\u26FF\u2700-\u27BF])+', 
                                re.UNICODE)

                text = myre.sub(r'', text)

                text = re.sub(r"[']",'', text)
                
                return (text)

        def unixtime_to_datetime(self, time):

                time = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
                return time

        def utctime_to_kotime(self, time):
                
                time = re.sub('T', ' ', time)
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                time = time + datetime.timedelta(hours=9)
                return time


        def xls_to_csv(xls):
            csv_file = xls.replace('xls', 'csv')

            with xlrd.open_workbook(xls) as wb:
                sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
                with open(csv_file, 'wb') as f:
                    c = csv.writer(f)
                    for r in range(sh.nrows):
                        c.writerow(sh.row_values(r))


        def xlsx_to_csv(xlsx):
            csv_file = xlsx.replace('xlsx', 'csv')

            wb = openpyxl.load_workbook(xlsx)
            sh = wb.get_active_sheet()
            with open(csv_file, 'wb') as f:
                c = csv.writer(f)
                for r in sh.rows:
                    c.writerow([cell.value for cell in r])

