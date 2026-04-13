// ============================================================
//  ESP32-CAM FAST MJPEG STREAM
//  Settings ported from ESP32-CAM UMSL v0.2
//  © Advanced Systems Lab UMSL 2026
// AI Thinker Board
// ============================================================

#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>
#include "esp_wifi.h"
#include "esp_bt.h"

// ============================================================
//  WiFi – Station (connect to home router)
// ============================================================
const char* ssid     = "NETGEAR95";      // ← change this
const char* password = "grandbanana337";  // ← change this

WebServer server(80);

// ============================================================
//  Camera Pins – AI Thinker ESP32-CAM
// ============================================================
#define PWDN_GPIO_NUM   32
#define RESET_GPIO_NUM  -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM   26
#define SIOC_GPIO_NUM   27
#define Y9_GPIO_NUM     35
#define Y8_GPIO_NUM     34
#define Y7_GPIO_NUM     39
#define Y6_GPIO_NUM     36
#define Y5_GPIO_NUM     21
#define Y4_GPIO_NUM     19
#define Y3_GPIO_NUM     18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM  25
#define HREF_GPIO_NUM   23
#define PCLK_GPIO_NUM   22

// ============================================================
//  Stream boundary constants
// ============================================================
#define PART_BOUNDARY "frame"

// ============================================================
//  Viewer HTML
// ============================================================
const char HTML_PAGE[] PROGMEM = R"(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{
  margin:0;
  background:#000;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
}
img{
  width:100vw;
  max-height:100vh;
  object-fit:contain;
}
</style>
</head>
<body>
<img src="/stream">
</body>
</html>
)";

// ============================================================
//  Root
// ============================================================
void handleRoot() {
    server.send_P(200, "text/html", HTML_PAGE);
}

// ============================================================
//  MJPEG Stream
// ============================================================
void handleStream() {
    WiFiClient client = server.client();
    client.setNoDelay(true);

    client.print("HTTP/1.1 200 OK\r\n");
    client.print("Content-Type: multipart/x-mixed-replace;boundary=" PART_BOUNDARY "\r\n");
    client.print("Cache-Control: no-cache, no-store, must-revalidate\r\n");
    client.print("Pragma: no-cache\r\n");
    client.print("Access-Control-Allow-Origin: *\r\n");
    client.print("\r\n");

    char partBuf[64];

    while (client.connected()) {
        camera_fb_t* fb = esp_camera_fb_get();
        if (!fb) { delay(5); continue; }

        client.print("--" PART_BOUNDARY "\r\n");
        client.print("Content-Type: image/jpeg\r\n");
        snprintf(partBuf, sizeof(partBuf), "Content-Length: %u\r\n\r\n", fb->len);
        client.print(partBuf);

        const size_t CHUNK = 4096;
        size_t sent = 0;
        while (sent < fb->len) {
            size_t toSend = min(CHUNK, fb->len - sent);
            client.write(fb->buf + sent, toSend);
            sent += toSend;
        }
        client.print("\r\n");

        esp_camera_fb_return(fb);
    }

    Serial.println("📡 Stream client disconnected");
}

// ============================================================
//  Camera – UMSL v0.2 settings
// ============================================================
void setupCamera() {
    camera_config_t cfg;

    cfg.ledc_channel = LEDC_CHANNEL_0;
    cfg.ledc_timer   = LEDC_TIMER_0;

    cfg.pin_d0       = Y2_GPIO_NUM;
    cfg.pin_d1       = Y3_GPIO_NUM;
    cfg.pin_d2       = Y4_GPIO_NUM;
    cfg.pin_d3       = Y5_GPIO_NUM;
    cfg.pin_d4       = Y6_GPIO_NUM;
    cfg.pin_d5       = Y7_GPIO_NUM;
    cfg.pin_d6       = Y8_GPIO_NUM;
    cfg.pin_d7       = Y9_GPIO_NUM;
    cfg.pin_xclk     = XCLK_GPIO_NUM;
    cfg.pin_pclk     = PCLK_GPIO_NUM;
    cfg.pin_vsync    = VSYNC_GPIO_NUM;
    cfg.pin_href     = HREF_GPIO_NUM;
    cfg.pin_sccb_sda = SIOD_GPIO_NUM;
    cfg.pin_sccb_scl = SIOC_GPIO_NUM;
    cfg.pin_pwdn     = PWDN_GPIO_NUM;
    cfg.pin_reset    = RESET_GPIO_NUM;

    cfg.xclk_freq_hz  = 20000000;
    cfg.pixel_format  = PIXFORMAT_JPEG;
    cfg.frame_size    = FRAMESIZE_QVGA;
    cfg.jpeg_quality  = 15;
    cfg.fb_count      = 3;
    cfg.grab_mode     = CAMERA_GRAB_LATEST;
    cfg.fb_location   = CAMERA_FB_IN_PSRAM;

    if (esp_camera_init(&cfg) != ESP_OK) {
        cfg.frame_size   = FRAMESIZE_QQVGA;
        cfg.jpeg_quality = 20;
        cfg.xclk_freq_hz = 10000000;
        cfg.fb_count     = 2;
        if (esp_camera_init(&cfg) != ESP_OK) {
            Serial.println("❌ Camera init failed!");
            return;
        }
        Serial.println("⚠️ Camera fallback mode");
    }

    sensor_t* s = esp_camera_sensor_get();
    if (s && s->id.PID == OV2640_PID) {
        s->set_framesize(s,      FRAMESIZE_QVGA);
        s->set_vflip(s,          1);
        s->set_hmirror(s,        1);
        s->set_brightness(s,     1);
        s->set_contrast(s,       0);
        s->set_saturation(s,     0);
        s->set_special_effect(s, 0);
        s->set_whitebal(s,       1);
        s->set_awb_gain(s,       1);
        s->set_gainceiling(s,    GAINCEILING_8X);
        s->set_colorbar(s,       0);
        s->set_ae_level(s,       0);
        s->set_aec2(s,           1);
        s->set_dcw(s,            1);
    }

    Serial.println("✅ Camera ready");
}

// ============================================================
//  Setup
// ============================================================
void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println("\n╔══════════════════════════════════════════╗");
    Serial.println("║  ESP32-CAM Fast Stream  (STA Mode)       ║");
    Serial.println("║  © Advanced Systems Lab UMSL 2026        ║");
    Serial.println("╚══════════════════════════════════════════╝\n");

    esp_bt_controller_deinit();
    setCpuFrequencyMhz(240);

    setupCamera();

    // ── WiFi Station Mode ────────────────────────────────────
    WiFi.mode(WIFI_STA);
    esp_wifi_set_ps(WIFI_PS_NONE);          // disable power-saving
    esp_wifi_set_max_tx_power(78);          // ~19.5 dBm max TX

    WiFi.begin(ssid, password);
    Serial.printf("🔌 Connecting to \"%s\" ", ssid);

    uint8_t attempts = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        if (++attempts > 40) {             // 20-second timeout
            Serial.println("\n❌ WiFi connection failed! Check SSID/password.");
            return;
        }
    }

    Serial.println(" ✅");
    Serial.printf("📡 IP      : %s\n",   WiFi.localIP().toString().c_str());
    Serial.printf("📶 RSSI    : %d dBm\n", WiFi.RSSI());
    Serial.printf("🎥 Stream  : http://%s/stream\n", WiFi.localIP().toString().c_str());
    Serial.printf("🌐 Viewer  : http://%s/\n",       WiFi.localIP().toString().c_str());

    server.on("/",       handleRoot);
    server.on("/stream", handleStream);
    server.onNotFound([]() { server.send(404, "text/plain", "404 Not Found"); });

    server.begin();
    Serial.println("✅ Server ready\n==========================================");
}

// ============================================================
//  Loop
// ============================================================
void loop() {
    // Auto-reconnect if WiFi drops
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("⚠️  WiFi lost – reconnecting...");
        WiFi.reconnect();
        delay(5000);
    }
    server.handleClient();
}