"""freshdesk tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_freshdesk import streams


class Tapfreshdesk(Tap):
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

    def discover_streams(self) -> list[streams.FreshdeskStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.AgentsStream(self),
            streams.CompaniesStream(self),
            streams.TicketsStream(self),
            streams.TicketFieldsStream(self),
            streams.GroupsStream(self),
            streams.ContactsStream(self),
        ]


if __name__ == "__main__":
    Tapfreshdesk.cli()
