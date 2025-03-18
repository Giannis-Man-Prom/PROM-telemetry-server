#include <WiFi.h>

const char *ssid = "Telemetry_Hotspot";
const char *password = "cargovroom";

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  Serial.println("Hotspot Created.");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {}
