import psycopg2

# DESCRIPTION:
#
# WHAT FOR:  sxf2pg's 2nd mode - all maps in 1 tables's set with multiple styles
# WHAT DO:   rollback given map in table set
#

def deleteRowsInTables(_sxfMapName):
    # delete rows of given map in common set
    # 1. search by name in metadata table (loaded_sxf_maps)
    # 2. cascade deleting by map id in current scale tables set

    print "Search and delete " + _sxfMapName + " map rows from common set..." 
    _sxfMapName = "%" + _sxfMapName + "%" # percents for postgres pattern-search

    h = 'dozor642'
    d = 'sxf_osm'
    u = 'innotest'
    p = 'innotest'

    conn = psycopg2.connect(host=h, database=d, user=u, password=p)
    cur = conn.cursor()

    query = "DELETE FROM loaded_sxf_maps WHERE map_id = (SELECT map_id FROM loaded_sxf_maps WHERE map_name LIKE %s);"
    print "SQL: " + query
    cur.execute(query, [_sxfMapName])
    print "POSTGRES: " + cur.statusmessage

    if cur.rowcount == 0:
        print "ERROR: no such map in database. Abort."
        cur.close()
        conn.close()
        return

    # Make the changes to the database persistent (?)
    conn.commit()
    
    cur.close()
    conn.close()

    print "OK. Map deleted" 

def showAllMapsInDatabase(_scale):
    
    print "Maps stored in database of " + _scale + " scale:"
    
    h = 'dozor642'
    d = 'sxf_osm'
    u = 'innotest'
    p = 'innotest'

    conn = psycopg2.connect(host=h, database=d, user=u, password=p)
    cur = conn.cursor()

    query = "SELECT map_name FROM loaded_sxf_maps WHERE scale = %s;"
    cur.execute(query, [_scale])
    print "POSTGRES: " + cur.statusmessage

    if cur.rowcount == 0:
        print "WARNING: maps of given scale not found."
        cur.close()
        conn.close()
        return

    # TODO: by field index
    for rec in cur:
        print rec

    # Make the changes to the database persistent
    conn.commit()

    cur.close()
    conn.close()

# ENTRY POINT
if __name__ ==  "__main__":

    import sys
    
    if len(sys.argv) == 1:
        print """
        Usage modes:
            1. rollback_sxfmap.py -f <filename> ('.sxf' not neccesary)"
            2. rollback_sxfmap.py -sm <scale> (Show Maps of given scales in database)
        """
    elif len(sys.argv) == 2:
            sxfMapName = sys.argv[1]
            deleteRowsInTables(sxfMapName)
    elif len(sys.argv) == 3:
            if sys.argv[1] == '-sm':
                scale = sys.argv[2]
                showAllMapsInDatabase(scale)
    print "OK. Exit"

