const int pinPot = A0;   
const int pinTemp = A1;  
const int pinLed = 13;   

void setup() {
  Serial.begin(115200);
  pinMode(pinLed, OUTPUT);
}

void loop() {
  // --- 1. LECTURA DEL POTENCIÓMETRO ---
  analogRead(pinPot);       
  delay(2);                 
  int valorPot = analogRead(pinPot);

  // --- 2. EL FILTRO MÁGICO PARA LA TEMPERATURA ---
  long sumaTemp = 0; // Aquí guardaremos la suma de las lecturas
  
  // Tomamos 25 lecturas en chinga para sacar un promedio
  for(int i = 0; i < 25; i++) {
    sumaTemp = sumaTemp + analogRead(pinTemp);
    delay(2); // Mini pausa para no saturar el lector
  }
  
  // Sacamos el promedio limpio
  int valorTempLimpio = sumaTemp / 25; 
  
  // --- 3. LÓGICA DEL LED ---
  if (valorPot > 512) {
    digitalWrite(pinLed, HIGH);
  } else {
    digitalWrite(pinLed, LOW);
  }
  
  // --- 4. ENVIAR A PYTHON ---
  Serial.print(valorPot);
  Serial.print(",");
  Serial.println(valorTempLimpio); // Enviamos el dato ya sin picos
  
  delay(10); 
}