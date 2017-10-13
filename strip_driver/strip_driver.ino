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
  while (Serial.available() > 0) {
    Serial.read();
  }
}

void loop() {
  // Loop period 3~5 milliseconds
  byte bytes [60]; // Buffer for incoming colors
  uint16_t encoded_rgb;
  uint32_t color;
  bool updateBit;  // If HIGH, update the pixel color
                   // Allows some pixels to be skipped
                   // on new incoming data buffer.
  static int b = 0;
  
  while (Serial.available() > 1) {
    bytes[2*b] = Serial.read();
    bytes[2*b+1] = Serial.read();
    b++;
  }
  if (b == 59){
    for (int i=0; i<60; i+=2){
      encoded_rgb = bytes[i] + (bytes[i+1] << 8); // Reconstruct the Short
      updateBit = encoded_rgb >> 15;

      if (updateBit == true){
        color = decode_rgb(encoded_rgb);
        strip.setPixelColor(i/2, color);
      }
    }
    strip.show();
    b = 0;
  }
}

uint32_t decode_rgb(uint16_t rgb){
  uint8_t B = ceil( (rgb >> 0  & 0x1F) * 8.2258); // Scales to full
  uint8_t G = ceil( (rgb >> 5  & 0x1F) * 8.2258); // 0 - 255
  uint8_t R = ceil( (rgb >> 10 & 0x1F) * 8.2258); // range
  return strip.Color(R, G, B);
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
