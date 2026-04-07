#include <ArduinoJson.h>
#include <AccelStepper.h>

// --- SETTINGS & THRESHOLDS ---
#define DEAD_ZONE 25         
#define motorInterfaceType 1 
#define LaserPin 13          

// --- PIN DEFINITIONS ---
const int stepX = 26; const int dirX = 27;
const int stepY = 32; const int dirY = 25;

// --- SOFT LIMITS ---
const long maxStepsX = 800;  
const long maxStepsY = 400;  

// --- STEPPER INSTANCES ---
AccelStepper stepperX(motorInterfaceType, stepX, dirX);
AccelStepper stepperY(motorInterfaceType, stepY, dirY);

// --- GLOBAL VARIABLES ---
const int moveSpeed = 250;    
unsigned long lastMsgTime = 0; 

// This tells the compiler the function exists before we use it
void stopEverything(); 

void setup() {
  Serial.begin(115200);
  
  pinMode(LaserPin, OUTPUT);
  digitalWrite(LaserPin, LOW);

  stepperX.setMaxSpeed(1000);
  stepperY.setMaxSpeed(1000);
  
  // Reset positions to 0 (Make sure camera is centered manually first!)
  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    JsonDocument doc; 
    DeserializationError error = deserializeJson(doc, msg);

    if (!error) {
      lastMsgTime = millis(); 
      
      int targetX = doc["x"];     
      int targetY = doc["y"];     
      bool active = doc["active"]; 
      bool laserReq = doc["laser"]; 

      if (active) {
        // --- X AXIS (PAN) ---
        long posX = stepperX.currentPosition();
        if (targetX > DEAD_ZONE && posX < maxStepsX) {
          stepperX.setSpeed(moveSpeed);
        } 
        else if (targetX < -DEAD_ZONE && posX > -maxStepsX) {
          stepperX.setSpeed(-moveSpeed);
        } 
        else {
          stepperX.setSpeed(0);
        }

        // --- Y AXIS (TILT) ---
        long posY = stepperY.currentPosition();
        if (targetY > DEAD_ZONE && posY < maxStepsY) {
          stepperY.setSpeed(moveSpeed);
        } 
        else if (targetY < -DEAD_ZONE && posY > -maxStepsY) {
          stepperY.setSpeed(-moveSpeed);
        } 
        else {
          stepperY.setSpeed(0);
        }

        // --- LASER ---
        digitalWrite(LaserPin, laserReq ? HIGH : LOW);

      } else {
        stopEverything();
      }
    }
  }

  // Safety Timeout: Stop if no message for 0.5s
  if (millis() - lastMsgTime > 500) {
    stopEverything();
  }

  stepperX.runSpeed();
  stepperY.runSpeed();
}

// The actual function definition
void stopEverything() {
  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
  digitalWrite(LaserPin, LOW);
}