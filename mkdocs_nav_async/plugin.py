import os
import time
import shutil
from mkdocs.plugins import BasePlugin
import importlib.resources as pkg_resources
import lxml.html
import re

class NavAsync(BasePlugin):

    def on_startup(self, command, dirty):
        """
        Copy the spinner SVG file only once at the beginning of the build process.
        This method does not have access to 'config', so we won't use it here.
        """
        pass

    def on_post_page(self, output_content, page, config):
        """
        Processes each page after it is built.
        Clears the navigation and inserts a spinner and script for asynchronous navigation loading.
        """
        start_time = time.time()
        absolute_path = self.config.get('path', "")
        site_dir = config.get('site_dir', None)
        if site_dir is None:
            raise KeyError("The 'site_dir' key is missing in the configuration.")

        nav_file_path = os.path.join(site_dir, 'nav.html')

        # Copy the spinner SVG file (only needs to happen once, check if already exists)
        svg_dest = os.path.join(site_dir, 'bars-rotate-fade.svg')
        if not os.path.exists(svg_dest):
            self.copy_spinner_svg(svg_dest)

        # Process the current page to clear navigation and insert spinner
        tree = lxml.html.fromstring(output_content)

        classAttr = "md-nav__list"
        # Encontrar el elemento <ul> con la clase 'md-nav__list' usando XPath
        nav_div = tree.xpath(f"//ul[@class='{classAttr}']") # Find the navigation

        if nav_div:
            # If it's the first page processed, extract and save the navigation
            if not os.path.exists(nav_file_path):
                self.save_navigation_to_file(nav_div[0], nav_file_path)  # Use nav_div[0] instead of passing list

            nav_div[0].clear()
            nav_div[0].set('class', classAttr)
            
            self.insert_spinner_and_script(nav_div[0], tree, absolute_path)

        end_time = time.time()
        print(f"Processed {page.file.src_path} in {end_time - start_time:.2f} seconds")

        # Return the modified content for this page
        modified_html = lxml.html.tostring(tree, pretty_print=True, encoding='unicode')
        return modified_html

    def copy_spinner_svg(self, svg_dest):
        """ Copies the spinner SVG file to the generated site. """
        with pkg_resources.path('mkdocs_nav_async.loading_icons', 'bars.svg') as svg_src:
            shutil.copy(svg_src, svg_dest)
        print(f"Spinner SVG copied to: {svg_dest}")

    def save_navigation_to_file(self, nav_element, nav_file_path):
        """Guarda la navegación en un archivo HTML separado."""
        with open(nav_file_path, 'w', encoding='utf-8') as nav_file:
            content = lxml.html.tostring(nav_element, pretty_print=True, encoding='unicode')
            content = re.sub(r'\n\s*\n+', '\n', content)
            nav_file.write(content)
        print(f"Navigation saved to: {nav_file_path}")

    def insert_spinner_and_script(self, nav_element, tree, absolute_path):
        """Inserta el spinner y el script de carga asincrónica en la página HTML."""
        # Crear el nodo del spinner
        spinner_div = lxml.html.Element("div", id="loading-spinner", style="display:flex;justify-content:center;align-items:center;height:100px;")
        spinner_img = lxml.html.Element("img", src=f"/{absolute_path}/bars-rotate-fade.svg", alt="Loading...", style="width:50px;")
        spinner_div.append(spinner_img)

        # Añadir el spinner a la navegación
        nav_element.append(spinner_div)

        # Crear el script asíncrono
        script = lxml.html.Element("script")
        script.text = """
        document.addEventListener("DOMContentLoaded", function() {
            var spinner = document.getElementById("loading-spinner");
            var navContainer = document.querySelector("ul.md-nav__list");

            // Use fetch to load the content of nav.html
            fetch('""" + absolute_path + """/nav.html')
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(function(html) {
                    navContainer.innerHTML = html;
                    spinner.style.display = "none";  // Hide the spinner once loaded
                })
                .catch(function(error) {
                    console.error('Error loading navigation:', error);
                    spinner.style.display = "none";  // Hide the spinner even if there's an error
                });
        });
        """

        # Añadir el script al final del body
        tree.body.append(script)
