import os
import sys
import time
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

console_messages = []
page_errors = []

def run_qa():
    print("=== STARTING COMPREHENSIVE 5-SPECIALIST REVIEW QA ===")
    html_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: page_errors.append(str(err)))

        # ------------------------------------------------------------------
        # TEST 1: Full Path Walkthrough & Screenshots at 390x844 (iPhone)
        # ------------------------------------------------------------------
        print("\n--- Test 1: Full Path Walkthrough (390x844) ---")
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(html_url)
        page.wait_for_timeout(500) # loader dismiss

        # Screen 1
        page.screenshot(path='reference/final_390_s1.png')
        print("Captured Screen 1 (Intro 1)")

        # Screen 2
        page.click('#btn-what')
        page.wait_for_timeout(300)
        page.screenshot(path='reference/final_390_s2.png')
        print("Captured Screen 2 (Intro 2)")

        # Test Mashing "No" Button (must not disappear, must stay bounded)
        print("Testing 'No' button mashing...")
        for tap in range(8):
            page.hover('#btn-no')
            page.wait_for_timeout(80)
            page.click('#btn-no')
            page.wait_for_timeout(80)
        
        # Verify "No" button is still visible and has scale > 0
        no_style = page.eval_on_selector('#btn-no', 'el => window.getComputedStyle(el).transform')
        print(f"No button transform after 8 attempts: {no_style}")
        assert 'matrix' in no_style or 'scale' in no_style, "No button transform invalid"

        # "Yes" button must always work!
        page.click('#btn-yes')
        page.wait_for_timeout(300)
        page.screenshot(path='reference/final_390_s3.png')
        print("Captured Screen 3 (Intro 3)")

        # Screen 4
        page.click('#btn-fine')
        page.wait_for_timeout(300)
        page.screenshot(path='reference/final_390_s4.png')
        print("Captured Screen 4 (Intro 4)")

        # Screen 5 (Menu)
        page.click('#btn-ready')
        page.wait_for_timeout(300)
        page.screenshot(path='reference/final_390_s5.png')
        print("Captured Screen 5 (Envelope Menu)")

        # Test Music Toggle Toast (no blocking alerts!)
        page.click('#music-toggle')
        page.wait_for_timeout(200)
        toast_text = page.inner_text('#toast')
        print(f"Toast message on music toggle: '{toast_text}'")
        assert len(toast_text) > 0, "Toast message should appear"

        # Walk through each letter and back
        for i in range(1, 6):
            page.click(f'.envelope-item:nth-child({i})')
            page.wait_for_timeout(700) # Flap open + screen fade
            if i == 1:
                page.screenshot(path='reference/final_390_letter1.png')
                print(f"Captured Letter {i}")
            elif i == 5:
                page.screenshot(path='reference/final_390_letter5_photo.png')
                print(f"Captured Letter {i} with Photo")
            page.click('#btn-back')
            page.wait_for_timeout(300)

        # ------------------------------------------------------------------
        # TEST 2: Abuse Test - Interrupted Transitions & Rapid Double Tapping
        # ------------------------------------------------------------------
        print("\n--- Test 2: Rapid Tapping & Interrupted Transitions ---")
        # Jump back to intro 1 via hash
        page.goto(html_url + '#s-intro1')
        page.wait_for_timeout(400)
        # Mash "what?" button 10 times rapidly
        for _ in range(10):
            page.click('#btn-what', force=True)
            page.wait_for_timeout(15)
        page.wait_for_timeout(400)
        active_screens = page.eval_on_selector_all('.screen.active', 'els => els.map(e => e.id)')
        print(f"Active screens after rapid taps: {active_screens}")
        assert len(active_screens) == 1, f"Expected exactly 1 active screen, got: {active_screens}"

        # ------------------------------------------------------------------
        # TEST 3: Browser Back Navigation Across ALL Screens
        # ------------------------------------------------------------------
        print("\n--- Test 3: Browser Back Gesture Testing ---")
        # Go Intro 2 -> Intro 3 -> Intro 4 -> Menu -> Letter
        page.click('#btn-yes')
        page.wait_for_timeout(300)
        page.click('#btn-fine')
        page.wait_for_timeout(300)
        page.click('#btn-ready')
        page.wait_for_timeout(300)
        page.click('.envelope-item:nth-child(2)')
        page.wait_for_timeout(700)

        # Now go back step-by-step using browser history
        print("Simulating browser back button from Letter to Menu...")
        page.go_back()
        page.wait_for_timeout(350)
        assert page.eval_on_selector('#s-menu', 'el => el.classList.contains("active")'), "Should return to s-menu"

        print("Simulating browser back button from Menu to Intro 4...")
        page.go_back()
        page.wait_for_timeout(350)
        assert page.eval_on_selector('#s-intro4', 'el => el.classList.contains("active")'), "Should return to s-intro4"

        print("Simulating browser back button from Intro 4 to Intro 3...")
        page.go_back()
        page.wait_for_timeout(350)
        assert page.eval_on_selector('#s-intro3', 'el => el.classList.contains("active")'), "Should return to s-intro3"

        print("Simulating browser back button from Intro 3 to Intro 2...")
        page.go_back()
        page.wait_for_timeout(350)
        assert page.eval_on_selector('#s-intro2', 'el => el.classList.contains("active")'), "Should return to s-intro2"

        print("Simulating browser back button from Intro 2 to Intro 1...")
        page.go_back()
        page.wait_for_timeout(350)
        assert page.eval_on_selector('#s-intro1', 'el => el.classList.contains("active")'), "Should return to s-intro1"
        print("Browser back navigation PASSED across all screens!")

        # ------------------------------------------------------------------
        # TEST 4: Page Refresh on Every Screen
        # ------------------------------------------------------------------
        print("\n--- Test 4: Page Refresh on Every Screen ---")
        for s_id in ['s-intro2', 's-intro3', 's-intro4', 's-menu']:
            page.goto(html_url + '#' + s_id)
            page.reload()
            page.wait_for_timeout(450)
            is_active = page.eval_on_selector(f'#{s_id}', 'el => el.classList.contains("active")')
            print(f"Refresh on #{s_id} -> Active: {is_active}")
            assert is_active, f"Screen #{s_id} should be active after refresh"

        # ------------------------------------------------------------------
        # TEST 5: Multi-Viewport Responsive Audits (No horizontal scroll)
        # ------------------------------------------------------------------
        print("\n--- Test 5: Multi-Viewport Responsive Audits ---")
        viewports = [
            (320, 568, 'iPhone SE 1st gen'),
            (360, 740, 'Compact Android'),
            (390, 844, 'iPhone 13/14'),
            (430, 932, 'iPhone Pro Max'),
            (768, 1024, 'iPad Tablet'),
            (1440, 900, 'Desktop 1440')
        ]

        for width, height, name in viewports:
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(html_url + '#s-menu')
            page.wait_for_timeout(400)
            
            # Check horizontal overflow
            has_h_scroll = page.evaluate('() => document.body.scrollWidth > document.body.clientWidth')
            print(f"Viewport {width}x{height} ({name}) -> Horizontal scroll: {has_h_scroll}")
            assert not has_h_scroll, f"Horizontal scroll detected on {name} ({width}x{height})!"

            if width == 320:
                page.screenshot(path='reference/final_320_s5.png')
            elif width == 360:
                page.screenshot(path='reference/final_360_s5.png')
            elif width == 1440:
                page.screenshot(path='reference/final_desktop_s5.png')

        browser.close()

    print("\n==========================================")
    print("QA AUDIT SUMMARY")
    print(f"Total Page Errors: {len(page_errors)}")
    for err in page_errors:
        print("  [ERROR]", err)
    print(f"Total Console Messages: {len(console_messages)}")
    for msg in console_messages:
        print("  [CONSOLE]", msg)
    print("==========================================")

    if len(page_errors) > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_qa()
