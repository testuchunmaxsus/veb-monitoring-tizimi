"""Loyiha sahifalaridan screenshot olish."""
import asyncio
import os
from playwright.async_api import async_playwright

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

FRONTEND = "http://localhost:5173"

PAGES = [
    ("login", "/login"),
    ("register", "/register"),
    ("dashboard", "/dashboard"),
    ("sites", "/sites"),
    ("site_overview", "/sites/1"),
    ("site_devices", "/sites/1?tab=devices"),
    ("site_geo", "/sites/1?tab=geo"),
    ("realtime", "/realtime"),
    ("reports", "/reports"),
    ("notifications", "/notifications"),
    ("settings", "/settings"),
]


async def login(page):
    await page.goto(f"{FRONTEND}/login", wait_until="networkidle")
    await page.fill('input[type="email"]', "demo@example.com")
    await page.fill('input[type="password"]', "demo1234")
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{FRONTEND}/dashboard", timeout=10000)
    await page.wait_for_load_state("networkidle")


async def screenshot_login(page, name):
    await page.goto(f"{FRONTEND}/login", wait_until="networkidle")
    await page.wait_for_timeout(500)
    path = os.path.join(OUT, f"app_{name}.png")
    await page.screenshot(path=path, full_page=False)
    return path


async def screenshot_register(page, name):
    await page.goto(f"{FRONTEND}/register", wait_until="networkidle")
    await page.wait_for_timeout(500)
    path = os.path.join(OUT, f"app_{name}.png")
    await page.screenshot(path=path, full_page=False)
    return path


async def screenshot_authed(page, name, path):
    await page.goto(f"{FRONTEND}{path}", wait_until="networkidle")
    await page.wait_for_timeout(2000)
    out = os.path.join(OUT, f"app_{name}.png")
    await page.screenshot(path=out, full_page=True)
    return out


async def click_tab(page, label, name):
    await page.goto(f"{FRONTEND}/sites/1", wait_until="networkidle")
    await page.wait_for_timeout(1500)
    try:
        await page.click(f'button:has-text("{label}")', timeout=3000)
        await page.wait_for_timeout(2000)
    except Exception as exc:
        print(f"  Tab '{label}' bosib bo'lmadi: {exc}")
    out = os.path.join(OUT, f"app_{name}.png")
    await page.screenshot(path=out, full_page=True)
    return out


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.5,
        )
        page = await context.new_page()
        # Console errorlarni ko'rmaslik
        page.on("pageerror", lambda exc: None)
        page.on("console", lambda msg: None)

        results = []

        # 1. Login (auth bo'lmagan holda)
        results.append(await screenshot_login(page, "login"))
        print("  app_login.png")

        # 2. Register
        results.append(await screenshot_register(page, "register"))
        print("  app_register.png")

        # 3. Login bo'lib, autentifikatsiya
        await login(page)

        # 4. Asosiy sahifalar
        for (name, path_) in [
            ("dashboard", "/dashboard"),
            ("sites", "/sites"),
            ("site_overview", "/sites/1"),
        ]:
            results.append(await screenshot_authed(page, name, path_))
            print(f"  app_{name}.png")

        # 5. Site Details tablar
        results.append(await click_tab(page, "Qurilmalar", "site_devices"))
        print("  app_site_devices.png")
        results.append(await click_tab(page, "Geografiya", "site_geo"))
        print("  app_site_geo.png")
        results.append(await click_tab(page, "Sahifalar", "site_pages"))
        print("  app_site_pages.png")

        # 6. Boshqa sahifalar
        for (name, path_) in [
            ("realtime", "/realtime"),
            ("reports", "/reports"),
            ("notifications", "/notifications"),
            ("settings", "/settings"),
        ]:
            results.append(await screenshot_authed(page, name, path_))
            print(f"  app_{name}.png")

        # 7. Admin paneli (alohida context)
        admin_page = await context.new_page()
        await admin_page.goto("http://localhost:8000/admin/login/", wait_until="networkidle")
        await admin_page.fill('input[name="username"]', "admin@example.com")
        await admin_page.fill('input[name="password"]', "admin12345")
        await admin_page.click('input[type="submit"]')
        await admin_page.wait_for_url("**/admin/", timeout=10000)
        await admin_page.wait_for_timeout(1000)
        admin_path = os.path.join(OUT, "app_admin.png")
        await admin_page.screenshot(path=admin_path, full_page=True)
        print("  app_admin.png")
        results.append(admin_path)

        # 8. Swagger UI
        swagger_page = await context.new_page()
        await swagger_page.goto("http://localhost:8000/api/docs/", wait_until="networkidle")
        await swagger_page.wait_for_timeout(2000)
        swagger_path = os.path.join(OUT, "app_swagger.png")
        await swagger_page.screenshot(path=swagger_path, full_page=False)
        print("  app_swagger.png")
        results.append(swagger_path)

        await browser.close()

        print(f"\nJami {len(results)} ta screenshot saqlandi: {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
