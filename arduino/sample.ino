#include <time.h>

char buffer[64] = { 0 };

void setup() {
  Serial.begin(115200);
}

int count = 1000;
int a0 = 0;
int a1 = 0;
int t = 0;

void loop() {
  for (int i = 0; i < count; ++i) {
    a0 = analogRead(A0);
    a1 = analogRead(A1);
    memset(buffer, 0, sizeof(buffer));
  }
  memset(buffer, 0, sizeof(buffer));
  t = (int)millis();
  sprintf(buffer, "%d, %d", t, t);
  Serial.println(buffer);
  delayMicroseconds(10);
}

