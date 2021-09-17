#include "esphome.h"
#include <FastLED.h>
#include <TimeLib.h>

#define FASTLED_ESP8266_RAW_PIN_ORDER           // this means we'll be using the raw esp8266 pin order -> GPIO_12, which is d6 on nodeMCU
#define LED_PIN 3                              // led data in connected to GPIO_12 (d6/nodeMCU)
#define LED_PWR_LIMIT 700                         // 650mA - Power limit in mA (voltage is set in setup() to 5v)
#define LED_DIGITS 4                              // 4 or 6 digits, can only be an even number as...
#define LED_PER_DIGITS_STRIP 32                   // ...two digits are made out of one piece of led strip with 32 leds...
#define LED_BETWEEN_DIGITS_STRIPS 3               // 3 leds between above strips - and all this gives us LED_COUNT... :D
#define LED_COUNT ( LED_DIGITS / 2 ) * LED_PER_DIGITS_STRIP + ( LED_DIGITS / 3 ) * LED_BETWEEN_DIGITS_STRIPS

CRGB leds[LED_COUNT];

CRGBPalette16 currentPalette;

byte displayMode = 1;                             // 0 = 12h, 1 = 24h (will be saved to EEPROM once set using buttons)
byte brightness = 140;                            // default brightness if none saved to eeprom yet / first run
byte lastSecond = 0;                              // used to remember the last drawn digit to avoid flickering/changes when syncing to rtc/ntp

byte segGroups[14][2] = {         // 14 segments per strip, each segment has 1-x led(s). So lets assign them in a way we get something similar for both digits
  // right (seen from front) digit. This is which led(s) can be seen in which of the 7 segments (two numbers: First and last led inside the segment, identical if only 1):
  {  4,  5 },                     // top, a
  {  6,  7 },                     // top right, b
  {  9, 10 },                     // bottom right, c
  { 11, 12 },                     // bottom, d
  { 13, 14 },                     // bottom left, e
  {  2,  3 },                     // top left, f
  {  0,  1 },                     // center, g
  // left (seen from front) digit
  { 26, 27 },                     // top, a
  { 28, 29 },                     // top right, b
  { 17, 18 },                     // bottom right, c
  { 19, 20 },                     // bottom, d
  { 21, 22 },                     // bottom left, e
  { 24, 25 },                     // top left, f
  { 30, 31 }                      // center, g
};
// Note: The first number always has to be the lower one as they're subtracted later on... (fix by using abs()? ^^)

// Using above arrays it's very easy to "talk" to the segments. Simply use 0-6 for the first 7 segments, add 7 (7-13) for the following ones per strip/two digits
byte digits[14][7] = {                    // Lets define 10 numbers (0-9) with 7 segments each, 1 = segment is on, 0 = segment is off
  {   1,   1,   1,   1,   1,   1,   0 },  // 0 -> Show segments a - f, don't show g (center one)
  {   0,   1,   1,   0,   0,   0,   0 },  // 1 -> Show segments b + c (top and bottom right), nothing else
  {   1,   1,   0,   1,   1,   0,   1 },  // 2 -> and so on...
  {   1,   1,   1,   1,   0,   0,   1 },  // 3
  {   0,   1,   1,   0,   0,   1,   1 },  // 4
  {   1,   0,   1,   1,   0,   1,   1 },  // 5
  {   1,   0,   1,   1,   1,   1,   1 },  // 6
  {   1,   1,   1,   0,   0,   0,   0 },  // 7
  {   1,   1,   1,   1,   1,   1,   1 },  // 8
  {   1,   1,   1,   1,   0,   1,   1 },  // 9
  {   0,   0,   0,   1,   1,   1,   1 },  // t -> some letters from here on (index 10-13, so this won't interfere with using digits 0-9 by using index 0-9
  {   0,   0,   0,   0,   1,   0,   1 },  // r
  {   0,   1,   1,   1,   0,   1,   1 },  // y
  {   0,   1,   1,   1,   1,   0,   1 }   // d
};

class Clock7Seg : public Component {
    public:
        void setup() override {
            delay(500);
            FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, LED_COUNT).setCorrection(TypicalSMD5050).setTemperature(DirectSunlight).setDither(1);
            FastLED.setMaxPowerInVoltsAndMilliamps(5, LED_PWR_LIMIT);
            FastLED.clear();
            FastLED.show();

        }

        void loop() override {

        }
    
        void showDigit(byte digit, byte color, byte pos) {
            // This draws numbers using the according segments as defined on top of the sketch (0 - 9)
            for (byte i = 0; i < 7; i++) {
                if (digits[digit][i] != 0) showSegment(i, color, pos);
            }
        }

        void showSegment(byte segment, byte color, byte segDisplay) {
            // This shows the segments from top of the sketch on a given position (segDisplay).
            // pos 0 is the most right one (seen from the front) where data in is connected to the arduino
            byte leds_per_segment = 1 + abs( segGroups[segment][1] - segGroups[segment][0] );         // get difference between 2nd and 1st value in array to get led count for this segment
            if ( segDisplay % 2 != 0 ) segment += 7;                                                  // if segDisplay/position is odd add 7 to segment
            for (byte i = 0; i < leds_per_segment; i++) {                                             // fill all leds inside current segment with color
                leds[( segGroups[segment][0] + ( segDisplay / 2 ) * ( LED_PER_DIGITS_STRIP + LED_BETWEEN_DIGITS_STRIPS ) ) + i] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
            }
        }

        void showDots(byte dots, byte color) {
            // in 12h mode and while in setup upper dots resemble AM, all dots resemble PM
            byte startPos = LED_PER_DIGITS_STRIP;
            if ( LED_BETWEEN_DIGITS_STRIPS % 2 == 0 ) {                                                                 // only SE/TE should have a even amount here (0/2 leds between digits)
                leds[startPos] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                if ( dots == 2 ) leds[startPos + 1] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
            } else {                                                                                                    // 3 LEDs between digit strips
                leds[startPos] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                if ( LED_DIGITS / 3 > 1 ) {
                    leds[startPos + LED_PER_DIGITS_STRIP + LED_BETWEEN_DIGITS_STRIPS] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                    leds[startPos + LED_PER_DIGITS_STRIP + LED_BETWEEN_DIGITS_STRIPS + 1] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                }
                if ( dots == 2 ) {
                    leds[startPos + 2] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                    if ( LED_DIGITS / 3 > 1 ) {
                        leds[startPos + LED_PER_DIGITS_STRIP + LED_BETWEEN_DIGITS_STRIPS + 2] = ColorFromPalette(currentPalette, color, brightness, LINEARBLEND);
                    }
                }
            }
        }

        void displayTime(time_t t, byte color, byte colorSpacing) {
            byte posOffset = 0;                                                                     // this offset will be used to move hours and minutes...
            if ( LED_DIGITS / 2 > 2) posOffset = 2;                                                 // ... to the left so we have room for the seconds when there's 6 digits available
            if ( displayMode == 0 ) {                                                               // if 12h mode is selected...
                if ( hourFormat12(t) >= 10 ) showDigit(1, color + colorSpacing * 2, 3 + posOffset);   // ...and hour > 10, display 1 at position 3
                    showDigit((hourFormat12(t) % 10), color + colorSpacing * 3, 2  + posOffset);          // display 2nd digit of HH anyways
            } else if ( displayMode == 1 ) {                                                        // if 24h mode is selected...
                if ( hour(t) > 9 ) showDigit(hour(t) / 10, color + colorSpacing * 2, 3 + posOffset);  // ...and hour > 9, show 1st digit at position 3 (this is to avoid a leading 0 from 0:00 - 9:00 in 24h mode)
                showDigit(hour(t) % 10, color + colorSpacing * 3, 2 + posOffset);                     // again, display 2nd digit of HH anyways
            }
            showDigit((minute(t) / 10), color + colorSpacing * 4, 1 + posOffset);                   // minutes thankfully don't differ between 12h/24h, so this can be outside the above if/else
            showDigit((minute(t) % 10), color + colorSpacing * 5, 0 + posOffset);                   // each digit is drawn with an increasing color (*2, *3, *4, *5) (*6 and *7 for seconds only in HH:MM:SS)
            if ( posOffset > 0 ) {
                showDigit((second(t) / 10), color + colorSpacing * 6, 1);
                showDigit((second(t) % 10), color + colorSpacing * 7, 0);
            }
            if ( second(t) % 2 == 0 ) showDots(2, second(t) * 4.25);                                // show : between hours and minutes on even seconds with the color cycling through the palette once per minute
            lastSecond = second(t);
        }
};    