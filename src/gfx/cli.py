"""CLI entry point for the gfx tool."""

import sys
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .formatters import (
    print_edges_table,
    print_info_table,
    print_json,
    print_metadata_table,
    print_nodes_table,
)
from .parser import GEXFGraph, GEXFParseError


console = Console()


def parse_attr_filter(
    ctx: click.Context, param: click.Parameter, value: tuple[str, ...]
) -> list[tuple[str, str]]:
    """Parse attribute filters in key=value format.

    Args:
        ctx: Click context.
        param: Click parameter.
        value: Tuple of key=value strings.

    Returns:
        List of (key, value) tuples.
    """
    filters = []
    for item in value:
        if "=" not in item:
            raise click.BadParameter(
                f"Invalid format '{item}'. Expected key=value format."
            )
        key, val = item.split("=", 1)
        filters.append((key.strip(), val.strip()))
    return filters


def load_graph(file_path: str) -> GEXFGraph:
    """Load a GEXF graph, handling errors gracefully.

    Args:
        file_path: Path to the GEXF file.

    Returns:
        Parsed GEXFGraph object.

    Raises:
        SystemExit: If the file cannot be parsed.
    """
    try:
        return GEXFGraph(file_path)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@click.group()
@click.version_option(version=__version__, prog_name="gfx")
def main() -> None:
    """GFX - A CLI tool for interrogating and browsing GEXF graph files.

    GEXF (Graph Exchange XML Format) is a standard format for representing
    graph data, commonly used with tools like Gephi.

    Examples:

        gfx info graph.gexf

        gfx nodes graph.gexf --attr type=server

        gfx edges graph.gexf --source node1 --json
    """
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def meta(file: str, as_json: bool) -> None:
    """Display metadata from a GEXF file.

    Shows information like creator, description, last modified date,
    graph mode, and default edge type.
    """
    graph = load_graph(file)

    if as_json:
        print_json(graph.metadata, console)
    else:
        print_metadata_table(graph.metadata, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def info(file: str, as_json: bool) -> None:
    """Display a summary of the graph.

    Shows node/edge counts and available attributes.
    """
    graph = load_graph(file)
    info_data = graph.get_info()

    if as_json:
        print_json(info_data, console)
    else:
        print_info_table(info_data, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--attr",
    "attr_filters",
    multiple=True,
    callback=parse_attr_filter,
    help="Filter by attribute (key=value). Can be specified multiple times.",
)
@click.option(
    "--label",
    "label_pattern",
    help="Filter by label pattern (supports * and ? wildcards).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option(
    "--no-attrs",
    is_flag=True,
    help="Hide the attributes column in table output.",
)
def nodes(
    file: str,
    attr_filters: list[tuple[str, str]],
    label_pattern: str | None,
    as_json: bool,
    no_attrs: bool,
) -> None:
    """List and filter nodes in the graph.

    Examples:

        gfx nodes graph.gexf

        gfx nodes graph.gexf --attr type=server

        gfx nodes graph.gexf --label "Server*" --json
    """
    graph = load_graph(file)
    matching_nodes = list(graph.nodes(attr_filters=attr_filters, label_pattern=label_pattern))

    if as_json:
        print_json(matching_nodes, console)
    else:
        print_nodes_table(matching_nodes, show_attributes=not no_attrs, console=console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--attr",
    "attr_filters",
    multiple=True,
    callback=parse_attr_filter,
    help="Filter by attribute (key=value). Can be specified multiple times.",
)
@click.option("--source", "source_filter", help="Filter by source node ID.")
@click.option("--target", "target_filter", help="Filter by target node ID.")
@click.option(
    "--type",
    "type_filter",
    help="Filter by edge type (e.g., directed, undirected).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option(
    "--no-attrs",
    is_flag=True,
    help="Hide the attributes column in table output.",
)
def edges(
    file: str,
    attr_filters: list[tuple[str, str]],
    source_filter: str | None,
    target_filter: str | None,
    type_filter: str | None,
    as_json: bool,
    no_attrs: bool,
) -> None:
    """List and filter edges in the graph.

    Examples:

        gfx edges graph.gexf

        gfx edges graph.gexf --source node1

        gfx edges graph.gexf --attr weight=1.0 --json
    """
    graph = load_graph(file)
    matching_edges = list(
        graph.edges(
            attr_filters=attr_filters,
            source_filter=source_filter,
            target_filter=target_filter,
            type_filter=type_filter,
        )
    )

    if as_json:
        print_json(matching_edges, console)
    else:
        print_edges_table(matching_edges, show_attributes=not no_attrs, console=console)


if __name__ == "__main__":
    main()
