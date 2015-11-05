#include <ESP8266WiFi.h>

const char ssid[]     = "zsbnet";
const char password[] = "zsuperben";

IPAddress host        = IPAddress(192,168,0,2);
const int port        = 8080;

const short int zone = 10;
const short int plant = 42;


void setup() {
    Serial.begin(115200);
    delay(10);
    WiFi.begin(ssid, password);
    Serial.println("Wifi Started...");
    

}

void loop() {
  // put your main code here, to run repeatedly:
    WiFiClient client;
    client.connect(host, port);
    int soil = analogRead(A0);
    client.printf("zone=%d plant=%d soil=%d", zone, plant, soil);
    client.println("Salut!");
    client.stop();
    delay(1000*60*2);

}
