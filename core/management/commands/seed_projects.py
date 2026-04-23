"""
Load realistic sample projects (covers generated with Pillow).

Usage:
    python manage.py seed_projects
    python manage.py seed_projects --append   # add samples even if projects already exist
"""

from copy import deepcopy
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Project

try:
    from PIL import Image, ImageDraw
except ImportError as e:  # pragma: no cover
    raise SystemExit("Pillow is required for seed_projects. Install with: pip install Pillow") from e


def _cover_image(title: str, accent: tuple) -> ContentFile:
    """Simple 800x450 PNG for project cards."""
    w, h = 800, 450
    base = (min(accent[0] + 40, 255), min(accent[1] + 40, 255), min(accent[2] + 50, 255))
    img = Image.new("RGB", (w, h), base)
    draw = ImageDraw.Draw(img)
    r, g, b = accent
    for x in range(0, w, 6):
        blend = (min(r + x // 8, 255), min(g + x // 12, 255), min(b + x // 10, 255))
        draw.rectangle([x, 0, x + 6, h], fill=blend)
    draw.rounded_rectangle([40, 120, w - 40, h - 80], radius=24, fill=(20, 24, 32))
    draw.rectangle([40, 120, w - 40, 160], fill=accent)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    name = f"{slugify(title)[:60] or 'project'}.png"
    return ContentFile(buf.read(), name=name)


SAMPLE_PROJECTS = [
    {
        "title": "Full-Stack Portfolio & AI Chat",
        "description": (
            "Personal portfolio with Django REST API, React + Vite + Chakra UI, JWT admin flows, "
            "and an AI assistant grounded in live site content (profile, projects, about). "
            "Includes rate limiting, session-backed chat history, and deployment-ready static handling."
        ),
        "live_link": None,
        "github_link": "https://github.com/topics/portfolio",
        "order": 0,
        "is_featured": True,
        "accent": (99, 102, 241),
    },
    {
        "title": "Serverless Contact & Webhook Gateway",
        "description": (
            "AWS SAM template exposing HTTP API → Lambda (Python) for contact form submissions: "
            "validation, structured logging, optional SES or third-party relay, and idempotent handling "
            "for high-traffic landing pages without maintaining a dedicated contact microservice."
        ),
        "live_link": "https://aws.amazon.com/lambda/",
        "github_link": "https://github.com/aws-samples/serverless-patterns",
        "order": 1,
        "is_featured": True,
        "accent": (14, 165, 233),
    },
    {
        "title": "REST Analytics Dashboard",
        "description": (
            "Internal operations dashboard consuming paginated REST endpoints, role-aware UI states, "
            "CSV export, and optimistic updates. Focus on accessible tables, skeleton loading, and "
            "defensive client caching to stay responsive on large datasets."
        ),
        "live_link": None,
        "github_link": "https://github.com/topics/dashboard",
        "order": 2,
        "is_featured": False,
        "accent": (16, 185, 129),
    },
    {
        "title": "CI/CD & Preview Environments",
        "description": (
            "GitHub Actions pipeline running lint, unit tests, and security scans; build artifacts for "
            "container deploys; ephemeral preview apps per pull request with seeded SQLite for QA."
        ),
        "live_link": "https://docs.github.com/en/actions",
        "github_link": "https://github.com/topics/ci-cd",
        "order": 3,
        "is_featured": False,
        "accent": (234, 88, 12),
    },
    {
        "title": "PostgreSQL Schema & Migration Toolkit",
        "description": (
            "Django data migrations for zero-downtime column additions, backfills from legacy JSON, "
            "and indexed full-text search over project descriptions. Includes rollback notes and "
            "staging verification checklist used before production cuts."
        ),
        "live_link": None,
        "github_link": "https://github.com/topics/postgresql",
        "order": 4,
        "is_featured": False,
        "accent": (168, 85, 247),
    },
    {
        "title": "Observability Starter for APIs",
        "description": (
            "Structured JSON logging, request IDs, slow-query logging hooks, and health/readiness "
            "endpoints compatible with container orchestrators. Designed so on-call engineers can "
            "trace a user report from CDN → app → database in minutes."
        ),
        "live_link": None,
        "github_link": "https://github.com/topics/observability",
        "order": 5,
        "is_featured": False,
        "accent": (244, 63, 94),
    },
]


class Command(BaseCommand):
    help = "Create realistic sample projects with generated cover images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--append",
            action="store_true",
            help="Create sample projects even if the database already has projects.",
        )

    def handle(self, *args, **options):
        append = options["append"]
        existing = Project.objects.count()
        if existing > 0 and not append:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipped: {existing} project(s) already exist. "
                    f"Run with --append to add samples anyway, or delete projects first."
                )
            )
            return

        created = 0
        for template in SAMPLE_PROJECTS:
            row = deepcopy(template)
            accent = row.pop("accent")
            title = row["title"]
            img = _cover_image(title, accent)
            Project.objects.create(**row, image=img)
            created += 1
            self.stdout.write(f"  + {title}")

        self.stdout.write(self.style.SUCCESS(f"Created {created} sample project(s)."))
