# NavAsync Plugin

## About the Developer

![myself](./myself.webp){ align=left width=150 }

Hi, I'm a software developer who is passionate about optimizing workflows and solving real-world problems through code. One day, I found myself working on a massive documentation project for a company with over 4000 HTML files across 13 languages. The project was consuming over **3GB** when zipped, which posed significant challenges for deployment and maintenance.

I quickly realized that the navigation content—repeated across every single HTML page—was a major contributor to the overall file size. The entire navigation structure was duplicated in each file, causing the size of the HTML files to grow exponentially as more pages and languages were added.

That's when I decided to create **NavAsync**.

---

## Why I Built NavAsync

The goal of **NavAsync** was simple: **reuse the navigation** across all pages instead of repeating it. By loading the navigation asynchronously after the page content has fully loaded, I was able to drastically reduce the size of each HTML file.

This change not only made the pages load faster, but it also helped me reduce the total size of the zipped project from **3GB to just 300MB**—a nearly 90% reduction!

This improvement was critical for the project’s performance and scalability, particularly for a site with thousands of pages in multiple languages.

---

## What Does NavAsync Do?

The **NavAsync** plugin improves performance for large MkDocs projects by deferring the loading of the navigation bar until the page content has loaded. This approach helps reduce the initial load time for pages, especially in large documentation sites with extensive navigation.

!!! tip "Key Features" - **Asynchronous navigation loading**: Loads the navigation bar asynchronously, allowing the main content to load first. - **Reduces HTML file sizes**: By reusing the navigation, the size of the HTML files decreases significantly, reducing overall bandwidth usage and speeding up deployment times. - **Customizable loading spinner**: You can configure a loading spinner to display while the navigation is loading. - **Scalable for large sites**: Ideal for large documentation projects with thousands of pages and multiple languages.

---

## Installation

To install the `NavAsync` plugin, follow these steps:

### Step 1: Install MkDocs and NavAsync

First, ensure you have **MkDocs** and the **NavAsync** plugin installed:

```bash
pip install mkdocs mkdocs-nav-async
```

### Step 2: Configure the Plugin in `mkdocs.yml`

Add the plugin to your `mkdocs.yml` configuration:

```yaml
plugins:
  - nav_async:
      prettify: true
      minify: true
```

---

## Results and Performance Gains

!!! success "Performance Achievements"
By using **NavAsync**, I was able to: - Reduce a project with 4000 pages across 13 languages from **3GB to 300MB** when zipped. - Decrease HTML file sizes by **60-70%** across the entire site. - Improve page load times, especially for users with slower connections or for projects hosted on limited bandwidth servers.

---

## Issues and Contributions

If you encounter any issues or have ideas for improvements, feel free to open an issue or contribute via pull requests. I'm always happy to collaborate!

- [GitHub Repository](https://github.com/0x10-z/mkdocs-nav-async)

---

## License

The `NavAsync` plugin is licensed under the MIT License.
