"""Output formatters for table and JSON display."""

import json
from typing import Any, Iterable

from rich.console import Console
from rich.table import Table

from .models import Edge, GraphMetadata, Node


def format_json(data: Any) -> str:
    """Format data as JSON string.

    Args:
        data: Data to serialize. Can be a dict, list, or model object.

    Returns:
        Pretty-printed JSON string.
    """
    if hasattr(data, "to_dict"):
        data = data.to_dict()
    elif isinstance(data, list):
        data = [item.to_dict() if hasattr(item, "to_dict") else item for item in data]

    return json.dumps(data, indent=2, default=str)


def print_json(data: Any, console: Console | None = None) -> None:
    """Print data as JSON to console.

    Args:
        data: Data to serialize and print.
        console: Rich console to use. Creates a new one if not provided.
    """
    console = console or Console()
    console.print(format_json(data))


def print_metadata_table(metadata: GraphMetadata, console: Console | None = None) -> None:
    """Print metadata as a formatted table.

    Args:
        metadata: Graph metadata to display.
        console: Rich console to use.
    """
    console = console or Console()

    table = Table(title="Graph Metadata", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Version", metadata.version or "N/A")
    table.add_row("Creator", metadata.creator or "N/A")
    table.add_row("Description", metadata.description or "N/A")
    table.add_row("Last Modified", metadata.last_modified or "N/A")
    table.add_row("Mode", metadata.mode)
    table.add_row("Default Edge Type", metadata.default_edge_type)
    table.add_row("Node Count", str(metadata.node_count))
    table.add_row("Edge Count", str(metadata.edge_count))

    console.print(table)


def print_nodes_table(
    nodes: Iterable[Node],
    show_attributes: bool = True,
    console: Console | None = None,
) -> None:
    """Print nodes as a formatted table.

    Args:
        nodes: Iterable of nodes to display.
        show_attributes: Whether to show the attributes column.
        console: Rich console to use.
    """
    console = console or Console()
    nodes_list = list(nodes)

    if not nodes_list:
        console.print("[yellow]No nodes found matching the filters.[/yellow]")
        return

    table = Table(title=f"Nodes ({len(nodes_list)})", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Label")
    if show_attributes:
        table.add_column("Attributes")

    for node in nodes_list:
        attrs_str = ""
        if show_attributes and node.attributes:
            attrs_str = ", ".join(f"{k}={v}" for k, v in node.attributes.items())

        table.add_row(
            node.id,
            node.label or "",
            attrs_str if show_attributes else None,
        )

    console.print(table)


def print_edges_table(
    edges: Iterable[Edge],
    show_attributes: bool = True,
    console: Console | None = None,
) -> None:
    """Print edges as a formatted table.

    Args:
        edges: Iterable of edges to display.
        show_attributes: Whether to show the attributes column.
        console: Rich console to use.
    """
    console = console or Console()
    edges_list = list(edges)

    if not edges_list:
        console.print("[yellow]No edges found matching the filters.[/yellow]")
        return

    table = Table(title=f"Edges ({len(edges_list)})", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Source")
    table.add_column("Target")
    table.add_column("Weight")
    table.add_column("Type")
    if show_attributes:
        table.add_column("Attributes")

    for edge in edges_list:
        attrs_str = ""
        if show_attributes and edge.attributes:
            attrs_str = ", ".join(f"{k}={v}" for k, v in edge.attributes.items())

        table.add_row(
            edge.id or "",
            edge.source,
            edge.target,
            str(edge.weight) if edge.weight is not None else "",
            edge.edge_type or "",
            attrs_str if show_attributes else None,
        )

    console.print(table)


def print_info_table(info: dict[str, Any], console: Console | None = None) -> None:
    """Print graph info summary as a formatted table.

    Args:
        info: Graph info dictionary.
        console: Rich console to use.
    """
    console = console or Console()

    # Main info table
    table = Table(title="Graph Summary", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("File", info.get("file", "N/A"))
    table.add_row("Version", info.get("version") or "N/A")
    table.add_row("Mode", info.get("mode", "N/A"))
    table.add_row("Default Edge Type", info.get("default_edge_type", "N/A"))
    table.add_row("Node Count", str(info.get("node_count", 0)))
    table.add_row("Edge Count", str(info.get("edge_count", 0)))

    console.print(table)
    console.print()

    # Node attributes
    node_attrs = info.get("node_attributes", [])
    if node_attrs:
        console.print("[bold]Node Attributes:[/bold]", ", ".join(node_attrs))
    else:
        console.print("[bold]Node Attributes:[/bold] [dim]None[/dim]")

    # Edge attributes
    edge_attrs = info.get("edge_attributes", [])
    if edge_attrs:
        console.print("[bold]Edge Attributes:[/bold]", ", ".join(edge_attrs))
    else:
        console.print("[bold]Edge Attributes:[/bold] [dim]None[/dim]")
