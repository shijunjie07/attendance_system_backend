// --------------------------------------------
// ESP32-CAM
// Script to handle:
//   1. communication with websocket server
//   2. ESP32-CAM Server 
// @author Shi Junjie A178915
// Last modified: Tue 11 June 2024
// --------------------------------------------

#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoWebsockets.h>
#include <ArduinoJson.h>
#include <base64.h>
#include "esp_camera.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "fb_gfx.h"
#include "soc/soc.h"              //disable brownout problems
#include "soc/rtc_cntl_reg.h"     //disable brownout problems
#include "driver/gpio.h"

// configuration for AI Thinker Camera board
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22


// // LED
#define BUILTIN_LED 4
const int pwmChannel = 0;
const int pwmFrequency = 5000;
const int pwmResolution = 8;
const int ledPin = BUILTIN_LED;

// WiFi config
const char* ssid = "your ssid";
const char* password = "your pwd";

// websocket server ip and port
const char* server_ip = "192.168.0.104";    // change to your server ip
const uint16_t server_port = 5000;

bool stream = false;
AsyncWebServer server(80);      // listen on port 80

const int camera_id = 1;        // camera id
const char* location = "DK1";   // camera location

camera_fb_t * fb = NULL;
size_t _jpg_buf_len = 0;
uint8_t * _jpg_buf = NULL;
uint8_t state = 0;

uint16_t img_sent_counter = 0;

using namespace websockets;
WebsocketsClient webSocket;

void enableLED(){
  ledcWrite(pwmChannel, 190);
}

void disableLED() {
  ledcWrite(pwmChannel, 0);
}

esp_err_t init_camera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_QXGA;     // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
  config.jpeg_quality = 0;               //10-63 lower number means higher quality
  config.fb_count = 2;
  
  
  // init camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("camera init FAIL: 0x%x", err);
    return err;
  }
  sensor_t * s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_VGA);
  Serial.println("camera init OK");
  return ESP_OK;
}

// send image as binary
void send_image(){
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("img capture failed");
    esp_camera_fb_return(fb);
    ESP.restart();
  }
  webSocket.sendBinary((const char*) fb->buf, fb->len);
  Serial.print(".");
  esp_camera_fb_return(fb);
}

// init ESP32-CAM server
void init_server(){
  server.on("/start_stream", HTTP_GET, [](AsyncWebServerRequest *request){
    stream = true;
    request->send(200, "text/plain", "Streaming started");
  });
  
  server.on("/stop_stream", HTTP_GET, [](AsyncWebServerRequest *request){
    stream = false;
    Serial.print("Stream will stop in 10 seconds: ");
    webSocket.close();
    Serial.println("stopped");
    request->send(200, "text/plain", "Streaming stopped");
  });
  
  server.begin();
}

// init WiFi connection
void init_wifi(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

// websocket event
void onSocketEventCallback(WebsocketsEvent event, String data){
  if (event == WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connection Opened");
  } else if (event == WebsocketsEvent::ConnectionClosed) {
      Serial.println("Connection Closed");
  }
}

// websocket message
void onSocketMessageCallback(WebsocketsMessage message){
    // Parse JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, message.data());

    if (error) {
        Serial.print("deserializeJson() failed: ");
        Serial.println(error.f_str());
        return;
    }

    JsonArray id_array = doc["id"];
    JsonArray live_array = doc["live"];
    JsonArray recorded_array = doc['recorded'];

    // print received messages
    for (size_t i = 0; i < id_array.size(); i++) {
      if (id_array[i].as<String>() != "invalid"){
        Serial.print("id: ");
        Serial.println(id_array[i].as<String>());

        Serial.print("live: ");
        Serial.println(live_array[i].as<String>());

        Serial.print("recorded: ");
        Serial.println(recorded_array[i].as<String>());

        Serial.println("---------------");
      }
    }

}

// init socket connection
bool init_ws(){
  bool connect = webSocket.connect(server_ip, server_port, "/socket.io/?EIO=4&transport=websocket");
  
  if (!connect) {
    Serial.print("WS connect failed!");
    Serial.println(WiFi.localIP());
    state = 3;
    return false;
  }
  if (state == 3) {
    return false;
  }
  
  Serial.println("WS connected");
  
  webSocket.onMessage(onSocketMessageCallback);
  webSocket.onEvent(onSocketEventCallback);
  return false;
};



void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);
  WiFi.begin(ssid, password);               // connect to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  init_camera();
  init_server();
  // init_ws();
  
  Serial.print("Server Running at 'http://");
  Serial.print(WiFi.localIP()) ;
  Serial.println(":80");

  // setup LED FLASH
  ledcSetup(pwmChannel, pwmFrequency, pwmResolution);
  ledcAttachPin(BUILTIN_LED, pwmChannel);
}

void loop() {
  // send image
  if (stream) {
    if (webSocket.available()){
      enableLED();
      send_image();
      webSocket.poll();
      // delay(100);
    }else{
      disableLED();
      Serial.println("receive message to start stream but Socket not connected.");
      Serial.println("--- ws connection will try again in 5 seconds: ");
      delay(10000);   // delay to wait for websocket server to start
      init_ws();      // attempt ws connection
    }
  }else{
    disableLED();
  }
 
}






