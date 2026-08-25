from datetime import date, timedelta
from django.core.management.base import BaseCommand
from accounts.models import AdminUser
from events.models import Event
from bookings.models import Booking
from core.models import Notification, Enquiry, HomepageContent
from destinations.models import Destination
from experiences.models import Experience
from gallery.models import GalleryItem
from testimonials.models import Testimonial
from faqs.models import FAQ
from stories.models import Story
from mining.models import MiningStage, MinerProfile
from site_settings.models import SiteSettings


class Command(BaseCommand):
    help = "Seeds demo data matching the React admin's mock data, for local development."

    def handle(self, *args, **options):
        self._seed_admin()
        self._seed_events()
        self._seed_bookings()
        self._seed_destinations()
        self._seed_gallery()
        self._seed_testimonials()
        self._seed_faqs()
        self._seed_stories()
        self._seed_mining()
        self._seed_site_settings()
        self._seed_homepage()
        self.stdout.write(self.style.SUCCESS("Done."))

    def _seed_admin(self):
        if not AdminUser.objects.filter(email="amina@pawmula.ltd").exists():
            AdminUser.objects.create_superuser(
                email="amina@pawmula.ltd", name="Amina Wanjiru", password="pawmula2026"
            )
            self.stdout.write(self.style.SUCCESS("Created super admin: amina@pawmula.ltd / pawmula2026"))

    def _seed_events(self):
        if Event.objects.filter(published=True).count() >= 2:
            return
        Event.objects.create(
            name="Migori Gold Trail Weekend", category="Mining",
            description="A two-day immersion into artisanal gold mining in Migori County, guided by working miners.",
            short_description="Two days with Migori's artisanal gold miners.",
            date=date.today() + timedelta(days=30), start_time="08:00", end_time="17:00",
            location="Masara, Migori County", county="Migori", price=4500, max_capacity=30,
            registered_count=22, registration_deadline=date.today() + timedelta(days=26),
            status="PUBLISHED", featured=True, published=True,
        )
        Event.objects.create(
            name="Thimlich Ohinga Heritage Walk", category="Heritage",
            description="Guided walking tour of the Thimlich Ohinga dry-stone enclosures, a UNESCO World Heritage Site.",
            short_description="Guided walk through the ancient stone enclosures.",
            date=date.today() + timedelta(days=16), start_time="09:00", end_time="13:00",
            location="Thimlich Ohinga, Migori County", county="Migori", price=1500, max_capacity=40,
            registered_count=40, registration_deadline=date.today() + timedelta(days=13),
            status="PUBLISHED", featured=True, published=True,
        )
        Event.objects.create(
            name="Community Cultural Evening", category="Community",
            description="An evening of Luo music, dance and food hosted by the Masara community.",
            short_description="An evening of music, dance and food.",
            date=date.today() + timedelta(days=52), start_time="17:00", end_time="21:00",
            location="Masara Community Grounds", county="Migori", price=800, max_capacity=100,
            registered_count=12, registration_deadline=date.today() + timedelta(days=50),
            status="DRAFT",
        )
        self.stdout.write(self.style.SUCCESS("Seeded 3 events"))

    def _seed_bookings(self):
        if Booking.objects.filter(status="CONFIRMED").count() >= 1:
            return
        b1 = Booking.objects.create(
            reference="PWM-1048", customer_name="John Doe", phone="+254 712 345 678",
            email="john@example.com", experiences=["Gold Mining Experience"], events=[],
            visit_date=date.today() + timedelta(days=30), guests=4, amount=18000, status="PENDING",
        )
        Booking.objects.create(
            reference="PWM-1047", customer_name="Grace Achieng", phone="+254 722 555 111",
            email="grace@example.com", experiences=["Gold Mining Experience", "Community Cultural Experience"],
            events=["Thimlich Ohinga Heritage Walk"], visit_date=date.today() + timedelta(days=16),
            guests=2, amount=7500, status="CONFIRMED", notes="Requested vegetarian meals.",
        )
        Notification.objects.create(
            type="booking", title="New booking received",
            body="John Doe booked Gold Mining Experience for 4 guests.", related_id=str(b1.id),
        )
        self.stdout.write(self.style.SUCCESS("Seeded 2 bookings + 1 notification"))

    def _seed_destinations(self):
        if Destination.objects.filter(published=True).count() >= 3:
            return
        d1 = Destination.objects.create(
            name="Thimlich Ohinga", county="Migori", location="Thimlich Ohinga, Migori County",
            short_description="A UNESCO World Heritage dry-stone enclosure site.",
            full_description="Thimlich Ohinga is the largest and best-preserved of the traditional dry-stone enclosures in the Lake Victoria region, dating back to the 16th century.",
            featured=True, published=True, display_order=1,
        )
        d2 = Destination.objects.create(
            name="Masara Gold Fields", county="Migori", location="Masara, Migori County",
            short_description="Artisanal gold mining community in the heart of Migori.",
            full_description="Masara is home to generations of artisanal gold miners, offering visitors an authentic look at Kenya's small-scale mining heritage.",
            featured=True, published=True, display_order=2,
        )
        d3 = Destination.objects.create(
            name="Lake Victoria Shoreline", county="Migori", location="Sori, Migori County",
            short_description="Quiet lakeside beaches on Africa's largest freshwater lake.",
            full_description="The Lake Victoria shoreline in Migori County offers peaceful beaches, fishing villages and boat trips to tropical islands far from tourist crowds.",
            featured=True, published=True, display_order=3,
        )
        d4 = Destination.objects.create(
            name="Tom Mboya Mausoleum", county="Migori", location="Kangeso, Migori County",
            short_description="Historic site honouring Kenya's independence-era leader.",
            full_description="The Tom Mboya Mausoleum preserves the legacy of one of Kenya's founding fathers, with guided tours covering his life, politics and assassination.",
            featured=False, published=True, display_order=4,
        )

        Experience.objects.create(
            name="Gold Mining Experience", category="Mining", destination=d2,
            description="Join working miners for a hands-on look at artisanal gold extraction, from panning to processing.",
            duration="Half day", price=4500, max_guests=15, featured=True, published=True,
        )
        Experience.objects.create(
            name="Thimlich Ohinga Walking Tour", category="Heritage", destination=d1,
            description="A guided walk through the ancient dry-stone enclosures with a local heritage expert.",
            duration="3 hours", price=1500, max_guests=20, featured=True, published=True,
        )
        Experience.objects.create(
            name="Lake Victoria Boat Trip", category="Nature", destination=d3,
            description="A sunset boat ride along the Lake Victoria shoreline with stops at fishing villages.",
            duration="4 hours", price=3000, max_guests=12, featured=True, published=True,
        )
        Experience.objects.create(
            name="Community Cultural Experience", category="Culture", destination=d2,
            description="Visit a Luo homestead for traditional cooking, storytelling and music.",
            duration="Half day", price=2500, max_guests=10, featured=False, published=True,
        )
        self.stdout.write(self.style.SUCCESS("Seeded 4 destinations + 4 experiences"))

    def _seed_gallery(self):
        if GalleryItem.objects.filter(published=True).count() >= 6:
            return
        placeholder = "https://placehold.co/800x600/1a3a2a/ffffff?text={}"
        items = [
            (placeholder.format("Thimlich+Ohinga"), "image", "Thimlich Ohinga", "Ancient dry-stone enclosures at sunrise", "Thimlich Ohinga stone walls", "Heritage"),
            (placeholder.format("Gold+Panning"), "image", "Gold Panning at Masara", "Miners pan for gold in the Migori River", "Gold panning in river", "Mining"),
            (placeholder.format("Lake+Victoria"), "image", "Lake Victoria Sunset", "Golden light over Africa's largest lake", "Lake Victoria at sunset", "Nature"),
            (placeholder.format("Mining+Pit"), "image", "Inside the Mining Pit", "A miner descends into an artisanal gold pit", "Artisanal mining pit", "Mining"),
            (placeholder.format("Community+Dance"), "image", "Community Dance", "Luo cultural dance performance at Masara", "Luo traditional dance", "Culture"),
            (placeholder.format("Stone+Walls"), "image", "Close-up of Stonework", "Detailed view of the dry-stone construction technique", "Dry-stone wall detail", "Heritage"),
            (placeholder.format("Fish+Market"), "image", "Sori Fish Market", "Daily catch arriving at the Lake Victoria shore", "Fish market at Sori", "Community"),
            (placeholder.format("Mining+Tools"), "image", "Mining Tools of the Trade", "Pickaxes, pans and crushers used in artisanal mining", "Artisanal mining tools", "Mining"),
        ]
        for url, ftype, title, caption, alt, cat in items:
            GalleryItem.objects.create(
                file_url=url, file_type=ftype, title=title, caption=caption,
                alt_text=alt, category=cat, featured=cat in ("Heritage", "Mining"),
                published=True,
            )
        self.stdout.write(self.style.SUCCESS("Seeded 8 gallery items"))

    def _seed_testimonials(self):
        if Testimonial.objects.filter(published=True).count() >= 3:
            return
        Testimonial.objects.create(
            name="Amara Nyong'o", location="Nairobi, Kenya", role="Travel Writer",
            quote="The mining walk was the most honest travel experience I have ever had. Every step told a story of resilience and craft.",
            rating=5, featured=True, published=True, display_order=1,
        )
        Testimonial.objects.create(
            name="Daniel Fischer", location="Berlin, Germany", role="Backpacker",
            quote="Thim Lich Ohinga at sunrise, with a local guide who grew up in its shadow — that is the kind of travel I seek.",
            rating=5, featured=True, published=True, display_order=2,
        )
        Testimonial.objects.create(
            name="Prof. Lydia Kimani", location="Kisumu, Kenya", role="Archaeology Lecturer",
            quote="Our students saw the full processing chain. The miners explained every step with a pride that no textbook can replicate.",
            rating=5, featured=True, published=True, display_order=3,
        )
        self.stdout.write(self.style.SUCCESS("Seeded 3 testimonials"))

    def _seed_faqs(self):
        if FAQ.objects.filter(published=True).count() >= 5:
            return
        faqs = [
            ("Is visiting an active mine safe?", "Yes. All mining visits are supervised by trained guides and follow safety protocols. Helmets and protective gear are provided."),
            ("How much do tours cost?", "Prices range from KES 1,500 to KES 18,000 depending on the destination and experience type. See individual listings for details."),
            ("Where do we stay?", "We partner with local guesthouses, community homestays and mid-range hotels in Migori and Kisumu counties."),
            ("How do we get there?", "Migori is accessible by road from Nairobi (5-6 hours) or by flight to Kisumu then road transfer. We can arrange transfers from the nearest regional hub."),
            ("Do miners benefit from these visits?", "Absolutely. A significant portion of tour fees goes directly to mining cooperatives and community development funds."),
            ("What payment methods do you accept?", "M-Pesa, bank transfer and cash. International visitors can pay via card through our secure payment link."),
        ]
        for i, (q, a) in enumerate(faqs, 1):
            FAQ.objects.create(question=q, answer=a, display_order=i, published=True)
        self.stdout.write(self.style.SUCCESS("Seeded 6 FAQs"))

    def _seed_stories(self):
        if Story.objects.filter(published=True).count() >= 3:
            return
        story1_content = (
            "Before dawn, Otieno Ochieng straps on his headlamp and walks "
            "two kilometers to the pit mouth. By the time the sun clears the "
            "hillside, he has already been working for three hours.\n\n"
            "Artisanal mining in Migori County is not industrial extraction. "
            "It is craft, patience and generational knowledge passed down "
            "through families. The tools have changed, but the essential "
            "relationship between miner and rock remains.\n\n"
            "Otieno has been mining for twenty-three years. He knows the "
            "veins in his section of the pit the way a farmer knows his "
            "fields. He can tell by the color of the tailings whether gold "
            "is near.\n\n"
            "Tourism has changed things. When Pawmula first brought visitors "
            "to the pit, the miners were skeptical. Now they compete for the "
            "chance to guide a group through their workplace. It is extra "
            "income, yes, but it is also recognition."
        )
        Story.objects.create(
            title="A Day in the Life of an Artisanal Miner", category="Mining",
            excerpt="Before dawn, Otieno Ochieng straps on his headlamp and walks two kilometers to the pit mouth.",
            content=story1_content,
            author="Pawmula Editorial", location="Masara, Migori County",
            publish_date=date(2026, 3, 12), status="PUBLISHED", published=True, featured=True,
        )
        story2_content = (
            "Gold has been mined in western Kenya for over a century. The "
            "story of Migori's gold fields is inseparable from the story of "
            "its people.\n\n"
            "The first recorded small-scale mining in the region dates to the "
            "1930s, when colonial prospectors identified alluvial deposits "
            "along the Migori River. But local communities had long known "
            "about the yellow metal in the riverbeds.\n\n"
            "After independence, the government formalized some mining "
            "operations but left much of the artisanal work in a legal gray "
            "zone. It was not until the 2000s that cooperative structures "
            "began to emerge.\n\n"
            "Today, Migori County hosts an estimated 20,000 artisanal miners. "
            "They work in shifting teams, moving between sites as deposits "
            "are exhausted and new ones are discovered."
        )
        Story.objects.create(
            title="The History of Gold Mining in Migori", category="Heritage",
            excerpt="Gold has been mined in western Kenya for over a century.",
            content=story2_content,
            author="Pawmula Editorial", location="Migori County",
            publish_date=date(2026, 2, 28), status="PUBLISHED", published=True,
        )
        story3_content = (
            "Day One: Heritage and History\n\n"
            "Start at Thimlich Ohinga, arriving early to beat the midday "
            "heat. The dry-stone enclosures are best seen in morning light "
            "when the shadows define the walls. Allow two hours for the "
            "guided walk.\n\n"
            "After lunch in Migori town, visit the Tom Mboya Mausoleum to "
            "learn about Kenya's independence-era politics.\n\n"
            "Day Two: Mining and Culture\n\n"
            "Spend the morning at Masara gold fields. The mining experience "
            "tour includes a walk through active pits, a demonstration of "
            "the processing chain and a chance to pan for gold yourself.\n\n"
            "In the afternoon, visit a community homestead for a cultural "
            "session. Learn about Luo homestead design and traditional "
            "cooking.\n\n"
            "Day Three: Nature and Beach\n\n"
            "Drive to Lake Victoria and spend the morning at either Muhuru "
            "Bay or Sori Beach. Both offer quiet waterside settings far from "
            "the tourist crowds."
        )
        Story.objects.create(
            title="Travel Guide: Three Days Around Migori", category="Guide",
            excerpt="A three-day itinerary covering heritage sites, mining experiences, nature walks and community cultural encounters.",
            content=story3_content,
            author="Pawmula Editorial", location="Migori County",
            publish_date=date(2026, 2, 10), status="PUBLISHED", published=True,
        )
        self.stdout.write(self.style.SUCCESS("Seeded 3 stories"))

    def _seed_mining(self):
        if MiningStage.objects.filter(published=True).count() >= 6:
            return
        stages = [
            ("Extraction", "Miners extract gold-bearing ore from open pits or shallow underground tunnels using hand tools and compressed-air drills.", "Pickaxes, shovels, compressed-air drills, headlamps", "Hard hats, steel-toed boots, dust masks, ventilation checks", "The extraction team"),
            ("Crushing", "Large rocks are broken down into smaller fragments using manual or mechanical crushers.", "Jaw crushers, hammer mills, steel plates", "Hearing protection, dust masks, gloves", "The crushing crew"),
            ("Milling", "Crushed ore is ground into fine powder using ball mills or stamp mills to liberate gold particles from the host rock.", "Ball mills, stamp mills, water supply", "Hearing protection, gloves, eye protection", "The milling operators"),
            ("Concentration", "The milled powder is mixed with water and processed through sluice boxes or shaking tables to concentrate heavy gold particles.", "Sluice boxes, shaking tables, water pumps", "Rubber boots, gloves, slip-resistant surfaces", "The concentration team"),
            ("Amalgamation", "Mercury is added to the concentrated ore to form a gold-mercury amalgam. This step requires careful handling and ventilation.", "Mercury, mixing pans, ventilation equipment", "Nitrile gloves, respirators, fume extraction", "Trained amalgamation specialists"),
            ("Leaching", "Cyanide solution is sometimes used to dissolve remaining gold from lower-grade ore. This is a controlled process with strict safety protocols.", "Leach tanks, cyanide solution, pH meters", "Full-face respirators, chemical-resistant suits, emergency showers", "Certified chemical operators"),
            ("Elution", "The gold is stripped from activated carbon using a hot caustic solution in a controlled process.", "Elution columns, heating systems, caustic solution", "Heat-resistant gloves, face shields, chemical-resistant aprons", "Process engineers"),
            ("Gold Recovery", "Final smelting and casting of recovered gold into bars or granules for sale to refineries.", "Furnaces, crucibles, moulds, precision scales", "Heat-resistant clothing, face shields, ventilation", "The smelting team"),
        ]
        for i, (name, desc, equip, safety, role) in enumerate(stages, 1):
            MiningStage.objects.create(
                name=name, description=desc, equipment=equip, safety_info=safety,
                role=role, display_order=i, published=True,
            )

        miners = [
            ("Otieno Ochieng", 23, "I started mining with my father when I was sixteen. Back then we used only shovels and pans. The rock gives nothing to the impatient — you learn that in your first week or you leave.", "The rock gives nothing to the impatient. You learn patience here or you leave."),
            ("Akinyi Were", 15, "Women were invisible in the mines for years. Now we run our own cooperative. We used to be invisible at the sluice — now we run our own cooperative. That is the real gold.", "We used to be invisible at the sluice — now we run our own cooperative. That is the real gold."),
            ("Brian Omondi", 8, "I came to mining after university. People thought I was crazy. But safer mining is not slower mining — it is smarter mining. We are proving that every day.", "Safer mining is not slower mining — it is smarter mining. We are proving that every day."),
        ]
        for i, (name, years, story, quote) in enumerate(miners, 1):
            MinerProfile.objects.create(
                name=name, years_active=years, story=story, quote=quote,
                featured=True, published=True, display_order=i,
            )
        self.stdout.write(self.style.SUCCESS("Seeded 8 mining stages + 3 miner profiles"))

    def _seed_site_settings(self):
        settings = SiteSettings.get_solo()
        if settings.company_name != "PAWMULA.LTD":
            return
        settings.phone_numbers = ["+254724 548 142", "+254715 130 559"]
        settings.social_links = {
            "instagram": "https://instagram.com/pawmula",
            "facebook": "https://facebook.com/pawmula",
            "youtube": "https://youtube.com/@pawmula",
        }
        settings.map_embed_url = "https://www.openstreetmap.org/export/embed.html?bbox=34.0,0.0,34.5,0.5"
        settings.save()
        self.stdout.write(self.style.SUCCESS("Seeded site settings"))

    def _seed_homepage(self):
        hp = HomepageContent.get_solo()
        if hp.hero_heading != HomepageContent._meta.get_field("hero_heading").default:
            return
        hp.featured_destination_slugs = [
            "thimlich-ohinga", "kakamega-forest", "kit-mikayi",
            "rusinga-fossil-sites", "gogo-falls", "kisumu-impala-sanctuary",
        ]
        hp.trust_badges = [
            {"icon": "Users", "title": "Community-driven tourism", "text": "Every journey is hosted and guided by local communities."},
            {"icon": "Pickaxe", "title": "Authentic mining experiences", "text": "Walk through active mines with the people who work them."},
            {"icon": "MapPin", "title": "Professional guides", "text": "Knowledgeable local guides at every destination."},
            {"icon": "Shield", "title": "Safe travel", "text": "Safety-first approach at every mining and adventure site."},
            {"icon": "Leaf", "title": "Sustainable development", "text": "Tourism revenue directly funds community projects."},
        ]
        hp.about_blocks = [
            {"heading": "Our story", "paragraph": "Pawmula Ltd was founded to open Kenya's hidden heritage to the world. We believed that the stories, landscapes and craft of western Kenya deserved a platform built by the people who live them."},
            {"heading": "Our mission", "paragraph": "To create sustainable tourism pathways that benefit local communities while delivering authentic, transformative travel experiences."},
            {"heading": "Our vision", "paragraph": "A western Kenya where heritage tourism empowers communities to preserve and share their culture on their own terms."},
            {"heading": "Community impact", "paragraph": "Every booking directly supports mining cooperatives, cultural preservation projects and youth employment initiatives across Migori and Kisumu counties."},
        ]
        hp.community_stats = [
            {"label": "Families Supported", "value": 1240},
            {"label": "Youth Empowered", "value": 480},
            {"label": "Mining Cooperatives", "value": 17},
            {"label": "Visitors Hosted", "value": 6300},
            {"label": "Community Projects", "value": 32},
        ]
        hp.cta_title = "Your journey into Kenya's heritage starts here"
        hp.cta_subtitle = "Whether you are drawn to ancient stone walls, gold-bearing rock or the rhythm of a lakeside community, we will build a journey that is yours."
        hp.save()
        self.stdout.write(self.style.SUCCESS("Seeded homepage content"))
