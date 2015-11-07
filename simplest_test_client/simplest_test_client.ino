#include <ESP8266WiFi.h>




const char ssid[]     = "zsbnet";
const char password[] = "zsuperben";

IPAddress host        = IPAddress(192, 168, 0, 201);
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

  int soil = analogRead(A0);
  WiFiClient client;
  Serial.printf("Instanciated Client.\n");
  Serial.printf("zone=%d plant=%d soil=%d \n", zone, plant, soil);
  client.connect(host, port);
  Serial.printf("Connected\n");
  client.printf("zone=%d plant=%d soil=%d", zone, plant, soil);
  client.flush();
  client.println("Salut!");
  client.stop();
  delay(1000 * 60 * 2);
}
