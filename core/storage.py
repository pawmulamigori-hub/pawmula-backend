"""
Supabase Storage integration — spec section 27's upload pipeline:

    Admin -> React -> Django API -> Supabase Storage -> public URL -> saved on the record

The service-role key never leaves this server (spec's explicit security
requirement: never expose it in React). This talks to Supabase's Storage
REST API directly over HTTPS rather than pulling in the full supabase-py
SDK, since all we need is upload + public URL.

NOTE: this has been written against Supabase's documented Storage REST API
but has NOT been exercised against a live Supabase project in this
environment (no project exists yet, and this sandbox has no network path
to supabase.co). Test it against a real project before relying on it —
unlike everything else in this backend, this one path is unverified.
"""

import mimetypes
import uuid

import requests
from django.conf import settings


class SupabaseStorageError(Exception):
    pass


def _require_config():
    if not (settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY):
        raise SupabaseStorageError(
            "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY are not set. "
            "Add them to .env once the Supabase project exists."
        )


def upload_file(file_obj, category: str = "general") -> dict:
    """
    Uploads a Django UploadedFile to Supabase Storage and returns:
        {"url": "<public url>", "path": "<storage path>"}

    `category` becomes a folder prefix (e.g. "events", "destinations",
    "gallery") so the bucket stays organised the way spec section 15's
    gallery categories expect.
    """
    _require_config()

    ext = ""
    if "." in file_obj.name:
        ext = "." + file_obj.name.rsplit(".", 1)[-1]
    path = f"{category}/{uuid.uuid4().hex}{ext}"

    content_type = file_obj.content_type or mimetypes.guess_type(file_obj.name)[0] or "application/octet-stream"

    upload_url = (
        f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_STORAGE_BUCKET}/{path}"
    )
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": content_type,
        "x-upsert": "false",
    }

    response = requests.post(upload_url, headers=headers, data=file_obj.read(), timeout=30)
    if response.status_code not in (200, 201):
        raise SupabaseStorageError(f"Supabase Storage upload failed ({response.status_code}): {response.text}")

    public_url = (
        f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_STORAGE_BUCKET}/{path}"
    )
    return {"url": public_url, "path": path}


def delete_file(path: str) -> None:
    _require_config()
    delete_url = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_STORAGE_BUCKET}/{path}"
    headers = {"Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}"}
    requests.delete(delete_url, headers=headers, timeout=30)
