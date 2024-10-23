# MkDocs Navigation Async

**MkDocs Navigation Async** is an MkDocs plugin designed to extract navigation from one page of your site and load it asynchronously across the other pages. This helps reduce HTML duplication for large sites by keeping navigation in a separate file and injecting it via JavaScript. It also shows a loading spinner until the navigation is fully loaded.

## Features

- Extracts navigation from a single page and applies it to the rest of the site.
- Reduces the HTML size of each page by dynamically loading the navigation via `fetch`.
- Uses threads to speed up the removal of navigation from other pages.
- Displays a loading spinner while the navigation is being fetched.

## Installation

You can install the plugin via `pip` by adding the following line to your `requirements.txt` or installing it directly:

```bash
pip install mkdocs-nav-async
```

Or install it directly from your local development environment using the `-e` option:

```bash
pip install -e .
```

## Usage

Once installed, configure the plugin in your `mkdocs.yml` configuration file:

```yaml
plugins:
  - nav_async
```

You can also specify options like prettify, in order to prettify output html:

```yaml
plugins:
  - nav_async:
      prettify: true
      minify: true
```

## How it Works

The plugin extracts the navigation from the first page it processes and saves it as `nav.html`. Then it replaces the navigation in each page with a placeholder and loads the navigation asynchronously when the page is visited. A spinner is shown during the loading process.

### Example `mkdocs.yml`:

```yaml
site_name: "My Documentation"
theme:
  name: "material"

plugins:
  - nav_async:
      prettify: true # Optional, specify output html prettified
      minify: true # Optional, minify html output

extra_css:
  - css/custom.css # Optional, if you want to customize the spinner or styling

nav:
  - Home: index.md
  - About: about.md
  - Contact: contact.md
```

## Debugging in Development

To debug the plugin locally during development, follow these steps:

1. Clone or download the plugin to your local environment.
2. Install it in "editable" mode using the following command in the plugin’s directory:

   ```bash
   pip install -e .
   ```

   This will install the plugin in development mode, allowing you to make changes without having to reinstall it each time.

3. Run `mkdocs serve` in your project’s directory to serve your documentation locally. Any changes you make to the plugin will be immediately reflected when you reload the MkDocs server.

4. Use Python's `print()` or a logger to print debugging information to the console.

### Example Debugging Output

When running the plugin, you can expect to see output like this:

```bash
Taking nav from: /path/to/site/index.html
Spinner SVG copied to: /path/to/site/bars-rotate-fade.svg
Starting to clear navigation in pages using ThreadPool (50 files)...
Total execution time: 1.35 seconds
```

## Customization

- **Spinner Icon**: The default spinner icon is an SVG file (`bars-rotate-fade.svg`). You can replace this with your own by modifying the plugin or adding your own spinner.
- **Asynchronous Loading**: The plugin uses `fetch` to load the navigation dynamically. You can customize the JavaScript if needed by modifying the `insert_spinner_and_script` function.

## Performance Statistics

- With this plugin using `BeautifulSoup4`, it processes each page in 0.8 seconds. In a 4000 files project, 53min.
- With this plugin using `lxml`, it processes each page in 0.08 seconds. In a 4000 files project, 5min.
- Using this plugin with `on_post_page` in a project with over 4000 files adds an additional 6 minutes to the build time compared to not using the plugin.
- Using this plugin with `on_post_build` in a project with over 4000 files also adds an additional 6 minutes to the build time compared to not using the plugin.

## License

This project is licensed under the [MIT License](LICENSE).
