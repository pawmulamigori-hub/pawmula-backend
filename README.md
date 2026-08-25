# PAWMULA Backend — Django + DRF API

REST API backing the `pawmula-admin` React app (and eventually the public
`pawmula-frontend` site, per spec section 39's admin -> Django -> Supabase
-> public-site pipeline).

## Verified end-to-end

This isn't a scaffold that's only been eyeballed — it's been run and tested:
migrations apply cleanly, demo data seeds, and every endpoint the React
admin actually calls has been hit with real HTTP requests (login, dashboard
stats, events CRUD + publish + duplicate, bookings + status + notes,
destinations CRUD + publish, experiences CRUD + publish + destination
linking, notifications, audit log, RBAC-enforced 403s, and the public
booking endpoint that triggers a real-time notification). See "Smoke test"
below to reproduce.

## API surface implemented

| Area | Endpoints |
|---|---|
| Auth | `POST /api/auth/login/`, `GET /api/auth/me/`, `POST /api/auth/logout/` |
| Events | full CRUD at `/api/events/`, `+ /set-status/`, `+ /duplicate/` |
| Bookings | `/api/bookings/` (list/retrieve), `+ /set-status/`, `+ /notes/`, plus `POST /api/public/bookings/` (no auth — for the public site) |
| Destinations | full CRUD at `/api/destinations/`, `+ /set-published/`, `+ /reorder/` |
| Experiences | full CRUD at `/api/experiences/`, `+ /set-published/` (FK to Destination) |
| Media | `POST /api/media/upload/` — multipart upload to Supabase Storage, returns public URL |
| Dashboard | `/api/dashboard/stats/`, `/bookings-over-time/`, `/popular-experiences/` (now computed from real Destination/Experience/Booking data) |
| Notifications | `/api/notifications/`, `+ /{id}/read/`, `+ /mark-all-read/` |
| Users | `/api/users/` (list), `+ /invite/` — Super Admin only |
| Audit log | `/api/audit-log/` |
| Messages/Enquiries | `/api/messages/` |

Every mutating admin action writes to `AuditLogEntry` (`core/audit.py`).
RBAC is enforced server-side in `accounts/permissions.py` — the frontend's
sidebar filtering is UX convenience only, this is what actually blocks
requests (verified: an EDITOR gets a real 403 hitting `/api/events/`).

## What's not built yet

Matches the remaining `ModuleStub` pages in the React admin: Mining, Miner
Stories, Gallery, Stories, Testimonials, Website Content, SEO, Settings.
Each needs a model — follow `destinations/` or `events/` as the template
(camelCase serializer aliases, django-filter FilterSet, ViewSet with
`log_action()` calls) — plus a `<name>Api.js` and real page on the
frontend, replacing its `ModuleStub`.

The media upload endpoint (`core/storage.py`, spec section 27) is written
against Supabase's documented Storage REST API but has **not** been
exercised against a live Supabase project — there isn't one yet, and this
sandbox has no network path to supabase.co. Test it for real once
`SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` are set. Everything else in
this README's "verified end-to-end" list has actually been run.

Also not built: WebSocket/SSE upgrade for notifications (polling works and
matches spec section 9's explicit "polling or WebSockets/SSE" allowance),
email delivery for admin invites (creates the user with a random temp
password that isn't emailed anywhere yet — marked TODO in
`accounts/serializers.py`).

## Stack

Django 6.1, Django REST Framework, SimpleJWT, django-cors-headers,
django-filter. Postgres (Supabase) in production via `DATABASE_URL`, SQLite
locally when that's unset — so this runs standalone before a Supabase
project exists.

## Setup

```
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # fill in DATABASE_URL etc. when ready
python manage.py migrate
python manage.py seed_demo_data    # optional — matches the admin's old mock data
python manage.py runserver 0.0.0.0:8000
```

Demo login: `amina@pawmula.ltd` / `pawmula2026`

## Connecting Supabase

1. Create a Supabase project, grab the Postgres connection string from
   Project Settings → Database → Connection string (URI mode)
2. Put it in `.env` as `DATABASE_URL`
3. Put the Storage credentials in `.env` too (`SUPABASE_URL`,
   `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_STORAGE_BUCKET`) — media upload
   wiring is the next piece to build, see "What's not built yet" below
4. `python manage.py migrate` again to create tables in Supabase Postgres
   instead of SQLite

The service-role key stays server-side only, in this backend's `.env` —
never sent to or exposed by the React admin, per the original spec's
security requirement.

## Smoke test

With the server running:

```
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"amina@pawmula.ltd","password":"pawmula2026"}'
```

Copy the `token` from the response and:

```
curl http://localhost:8000/api/events/ -H "Authorization: Bearer <token>"
```
