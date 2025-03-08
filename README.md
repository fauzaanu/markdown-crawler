# markdown-crawler

**markdown-crawler** is a Python tool that crawls websites and neatly saves their text content into markdown files,
providing a convenient way to archive the text content of the web locally. It can be a personal knowledge base, or
something more to query through a Large Language Model (LLM) using RAG or some other method.

## How It Works

- Automatically visits and retrieves webpage content.
- Saves each page's visible text content exactly as is.
- Organizes files neatly in directories that replicates the structure of the original website URLs.
- Finally exports a main markdown file that compiles all the content in all the markdown files.

## Quick Start

Install dependencies using [`uv`](https://github.com/astral-sh/uv):

```bash
uv sync
```

Run the crawler:

```bash
uv run python main.py
```

When prompted, provide:

- **Start URL:** URL of the website to start crawling.
- The Glob pattern to match URLs to crawl.
- **Folder name:** Directory to store your markdown files and the compiled PDF.

### Example Output Structure

Your markdown files will be neatly structured to match the crawled website's URL structure:

```
crawls/
└── example
    └── example.com
        ├── breaking
        │   └── 1195928
        │       └── index.md
        └── coffee
            └── 27
                └── index.md

example.md
```