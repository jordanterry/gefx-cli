---
sidebar_position: 4
title: GEXF Format
---

# Understanding the GEXF Format

GEXF (Graph Exchange XML Format) is an XML-based file format for representing graph structures. It was created for the [Gephi](https://gephi.org/) graph visualization platform but is now widely used across many graph tools.

## Basic Structure

A GEXF file has this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <meta lastmodifieddate="2024-01-15">
        <creator>Your Tool Name</creator>
        <description>Description of the graph</description>
    </meta>
    <graph mode="static" defaultedgetype="directed">
        <attributes class="node">
            <!-- Node attribute definitions -->
        </attributes>
        <attributes class="edge">
            <!-- Edge attribute definitions -->
        </attributes>
        <nodes>
            <!-- Node elements -->
        </nodes>
        <edges>
            <!-- Edge elements -->
        </edges>
    </graph>
</gexf>
```

## Elements

### The `<gexf>` Root Element

The root element declares the namespace and version:

```xml
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
```

Supported versions:
- `1.1` - Older format
- `1.2` - Most common, widely supported
- `1.3` - Latest version

### The `<meta>` Element

Optional metadata about the file:

```xml
<meta lastmodifieddate="2024-01-15">
    <creator>Gephi 0.10.1</creator>
    <description>Social network analysis</description>
</meta>
```

| Element | Description |
|---------|-------------|
| `lastmodifieddate` | Date in YYYY-MM-DD format |
| `creator` | Tool or person who created the file |
| `description` | Human-readable description |

### The `<graph>` Element

Defines the graph structure:

```xml
<graph mode="static" defaultedgetype="directed">
```

| Attribute | Values | Description |
|-----------|--------|-------------|
| `mode` | `static`, `dynamic` | Whether the graph changes over time |
| `defaultedgetype` | `directed`, `undirected`, `mutual` | Default edge direction |

### Attribute Definitions

Before using attributes on nodes or edges, you must declare them:

```xml
<attributes class="node">
    <attribute id="0" title="type" type="string"/>
    <attribute id="1" title="weight" type="float"/>
    <attribute id="2" title="active" type="boolean">
        <default>true</default>
    </attribute>
</attributes>
```

Supported types:
- `string` - Text values
- `integer` - Whole numbers
- `float` / `double` - Decimal numbers
- `boolean` - true/false
- `date` - Date values

### Node Elements

```xml
<nodes>
    <node id="n1" label="Web Server">
        <attvalues>
            <attvalue for="0" value="server"/>
            <attvalue for="1" value="1.5"/>
        </attvalues>
    </node>
</nodes>
```

| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Unique identifier |
| `label` | No | Human-readable name |

### Edge Elements

```xml
<edges>
    <edge id="e1" source="n1" target="n2" weight="1.0">
        <attvalues>
            <attvalue for="0" value="connects"/>
        </attvalues>
    </edge>
</edges>
```

| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | No | Unique identifier |
| `source` | Yes | ID of source node |
| `target` | Yes | ID of target node |
| `weight` | No | Edge weight (numeric) |
| `type` | No | Override default edge type |

## Complete Example

Here's a complete, valid GEXF file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <meta lastmodifieddate="2024-01-15">
        <creator>grph CLI Documentation</creator>
        <description>A simple infrastructure network</description>
    </meta>
    <graph mode="static" defaultedgetype="directed">
        <attributes class="node">
            <attribute id="0" title="type" type="string"/>
            <attribute id="1" title="weight" type="float"/>
        </attributes>
        <attributes class="edge">
            <attribute id="0" title="relationship" type="string"/>
        </attributes>
        <nodes>
            <node id="lb1" label="Load Balancer">
                <attvalues>
                    <attvalue for="0" value="loadbalancer"/>
                    <attvalue for="1" value="0.5"/>
                </attvalues>
            </node>
            <node id="server1" label="Web Server 1">
                <attvalues>
                    <attvalue for="0" value="server"/>
                    <attvalue for="1" value="1.5"/>
                </attvalues>
            </node>
            <node id="db1" label="Database">
                <attvalues>
                    <attvalue for="0" value="database"/>
                    <attvalue for="1" value="3.0"/>
                </attvalues>
            </node>
        </nodes>
        <edges>
            <edge id="e0" source="lb1" target="server1" weight="1.0">
                <attvalues>
                    <attvalue for="0" value="routes"/>
                </attvalues>
            </edge>
            <edge id="e1" source="server1" target="db1" weight="2.0">
                <attvalues>
                    <attvalue for="0" value="queries"/>
                </attvalues>
            </edge>
        </edges>
    </graph>
</gexf>
```

## Common Issues

### Namespace Mismatch

grph CLI (via NetworkX) expects specific namespace URLs:

| Version | Expected Namespace |
|---------|-------------------|
| 1.1 | `http://www.gexf.net/1.1draft` |
| 1.2 | `http://www.gexf.net/1.2draft` |
| 1.3 | `http://gexf.net/1.3` |

If your file uses a different namespace URL, you may get a "No `<graph>` element" error.

### Missing Attribute Definitions

If you use attributes on nodes/edges, you must define them first:

```xml
<!-- Define attributes BEFORE using them -->
<attributes class="node">
    <attribute id="0" title="type" type="string"/>
</attributes>
<nodes>
    <node id="n1">
        <attvalues>
            <attvalue for="0" value="server"/>  <!-- References id="0" above -->
        </attvalues>
    </node>
</nodes>
```

## Resources

- [Official GEXF Specification](https://gexf.net/)
- [GEXF Schema](https://gexf.net/schema.html)
- [Gephi Documentation](https://gephi.org/users/)
- [NetworkX GEXF Support](https://networkx.org/documentation/stable/reference/readwrite/gexf.html)
