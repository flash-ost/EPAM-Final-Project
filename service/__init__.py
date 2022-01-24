"""
Module contains functions for CRUD operations with database.
"""

from .users_ops import check_credentials, check_username, register_user
from .entries_ops import add_entry, add_movie, check_movie, delete_entry, edit_entry, get_entry, get_list, populate_db