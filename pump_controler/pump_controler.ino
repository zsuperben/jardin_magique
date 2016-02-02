/*
  Web Server

 A simple web server that shows the value of the analog input pins.
 using an Arduino Wiznet Ethernet shield.

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Analog inputs attached to pins A0 through A5 (optional)

 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe

 */

#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 1, 177);

// Initialize the Ethernet server library
// with the IP address and port you want to use
// (port 80 is default for HTTP):
EthernetServer server(80);

void setup() {
  Serial.begin(9600);
  Serial.println("Bonjour!");
  int i;
  for(i=2; i<10; i++) {
    //pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  // Prepare OUTPUT mode for the pins connected to the pumps MOSFET.
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);

  Serial.println("Lowered pumps switches");
  analogWrite(11,0);
  Serial.println("lowered analogs");
  // Open serial communications and wait for port to open:
  analogWrite(11, 90);
  Serial.println("11 is up");

  
  // start the Ethernet connection and the server:
  Ethernet.begin(mac);
  Serial.println("I decided that Ethnernet is ready");
  analogWrite(12, 90);
  Serial.println("So I'm pulling 12 UP");
  server.begin();
  Serial.println("I am now serving TCP stuff on port 80");
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
  analogWrite(13,90);
  delay(1000);
  for (int t = 2;t<10;t++){
    digitalWrite(t, LOW); 
  }
  analogWrite(13,0);
  
}

String request;

void loop() {
  // listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    Serial.println("new client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {

          // PRocess request before talking.
          process_request(request);
          
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println("Refresh: 5");  // refresh the page automatically every 5 sec
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          // output the value of each analog input pin
          for (int analogChannel = 0; analogChannel < 6; analogChannel++) {
            int sensorReading = analogRead(analogChannel);
            client.print("analog input ");
            client.print(analogChannel);
            client.print(" is ");
            client.print(sensorReading);
            client.println("<br />");
          }
          client.println("</html>");
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        }
        else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
          if(request.length() < 1024)
            request += c;
          else
            request = "";
        }
      }
    }
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
}


void process_request(String http_req) {
  if( http_req.indexOf("sw1=on") >=0 )
    digitalWrite(3, HIGH);
  else if( http_req.indexOf("sw1=off") >= 0 )
    digitalWrite(3, LOW);
  if( http_req.indexOf("sw2=on") >= 0 )
    digitalWrite(4, HIGH);
  else if( http_req.indexOf("sw2=off") >= 0)
    digitalWrite(4, LOW);
  if( http_req.indexOf("sw3=on") >= 0)
    digitalWrite(5, HIGH);
  else if( http_req.indexOf("sw3=off") >= 0)
    digitalWrite(5, LOW);
  if( http_req.indexOf("sw0=on") >= 0 )
    digitalWrite(2, HIGH);
  else if( http_req.indexOf("sw0=off") >= 0 )
    digitalWrite(2, LOW);
  if( http_req.indexOf("sw4=on") >= 0)
    digitalWrite(6, HIGH);
  else if( http_req.indexOf("sw4=off") >= 0)
    digitalWrite(6, LOW);
  if( http_req.indexOf("sw5=on") >= 0)
    digitalWrite(7, HIGH);
  else if( http_req.indexOf("sw5=off") >= 0)
    digitalWrite(7, LOW);
  if( http_req.indexOf("sw6=on") >= 0)
    digitalWrite(8, HIGH);
  else if( http_req.indexOf("sw6=off") >= 0)
    digitalWrite(8, LOW);
  if( http_req.indexOf("sw7=on") >= 0)
    digitalWrite(9, HIGH);
  else if( http_req.indexOf("sw7=off") >= 0)
    digitalWrite(9, LOW);    
  request = "";
}

