"""Stream type classes for tap-freshdesk."""

from __future__ import annotations

from pathlib import Path
import copy

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk import Tap, metrics

from tap_freshdesk.client import FreshdeskStream, PagedFreshdeskStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AgentsStream(PagedFreshdeskStream):
    name = "agents"
    

class CompaniesStream(PagedFreshdeskStream):
    name = "companies"


class TicketFieldsStream(FreshdeskStream):
    name = "ticket_fields"


class GroupsStream(PagedFreshdeskStream):
    name = "groups"


class ContactsStream(PagedFreshdeskStream):
    name = "contacts"

class EmailConfigsStream(PagedFreshdeskStream):
    name = "email_configs"

class SlaPoliciesStream(PagedFreshdeskStream):
    name = "sla_policies"

class TicketsAbridgedStream(PagedFreshdeskStream):
    name = "tickets_abridged"
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
    
    @property
    def is_sorted(self) -> bool:
        """Expect stream to be sorted.

        When `True`, incremental streams will attempt to resume if unexpectedly
        interrupted.

        Returns:
            `True` if stream is sorted. Defaults to `False`.
        """
        return True
    
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        context = context or {}
        params = super().get_url_params(context, next_page_token)
        params['per_page'] = 100
        # Adding these parameters for sorting
        params['order_type'] = "asc"
        params['order_by'] = "updated_at"
        if next_page_token: 
            params["page"] = next_page_token
        if 'updated_since' not in context:
            params['updated_since'] = self.get_starting_timestamp(context)
        return params
    
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
    name = 'tickets_detail'   # needs the z's to run AFTER ticket_summary

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
        context = context or {}

        for ticket_id in self.ticket_ids:
            context['ticket_id'] = ticket_id

            paginator = self.get_new_paginator()
            decorated_request = self.request_decorator(self._request)

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

class ConversationsStream(PagedFreshdeskStream):

    name = "conversations"

    # EpicIssues streams should be invoked once per parent epic:
    parent_stream_type = TicketsDetailStream
    ignore_parent_replication_keys = True

    # Path is auto-populated using parent context keys:
    path = "/tickets/{ticket_id}/conversations"

    state_partitioning_keys = []