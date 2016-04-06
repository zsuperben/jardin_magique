/*
  To upload through terminal you can use: curl -F "image=@firmware.bin" esp8266-webupdate.local/update
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>




#define LIGHT 12
#define WATER 13
#define MAX_WATER_TIME 10000
#define OVERVIEW 2

const char* host = "esp8266-webupdate";
const char* ssid = "Livebox-B6C4";
const char* password = "...";

ESP8266WebServer server(80);
const char* serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";

void handle_upload(){

if(server.uri() != "/update") return;
      HTTPUpload& upload = server.upload();
      if(upload.status == UPLOAD_FILE_START){
        Serial.setDebugOutput(true);
        WiFiUDP::stopAll();
        Serial.printf("Update: %s\n", upload.filename.c_str());
        uint32_t maxSketchSpace = (ESP.getFreeSketchSpace() - 0x1000) & 0xFFFFF000;
        if(!Update.begin(maxSketchSpace)){//start with max available size
          Update.printError(Serial);
        }
      } else if(upload.status == UPLOAD_FILE_WRITE){
        if(Update.write(upload.buf, upload.currentSize) != upload.currentSize){
          Update.printError(Serial);
        }
      } else if(upload.status == UPLOAD_FILE_END){
        if(Update.end(true)){ //true to set the size to the current progress
          Serial.printf("Update Success: %u\nRebooting...\n", upload.totalSize);
        } else {
          Update.printError(Serial);
        }
        Serial.setDebugOutput(false);
      }
      yield();
    }

void handle_post_on_update() {
      server.sendHeader("Connection", "close");
      server.sendHeader("Access-Control-Allow-Origin", "*");
      server.send(200, "text/plain", (Update.hasError())?"FAIL":"OK");
      ESP.restart();
    }

void home_page(){
      server.sendHeader("Connection", "close");
      server.sendHeader("Access-Control-Allow-Origin", "*");
      server.send(200, "text/html", serverIndex);
    }
    
void PublishSensorData(){
      int moist  = analogRead(A0);
      float temp ;
      short int hum ;
}

long double start_light = 0;
void handleLightUp(){
  digitalWrite(LIGHT, HIGH);
  start_light = millis();
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", pageRender(LIGHT,"up"));
}

void handleLightDown(){
  digitalWrite(LIGHT, LOW);
  server.sendHeader("Connection","close");
  server.send(200, "text/html", pageRender(LIGHT, "down"));
}

long double start_water = 0;
void HandleWaterOn(){
  digitalWrite(WATER, HIGH);
  start_water = millis();
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", pageRender(WATER, "On"));
}

void HandleWaterOff(){
  digitalWrite(WATER, LOW);
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", pageRender(WATER, "off"));
}

char * pageRender(short int  pagetype, char * action){
  
  char * format = GetTemplate(pagetype);
  char * return_str;
  sprintf(return_str, format, action);
  return return_str;
}

char * GetTemplate(short int type){
  switch(type){
    case 13:
      return "PUT SOME WATER HTML HERE";
    case 12:
      return "SOME LIGHT DIFFERENT HTML";
    case 2:
      return "Even different HTML CODE ";
  }
}
long double timer = 0, lastcall = 0 ;

void Overview(void){
	server.sendHeader("Connection", "close");
	server.send(200, "text/html", pageRender(OVERVIEW, NULL));
}

void setup(void){
  Serial.begin(115200);
  Serial.println();
  Serial.println("Booting Sketch...");
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);
  if(WiFi.waitForConnectResult() == WL_CONNECTED){
    // Sets the avahi kinda shit, most probably useless... 
    //need to check what could be done with that 
    MDNS.begin(host); 
    server.on("/", Overview);
    server.on("/update", HTTP_GET, home_page );
    // Moved to external function for lisibility
    server.onFileUpload(handle_upload);
    server.on("/update", HTTP_POST, handle_post_on_update );
    server.on("/light/on", handleLightUp);
    server.on("/light/off", handleLightDown);
    server.on("/water/on", HandleWaterOn);
    server.on("/water/off", HandleWaterOff);
    server.begin();
    MDNS.addService("http", "tcp", 80);
  
    Serial.printf("Ready! Open http://%s.local in your browser\n", host);
  } else {
    Serial.println("WiFi Failed");
  }
}


void loop(void){
	timer = millis();
	if(millis() - start_water > MAX_WATER_TIME && digitalRead(WATER) ){
		digitalWrite(WATER, LOW);
	}
	if(timer - lastcall > 1000*120 ){
		//publish_results();
		lastcall = millis();
	}
  server.handleClient();
  delay(1);
} 
