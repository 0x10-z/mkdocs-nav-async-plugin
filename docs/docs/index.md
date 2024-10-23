# NavAsync Plugin Documentation

Welcome to the documentation for the **NavAsync** plugin. This plugin enhances the navigation functionality of MkDocs sites by asynchronously loading the navigation bar to improve page load times and performance.

With this plugin, you can load the navigation bar after the page content is fully loaded, reducing the initial load time for large MkDocs projects with hundreds or thousands of pages.

## Features

- **Asynchronous navigation loading**: Improves page load performance by deferring the loading of the navigation bar.
- **Customizable loading spinner**: You can configure the spinner icon shown during the loading of the navigation.
- **Reduces HTML file sizes**: By reusing the navigation across all pages, the plugin reduces the size of HTML files, especially in projects with large navigation.
- **Supports large sites**: Efficient for sites with hundreds or thousands of pages.
- **Integrates with Material for MkDocs**: Fully compatible with the Material theme for MkDocs.

---

## Installation

To install the `NavAsync` plugin, simply add it to your `mkdocs.yml` configuration file. First, ensure you have **MkDocs** and **Material for MkDocs** installed.

### Step 1: Install MkDocs and Material for MkDocs

If you haven't already, install **MkDocs** and **Material for MkDocs**:

```bash
pip install mkdocs mkdocs-material
```

### Step 2: Install the NavAsync Plugin

Install the `NavAsync` plugin using pip:

```bash
pip install navasync
```

### Step 3: Configure the Plugin in `mkdocs.yml`

Add the following configuration to your `mkdocs.yml` file:

```yaml
plugins:
  - nav_async:
      prettify: true
      minify: true
```

### Step 4: Run MkDocs

Once configured, you can build or serve your MkDocs site as usual:

```bash
mkdocs serve
```

This command will start a local development server where you can see the NavAsync plugin in action.

---

## How it Works

In traditional MkDocs setups, the navigation content is repeated on every page, which can significantly increase the size of the HTML files, especially for sites with large navigation structures. This duplication of navigation content can result in much larger files, making the site slower to load and more bandwidth-intensive.

The **NavAsync** plugin solves this issue by **reusing the same navigation** across all pages. Instead of including the full navigation in every HTML file, the plugin replaces it with a lightweight placeholder and loads the navigation asynchronously after the page content is fully loaded. This approach drastically reduces the size of the HTML files.

### Example of File Size Reduction

For large projects with extensive navigation, you can reduce the size of your HTML files by **60-70%** by using this plugin. This is particularly useful in projects with thousands of pages, where each page traditionally carries the full navigation structure. By removing the redundant navigation from each page, the size of the files is greatly minimized.

---

## Configuration Options

The `NavAsync` plugin comes with a few configuration options that can be customized in your `mkdocs.yml` file:

- **`prettify`**: Prettify output html.
  - Type: `bool`
  - Default: `false`
- **`minify`**: Minify output html.
  - Type: `bool`
  - Default: `false`

### Example Configuration

```yaml
plugins:
  - nav_async:
      prettify: true
      minify: true
```

---

## Performance Benefits

The **NavAsync** plugin not only improves the loading performance by asynchronously loading the navigation but also reduces the overall size of the HTML files, resulting in faster load times and reduced bandwidth usage.

In tests, the plugin has shown the following improvements:

- **Without the plugin**: Page load time and file size are significantly higher due to the repetition of navigation content across all pages.
- **With the plugin**: The navigation is loaded asynchronously, reducing the HTML file sizes by up to 70%, which leads to faster page loads and a more efficient site.

---

## Examples

### Basic Example

To see the `NavAsync` plugin in action, you can try the following example:

```yaml
plugins:
  - nav_async:
      prettify: true
      minify: true
```

This configuration will asynchronously load the navigation with a custom spinner icon.

---

## Issues and Contributions

If you encounter any issues or want to contribute to the development of this plugin, feel free to check out the repository on GitHub:

- [GitHub Repository](https://github.com/your-repo/navasync)

Feel free to submit pull requests or report bugs.

---

## License

The `NavAsync` plugin is licensed under the MIT License.
