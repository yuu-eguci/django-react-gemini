import importlib
import os
from unittest import mock

from django.test import SimpleTestCase


def load_staging_settings(env: dict[str, str]):
    with mock.patch.dict(os.environ, env):
        return importlib.reload(importlib.import_module("config.settings_staging"))


class StagingSettingsTests(SimpleTestCase):
    def test_debug_is_disabled(self):
        self.assertFalse(load_staging_settings({}).DEBUG)

    def test_allowed_hosts_come_from_env(self):
        settings = load_staging_settings({"DJANGO_ALLOWED_HOSTS": "example.com,localhost"})
        self.assertEqual(settings.ALLOWED_HOSTS, ["example.com", "localhost"])

    def test_allowed_hosts_are_empty_without_env(self):
        with mock.patch.dict(os.environ):
            os.environ.pop("DJANGO_ALLOWED_HOSTS", None)
            settings = importlib.reload(importlib.import_module("config.settings_staging"))
        self.assertEqual(settings.ALLOWED_HOSTS, [])
