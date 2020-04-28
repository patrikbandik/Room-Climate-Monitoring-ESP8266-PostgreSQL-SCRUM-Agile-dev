import paho.mqtt.client as mqtt
import psycopg2
import time
import os
import sys
import datetime
from time import clock

while True:
    connection = psycopg2.connect(user="postgres",
                                  password="romi2000",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="project3")
    cur = connection.cursor()


    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("baaa/#")


    def on_message(client, userdata, msg):
        # each room needs to have its room number (eg. baaa/first_f/108.2/temp)
        # checks for temperature
        if ("baaa/first_f/108.2/temp" in msg.topic):
            global temp
            temp = float(msg.payload)
            print("Temp done")
            global done1
            done1 = 1

        # checks for humidity
        if ("baaa/first_f/108.2/hum" in msg.topic):
            global room_num
            global hum
            global timestamp
            global floor_num
            room_num = 108.2
            floor_num = 1
            timestamp = datetime.datetime.today()
            print(timestamp)
            hum = float(msg.payload)
            print("Hum done")
            global done2
            done2 = 1

        if ("baaa/first_f/108.2/light" in msg.topic):
            global light
            light = int(msg.payload)
            first_time = time.perf_counter()
            print(first_time)
            global done3
            # done3 = 1
            if light == 0:
                second_time = time.perf_counter()
                print("Timer starts")
                third_time = time.perf_counter()
                if third_time - second_time == 3:
                    print("Time reached goal")
                    timer = 1
                else:
                    print("Goal not met. ")

        # inserting all the information to the database
        if done1 + done2 == 2:
            print("Print z mqtt.")
            done1 = 0
            done2 = 0
            postgres_insert_query = """ INSERT INTO baaa (room_id,floor_id,temperature, humidity,time_stamp) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (room_num, floor_num, temp, hum, timestamp)
            cur.execute(postgres_insert_query, record_to_insert)
            print("Done")

            connection.commit()
            print("Commited")
            # cur.close()
            # connection.close()
            # os.execl(sys.executable, os.path.abspath('python "C:/Users/roman/PycharmProjects/project3/mqtt_to_database.py"'), *sys.argv)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_forever()
