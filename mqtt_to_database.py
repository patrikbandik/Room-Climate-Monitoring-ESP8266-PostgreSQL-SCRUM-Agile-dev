#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <EEPROM.h>
#define DHTP 14
#define DHTTYPE DHT22

DHT dht(DHTP, DHTTYPE);

const char* ssid = "ZH2O";
const char* password = "XwpfnCcy";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);

int sensor = A0;
int sensorvalues = 0;

long lastMsg = 0;
int value = 0;

float hum;
float temperature;
float light;

float gps_x;
float gps_y;

int cur_light_val;
int saved_light_val;

int EEadress2;
int EEaddress;

char msg1[50];
char msg2[80];
char msg3 [80];
char msg4 [80];
char msg5 [80];

int counter = 0;

static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
SoftwareSerial ss(4, 5);

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      //if (recon == 1):
       // Serial.println("Reconecting in 5 sec.");
      delay(300);
     // else:
       // Serial.println("Reconecting in 5 min.")
       // delay(300000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);   
  Serial.begin(115200);
  dht.begin();
   setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  EEPROM.begin(32);
  ss.begin(GPSBaud);
  pinMode(2,OUTPUT);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
   // Serial.println(msg);

   // snprintf (msg2, 50, "%.2f",high); 
    //snprintf (msg3 , 50, "%.2f", low);
    //snprintf (msg4,50, "%.2f", normal);

    
    hum = dht.readHumidity();
    temperature = dht.readTemperature();
    light = analogRead(A0);
    gps_x = 47.767958;
    gps_y = 18.095432;
    
    // 47.767958,18.095432
    
  /// while (ss.available() > 0)
    // if (gps.encode(ss.read())){
      //Serial.print(F("Location: "));
     // if (gps.location.isValid())
      //{
      //  Serial.print("Latitued: ");
      //  Serial.println(gps.location.lat(), 6);
       // Serial.print("Longtitude: ");
       // Serial.println(gps.location.lng(), 6);
      //}
     // else
     // {
       // Serial.print(F("INVALID"));
     //}
       // Serial.println();
    // }
        
    //if (millis() > 5000 && gps.charsProcessed() < 10)
    //{
     // Serial.println(F("No GPS detected: check wiring."));
     // while(true);
    //}

    digitalWrite(2,HIGH);
    
    snprintf (msg1,50, "%.2f", temperature);
    Serial.print("Temperature is:");
    Serial.println(temperature);
    
    snprintf (msg2 , 50, "%.2f", hum);
    Serial.print("Humidity is:");
    Serial.println(hum);

    if (isnan(temperature) || isnan(hum)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }


    snprintf(msg3,50,"%.2f",light);
    Serial.print("Light is:");
    Serial.println(light);

    snprintf (msg4 , 50, "%.6f",gps_x);
    Serial.print("Latitude(x): ");
    Serial.println(gps_x , 6);

    snprintf (msg5 , 50, "%.6f",gps_y);
    Serial.print("Latitude(y): ");
    Serial.println(gps_y , 6);
    

    if (light<256){
    Serial.println("Low visibility");
    analogWrite(2,0);
    cur_light_val = 1;
    }
    if (light> 256 and light<512){
    Serial.println("Bad visibility");
    analogWrite(2,40);
    cur_light_val = 2;
    }
    if (light>512 and light<768){
    Serial.print("Good visibility");
    analogWrite(2,200);
    cur_light_val = 3;
    }
    if (light>768){
     Serial.println("Max visibility");
    analogWrite(2,255);
    cur_light_val = 4;
    }
    

    client.publish("baaa/first_f/108.2/temp",msg1);
    client.publish("baaa/first_f/108.2/hum",msg2);
    client.publish("baaa/first_f/108.2/light",msg3);
    client.publish("baaa/first_f/108.2/gps_x",msg4);
    client.publish("baaa/first_f/108.2/gps_y",msg5);
    Serial.println("-----------------------------");

    
    EEadress2 = 6;
    EEaddress = 1;
    
    EEPROM.get(EEaddress,counter);
    Serial.print("Counter is:");
    Serial.println(counter);
  
    EEPROM.get(EEadress2,saved_light_val);
    Serial.print("Saved light value is:");
    Serial.println(saved_light_val);
    
    Serial.print("Measured light value:");
    Serial.println( cur_light_val);
    
     // checks for previous light values 
    if (saved_light_val == 3 and  cur_light_val == 3){ // set to 1 for dark 
      Serial.println("Room is dark. Going to sleep mode.");
      Serial.println("-----------------------------");
      delay(250);
      ESP.deepSleep(40e6); //needts to be 20 min 
    }
     
     // checks counter for sleep at end of the day
    if (counter == 13){ // needts to be 144 -- 12 times per hour for 12 hours 
      Serial.println("End of the day. Going to sleep mode."); 
      for (int i = 0 ; i < EEPROM.length() ; i++) { //Run this when u want to erase EEPROM 
        EEPROM.write(i, 0);
        EEPROM.commit();
      }
      Serial.println("EEPROM cleaned");
      Serial.println("-----------------------------");
      ESP.deepSleep(20e6); // sleep needs to be 12 hours -- 43 190 sec is 12 hours  
    }
    
    saved_light_val = cur_light_val; 
   
    EEPROM.put(EEadress2,saved_light_val);
    counter++;
    EEPROM.put(EEaddress,counter);
   
   //for (int i = 0 ; i < EEPROM.length() ; i++) { //Run this when u want to erase EEPROM 
   //EEPROM.write(i, 0);
 //}
 //Serial.println("EEPROM cleaned");
    
    EEPROM.commit();
    
    Serial.println("Data stored in memory");
    Serial.println("Going into deep sleep");
    Serial.println("-----------------------------");
    delay(250);
    ESP.deepSleep((20e6)); //cable in D0 and in RST needs to be plugged in after teh code started after deep sleep it takes cca 10 sec to reconect 
    
}
}

// for GPS
void displayInfo()
{
  Serial.print(F("Location: ")); 
  if (gps.location.isValid())
  {
    Serial.println(gps.location.lat(), 6);
    Serial.println(gps.location.lng(), 6);
  }
  else
  {
    Serial.print(F("INVALID"));
  }
  Serial.println();
}
