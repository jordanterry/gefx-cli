import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'index',
    'getting-started',
    {
      type: 'category',
      label: 'CLI Reference',
      collapsed: false,
      items: [
        'cli-reference/index',
        'cli-reference/info',
        'cli-reference/meta',
        'cli-reference/nodes',
        'cli-reference/edges',
      ],
    },
    'gexf-format',
    {
      type: 'category',
      label: 'Examples',
      collapsed: false,
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
