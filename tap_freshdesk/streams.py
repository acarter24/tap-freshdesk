"""Stream type classes for tap-freshdesk."""

from __future__ import annotations

from pathlib import Path
import copy

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk import Tap, metrics

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


class TicketsSummaryStream(PagedFreshdeskStream):
    name = "tickets_summary"
    replication_key = 'updated_at'

    def __init__(self, *args, **kwargs):
        self.ticket_ids: set = kwargs.pop('ticket_ids')
        super().__init__(*args, **kwargs)
    
    @property
    def path(self) -> str:
        return '/tickets'
    
    @property
    def schema_filepath(self) -> Path | None:
        return SCHEMAS_DIR / 'tickets.json'
    
    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        context = context or {}
        records = self.request_records(context=context)
        for rec in records:
            self.post_process(rec)
            yield rec

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        self.ticket_ids.add(row['id'])

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "ticket_id": record["id"],
        }

class TicketsDetailStream(FreshdeskStream):
    name = 'zzzz_tickets_detail'   # needs the z's to run AFTER ticket_summary

    def __init__(self, *args, **kwargs):
        self.ticket_ids: set = kwargs.pop('ticket_ids')
        super().__init__(*args, **kwargs)

    @property
    def path(self) -> str:
        return '/tickets'
    
    @property
    def schema_filepath(self) -> Path | None:
        return SCHEMAS_DIR / 'tickets.json'

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

    def request_records(self, context: dict | None) -> Iterable[dict]:
        """Request records from REST endpoint(s), returning response records.

        If pagination is detected, pages will be recursed automatically.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            An item for every record in the response.
        """
        paginator = self.get_new_paginator()
        decorated_request = self.request_decorator(self._request)
        context = context or {}
        
        for ticket_id in self.ticket_ids:
            context['ticket_id'] = ticket_id

            with metrics.http_request_counter(self.name, self.path) as request_counter:
                request_counter.context = context

                while not paginator.finished:
                    prepared_request = self.prepare_request(
                        context,
                        next_page_token=paginator.current_value,
                    )
                    resp = decorated_request(prepared_request, context)
                    request_counter.increment()
                    self.update_sync_costs(prepared_request, resp, context)
                    yield from self.parse_response(resp)

                    paginator.advance(resp)

class ConversationsStream(FreshdeskStream):

    name = "conversations"

    # EpicIssues streams should be invoked once per parent epic:
    parent_stream_type = TicketsDetailStream
    ignore_parent_replication_keys = True

    # Path is auto-populated using parent context keys:
    path = "/tickets/{ticket_id}/conversations"

    state_partitioning_keys = []