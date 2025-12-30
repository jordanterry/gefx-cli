import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'grph',
  tagline: 'Like grep, but for graphs. A CLI tool for exploring, analyzing, and querying graph files.',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // Set the production url of your site here
  url: 'https://jordanterry.github.io',
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/grph/',

  // GitHub pages deployment config.
  organizationName: 'jordanterry',
  projectName: 'grph',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/', // Docs as the main content
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'grph',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/jordanterry/grph',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/getting-started',
            },
            {
              label: 'CLI Reference',
              to: '/cli-reference',
            },
            {
              label: 'GEXF Format',
              to: '/gexf-format',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GEXF Specification',
              href: 'https://gexf.net/',
            },
            {
              label: 'Gephi',
              href: 'https://gephi.org/',
            },
            {
              label: 'NetworkX',
              href: 'https://networkx.org/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/jordanterry/grph',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/grph-cli/',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} grph. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
