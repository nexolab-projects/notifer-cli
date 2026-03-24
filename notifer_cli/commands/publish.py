"""Publish command."""
import click
from rich.console import Console
from rich.panel import Panel

from ..client import NotiferClient
from ..config import Config

console = Console()


@click.command()
@click.argument("topic")
@click.argument("message")
@click.option("--title", "-t", help="Message title")
@click.option("--priority", "-p", type=int, default=3, help="Priority (1-5, default: 3)")
@click.option("--tags", help="Comma-separated tags")
@click.option("--api-key", help="API key for authentication")
@click.option("--topic-token", help="Topic access token for private topics")
@click.option("--server", help="Override server URL")
def publish(topic, message, title, priority, tags, api_key, topic_token, server):
    """
    Publish a message to a topic.

    Requires authentication via API key (--api-key or config).
    For private topics, use --topic-token with a topic access token.

    \b
    Examples:
      notifer publish my-topic "Hello World!"
      notifer publish alerts "Server down!" --priority 5 --tags urgent,server
      notifer publish deploy "# Success\\n\\n**Deployed** v1.2.3" --title "Deploy"
      notifer publish private-topic "Secret" --topic-token tk_abc123
    """
    try:
        # Load config
        config = Config.load()

        # Override with command options
        if server:
            config.server = server
        if api_key:
            config.api_key = api_key

        # Check authentication
        if not config.api_key and not topic_token:
            console.print(
                "[red]✗ Authentication required to publish messages.[/red]\n\n"
                "Set your API key:\n"
                "  [cyan]notifer config set api-key YOUR_API_KEY[/cyan]\n\n"
                "Or pass it directly:\n"
                "  [cyan]notifer publish my-topic \"Hello\" --api-key YOUR_API_KEY[/cyan]\n\n"
                "For private topics, use a topic access token:\n"
                "  [cyan]notifer publish my-topic \"Hello\" --topic-token tk_...[/cyan]\n\n"
                "Get your API key at [cyan]https://app.notifer.io[/cyan]"
            )
            raise click.Abort()

        # Parse tags
        tag_list = tags.split(",") if tags else []

        # Create client and publish
        client = NotiferClient(config)
        result = client.publish(
            topic=topic,
            message=message,
            title=title,
            priority=priority,
            tags=tag_list,
            topic_token=topic_token,
        )

        # Success message
        console.print(
            Panel(
                f"[green]✓[/green] Message published to [cyan]{topic}[/cyan]\n\n"
                f"ID: {result['id']}\n"
                f"Timestamp: {result['timestamp']}\n"
                f"Priority: {result['priority']}",
                title="Published",
                border_style="green",
            )
        )

    except click.Abort:
        raise
    except Exception as e:
        # Try to get detailed error message from response
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get('detail', error_msg)
                error_msg = detail
            except Exception:
                pass
        console.print(f"[red]✗ Error:[/red] {error_msg}", style="red")
        raise click.Abort()
