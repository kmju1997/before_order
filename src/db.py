import mysql.connector

def connect_db():
    mydb = mysql.connector.connect(
    host="beforeordermysqlserver.mysql.database.azure.com",
    user="goalkeeper@beforeordermysqlserver",
    password="Christian0118!",
    database="food",
    ssl_ca="ssl_certificiate.pem"
    )
    mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_ci')
    return mydb

# retrieves information for the given dish names in foreign language
# ko_dishes will be transformed to a list as a string will be split into single letters else
# returns dictionary with database columns as keys
def get_dishes(mydb, ko_dishes):
    assert mydb != None
    # we dont need to connect to db when there are no dishes to check
    if not ko_dishes:
        return []
    # transform to list
    if type(ko_dishes) is not list:
        ko_dishes = [ko_dishes]

    # create sql cursor for querying statements, get result as dictionary
    cursor = mydb.cursor(buffered=True,dictionary=True)
    infos = []
    for ko_dish in ko_dishes:
        query = ("SELECT dish.name, dish.description, ko_en.name as 'ko_name', LOCATE(ko_en.name, '{0}') AS 'pos', LENGTH(ko_en.name) AS 'len', x.len, x.pos "
                "FROM dish, ko_en left outer join (SELECT LOCATE(ko_en.name, '{0}') AS 'pos', "
                "MAX(LENGTH(ko_en.name)) AS 'len' "
                "FROM ko_en "
                "Group by pos "
                "HAVING pos != 0) x on x.len = len "
                "WHERE dish.id = ko_en.dish_id "
                "HAVING pos != 0 AND x.len = len AND x.pos = pos "
                "ORDER BY pos".format(ko_dish))
        print(query)
        cursor.execute(query)
        for row in cursor:
                
            infos.append(row)
    cursor.close()

    if len(infos) > 0 :
        pass
        #handle for multiple results




    #if it has one or zero directly returns infos 
    return infos