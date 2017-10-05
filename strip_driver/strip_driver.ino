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
  while (Serial.available() > 1) {
    strip.setPixelColor(1, strip.Color(10,10,10));
    strip.show();
    delay(500);
    strip.setPixelColor(1, strip.Color(0,0,0));
    strip.show();
    
    char x1 = Serial.read();
    char x2 = Serial.read();
    unsigned short result = x1 + (x2 << 8); // Reconstruct the Short

    unsigned char B = ceil((result >> 0  & 0x1F) * 8.2258);
    unsigned char G = ceil((result >> 5  & 0x1F) * 8.2258);
    unsigned char R = ceil((result >> 10 & 0x1F) * 8.2258);
    Serial.println("R Value");
    Serial.println(R);
    Serial.println("G Value");
    Serial.println(G);
    Serial.println("B Value");
    Serial.println(B);
    
    strip.setPixelColor(0, strip.Color(R,G,B));
    strip.show();
  }
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
