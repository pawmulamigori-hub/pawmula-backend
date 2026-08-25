from rest_framework.permissions import BasePermission

# Mirrors src/context/AuthContext.jsx SECTION_ACCESS on the frontend.
# THIS is the version that's actually enforced.
SECTION_ACCESS = {
    "bookings": ["SUPER_ADMIN", "ADMIN", "BOOKING_MANAGER"],
    "events": ["SUPER_ADMIN", "ADMIN", "EVENT_MANAGER"],
    "content": ["SUPER_ADMIN", "ADMIN", "CONTENT_MANAGER", "EDITOR"],
    "website": ["SUPER_ADMIN", "ADMIN", "CONTENT_MANAGER"],
    "users": ["SUPER_ADMIN"],
    "settings": ["SUPER_ADMIN", "ADMIN"],
    "mining": ["SUPER_ADMIN", "ADMIN", "CONTENT_MANAGER", "EDITOR"],
    "stories": ["SUPER_ADMIN", "ADMIN", "EVENT_MANAGER", "CONTENT_MANAGER"],
    "testimonials": ["SUPER_ADMIN", "ADMIN", "CONTENT_MANAGER", "EDITOR"],
    "faqs": ["SUPER_ADMIN", "ADMIN", "CONTENT_MANAGER", "EDITOR"],
}


def make_section_permission(section):
    class _SectionPermission(BasePermission):
        message = f"Your role doesn't have access to {section}."

        def has_permission(self, request, view):
            user = request.user
            if not user or not user.is_authenticated:
                return False
            return user.role in SECTION_ACCESS.get(section, [])

    return _SectionPermission


IsBookingManager = make_section_permission("bookings")
IsEventManager = make_section_permission("events")
IsContentManager = make_section_permission("content")
IsSuperAdmin = make_section_permission("users")
IsMiningManager = make_section_permission("mining")
IsStoryManager = make_section_permission("stories")
IsTestimonialManager = make_section_permission("testimonials")
IsFAQManager = make_section_permission("faqs")
