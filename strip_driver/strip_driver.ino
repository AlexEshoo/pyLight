#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(30, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();

  Serial.begin(115200);

  String msg;
  

}

int strip_colors[3];

void loop() {
  bool flag = false;
  while (Serial.available() > 2) {
    flag = true;
    int r = Serial.read();
    int g = Serial.read();
    int b = Serial.read();
    
    strip_colors[0] = r;
    strip_colors[1] = g;
    strip_colors[2] = b;
    //delay(10);
  }
  for (int i; i<30; i++) {
    strip.setPixelColor(i, strip.Color(strip_colors[0],strip_colors[1],strip_colors[2]));
  }
  strip.show();
  /*if (flag == true) {
    Serial.write(strip_colors[0][0]);
    flag = false;
  }*/
}

void breath(int dt) {
  for (int i=0; i<256; i++){
    for (int j=0; j<strip.numPixels(); j++) {
      strip.setPixelColor(j, strip.Color(i,0,0));
    }
    strip.show();
    delay(dt);
  }
  for (int i=255; i>-1; i--){
    for (int j=0; j<strip.numPixels(); j++) {
      strip.setPixelColor(j, strip.Color(i,0,0));
    }
    strip.show();
    delay(dt);
  }
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
