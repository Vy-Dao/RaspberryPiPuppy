const int trigPinLeft = 9;
const int echoPinLeft = 8;
const int trigPinRight = 11;
const int echoPinRight = 10;
const int trigPinMid = 12;
const int echoPinMid = 13;
float durationLeft, distanceLeft; 
float durationMid, distanceMid; 
float durationRight, distanceRight; 

void setup() {
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);
  pinMode(trigPinMid, OUTPUT);
  pinMode(echoPinMid, INPUT);
  Serial.begin(9600);
}

void loop() {
  //Left Sensor
  // Calculating time and distance
  digitalWrite(trigPinLeft, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinLeft, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinLeft, LOW);
  // Read the signal from the sensor: a HIGH pulse whose
  pinMode(echoPinLeft, INPUT);
  durationLeft = pulseIn(echoPinLeft, HIGH);
  distanceLeft = (durationLeft/2) / 29.1;
  
  //Right Sensor
  // Calculating time and distance
  digitalWrite(trigPinRight, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinRight, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinRight, LOW);
  // Read the signal from the sensor: a HIGH pulse whose
  pinMode(echoPinRight, INPUT);
  durationRight = pulseIn(echoPinRight, HIGH);
  distanceRight = (durationRight/2) / 29.1;

  //Middle Sensor
  // Calculating time and distance
  digitalWrite(trigPinMid, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinMid, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinMid, LOW);
  // Read the signal from the sensor: a HIGH pulse whose
  pinMode(echoPinMid, INPUT);
  durationMid = pulseIn(echoPinMid, HIGH);
  distanceMid = (durationMid/2) / 29.1;
  
  Serial.print(distanceRight);
  Serial.print(",");
  Serial.print(distanceLeft);
  Serial.print(",");
  Serial.print(distanceMid);
  Serial.println();
  delay(500);

}
