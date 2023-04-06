"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_freshdesk.tap import Tapfreshdesk


SAMPLE_CONFIG = {
    # "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    # TODO: Initialize minimal tap config
    "username": "KSmtJIb2TNLVbVCevGx",
    "password": ".",
    "start_date": "2021-01-01",
    "domain": "hellostudent"
}


# Run standard built-in tap tests from the SDK:
TestTapfreshdesk = get_tap_test_class(
    tap_class=Tapfreshdesk,
    config=SAMPLE_CONFIG
)


print('hi')

# TODO: Create additional tests as appropriate for your tap.
