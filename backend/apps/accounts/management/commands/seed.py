"""Demo ma'lumotlar generatsiyasi management command."""
import hashlib
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.notifications.models import Notification
from apps.sites.models import Site
from apps.tracking.models import Event, PageView, Session

User = get_user_model()


class Command(BaseCommand):
    help = "Demo ma'lumotlar bilan bazani to'ldiradi"

    def handle(self, *args, **options):
        if Session.objects.exists():
            self.stdout.write(self.style.SUCCESS("Seed data allaqachon mavjud. O'tkazib yuborildi."))
            return

        self.stdout.write("Demo ma'lumotlar yaratilmoqda...")

        user, created = User.objects.get_or_create(
            email="demo@example.com",
            defaults={"full_name": "Demo Foydalanuvchi", "is_active": True},
        )
        if created:
            user.set_password("demo1234")
            user.save()
            self.stdout.write(f"  + Foydalanuvchi: {user.email}")

        sites = []
        for name, domain in [("Mening blogim", "blog.example.com"), ("Online do'kon", "shop.example.com")]:
            site, _ = Site.objects.get_or_create(user=user, domain=domain, defaults={"name": name})
            sites.append(site)
            self.stdout.write(f"  + Sayt: {site.name}")

        countries = [
            ("UZ", "Uzbekistan", "Toshkent", 41.31, 69.24),
            ("RU", "Russia", "Moscow", 55.75, 37.61),
            ("KZ", "Kazakhstan", "Almaty", 43.25, 76.91),
            ("US", "United States", "New York", 40.71, -74.00),
        ]
        browsers = [("Chrome", "121.0"), ("Firefox", "122.0"), ("Safari", "17.2"), ("Edge", "121.0")]
        oses = [("Windows", "10"), ("macOS", "14"), ("Android", "13"), ("iOS", "17")]
        pages = ["/", "/about", "/blog", "/blog/post-1", "/contact", "/services", "/pricing"]
        referrers = ["", "https://google.com", "https://facebook.com", "https://t.me/somechannel"]

        for site in sites:
            for i in range(50):
                country = random.choice(countries)
                browser = random.choice(browsers)
                os_info = random.choice(oses)
                started = timezone.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
                session = Session.objects.create(
                    site=site,
                    session_uid=hashlib.md5(f"{site.id}-{i}".encode()).hexdigest(),
                    ip_hash=hashlib.sha256(f"{random.random()}".encode()).hexdigest(),
                    country=country[1],
                    country_code=country[0],
                    city=country[2],
                    latitude=country[3],
                    longitude=country[4],
                    browser=browser[0],
                    browser_version=browser[1],
                    os=os_info[0],
                    os_version=os_info[1],
                    device="Mobile" if random.random() < 0.4 else "Desktop",
                    is_mobile=random.random() < 0.4,
                    referrer=random.choice(referrers),
                    started_at=started,
                )
                session.started_at = started
                session.save(update_fields=["started_at"])

                page_count = random.randint(1, 5)
                for j in range(page_count):
                    pv_time = started + timedelta(seconds=j * random.randint(10, 60))
                    pv = PageView.objects.create(
                        site=site,
                        session=session,
                        url=random.choice(pages),
                        title=f"Sahifa {j + 1}",
                        referrer=session.referrer if j == 0 else "",
                        load_time_ms=random.randint(500, 3000),
                        lcp_ms=random.randint(800, 2500),
                        fcp_ms=random.randint(400, 1500),
                        ttfb_ms=random.randint(100, 800),
                    )
                    pv.timestamp = pv_time
                    pv.save(update_fields=["timestamp"])

                    if random.random() < 0.3:
                        e = Event.objects.create(
                            site=site,
                            session=session,
                            type="click",
                            target=f"button.{random.choice(['cta', 'menu', 'submit'])}",
                            metadata={"x": random.randint(0, 1920), "y": random.randint(0, 1080)},
                        )
                        e.timestamp = pv_time
                        e.save(update_fields=["timestamp"])

                session.page_count = page_count
                session.is_bounce = page_count == 1
                session.duration_sec = (page_count - 1) * 30 if page_count > 1 else 0
                session.ended_at = started + timedelta(seconds=session.duration_sec or 0)
                session.save()

        Notification.objects.create(
            user=user,
            site=sites[0],
            type=Notification.Type.ANOMALY,
            title="Trafik anomaliyasi aniqlandi",
            message="Soat 14:00'da trafik 200% oshib ketdi.",
        )
        Notification.objects.create(
            user=user,
            site=sites[1],
            type=Notification.Type.INFO,
            title="Yangi statistika tayyor",
            message="Haftalik hisobot generatsiya qilindi.",
            is_read=True,
        )

        self.stdout.write(self.style.SUCCESS("Demo ma'lumotlar muvaffaqiyatli yaratildi!"))
        self.stdout.write(self.style.SUCCESS("Login: demo@example.com / demo1234"))
