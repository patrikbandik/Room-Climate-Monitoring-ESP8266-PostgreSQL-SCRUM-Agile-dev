#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
int sensor = A0;
int sensorvalues = 0;
// Update these with values suitable for your network.

#define DHTP 2
#define DHTTYPE DHT22

DHT dht(DHTP, DHTTYPE);

const char* ssid = "ZH2O";
const char* password = "XwpfnCcy";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
char msg2[80];
char msg3 [80];
char msg4 [80];
char msg5 [80];
char msg6 [80];

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
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
     sensorvalues = analogRead(sensor);
    Serial.print("The voltage is: ");
    Serial.println(sensorvalues);
    float voltage = sensorvalues * (3.3/1023);
    Serial.print("The voltage: ");
    Serial.println(voltage);
    float temp = (voltage*1000 -500)/10;
    Serial.print("Temperature is: ");
    Serial.println(temp);
    delay(2000);
    snprintf (msg, 50,"%.2f",temp);  
    
    float hum;
    float temperature;
    Serial.println(msg);

   // snprintf (msg2, 50, "%.2f",high); 
    //snprintf (msg3 , 50, "%.2f", low);
    //snprintf (msg4,50, "%.2f", normal);
    hum = dht.readHumidity();
    temperature = dht.readTemperature();
   
   
    snprintf (msg5 , 50, "%.2f", hum);
    Serial.print("Humidity is:");
    Serial.println(hum);
    snprintf (msg6,50, "%.2f", temperature);
    Serial.print("Temperature is:");
    Serial.println(temperature);
    //client.publish("Romes/temperature", msg);
    //client.publish("Romes/humidity",msg5);
    client.publish("baaa/first_f/108.2/temp",msg6);
    client.publish("baaa/first_f/108.2/hum",msg5);
    Serial.print("Sleep");
    delay(3000); //300000 for 5 min sleep 
    
