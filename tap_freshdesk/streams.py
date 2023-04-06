"""Stream type classes for tap-freshdesk."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshdesk.client import FreshdeskStream, PagedFreshdeskStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.
    

class AgentsStream(FreshdeskStream):
    """Define custom stream."""

    name = "agents"
    path = "/agents"
    primary_keys = ["id"]
    

class CompaniesStream(FreshdeskStream):
    """Define custom stream."""

    name = "companies"
    path = "/companies"
    primary_keys = ["id"]


class TicketsStream(PagedFreshdeskStream):
    """Define custom stream."""

    name = "tickets"
    path = "/tickets"
    primary_keys = ["id"]


class TicketFieldsStream(FreshdeskStream):
    """Define custom stream."""

    name = "ticket_fields"
    path = "/ticket_fields"
    primary_keys = ["id"]

class GroupsStream(FreshdeskStream):
    """Define custom stream."""

    name = "groups"
    path = "/groups"
    primary_keys = ["id"]


class ContactsStream(FreshdeskStream):
    """Define custom stream."""

    name = "contacts"
    path = "/contacts"
    primary_keys = ["id"]
