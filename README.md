# tap-freshdesk

`tap-freshdesk` is a Singer tap for freshdesk.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-freshdesk
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-freshdesk.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-freshdesk --about --format=markdown
```
-->

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-freshdesk --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

#### Embeds
The Freshdesk Tickets API allows for a number of 'embeds' - these are extra fields which can be returned from the API, at the cost of consuming more 'credits'.
Turning on these embeds will return more data, but mean that the 'cooloff' happens sooner, and overall syncs may take longer.

See Freshdesk docs here: https://developers.freshdesk.com/api/#view_a_ticket

The available embeds for tickets are specified under the `embeds -> tickets_detail` config key:
```
config:
  embeds:
    tickets_detail:
      - stats
      - sla_policy
      - company
      - requester
```

These extra values will be returned as json objects rather than unpacked in the main schema.

If you don't need these data items, then just don't include the `embeds` key in `meltano.yml` and only the base ticket fields will be returned.

As Freshdesk enables more embeds, they will be added here.

### Source Authentication and Authorization

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-freshdesk` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-freshdesk --version
tap-freshdesk --help
tap-freshdesk --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_freshdesk/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-freshdesk` CLI interface directly using `poetry run`:

```bash
poetry run tap-freshdesk --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-freshdesk
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-freshdesk --version
# OR run a test `elt` pipeline:
meltano elt tap-freshdesk target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
