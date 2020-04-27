import paho.mqtt.client as mqtt
import psycopg2
import time
import os
import sys
import datetime

while True:
    connection = psycopg2.connect(user = "postgres",
                                      password = "romi2000",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "project3db")
    cur = connection.cursor()

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("Romes/#")

    def on_message(client, userdata, msg):
        # each room needs to have its room number (eg. Romes/projecttest/temperature/108.2)
        #checks for temperature
        if ("Romes/projecttest/temperature/108.2" in msg.topic): #each room needs to have its room number (eg. Romes/projecttest/temperature/108.2)
            global temp
            temp = float(msg.payload)
            print("Temp done")
            global done1
            done1 = 1

        #checks for humidity
        if ("Romes/projecttest/humidity/108.2" in msg.topic):
            global room_num
            global hum
            global timestamp
            room_num = 108.2
            timestamp = datetime.datetime.today()
            print(timestamp)
            hum = float(msg.payload)
            print("Hum done")
            global done2
            done2 = 1

        #inserting all the information to the database
        if done1+done2 == 2:
            print("Print z mqtt.")
            done1 = 0
            done2 = 0
            postgres_insert_query = """ INSERT INTO testproject3 (room_id, temperature, humidity,time_stamp) VALUES (%s,%s,%s,%s)"""
            record_to_insert = (room_num, temp, hum, timestamp)
            cur.execute(postgres_insert_query, record_to_insert)
            print("Done")


            connection.commit()
            print("Commited")
            #cur.close()
            #connection.close()
            #os.execl(sys.executable, os.path.abspath('python "C:/Users/roman/PycharmProjects/project3/mqtt_to_database.py"'), *sys.argv)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_forever()