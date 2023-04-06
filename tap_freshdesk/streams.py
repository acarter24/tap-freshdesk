"""Stream type classes for tap-freshdesk."""

from __future__ import annotations

from pathlib import Path
import copy

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk import Tap

from tap_freshdesk.client import FreshdeskStream, PagedFreshdeskStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.
    


class FakeTapfreshdesk(Tap):
    """freshdesk tap class."""

    name = "tap-freshdesk"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="Project IDs to replicate",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "domain",
            th.StringType,
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[FreshdeskStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            TicketsStream(self),
        ]

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

class TicketDetailStream(FreshdeskStream):
    _LOG_REQUEST_METRIC_URLS = True
    name = 'tickets'
    replication_key = 'updated_at'

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "ticket_id": record["id"],
        }

    def get_url(self, context: dict | None) -> str:
        url = "".join([self.url_base, self.path])
        if 'ticket_id' in context:
            ticket_id = context.pop('ticket_id')
            url = url + f'/{ticket_id}'
        vals = copy.copy(dict(self.config))
        vals.update(context or {})
        for k, v in vals.items():
            search_text = "".join(["{", k, "}"])
            if search_text in url:
                url = url.replace(search_text, self._url_encode(v))
        return url

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        context = context or {}
        if 'updated_at' not in context:  #  have to provide manually
            context['updated_at'] = self._config['start_date']
        records = list(FakeTapfreshdesk(config=self._config).streams['tickets'].get_records(context=context))
        ticket_ids = [v['id'] for v in records]
        for ticket_id in ticket_ids:
            context['ticket_id'] = ticket_id
            records = self.request_records(context=context)
            for rec in records:
                yield rec

class ConversationsStream(FreshdeskStream):
    # Note that this class inherits from the GitlabStream base class, and not from
    # the EpicsStream class.

    _LOG_REQUEST_METRIC_URLS = True

    name = "conversations"

    # EpicIssues streams should be invoked once per parent epic:
    parent_stream_type = TicketDetailStream

    # Assume epics don't have `updated_at` incremented when issues are changed:
    ignore_parent_replication_keys = True

    # Path is auto-populated using parent context keys:
    path = "/tickets/{ticket_id}/conversations"

    state_partitioning_keys = []

class FakeTapfreshdesk(Tap):
    """freshdesk tap class."""

    name = "tap-freshdesk"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="Project IDs to replicate",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "domain",
            th.StringType,
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[FreshdeskStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            TicketsStream(self),
        ]