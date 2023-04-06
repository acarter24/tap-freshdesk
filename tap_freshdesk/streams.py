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
    name = "agents"
    

class CompaniesStream(FreshdeskStream):
    name = "companies"


class TicketFieldsStream(FreshdeskStream):
    name = "ticket_fields"


class GroupsStream(FreshdeskStream):
    name = "groups"


class ContactsStream(FreshdeskStream):
    name = "contacts"


class TicketsStream(PagedFreshdeskStream):
    name = "tickets"