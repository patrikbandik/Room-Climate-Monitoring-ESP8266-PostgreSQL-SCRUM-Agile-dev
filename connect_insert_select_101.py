import psycopg2

#connect to the db
con = psycopg2.connect(
            host = "localhost",
            database = "MyDatabase",
            user = "postgres",
            password = "ubuntu")
#cursor
cur = con.cursor()

#insert
cur.execute("insert into iot_data (gps_positionx, gps_positiony, messtype)" \
            "values (%s, %s, %s)", (69.44, 96.6574, 'Cottage'))

#select (you should select only things that you are using)
cur.execute("select * from iot_data")

rows = cur.fetchall()

for r in rows:
    print(f"data_id{r[0]} gps_positionx {r[1]} gps_positiony {r[2]} " \
          "messtype: {r[3]} ; timestamp {r[4]}")
    print("")

#commit the changes
con.commit()
#close cursor
cur.close()
#close the connection
con.close()
