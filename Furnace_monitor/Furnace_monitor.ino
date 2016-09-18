#include <LiquidCrystal.h>
#include <max6675.h>

// initialize the library with the numbers of the interface pins
// LiquidCrystal(rs, enable, d4, d5, d6, d7) 
LiquidCrystal lcd(8, 7, 6, 5, 4, 3);
const int BCKLIGHTPIN  = 2;

const int thermoDO1 = A0;
const int thermoCS1 = A1;
const int thermoCLK1 = A2;

MAX6675 thermocouple1(thermoCLK1, thermoCS1, thermoDO1);


//red+black wires
const int therm1pin = A3;

//green+white wires
const int therm2pin = A4;

//yellow+blue wires
const int therm3pin = A5;

const float R0 = 9.7e3; //using a 10k resistor
const float B = 3977.0;
const float T0 = 273.15 + 25.0;
const byte ohm = 0b11110100;
const byte degree = 1;
const byte rarrow = 2;

// degree centigrade
byte degree_char[8] = {
  B01000,
  B10100,
  B01000,
  B00011,
  B00100,
  B00100,
  B00011,
  B00000
};
 
 
// arrow right
byte right_arrow[8] = {
  B00000,
  B00100,
  B00010,
  B11111,
  B00010,
  B00100,
  B00000,
  B00000
};
 
// arrow left
byte left_arrow[8] = {
  B00000,
  B00100,
  B01000,
  B11111,
  B01000,
  B00100,
  B00000,
  B00000
};

void setup() {
  Serial.begin(9600);
  pinMode(BCKLIGHTPIN, OUTPUT);
  digitalWrite(BCKLIGHTPIN, HIGH);
  lcd.createChar(degree, degree_char);
  lcd.createChar(rarrow, right_arrow);
  
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.write(byte(223));
}

float V2T(float V) {
  //calculate the resistance of the thermistor
  float alpha = V / 1023.0;
  float R = alpha / (1.0 - alpha) * R0;
  
  //use the equation
  float T = 1.0 / (1.0 / T0 + log(R / R0) / B) - 273.15;
  return T;
}

void loop() {
  
  
  float Therm = thermocouple1.readCelsius();
  float V1 = analogRead(therm1pin);
  float V2 = analogRead(therm2pin);
  float V3 = analogRead(therm3pin);
  
  float T1 = V2T(V1);
  float T2 = V2T(V2);
  float T3 = V2T(V3);
  
  lcd.clear();
  
  lcd.print("In: "); lcd.print(int(T2));lcd.write(degree);
  lcd.print(" Out: "); lcd.print(int(T3));lcd.write(degree);
  lcd.setCursor(0,1);
  lcd.print("Tank Temp: ");
  lcd.print(int(T1));lcd.write(degree);
  
  //Serial.print(Therm); Serial.print("\t");
  Serial.print("{");
  Serial.print("\"tank\" : "); Serial.print(T1); Serial.print(", ");
  Serial.print("\"fire->tank\" : "); Serial.print(T2); Serial.print(", ");
  Serial.print("\"tank->fire\" : "); Serial.print(T3); Serial.print(" }\n");
  
  delay(1000);
}
