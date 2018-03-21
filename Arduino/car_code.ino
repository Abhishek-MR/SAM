

#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>


#define wifi_ssid "Butter Chicken"
#define wifi_password "a1234567"

#define mqtt_server "m13.cloudmqtt.com"
#define mqtt_user "ptbelqhi"
#define mqtt_password "wdJXMPWzv6Q5"

#define topic_iot "car"

int i=0;

//clutch
const int trigPin = D1;
const int echoPin = D2;
//accelerator
const int trigPin1 = D4; //D5
const int echoPin1 = D3;  //D6


char inbyte = 0;
// defines variables
long duration;
long duration1;
int distance1,distance2;

int case1;
int case2;
int case3;
int case4;

String car="car";

WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(trigPin1, OUTPUT); 
  pinMode(echoPin1, INPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 13476);
  client.setCallback(callback);

}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // If you do not want to use a username and password, change next line to
    // if (client.connect("ESP8266Client")) {
    if (client.connect("ESP8266Client",mqtt_user,mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
   Serial.println();
}

void publishstr(String comm)
{
  client.publish(topic_iot,(comm).c_str() , true);
}



void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //ong now = millis();

  String val = String(i);

  inbyte = Serial.read();
          
           // Clears the trigPin
             digitalWrite(trigPin, LOW);
             
              digitalWrite(trigPin, HIGH);
               delay(10);
              digitalWrite(trigPin, LOW);
              
              duration1 = pulseIn(echoPin, HIGH);
              
                distance1= duration1*0.034/2;

          Serial.println(distance1);
             
             
           
           // Clears the trigPin
             digitalWrite(trigPin1, LOW);
              
              digitalWrite(trigPin1, HIGH);
                delay(10);
              digitalWrite(trigPin1, LOW);
              
              duration = pulseIn(echoPin1, HIGH);
              
                distance2= duration*0.034/2;

                          Serial.println(distance2);

                                      client.publish(topic_iot,String(1).c_str() , true);


              
//algo
        
        if((distance1>=12) && (distance2 <=4))
        {
          case1++;
          if(case1%5==0){
            Serial.println("proper driving");
            client.publish(topic_iot,String(1).c_str() , true);
          }
        }
          
         //Clutch at initial and acc. goes max
        else if((distance1<=11)&&(distance1>5) && (distance2 <=11))
         {
          case2++;
          if(case2%5==0){
            Serial.println("proper driving");
            
            client.publish(topic_iot,String(2).c_str() , true);
          }
        }
                 
         else if((distance1<=5) && (distance2<=11))
            {
          case3++;
          if(case3%5==0){
            Serial.println("nto proper");
            client.publish(topic_iot,String(3).c_str() , true);
          }
        }
        // Full clutch and 20% acc
         else
            case4++;// Success  
            {
          case4++;
          if(case4%5==0){
            Serial.println("full clutch");
            client.publish(topic_iot,String(4).c_str() , true);
          }
        }  
     
          delay(1000);
          
  
}

