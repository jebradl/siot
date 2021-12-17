#include <WiFi.h>
#include <HTTPClient.h>

// secret values imported
const char* ssid = "";
const char* password = "";
String apiKey = "";

// domain URL path for HTTP POST request
const char* serverName = "http://api.thingspeak.com/update";

unsigned long lastTime = 0;
unsigned long timerDelay = 90000000;

// defining inputs for LDR and TCS320

#define Light 33

#define S0 13
#define S1 14
#define S2 15
#define S3 16
#define sensorOut 17

// integer frequencies read by the photodiodes

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;


void setup() {
  // outputs of the TCS320
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  // sensorOut as an input
  pinMode(sensorOut, INPUT);
  
  // frequency scaling set to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
   // begin serial communication 
  Serial.begin(115200);
  delay(1000);

  // wifi connection checker
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}



void loop() {
  // reading ldr value
  int ldr_val = analogRead(Light);
  Serial.println(ldr_val);

  // reading red val
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  // output frequency
  redFrequency = pulseIn(sensorOut, LOW);
  
  // reading green val
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  
  // output frequency
  greenFrequency = pulseIn(sensorOut, LOW);
 
  // reading blue val
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  
  // output frequency
  blueFrequency = pulseIn(sensorOut, LOW);




  //send an HTTP POST request every minute and a half
  if ((millis() - lastTime) > timerDelay) {
    // check wiFi is connected
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
    
      // set up URL path
      http.begin(client, serverName);
      
      // content-type header
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      // data for HTTP POST
      String httpRequestData = "api_key=" + apiKey + "&field1=" + ldr_val + "&field2=" + redFrequency + "&field3=" + greenFrequency + "&field4=" + blueFrequency;           
      // HTTP POST request
      int httpResponseCode = http.POST(httpRequestData);

     
      Serial.print("HTTP Response codes: ");
      Serial.println(httpResponseCode);
        
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
  

}
