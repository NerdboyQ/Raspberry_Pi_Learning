#if !defined(INCLUDE_NETWORK_C)
#define INCLUDE_NETWORK_C

#include "common.h"
#include "hardware/rtc.h"

// Callback triggered when the NTP server replies
static void ntp_recv(void *arg, struct udp_pcb *pcb, struct pbuf *p, const ip_addr_t *addr, u16_t port) {
    if (p != NULL) {
        if (p->tot_len == NTP_MSG_LEN) {
            uint8_t seconds_buf[4];
            // Bytes 40-43 contain the 32-bit transmit timestamp (seconds since 1900)
            pbuf_copy_partial(p, seconds_buf, sizeof(seconds_buf), 40);
            uint32_t seconds_since_1900 = (seconds_buf[0] << 24) | (seconds_buf[1] << 16) |
                                          (seconds_buf[2] << 8)  |  seconds_buf[3];

            time_t epoch = seconds_since_1900 - NTP_DELTA;
            struct tm *utc = gmtime(&epoch);

            // Load into the RP2040 hardware RTC
            datetime_t t = {
                .year  = utc->tm_year + 1900,
                .month = utc->tm_mon + 1,
                .day   = utc->tm_mday,
                .dotw  = utc->tm_wday,
                .hour  = utc->tm_hour,
                .min   = utc->tm_min,
                .sec   = utc->tm_sec
            };
            rtc_set_datetime(&t);
            printf("Synced UTC: %04d-%02d-%02d %02d:%02d:%02d\n",
                   t.year, t.month, t.day, t.hour, t.min, t.sec);
            ntp_done = true;
        }
        pbuf_free(p);
    }
}

static void send_ntp_request(struct udp_pcb *pcb, const ip_addr_t *ntp_ip) {
    cyw43_arch_lwip_begin();
    struct pbuf *p = pbuf_alloc(PBUF_TRANSPORT, NTP_MSG_LEN, PBUF_RAM);
    memset(p->payload, 0, NTP_MSG_LEN);
    ((uint8_t *)p->payload)[0] = 0x1B; // LI = 0, VN = 3, Mode = 3 (Client)
    udp_sendto(pcb, p, ntp_ip, NTP_PORT);
    pbuf_free(p);
    cyw43_arch_lwip_end();
}

#endif // INCLUDE_NETWORK_C