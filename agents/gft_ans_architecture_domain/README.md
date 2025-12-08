# Architecture Domain ANS Agent

## Overview

The Architecture Domain ANS Agent is an intelligent assistant designed to analyze and issue architectural opinions (pareceres). It automates the evaluation of suppliers and services by considering available integrations, historical opinions, technological drivers, and compliance with Banco BV policies.

The agent suggests opinions (Favorable, Favorable with Reservations, or Unfavorable) based on objective criteria and data retrieved from various sources.

## Features

-   **OneTrust Integration**: Retrieves supplier context, contract details, and expiration dates.
-   **CMDB Integration**: Fetches service details, technological drivers, and lifecycle status.
-   **Historical Analysis**: Searches for similar past opinions to ensure consistency.
-   **Policy Compliance**: Checks against internal policies and guidelines.
-   **Opinion Suggestion**: Generates a suggested opinion based on gathered data.

## Prerequisites

-   Python 3.10+
-   Google Cloud SDK (gcloud) installed and authenticated
-   Vertex AI API enabled in your Google Cloud project

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd architecture-domain-ans
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory or set the following environment variables:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
USE_MOCK=true  # Set to 'false' to use real APIs (when implemented)
```

## Usage

### Running the Agent

You can run the example usage script to see the agent in action:

```bash
python example_usage.py
```

### API Mode

To run the agent in API mode (if applicable):

```bash
python example_usage_api_mode.py
```

## Testing

To run the unit tests:

```bash
pytest
```

## Tools

The agent is equipped with the following tools:

-   `integrar_onetrust`: Queries OneTrust for supplier information.
-   `consultar_cmdb`: Queries CMDB for service information.
-   `carregar_insumos`: Loads historical data and inputs.
-   `capturar_vencimento`: Checks for contract expiration.
-   `carregar_ressalvas`: Checks for pending reservations.
-   `sugerir_parecer`: Generates a suggested opinion.
-   `registrar_parecer`: Registers the final opinion (mock implementation).

## Project Structure

-   `architecture_domain_ans/`: Main package source code.
    -   `agent.py`: Agent definition and initialization.
    -   `tools/`: Tool implementations.
    -   `models/`: Data models.
    -   `adapters/`: Data access adapters (Mock/API).
    -   `mock/`: Mock data.
-   `tests/`: Unit tests.
