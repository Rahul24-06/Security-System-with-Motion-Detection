
int Pyro = A1;
unsigned long PyroRead = 0;

unsigned long IR_threshold = 198000;

// Note: SS-430 has two pulses of 200msec per detection.

// IR_threshold is in microsec (usec), therefore 198msec threshold

int LED = 13;

int Detected = LOW;

int IR_sensed = 0;

void setup() {

  pinMode (13, OUTPUT); //LED Connected to Pin 13

  pinMode (A1, INPUT); // IR Sensor connected to A1

}

void loop() {

  while ((IR_sensed < 2)) { //Break after 2 good triggers

    PyroRead = pulseIn(A1, HIGH); //Measure trigger point

    if (PyroRead > IR_threshold) { //Make sure trigger is over 198msec)

      IR_sensed++; //Mark as a good trigger

    }

  }

  if (Detected == HIGH) { // Turn LED OFF if it was previous ON

    Detected = LOW;

    digitalWrite(13, LOW);

  }

  else {

    Detected = HIGH; // Turn LED ON if it was previous OFF

    digitalWrite(13, HIGH);

  }

  PyroRead = 0; // Reset readings

  IR_sensed = 0;

  delay(1000); // Accept triggers after a second
}
