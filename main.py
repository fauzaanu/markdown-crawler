import asyncio
import datetime
import os
from urllib.parse import urlparse

import typer
from crawlee import Glob, ConcurrencySettings
from crawlee.configuration import Configuration
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from rich import print as rprint

from compile import merge_md
from conf import URL, USER_DEFINED_GLOB_EXCLUDES, USER_DEFINED_GLOB_INCLUDES


async def main() -> None:
    OneByOne = ConcurrencySettings(desired_concurrency=1, max_concurrency=1)

    config = Configuration.get_global_configuration()
    config.persist_storage = False

    crawler = PlaywrightCrawler(
        user_data_dir='crawl-browser',
        headless=True,
        browser_type='firefox',
        request_handler_timeout=datetime.timedelta(seconds=300),
        retry_on_blocked=True,
        concurrency_settings=OneByOne
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        url = context.request.url
        context.log.info(f'Processing {url} ...')

        folder = FOLDER
        os.makedirs(folder, exist_ok=True)

        # Parse URL
        parsed = urlparse(url)
        domain = parsed.netloc  # e.g. "developers.facebook.com"
        path = parsed.path  # e.g. "/docs/marketing-api/hello"

        # Remove leading/trailing slashes
        # We'll handle trailing slash logic for 'index.md' below.
        path = path.strip('/')

        # Break path into segments
        path_segments = [seg for seg in path.split('/') if seg]

        # If there's no path segment, that means it's just domain.com/ => index.md
        if not path_segments:
            # marketing-apis/<domain>/index.md
            file_dir = os.path.join(folder, domain)
            file_name = "index.md"

            # Make the directory path
            os.makedirs(file_dir, exist_ok=True)
            full_path = os.path.join(file_dir, file_name)

            # Write out the text content
            with open(full_path, 'w', encoding="utf-8") as f:
                title = await context.page.title()
                body_text = await context.page.evaluate('document.body.innerText')
                f.write(f"Retrived from: {url}\n\n")
                f.write(f"# {title}\n\n")
                f.write(f"{body_text}\n\n")

            context.log.info(f"File saved to {full_path}")
        else:
            # Check last segment for an extension
            last_segment = path_segments[-1]
            name, ext = os.path.splitext(last_segment)

            if ext:
                # If the last segment has an extension, replace with .md
                # or keep the same extension if you prefer.
                file_name = name + ".md"
                # All segments except last become the folder structure
                dir_parts = path_segments[:-1]
            else:
                # If there's no extension, treat last segment as a folder => use index.md
                file_name = "index.md"
                dir_parts = path_segments

            file_dir = os.path.join(folder, domain, *dir_parts)

            # Make the directory path
            os.makedirs(file_dir, exist_ok=True)
            full_path = os.path.join(file_dir, file_name)

            # Write out the text content
            with open(full_path, 'w', encoding="utf-8") as f:
                title = await context.page.title()
                body_text = await context.page.evaluate('document.body.innerText')
                f.write(f"Retrived from: {url}\n\n")
                f.write(f"# {title}\n\n")
                f.write(f"{body_text}\n\n")

            context.log.info(f"File saved to {full_path}")

        # Follow links
        await context.enqueue_links(
            include=[Glob(glob) for glob in GLOB_INCLUDES],
            exclude=[Glob(glob) for glob in GLOB_EXCLUDES]
        )

    await crawler.run([URL])


if __name__ == '__main__':
    try:
        banner = r"""
                              _        _                                                           _             
                             | |      | |                                                         | |            
      _ __ ___    __ _  _ __ | | __ __| |  ___ __      __ _ __  ______  ___  _ __  __ _ __      __| |  ___  _ __ 
     | '_ ` _ \  / _` || '__|| |/ // _` | / _ \\ \ /\ / /| '_ \|______|/ __|| '__|/ _` |\ \ /\ / /| | / _ \| '__|
     | | | | | || (_| || |   |   <| (_| || (_) |\ V  V / | | | |      | (__ | |  | (_| | \ V  V / | ||  __/| |   
     |_| |_| |_| \__,_||_|   |_|\_\\__,_| \___/  \_/\_/  |_| |_|       \___||_|   \__,_|  \_/\_/  |_| \___||_|   
                                                                                                                 
                                                                                                            
        """
        rprint(f"\n[bold green]{banner}[/bold green]\n")

        rprint("\n[bold blue]markdown-crawler settings are in conf.py, you should edit that file.[/bold blue]\n")
        rprint(f"[bold green]crawling {URL} ...[/bold green]\n")

        USER_FOLDER = typer.prompt("Enter the folder name to store files ->")
        os.makedirs("crawls", exist_ok=True)
        FOLDER = os.path.join("crawls", USER_FOLDER)

        # Collect glob includes and excludes using the helper function
        GLOB_INCLUDES = [f"{URL}/**"] if not USER_DEFINED_GLOB_INCLUDES else USER_DEFINED_GLOB_INCLUDES
        GLOB_EXCLUDES = [] if not USER_DEFINED_GLOB_EXCLUDES else USER_DEFINED_GLOB_EXCLUDES

        # Run the crawler and merge markdown files
        asyncio.run(main())
        merge_md(FOLDER, f"{FOLDER}.md")

        rprint(f"\n[bold magenta]Operation complete. Files saved in {FOLDER}.md[/bold magenta]")
    except Exception as e:
        rprint(f"\n[bold red]Error: {e}[/bold red]")
