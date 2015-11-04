#include <ESP8266WiFi.h>
#include <EEPROM.h>


WiFiClient client ; 
IPAddress server(10,69,69,69);
unsigned long lastConnectionTime  = 0 ; 
boolean lastConnected = false ; 
const unsigned long postingInterval = 5 * 60 * 1000 ; // 5 fois 60 secondes fois 1000 : valeur en millisecondes
String name = "unconfigured" ; 

char Config[1024];



String get_config(IPAddress srv) { 
  
    String Config;
    Serial.println("Configuring parameters for first connection...") ;
    client.connect(srv, 80 ); 
    client.println("GET /configuration/get    HTTP/1.1");
    client.println("Host: www.jardin-magique.net");
    client.println("User-Agent: jardin-magique-sensor");
    client.println("From: ben@hacktopie.net");
    client.println('\r\n');
    if (client.available()) {
    char c ;
    while( c = client.read()) {
        Config += c;
      }
    }
    client.stop();
    client.flush();

    return Config;

}


String read_config_from_EEPROM(){
  char chk = EEPROM.read(1024);
  if (chk == 'Y') {
    // This is the test byte we found it is position to 'Y' ASCII
    // This means a configuration is present and can be loaded 
    for(int i=0;i<1024;i++){
      Config[i] = EEPROM.read(i); //  here we load the configuration byte per byte.
    }

    // Now we have a char Config[1024] object that contains all the configuration we will need 
    // Field Separation : '\n'
    // Key/Value separaton : '='
  }
  return String(Config);
}

typedef struct mac {
  byte addr[6];
  }


byte[6] setMac() {
  
  byte last = byte(random(0,255)) ; 
  byte more = byte(random(0,255)) ;
  return { 0xDE, 0xAD, 0xBE, 0xEF, more , last } ;  

}
  
void setup() {

  Serial.begin(9600); 


  while(!client) {
      Serial.println("Ethernet DHCP configuration not ready... retrying");
      delay(100) ; 
      
  }
  Serial.print("My IP address is : ");
  Serial.println(WiFi.localIP());

}

void loop() {
  
  
  // if there's incoming data from the net connection.
  // send it out the serial port.  This is for debugging
  // purposes only:
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }
  
  // Building up autoconfig dialog, nothing is certain. 
  // We want to get a name, and make sure this is stable through reboot.
  // DHCP config on the server is the most helping part. But here we can 
  // make sure we get a name that will be userfriendly and will be display in the UI 
/*  
  if (!client.connected() && !isConfigured) {
    get_config(server);
  }
*/  
  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }

  // if you're not connected, and ten seconds have passed since
  // your last connection, then connect again and send data:
  if(!client.connected() && (millis() - lastConnectionTime > postingInterval)) {
    httpRequest();
  }
  // store the state of the connection for next time through
  // the loop:
  lastConnected = client.connected();
}



// this method makes a HTTP connection to the server:

void httpRequest() {
  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println("POST /record/"+ name +" HTTP/1.1");
    client.println("Host: www.arduino.cc");
    client.println("User-Agent: jardin-magique-sensor");
    client.println("Connection: close");
    client.println();

    // note the time that the connection was made:
    lastConnectionTime = millis();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println("disconnecting.");
    client.flush();
    client.stop();
  }
  
}


