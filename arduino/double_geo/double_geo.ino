#include <time.h>

char buffer[64] = { 0 };

void setup() {
  Serial.begin(115200);
}

void loop() {
  int a0 = analogRead(A0);
  int a1 = analogRead(A1);
  sprintf(buffer, "%d,%d", a0, a1);
  Serial.println(buffer);
  delayMicroseconds(1000);
}

