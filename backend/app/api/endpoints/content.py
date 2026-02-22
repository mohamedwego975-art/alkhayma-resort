from fastapi import APIRouter
from typing import Dict, List, Any

router = APIRouter(prefix="/content", tags=["content"])

# Dynamic page content
PAGE_CONTENT = {
    "home": {
        "hero": {
            "title": "الخيمة Beach Resort",
            "subtitle": "Experience luxury, comfort, and unforgettable moments on the Red Sea",
            "cta_primary": "Book Your Stay",
            "cta_secondary": "Explore Beach"
        },
        "services": [
            {"name": "Rooms", "icon": "🏨", "description": "Luxury rooms with stunning sea views", "link": "/rooms"},
            {"name": "Beach", "icon": "🏖️", "description": "Private beach with VIP cabanas", "link": "/beach"},
            {"name": "Restaurant", "icon": "🍽️", "description": "Fine dining with local cuisine", "link": "/restaurant"},
            {"name": "Cafe", "icon": "☕", "description": "Relax with premium coffee & tea", "link": "/cafe"},
            {"name": "Activities", "icon": "🎯", "description": "Water sports and entertainment", "link": "/activities"},
            {"name": "Events", "icon": "🎉", "description": "Weddings, parties & corporate events", "link": "/events"}
        ],
        "featured_packages": [
            {
                "id": 1,
                "name": "Romantic Getaway",
                "description": "Perfect for couples seeking a romantic escape",
                "price": 299,
                "savings": 20,
                "icon": "💑",
                "features": ["2 Nights Stay", "Beach Dinner", "Couple Spa", "Breakfast"]
            },
            {
                "id": 2,
                "name": "Family Fun Pack",
                "description": "Activities and amenities for the whole family",
                "price": 450,
                "savings": 15,
                "icon": "👨‍👩‍👧‍👦",
                "features": ["3 Nights Stay", "Kids Activities", "All Meals", "Water Sports"]
            },
            {
                "id": 3,
                "name": "Ultimate Luxury",
                "description": "The complete luxury experience",
                "price": 599,
                "savings": 25,
                "icon": "👑",
                "features": ["VIP Beach", "Private Cabana", "All-Inclusive", "Airport Transfer"]
            }
        ],
        "testimonials": [
            {
                "rating": 5,
                "quote": "An absolutely magical experience. The staff went above and beyond to make our anniversary special.",
                "name": "Sarah Johnson",
                "country": "United Kingdom",
                "flag": "🇬🇧"
            },
            {
                "rating": 5,
                "quote": "Best vacation spot on the Red Sea! The VIP beach experience was worth every penny.",
                "name": "Ahmed Hassan",
                "country": "Egypt",
                "flag": "🇪🇬"
            },
            {
                "rating": 5,
                "quote": "From booking to checkout, everything was perfect. The breakfast buffet is amazing!",
                "name": "Marie Dupont",
                "country": "France",
                "flag": "🇫🇷"
            }
        ],
        "stats": {
            "nationalities": "50+",
            "guests_per_year": "25,000+",
            "rooms": "120",
            "rating": "4.9"
        }
    },
    "about": {
        "story": {
            "title": "A Vision of Paradise",
            "content": "Founded in 2015, الخيمة Beach Resort began with a simple dream: to create a sanctuary where the natural beauty of the Red Sea meets world-class hospitality.",
            "years": "8+",
            "founding_year": "2015"
        },
        "values": [
            {
                "icon": "🌊",
                "title": "Excellence",
                "description": "We strive for excellence in every detail, from pristine beaches to personalized service."
            },
            {
                "icon": "🤝",
                "title": "Authenticity",
                "description": "We celebrate Egyptian hospitality and culture, sharing authentic experiences with our guests."
            },
            {
                "icon": "🌱",
                "title": "Sustainability",
                "description": "We're committed to protecting the Red Sea's marine ecosystem for future generations."
            }
        ],
        "facilities": [
            {"icon": "🏨", "title": "Luxury Accommodation", "description": "120 rooms and suites with stunning sea views"},
            {"icon": "🏖️", "title": "Private Beach", "description": "500m of pristine Red Sea coastline"},
            {"icon": "🍽️", "title": "Fine Dining", "description": "3 restaurants serving international cuisine"},
            {"icon": "☕", "title": "Beachfront Cafe", "description": "Premium coffee and light bites"},
            {"icon": "🏊", "title": "Swimming Pools", "description": "4 pools including infinity pool"},
            {"icon": "💆", "title": "Spa & Wellness", "description": "Full-service spa and fitness center"}
        ]
    },
    "restaurant": {
        "name": "Al-Bahr Restaurant",
        "description": "Experience culinary excellence at Al-Bahr (The Sea), our signature restaurant offering panoramic views of the Red Sea.",
        "hours": {
            "breakfast": "7:00 AM - 10:30 AM",
            "lunch": "12:30 PM - 3:00 PM",
            "dinner": "7:00 PM - 11:00 PM"
        },
        "menu_categories": [
            {
                "name": "Breakfast",
                "icon": "🌅",
                "items": [
                    {"name": "Egyptian Breakfast", "price": 12, "description": "Ful medames, falafel, eggs, pita bread, tahini"},
                    {"name": "Continental", "price": 15, "description": "Pastries, cold cuts, cheese, fresh fruit, coffee"},
                    {"name": "Sea View Pancakes", "price": 14, "description": "Fluffy pancakes with maple syrup and fresh berries"}
                ]
            },
            {
                "name": "Main Courses",
                "icon": "🍖",
                "items": [
                    {"name": "Grilled Sea Bass", "price": 28, "description": "Fresh catch with lemon butter sauce, grilled vegetables", "badge": "Chef's Choice"},
                    {"name": "Lamb Tagine", "price": 32, "description": "Tender lamb with apricots, almonds, and Moroccan spices"},
                    {"name": "Ribeye Steak", "price": 45, "description": "Premium cut with truffle mashed potatoes", "badge": "Premium"}
                ]
            }
        ],
        "special_experiences": [
            {
                "icon": "🌅",
                "title": "Sunset Dinner",
                "description": "Romantic beachfront dining as the sun sets over the Red Sea.",
                "price": "$150 per couple"
            },
            {
                "icon": "🎣",
                "title": "Catch of the Day",
                "description": "Choose your fresh fish from our display and have it prepared to your liking.",
                "price": "Market price"
            },
            {
                "icon": "🍷",
                "title": "Wine Pairing",
                "description": "5-course tasting menu with carefully selected wine pairings.",
                "price": "$120 per person"
            }
        ]
    },
    "activities": {
        "water_sports": [
            {
                "icon": "🏄",
                "name": "Surfing & Windsurfing",
                "description": "Ride the Red Sea waves with professional instructors.",
                "price": 45,
                "unit": "hour"
            },
            {
                "icon": "🤿",
                "name": "Scuba Diving",
                "description": "Explore vibrant coral reefs and marine life.",
                "price": 85,
                "unit": "dive"
            },
            {
                "icon": "🐠",
                "name": "Snorkeling",
                "description": "Discover underwater wonders near the shore.",
                "price": 25,
                "unit": "session"
            }
        ],
        "desert_activities": [
            {
                "icon": "🏜️",
                "name": "Desert Safari",
                "description": "4x4 adventure into the Sinai desert",
                "price": 75
            },
            {
                "icon": "🐪",
                "name": "Camel Riding",
                "description": "Traditional Bedouin experience",
                "price": 40
            },
            {
                "icon": "🏎️",
                "name": "ATV Quad Biking",
                "description": "Thrilling desert ride",
                "price": 55
            }
        ],
        "kids_club": {
            "hours": "9:00 AM - 6:00 PM",
            "ages": "4-12",
            "price": "Free for guests",
            "activities": [
                "Beach games and sandcastle building",
                "Arts and crafts workshops",
                "Swimming lessons",
                "Movie nights"
            ]
        }
    },
    "faq": [
        {
            "question": "What are the check-in and check-out times?",
            "answer": "Check-in is from 3:00 PM and check-out is until 12:00 PM. Early check-in and late check-out are available upon request."
        },
        {
            "question": "Is airport transfer available?",
            "answer": "Yes, we offer complimentary airport transfers from Sharm El Sheikh Airport. Please provide your flight details when booking."
        },
        {
            "question": "Do you have WiFi?",
            "answer": "Yes, complimentary high-speed WiFi is available throughout the resort."
        },
        {
            "question": "Are pets allowed?",
            "answer": "We regret that pets are not allowed at the resort, with the exception of service animals."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards, Paymob, Stripe, and cash payments in USD and EGP."
        }
    ]
}

@router.get("/page/{page_name}")
async def get_page_content(page_name: str) -> Dict[str, Any]:
    """Get dynamic content for a specific page"""
    if page_name not in PAGE_CONTENT:
        return {"error": "Page not found", "available_pages": list(PAGE_CONTENT.keys())}
    return {"page": page_name, "content": PAGE_CONTENT[page_name]}

@router.get("/pages")
async def get_all_pages() -> List[str]:
    """Get list of all available pages"""
    return list(PAGE_CONTENT.keys())

@router.get("/home")
async def get_home_content() -> Dict[str, Any]:
    """Get home page content"""
    return PAGE_CONTENT["home"]

@router.get("/about")
async def get_about_content() -> Dict[str, Any]:
    """Get about page content"""
    return PAGE_CONTENT["about"]

@router.get("/restaurant")
async def get_restaurant_content() -> Dict[str, Any]:
    """Get restaurant page content"""
    return PAGE_CONTENT["restaurant"]

@router.get("/activities")
async def get_activities_content() -> Dict[str, Any]:
    """Get activities page content"""
    return PAGE_CONTENT["activities"]

@router.get("/faq")
async def get_faq_content() -> List[Dict[str, str]]:
    """Get FAQ content"""
    return PAGE_CONTENT["faq"]
@router.get("/blog")
async def get_blog_posts() -> List[Dict[str, Any]]:
    """Get blog posts content"""
    blog_posts = [
        {
            "id": 1,
            "title": "Top 5 Beach Activities in Red Sea",
            "slug": "top-5-beach-activities",
            "excerpt": "Discover the most exciting water sports and beach activities available at our resort.",
            "content": "The Red Sea offers some of the world's best beach experiences...",
            "author": "Resort Blog",
            "published_at": "2026-02-15",
            "featured_image": "https://via.placeholder.com/800x400",
            "category": "Activities",
            "read_time": "5 min"
        },
        {
            "id": 2,
            "title": "Planning the Perfect Beach Wedding",
            "slug": "perfect-beach-wedding",
            "excerpt": "A complete guide to planning your dream wedding on the beach.",
            "content": "Getting married on the beach is a magical experience...",
            "author": "Events Team",
            "published_at": "2026-02-10",
            "featured_image": "https://via.placeholder.com/800x400",
            "category": "Events",
            "read_time": "7 min"
        },
        {
            "id": 3,
            "title": "Luxury Dining Experience at Our Restaurant",
            "slug": "luxury-dining-experience",
            "excerpt": "Explore our world-class cuisine and dining facilities.",
            "content": "Our restaurant offers authentic Egyptian and international cuisine...",
            "author": "Chef Ali",
            "published_at": "2026-02-05",
            "featured_image": "https://via.placeholder.com/800x400",
            "category": "Dining",
            "read_time": "4 min"
        }
    ]
    return blog_posts