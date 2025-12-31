import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'index',
    'getting-started',
    {
      type: 'category',
      label: 'Tutorials',
      collapsed: false,
      items: [
        'tutorials/index',
        'tutorials/london-underground',
        'tutorials/easyjet-routing',
        'tutorials/npm-dependencies',
        'tutorials/social-network',
      ],
    },
    {
      type: 'category',
      label: 'How-to Guides',
      collapsed: true,
      items: [
        'how-to/index',
        'how-to/find-shortest-path',
        'how-to/find-all-routes',
        'how-to/find-influencers',
        'how-to/detect-circular-dependencies',
        'how-to/export-for-visualization',
        'how-to/filter-by-attributes',
        'how-to/extract-subgraphs',
        'how-to/analyze-impact',
        'how-to/find-bridge-nodes',
      ],
    },
    {
      type: 'category',
      label: 'Explanation',
      collapsed: true,
      items: [
        'explanation/index',
        'explanation/graph-concepts',
        'explanation/centrality-metrics',
        'explanation/when-to-use-grph',
      ],
    },
    {
      type: 'category',
      label: 'CLI Reference',
      collapsed: true,
      items: [
        'cli-reference/index',
        'cli-reference/info',
        'cli-reference/meta',
        'cli-reference/nodes',
        'cli-reference/edges',
        'cli-reference/neighbors',
        'cli-reference/path',
        'cli-reference/all-paths',
        'cli-reference/has-path',
        'cli-reference/reachable',
        'cli-reference/common-neighbors',
        'cli-reference/stats',
        'cli-reference/centrality',
        'cli-reference/components',
        'cli-reference/degree',
        'cli-reference/ego',
        'cli-reference/subgraph',
        'cli-reference/export',
      ],
    },
    'gexf-format',
    {
      type: 'category',
      label: 'Examples (Legacy)',
      collapsed: true,
      items: [
        'examples/filtering',
        'examples/json-output',
        'examples/scripting',
      ],
    },
    'api',
  ],
};

export default sidebars;
