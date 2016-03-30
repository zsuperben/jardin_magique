/*
  Web client

 This sketch connects to a website (http://www.google.com)
 using an Arduino Wiznet Ethernet shield.

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13

 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe, based on work by Adrian McEwen

 */

#include <SPI.h>
#include <Ethernet.h>

#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 7
 
// Setup a oneWire instance to communicate with any OneWire devices 
// (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
 
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
IPAddress server(192,168,0,201);  // numeric IP for Google (no DNS)
//char server[] = "www.google.com";    // name address for Google (using DNS)

// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(192, 168, 0, 227);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;
const short int zone[6]  = { 1, 1, 1, 1, 1, 1 };
const short int plant[6] = { 1, 2, 3, 4, 5, 6 };








void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);

  Serial.println("Hello World!");
  delay(5000);
  // start the Ethernet connection:
//  if (Ethernet.begin(mac) == 0) {
//    Serial.println("Failed to configure Ethernet using DHCP");
//    // no point in carrying on, so do nothing forevermore:
//    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
    sensors.begin();
  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:

}

const char* fmt = "{\"zone\": %2d, \"plant\": %2d, \"soil\": %3d, \"temp\": %s }";
char dstr[128] ;
char t[6];
float tmp;
void loop()
{
  // if there are incoming bytes available
  // from the server, read them and print them:
//  if (client.available()) {
//    char c = client.read();
//    Serial.print(c);
//  }

  String req;
  Serial.println("requesting temperature...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("Done.");
  tmp = sensors.getTempCByIndex(0);
  dtostrf(tmp,2,2,t);
  Serial.print("Temp is : ");
  Serial.println(tmp, 2);
    for(int i=0;i<3;i++){
      Serial.print(F("zone="));
      Serial.print(zone[i], DEC);
      Serial.print(F("   plant="));
      Serial.print(plant[i], DEC);
      Serial.print(F("   soil="));
      Serial.print(analogRead(i),DEC);
      Serial.print(F("   for plant "));
      Serial.print(i, DEC);
      Serial.println();
    }
  if (client.connect(server, 8888)) {
    Serial.println("connected");
    bool cnx = 1 ;
    // Make a HTTP request:
    
    for(int i=0;i<3;i++){
      //client.flush();
      if(!cnx){
        client.connect(server, 8888);
      }
      Serial.print(F("What the fuck~~\n"));
      client.println(F("POST /measure/ HTTP/1.1"));
      client.println(F("Host: 192.168.0.201"));
      client.println(F("User-Agent: sensor/0.1"));
      client.println(F("Connection: close"));
      client.println(F("Content-Type: application/x-www-urlencoded"));
      Serial.println("been there");
      sprintf(dstr, fmt, zone[i], plant[i], analogRead(i), t);
      Serial.print(dstr);
      client.print(F("Content-Length: "));
      client.print(strlen(dstr));
      client.print(F("\r\n"));
      client.print(F("\r\n"));
      client.print(dstr);
      client.print(F("\r\n"));
      client.flush();
      client.stop();
      cnx =0;
      delay(10000);    

      
    }

    
  }
  else {
    // kf you didn't get a connection to the server:
    Serial.println("connection failed");
  }

    client.stop();
  // if the server's disconnected, stop the client:111111111111
  delay(1000*20);

}


