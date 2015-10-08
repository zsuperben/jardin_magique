/*--------------------------------------------------------------------------------------+ 
|        This is the Arduino's sketch for Wifi enabled sensors based on ESP8866 chip.   |
|        You can find a TODO list in the same directory.                                |
|            - You need to make sure that you will post data to the right place/server  |
|            - You probably need to check the wireing config matches your setup         |
|            - You need to SET IP AND MAC ADDRESS HERE !                                |
|            - YOU NEED TO SET YOUR WIFI CONFIG                                         |
+--------------------------------------------------------------------------------------*/            

#include <ESP8266WiFi.h>

// SET WIFI CONFIG FIRST 
const char* ssid     = "YourSSID"            ;
const char* password = "..."                 ;
//--------------------------------------------
const char* host     = "data.jardin-magique" ;
const char* streamId = "" ; 
//--------------------------------------------


int get_wifi_connection(char * ssid, char * passwd) {
    Serial.println()                          ;
    Serial.println()                          ;
    Serial.print("Connecting to : ")          ;
    Serial.println(ssid)                      ;
    Serial.println()                          ;
    int ntries = 0                            ;
    WiFi.begin(ssid, passwd)                  ;
    while ( WiFi.status() != WL_CONNECTED) {
        delay(500)                            ;
        Serial.print('.')                     ;
        ntries++                              ;
        if(ntries > 60) {
            ntries = 0                        ;
            return 0                          ;
        }
    Serial.println(
        "Wifi connection established."
        )                                     ;
    Serial.print("My IP address is : ")       ;
    Serial.println(WiFi.localIP())            ;
    return 1    
}

int list_networks() {
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(200);
    Serial.println("scan start");

    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();
    Serial.println("scan done");
    if (n == 0)
       Serial.println("no networks found");
    else {
       Serial.print(n);
       Serial.println(" networks found");
       for (int i = 0; i < n; ++i) {
            // Print SSID and RSSI for each network found
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(WiFi.SSID(i));
            Serial.print(" (");
            Serial.print(WiFi.RSSI(i));
            Serial.print(")");
            Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE)?" ":"*");
            delay(10);
       }
    }
    Serial.println("");
    return n;
}

// One global client is potentially better than 
// starting a new client in each loop...
WiFiClient client                            ;
const char* url = 
"http://" + host + "/mesure/add/" + streamId ;

void setup() {
    Serial.begin(115200)                      ;
    delay(10)                                 ;
    Serial.println("Starting Microcontroler...");
    
}

void loop() {

    

}
