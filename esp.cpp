#include <ArduinoJson.h>
#include <AccelStepper.h>

#define Laser 16

#define DEAD_ZONE 30  // no = sign in #define

#define motorInterfaceType 1


const int stepPinY = 32;
const int dirPinY = 25;

const int stepPinX = 26;
const int dirPinX = 27;

AccelStepper stepperY(motorInterfaceType, stepPinY, dirPinY);
AccelStepper stepperX(motorInterfaceType, stepPinX, dirPinX);

const int moveSpeed = 200;


void setup() {
  Serial.begin(115200);

  pinMode(Laser, OUTPUT);

  stepperY.setMaxSpeed(1000);
  stepperX.setMaxSpeed(1000);
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    JsonDocument doc;  // replaces StaticJsonDocument
    DeserializationError error = deserializeJson(doc, msg);

    if (error) {
      Serial.println("Invalid JSON!");
      return;
    }

    int x = doc["x"];
    int y = doc["y"];
    bool active = doc["active"];
    bool laserAct = doc["laser"];

    // // x axis
    // if (x > DEAD_ZONE) {
    //   // move right
    // } else if (x < -DEAD_ZONE) {
    //   // move left
    // }

    if (laserAct){
      digitalWrite(Laser, HIGH);
    }
    else {
      digitalWrite(Laser, LOW);
    }

    if (active){
      if (y > DEAD_ZONE) {
        stepperY.setSpeed(moveSpeed);
      } else if (y < -DEAD_ZONE) {
        stepperY.setSpeed(-moveSpeed);
      }
      else{
        stepperY.setSpeed(0);
      }

      if (x > DEAD_ZONE) {
        stepperX.setSpeed(moveSpeed);
      } else if (x < -DEAD_ZONE) {
        stepperX.setSpeed(-moveSpeed);
      }
      else{
        stepperX.setSpeed(0);
      }


    }


    else {
      stepperY.setSpeed(0);
      stepperX.setSpeed(0);
    }


    
  }
  stepperY.runSpeed();
  stepperX.runSpeed();
}