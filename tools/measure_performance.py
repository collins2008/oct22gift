import os
import sys
import json
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def measure():
    print("=== MEASURING PERFORMANCE (SLOW 4G + 4x CPU THROTTLE) ===")
    html_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        
        # Connect CDP Session for throttling
        client = page.context.new_cdp_session(page)
        
        # 4x CPU slowdown
        client.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        
        # Slow 4G Network Throttling
        # 1.6 Mbps download = 200,000 bytes/sec
        # 750 Kbps upload = 93,750 bytes/sec
        # Latency = 150 ms
        client.send('Network.emulateNetworkConditions', {
            'offline': False,
            'downloadThroughput': 200 * 1024,
            'uploadThroughput': 93 * 1024,
            'latency': 150
        })

        requests = []
        transferred_bytes = 0

        def on_response(response):
            nonlocal transferred_bytes
            try:
                body = response.body()
                size = len(body)
                transferred_bytes += size
                requests.append({
                    'url': response.url.split('/')[-1],
                    'status': response.status,
                    'size': size
                })
            except Exception:
                pass

        page.on('response', on_response)

        start_time = page.evaluate('() => performance.now()')
        page.goto(html_url)
        page.wait_for_selector('.screen.active')
        end_time = page.evaluate('() => performance.now()')

        # Get performance timing
        perf_data = page.evaluate('''() => {
            const nav = performance.getEntriesByType('navigation')[0] || {};
            const paint = performance.getEntriesByType('paint');
            let fcp = 0;
            paint.forEach(p => {
                if (p.name === 'first-contentful-paint') fcp = p.startTime;
            });
            return {
                fcp: fcp,
                domInteractive: nav.domInteractive || 0,
                loadEventEnd: nav.loadEventEnd || 0
            };
        }''')

        # Measure CLS (Cumulative Layout Shift)
        cls = page.evaluate('''() => {
            return new Promise(resolve => {
                let clsScore = 0;
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            clsScore += entry.value;
                        }
                    }
                });
                observer.observe({ type: 'layout-shift', buffered: true });
                setTimeout(() => resolve(clsScore), 500);
            });
        }''')

        print(f"Request Count: {len(requests)}")
        print(f"First-Screen Total Transfer: {transferred_bytes / 1024:.2f} KB")
        print(f"Time to Interactive: {(end_time - start_time) / 1000:.2f} s")
        print(f"FCP (First Contentful Paint): {perf_data['fcp']:.2f} ms")
        print(f"CLS (Cumulative Layout Shift): {cls:.4f}")

        # Measure letter screen transition FPS / duration
        t0 = page.evaluate('() => performance.now()')
        page.click('#btn-what')
        page.wait_for_timeout(250)
        t1 = page.evaluate('() => performance.now()')
        print(f"Screen 1->2 Transition Duration: {t1 - t0:.2f} ms")

        browser.close()

if __name__ == '__main__':
    measure()
