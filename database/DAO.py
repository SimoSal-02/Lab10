from database.DB_connect import DBConnect
from model.coutryObj import Country


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllCountryYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.StateAbb, c.CCode, c.StateNme
                from country c,
                (select *
                from contiguity c 
                union all 
                select *
                from contiguity2006 c6
                )AS cc
                where cc.state1no = c.CCode
                and cc.year<=%s"""

        cursor.execute(query,(year,))
        for row in cursor:
            result.append(Country(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesYears(idMap,year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select cc.state1no, cc.state2no
                from (
                select *
                from contiguity c 
                union all 
                select *
                from contiguity2006 c6
                )AS cc
                where cc.year<=%s
                and cc.state1no<cc.state2no
                and cc.conttype=1
                order by state1ab asc"""


        cursor.execute(query,(year,))
        for row in cursor:
            result.append((idMap[row["state1no"]], idMap[row["state2no"]]))

        cursor.close()
        conn.close()
        return result

