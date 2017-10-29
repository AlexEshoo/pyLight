#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(30, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
  strip.setBrightness(255); // Future use for setting max brightness

  Serial.begin(115200);
}

void loop() {
  // Loop period 3~5 milliseconds
  static uint32_t timer;
  byte bytes [60]; // Buffer for incoming colors
  uint16_t encoded_rgb;
  uint32_t color;
  bool updateBit;  // If HIGH, update the pixel color
                   // Allows some pixels to be skipped
                   // on new incoming data buffer.

  if (millis() - timer > 5000) {
    rainbowCycle(5);
  }
  
  while (Serial.available() > 59) {
    Serial.readBytes(bytes, 60);
    for (int i=0; i<60; i+=2){
      encoded_rgb = bytes[i] + (bytes[i+1] << 8); // Reconstruct the Short
      updateBit = encoded_rgb >> 15;

      if (updateBit == true){
        color = decode_rgb(encoded_rgb);
        strip.setPixelColor(i/2, color);
      }
    }
    strip.show();
    timer = millis();
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
      if (Serial.available() > 0) {
        for (int k=0; k<strip.numPixels(); k++) {
          strip.setPixelColor(k, strip.Color(0,0,0));
        }
        return;
      }
    }
    strip.show();
    delay(dt); // These are deadly to the serial buffer if too long
  }
  for (int i=255; i>-1; i--){
    for (int j=0; j<strip.numPixels(); j++) {
      strip.setPixelColor(j, strip.Color(i,0,0));
      if (Serial.available() > 0) {
        for (int k=0; k<strip.numPixels(); k++) {
          strip.setPixelColor(k, strip.Color(0,0,0));
        }
        return;
      }
    }
    strip.show();
    delay(dt); // These are deadly to the serial buffer if too long
  }
}

void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256 * 5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
      if (Serial.available() > 0) {
        for (uint16_t k=0; k<strip.numPixels(); k++) {
          strip.setPixelColor(k, strip.Color(0,0,0));
        }
        return;
      }
    }
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
      if (Serial.available() > 0) {
        for (uint16_t k=0; k<strip.numPixels(); k++) {
          strip.setPixelColor(k, strip.Color(0,0,0));
        }
        return;
      }
    }
    strip.show();
    delay(wait);
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3,0);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3,0);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0,0);
}
