// ============================================================
// car_control.ino
// Light Seeking & Colour Detection Autonomous Car
// Arduino Uno — Motor Control, LDR Phototaxis, Obstacle Detection
// Receives serial commands from Jetson Nano
// ============================================================

// --- Motor Driver (L298N) Pins ---
#define IN1 6    // Left Motor Direction A
#define IN2 7    // Left Motor Direction B
#define IN3 8    // Right Motor Direction A
#define IN4 9    // Right Motor Direction B
#define ENA 10   // Left Motor Speed (PWM)
#define ENB 11   // Right Motor Speed (PWM)

// --- Ultrasonic Sensor Pins ---
#define TRIG_L 2
#define ECHO_L 3
#define TRIG_R 4
#define ECHO_R 5

// --- LDR Analog Pins ---
#define LDR_LEFT  A0
#define LDR_RIGHT A1

// --- Thresholds & Constants ---
#define OBSTACLE_DISTANCE_CM  20     // Stop if obstacle within 20cm
#define LDR_DIFF_THRESHOLD    50     // Minimum difference to trigger turn
#define MOTOR_SPEED_NORMAL    180    // 0-255
#define MOTOR_SPEED_TURN      130    // Slower speed while turning
#define MOTOR_SPEED_STOP      0

// --- State ---
String currentCommand = "NONE";     // Last command from Jetson Nano

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Motor pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Ultrasonic pins
  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);

  // LDR pins are analog input by default — no pinMode needed

  Serial.begin(9600);   // Communication with Jetson Nano
  stopMotors();

  Serial.println("Arduino Ready.");
}

// ============================================================
// MAIN LOOP
// ============================================================
void loop() {

  // 1. Read serial command from Jetson Nano if available
  if (Serial.available() > 0) {
    currentCommand = Serial.readStringUntil('\n');
    currentCommand.trim();
  }

  // 2. Always check for obstacles first — safety priority
  long distLeft  = getDistance(TRIG_L, ECHO_L);
  long distRight = getDistance(TRIG_R, ECHO_R);

  if (distLeft < OBSTACLE_DISTANCE_CM || distRight < OBSTACLE_DISTANCE_CM) {
    stopMotors();
    Serial.println("OBSTACLE_DETECTED");
    delay(200);
    return;   // Skip everything else this loop cycle
  }

  // 3. Act on Jetson Nano command
  if (currentCommand == "RED") {
    stopMotors();

  } else if (currentCommand == "GREEN") {
    moveForward(MOTOR_SPEED_NORMAL);

  } else if (currentCommand == "BLUE") {
    turnLeft(MOTOR_SPEED_TURN);

  } else if (currentCommand == "YELLOW") {
    turnRight(MOTOR_SPEED_TURN);

  } else {
    // No colour detected — follow light (phototaxis)
    followLight();
  }

  delay(50);  // Small loop delay for stability
}

// ============================================================
// PHOTOTAXIS — Follow the Brighter Light Source
// ============================================================
void followLight() {
  int leftLight  = analogRead(LDR_LEFT);   // Higher = brighter
  int rightLight = analogRead(LDR_RIGHT);
  int diff = leftLight - rightLight;

  if (diff > LDR_DIFF_THRESHOLD) {
    // Left side brighter — turn left
    turnLeft(MOTOR_SPEED_TURN);
  } else if (diff < -LDR_DIFF_THRESHOLD) {
    // Right side brighter — turn right
    turnRight(MOTOR_SPEED_TURN);
  } else {
    // Both sides equal — move forward toward light
    moveForward(MOTOR_SPEED_NORMAL);
  }
}

// ============================================================
// DISTANCE MEASUREMENT (HC-SR04)
// ============================================================
long getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);  // 30ms timeout
  long distance = duration * 0.034 / 2;           // Convert to cm
  return distance;
}

// ============================================================
// MOTOR CONTROL FUNCTIONS
// ============================================================

void moveForward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveBackward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW);   // Left motor backward
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);  // Right motor forward
  digitalWrite(IN4, LOW);
}

void turnRight(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH);  // Left motor forward
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);   // Right motor backward
  digitalWrite(IN4, HIGH);
}

void stopMotors() {
  analogWrite(ENA, MOTOR_SPEED_STOP);
  analogWrite(ENB, MOTOR_SPEED_STOP);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
