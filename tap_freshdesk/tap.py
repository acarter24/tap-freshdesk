"""freshdesk tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_freshdesk import streams


from pathlib import Path
config = Path(__file__).parent.parent / '.secrets' / 'config.json'

_ticket_ids = set()


class Tapfreshdesk(Tap):
    """freshdesk tap class."""

    name = "tap-freshdesk"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
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
        ## these two below to enable stream mapping
        th.Property(
            "stream_maps",
            th.ObjectType(),
        ),
        th.Property(
            "stream_map_config",
            th.ObjectType(),
        ),
    ).to_dict()

    

    def discover_streams(self) -> list[streams.FreshdeskStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.AgentsStream(self),
            streams.CompaniesStream(self),
            streams.TicketFieldsStream(self),
            streams.GroupsStream(self),
            streams.ContactsStream(self),
            streams.TicketsAbridgedStream(tap=self, ticket_ids=_ticket_ids),
            streams.TicketsDetailStream(tap=self, ticket_ids=_ticket_ids),
            streams.ConversationsStream(self),
        ]




if __name__ == "__main__":
    Tapfreshdesk(config=config).cli()
