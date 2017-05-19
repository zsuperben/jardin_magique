#include <SPI.h>
#include <Ethernet.h>

#define CRITICAL 2


// Server's IP 
IPAddress server(192,168,0,201);
// Our IP 
IPAddress ip(192,168,0,228);
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x01 };

// Our client object to use the ethernet 
EthernetClient client;

// Setup code 
void setup() {
  //Always start a serial console for debugging
  Serial.begin(9600); 
  // It seems a little delay here helps getting the ethernet chip ready
  Serial.println("Booting... (Actually just waiting doing nothing...)");
  delay(5000);
  Serial.println("Starting Ethernet");
  Ethernet.begin(mac, ip);
  // Some more delay for that filthy slow ethernet thing
  Serial.println("Ethernet is starting...");
  delay(1500); 
  // We now setup our pins 
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  Serial.println(F("End of setup function"));
  Serial.println(F("~~~~~~~~~~~~~~~~~~~~~"));
  Serial.println(F(""));
 }

void loop() {
  if(client.connect(server, 8888)){
    //We are connected tell the SErial
    Serial.println(F("We are connected to the server !"));  
    request();
    delay(3600000);
  }
  // connection is not ok 
  else {
    Serial.println(F("Could not connect to server, retrying in 30 seconds"));
    delay(30000);
    }
}
const char* format = "{\"cuve\": %d}";
char destination_string[26];

void request() {
    Serial.println(F("Starting Request."));
    // Start HTTP POST
    client.println(F("POST /wateralert/ HTTP/1.1"));
    client.println(F("Host: 192.168.0.201"));
    client.println(F("Connection: Close"));
    client.println(F("User-Agent: sensor/0.2"));
    client.println(F("Content-Type: application/x-www-urlencoded"));
    Serial.println(F("Computing argument string..."));
    sprintf(destination_string, format, get_measure());
    Serial.print(destination_string);
    client.print(F("Content-length: "));
    client.print(strlen(destination_string));
    client.print(F("\r\n"));
    client.print(F("\r\n"));
    client.print(destination_string);
    client.print(F("\r\n"));
    client.flush();
    client.stop();
}

int  get_measure() {
  int ret = 100 ; 
  if (digitalRead(8)){ret = 90;}
  if( digitalRead(7)){ret = 75;}
  if( digitalRead(6)){ret = 60;}
  if( digitalRead(5)){ret = 45;}
  if(digitalRead(4)){ret = 30;}
  if (digitalRead(3)){ret = 15;}
  if (digitalRead(CRITICAL)){ret = 0;}
  return ret;
  }


