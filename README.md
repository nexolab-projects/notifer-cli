# Notifer CLI

Command-line interface for [Notifer](https://notifer.io) - simple HTTP-based pub-sub notification service.

## Installation

```bash
pip install notifer-cli
```

Or install from source:

```bash
git clone https://github.com/nexolab-projects/notifer-cli.git
cd notifer-cli
pip install -e .
```

## Quick Start

### 1. Set your API key

Get your API key at [app.notifer.io](https://app.notifer.io) and configure the CLI:

```bash
notifer config set api-key noti_your_key_here
```

### 2. Create a topic (required before publishing)

Topics must exist before publishing. Create one first:

```bash
notifer topics create my-topic --description "My first topic"
```

### 3. Publish a message

```bash
# Simple message
notifer publish my-topic "Hello World!"

# With title and priority
notifer publish alerts "Server is down!" \
  --title "Alert" \
  --priority 5 \
  --tags urgent,server

# With markdown
notifer publish deployments "# Deploy Success\n\n**Status**: ✅" \
  --priority 4
```

### 4. Subscribe to messages

```bash
# Subscribe and print to console
notifer subscribe my-topic

# Subscribe to multiple topics
notifer subscribe alerts,deployments

# Save to file
notifer subscribe my-topic --output messages.jsonl
```

## Authentication

### API Key (required)

All write operations require an API key. Get one at [app.notifer.io](https://app.notifer.io).

```bash
# Save in config (recommended)
notifer config set api-key noti_abc123...

# Or pass directly per command
notifer publish my-topic "Message" --api-key noti_abc123...
```

### Topic Access Token (for private topics)

Private topics require a topic access token (`tk_...`) for read/write access:

```bash
# Publish to a private topic
notifer publish private-topic "Secret message" --topic-token tk_abc123...

# Subscribe to a private topic
notifer subscribe private-topic --topic-token tk_abc123...
```

Topic access tokens are created by the topic owner via the web app or API.

## Commands

### Publishing

```bash
notifer publish <topic> <message> [OPTIONS]

Options:
  -t, --title TEXT        Message title
  -p, --priority INTEGER  Priority (1-5, default: 3)
  --tags TEXT             Comma-separated tags
  --api-key TEXT          API key for authentication
  --topic-token TEXT      Topic access token for private topics
  --server TEXT           Override server URL
```

### Subscribing

```bash
notifer subscribe <topics> [OPTIONS]

Options:
  -o, --output PATH      Save messages to file (JSONL format)
  --since TEXT            Only show messages since timestamp
  --api-key TEXT          API key for authentication
  --topic-token TEXT      Topic access token for private topics
  --server TEXT           Override server URL
  --json                 Output raw JSON (no formatting)
```

### API Keys Management

```bash
# List API keys
notifer keys list

# Create new key
notifer keys create <name> [OPTIONS]

Options:
  -s, --scopes TEXT       Comma-separated scopes (default: *)
  -d, --description TEXT  Key description
  --expires TEXT          Expiration date (ISO format)

# Revoke key
notifer keys revoke <key-id>

# Delete key
notifer keys delete <key-id>
```

### Topics Management

```bash
# List topics
notifer topics list

# List your topics
notifer topics list --mine

# Create topic
notifer topics create <name> [OPTIONS]

Options:
  -d, --description TEXT  Topic description
  --private               Make topic private
  --no-discover           Hide from discovery

# Get topic info
notifer topics get <name>

# Delete topic
notifer topics delete <topic-id>
```

### Configuration

```bash
# Initialize config file (optional)
notifer config init

# Show current config
notifer config show

# Set API key
notifer config set api-key noti_abc123...

# Get config value
notifer config get api-key
```

## Configuration File

The CLI uses `~/.notifer.yaml` for configuration:

```yaml
api_key: noti_abc123...

defaults:
  priority: 3
  tags: []
```

The default server is `https://app.notifer.io`. Override it only if needed:

```yaml
server: https://custom-server.example.com
api_key: noti_abc123...

defaults:
  priority: 3
  tags: []
```

## Examples

### CI/CD Integration

```bash
#!/bin/bash
# deploy.sh

API_KEY="noti_abc123..."

# Notify on deploy start
notifer publish deployments "Deploy started for v1.2.3" \
  --title "Deploy" \
  --priority 3 \
  --tags deployment,production \
  --api-key "$API_KEY"

# Run deployment
./deploy-script.sh

# Notify on success/failure
if [ $? -eq 0 ]; then
  notifer publish deployments "# Deploy Success\n\nVersion **v1.2.3** deployed!" \
    --priority 4 \
    --tags deployment,success \
    --api-key "$API_KEY"
else
  notifer publish deployments "Deploy failed!" \
    --priority 5 \
    --tags deployment,failure \
    --api-key "$API_KEY"
fi
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh

# Subscribe to alerts and log to file
notifer subscribe alerts,errors \
  --output /var/log/notifer-alerts.jsonl \
  --api-key noti_abc123...
```

### GitHub Actions

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Notifer CLI
        run: pip install notifer-cli

      - name: Notify deploy start
        run: |
          notifer publish deployments "Deploy started: ${{ github.sha }}" \
            --api-key ${{ secrets.NOTIFER_API_KEY }}

      - name: Deploy
        run: ./deploy.sh

      - name: Notify success
        if: success()
        run: |
          notifer publish deployments "Deploy successful!" \
            --priority 4 \
            --api-key ${{ secrets.NOTIFER_API_KEY }}

      - name: Notify failure
        if: failure()
        run: |
          notifer publish deployments "Deploy failed!" \
            --priority 5 \
            --api-key ${{ secrets.NOTIFER_API_KEY }}
```

## License

MIT
