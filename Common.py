import datetime
import re


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


