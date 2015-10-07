/*--------------------------------------------------------------------------------------+ 
|        This is the Arduino's sketch for Wifi enabled sensors based on ESP8866 chip.   |
|        You can find a TODO list in the same directory.                                |
|            - You need to make sure that you will post data to the right place/server  |
|            - You probably need to check the wireing config matches your setup         |
|            - You need to SET IP AND MAC ADDRESS HERE !                                |
|            - YOU NEED TO SET YOUR WIFI CONFIG
+---------------------------------------------------------------------------------------+            
                                                                                       */
#include <ESP8266WiFi.h>

// SET WIFI CONFIG FIRST 
const char* ssid     = "YourSSID"            ;
const char* password = "..."                 ;
//--------------------------------------------
const char* host     = "data.jardin-magique" ;
const char* streamId = "" ; 


// One global client is potentially better than 
// starting a new client in each loop...
WiFiClient client                            ;
const char* url = 
"http://" + host + '/' + uri                 ;

void setup() {
    Serial.begin(115200)                      ;
    delay(10)                                 ;

    Serial.println()                          ;
    Serial.println()                          ;
    Serial.print("Connecting to : ")          ;
    Serial.println(ssid)                      ;

    WiFi.begin(ssid, password)                ;
    while ( WiFi.status() != WL_CONNECTED) {
        delay(500)                            ;
        Serial.print('.')                     ;
        }

    Serial.println()                          ;
    Serial.println(
        "Wifi connection established."
        )                                     ;

    Serial.print("My IP address is : ")       ;
    Serial.println(WiFi.localIP())            ;
    
    

}






void loop() {



}
