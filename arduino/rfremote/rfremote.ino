/* Copyright (C) 2020 Sean D'Epagnier <seandepagnier@gmail.com>
 *
 * This Program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation; either
 * version 3 of the License, or (at your option) any later version.
 */

#include <RCSwitch.h>

RCSwitch rf = RCSwitch();

#include <avr/sleep.h>
#include <avr/power.h>

#define LED1_ON  PORTB |= _BV(PB2)
#define LED1_OFF PORTB &= ~_BV(PB2)

#define LED2_ON  PORTB |= _BV(PB5)
#define LED2_OFF PORTB &= ~_BV(PB5)


#define BOOST_ON  PORTB |= _BV(PB0)
#define BOOST_OFF PORTB &= ~_BV(PB0)



// do nothing, just wake up
ISR(PCINT2_vect) {
}

// the setup routine runs once when you press reset:
void setup() {
    ADCSRA=0;
//    power_all_disable ();


    cli();
    CLKPR = _BV(CLKPCE);
    CLKPR = _BV(CLKPS1); // divide by 4 (2mhz)
    sei();

  PCICR |= _BV(PCIE2);
  PCMSK2 = 0xff; // port D used for 8 keys, wake on any change

  PORTD = 0xff; // internal pullup resistors for all port D
  rf.enableTransmit(9); // d9
  rf.setRepeatTransmit(7);

  // for led
  DDRB|=_BV(PB0) | _BV(PB2) | _BV(PB5);
}


// the loop routine runs over and over again forever:
static uint32_t code, timeout;
void loop() {
    // test keys
    uint32_t t0 = millis();
    if(PIND != 0xff) {
        BOOST_ON;
        code = 0xa91c00UL | PIND;
        timeout = t0;
    }

    if(code) {
        LED1_ON;
        if(t0 - timeout < 200UL) {
            LED2_ON;
            rf.send(code, 24);
        } else {
            LED2_OFF;
            rf.send(0x7c2933UL, 24); // release code
            code = 0;
            BOOST_OFF;
        }
    } else {
        LED1_OFF;
        // if all settings are correct (no BOD), deep sleep is 4uA
        // wrong settings will drain battery

        set_sleep_mode(SLEEP_MODE_PWR_DOWN);
        sleep_enable();
        sleep_bod_disable();
        sleep_cpu();
        delay(1);        // delay in between reads for stability
    }
}
