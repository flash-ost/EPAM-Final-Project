"""
Module contains unit tests for CRUD functions and REST API.
"""
from .base import BaseTestCase
from .test_users_ops import UserCase
from .test_entries_ops import EntryCase
from .test_api import EntryApiCase, UserApiCase