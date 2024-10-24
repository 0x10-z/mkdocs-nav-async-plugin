import importlib.resources as resources
import os
import random
import re
import shutil
import string
import time

import htmlmin
import lxml.html

from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin

class NavAsync(BasePlugin):
    minify = "minify"
    prettify = "prettify"
    config_scheme = (
        (prettify, Type(bool, default=False)),
        (minify, Type(bool, default=False)),
    )
    nav_filename = "@nav.html"

    def on_config(self, config):
        """
        Configures the plugin based on the provided configuration.

        This method retrieves the 'prettify' and 'minify' options from the plugin's configuration
        and prints a message indicating whether each option is enabled or disabled.

        Args:
            config (dict): The configuration dictionary with settings for the plugin.
        """
        for option in [self.prettify, self.minify]:
            is_enabled = self.config.get(option, False)
            status = "enabled" if is_enabled else "disabled"
            print(f"{option.capitalize()} is {status}")

    def on_startup(self, command, dirty):
        """
        Copy the spinner SVG file only once at the beginning of the build process.
        This method does not have access to 'config', so we won't use it here.
        """
        self.nav_filename = f"nav_{''.join(random.choices(string.ascii_letters + string.digits, k=5))}.html"

    def on_post_page(self, output_content, page, config):
        """
        Processes each page after it is built.
        Clears the navigation and inserts a spinner and script for asynchronous navigation loading.
        """
        start_time = time.time()
        site_url = config['site_url']
        site_dir = config.get('site_dir', None)
        prettify = self.config.get('prettify', False)
        minify = self.config.get('minify', False)
        if site_dir is None:
            raise KeyError("The 'site_dir' key is missing in the configuration.")

        nav_file_path = os.path.join(site_dir, self.nav_filename)

        svg_dest = os.path.join(site_dir, 'bars-rotate-fade.svg')
        if not os.path.exists(svg_dest):
            self.copy_spinner_svg(svg_dest)

        tree = lxml.html.fromstring(output_content)

        classAttr = "md-nav__list"
        nav_div = tree.xpath(f"//ul[@class='{classAttr}']")

        if nav_div:
            if not os.path.exists(nav_file_path):
                self.save_navigation_to_file(nav_div[0], nav_file_path, prettify, minify)

            nav_div[0].clear()
            nav_div[0].set('class', classAttr)
            nav_div[0].set('data-md-scrollfix')
            
            self.insert_spinner_and_script(nav_div[0], tree, site_url, self.nav_filename)

        end_time = time.time()
        print(f"Processed {page.file.src_path} in {end_time - start_time:.2f} seconds")

        modified_html = lxml.html.tostring(tree, pretty_print=prettify, encoding='unicode')
        if prettify:
            modified_html = re.sub(r'\n\s*\n+', '\n', modified_html)
        if minify:
            modified_html = htmlmin.minify(modified_html, remove_empty_space=True)
        return modified_html

    def copy_spinner_svg(self, svg_dest):
        """
        Copies the default spinner SVG file to the site directory at the specified path.

        Args:
            svg_dest (str): The path where the spinner SVG file is to be copied.

        Returns:
            None
        """
        svg_src = resources.files('mkdocs_nav_async.loading_icons').joinpath('bars.svg')
        shutil.copy(svg_src, svg_dest)
        print(f"Spinner SVG copied to: {svg_dest}")

    def save_navigation_to_file(self, nav_element, nav_file_path, prettify, minify):
        """
        Saves the navigation children to a file.

        Args:
            nav_element (lxml.etree._Element): The root navigation element.
            nav_file_path (str): The path where the navigation children will be saved.
            prettify (bool): If True, the saved HTML will be prettified with newlines and indentation.
            minify (bool): If True, the saved HTML will be minified by removing all whitespace.

        Returns:
            None
        """
        with open(nav_file_path, 'w', encoding='utf-8') as nav_file:
            content = ''.join([lxml.html.tostring(child, pretty_print=prettify, encoding='unicode') for child in nav_element])
            if prettify:
                content = re.sub(r'\n\s*\n+', '\n', content)
            if minify:
                content = htmlmin.minify(content, remove_empty_space=True)
            nav_file.write(content)
        print(f"Navigation children saved to: {nav_file_path}")


    def insert_spinner_and_script(self, nav_element, tree, site_url, nav_filename):
        """
        Inserts a spinner and script into the navigation element to load the navigation content asynchronously.

        Creates a spinner div with a loading icon and appends it to the navigation element. Then, it appends a script
        element to the body of the HTML document. The script fetches the content of the specified navigation file
        and injects it into the navigation element once loaded, hiding the spinner in the process. If there's an error
        loading the navigation, the spinner is still hidden and the error is logged to the console.

        Args:
            nav_element: The navigation element to insert the spinner and script into.
            tree: The root element of the HTML document.
            site_url: The URL of the site, used to construct the URL for the navigation file.
            nav_filename: The filename of the navigation file to load.
        """
        spinner_div = lxml.html.Element("div", id="loading-spinner", style="display:flex;justify-content:center;align-items:center;height:100px;")
        spinner_img = lxml.html.Element("img", src=f"{site_url}bars-rotate-fade.svg", alt="Loading...", style="width:50px;")
        spinner_div.append(spinner_img)

        nav_element.append(spinner_div)

        script = lxml.html.Element("script")
        script.text = """
        function openNavLinks() {
            const navLinks = document.querySelectorAll(".md-nav__link");

            if (navLinks.length === 0) {
                setTimeout(openNavLinks, 200);
                return;
            }

            const currentUrl = window.location.pathname;

            navLinks.forEach((link) => {
                const href = link.getAttribute("href");
                if (href && currentUrl.includes(href)) {
                link.classList.add("active");

                let parent = link.closest("li");
                while (parent) {
                    const toggleInput = parent.querySelector('input[type="checkbox"]');
                    if (toggleInput) {
                    toggleInput.checked = true;
                    }
                    parent = parent.parentElement.closest("li");
                }
                }
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            var spinner = document.getElementById("loading-spinner");
            var navContainer = document.querySelector("ul.md-nav__list");

            // Use fetch to load the content of """ + nav_filename + """
            fetch('""" + site_url + nav_filename +"""')
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(function(html) {
                    navContainer.innerHTML = html;
                    openNavLinks();
                    spinner.style.display = "none";  // Hide the spinner once loaded
                })
                .catch(function(error) {
                    console.error('Error loading navigation:', error);
                    spinner.style.display = "none";  // Hide the spinner even if there's an error
                });
        });
        """

        tree.body.append(script)
