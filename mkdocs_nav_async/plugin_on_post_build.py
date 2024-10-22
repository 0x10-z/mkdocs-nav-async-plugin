import os
import time
import shutil
from mkdocs.plugins import BasePlugin
from concurrent.futures import ThreadPoolExecutor
import importlib.resources as pkg_resources
import lxml.html
from tqdm import tqdm

class NavAsync(BasePlugin):

    def on_post_build(self, config):
        """
        Executes once the entire site is generated.
        Extracts the navigation from one page and applies it to the rest,
        using threads to clear the navigation from all pages and add a spinner.
        """
        start_time = time.time()

        site_dir = config['site_dir']
        nav_file_path = os.path.join(site_dir, 'nav.html')
        
        with pkg_resources.path('mkdocs_nav_async.loading_icons', 'bars.svg') as svg_path:
            svg_src = svg_path
            svg_dest = os.path.join(site_dir, 'bars-rotate-fade.svg')

            # Copy the spinner SVG file
            self.copy_spinner_svg(svg_src, svg_dest)

        # Process the first page to extract navigation
        self.extract_navigation_from_first_page(site_dir, nav_file_path)

        # Clear the navigation from the rest of the pages in parallel
        self.clear_navigation_in_all_pages(site_dir)

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

    def copy_spinner_svg(self, svg_src, svg_dest):
        """ Copies the spinner SVG file to the generated site. """
        shutil.copy(svg_src, svg_dest)
        print(f"Spinner SVG copied to: {svg_dest}")

    def extract_navigation_from_first_page(self, site_dir, nav_file_path):
        """ Processes the first page of the site to extract navigation and save it to a separate file. """
        for file in os.listdir(site_dir):
            if file.endswith('.html'):
                file_path = os.path.join(site_dir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = lxml.html.parse(f)
                    root = tree.getroot()

                print(f"Taking nav from: {file_path}")
                # Encontrar el elemento <ul> con la clase 'md-nav__list'
                nav_div = root.xpath("//ul[@class='md-nav__list']")

                if nav_div:
                    nav_element = nav_div[0]  # Seleccionamos el primer <ul> encontrado

                    # Guardar la navegación en un archivo HTML separado
                    with open(nav_file_path, 'w', encoding='utf-8') as nav_file:
                        nav_file.write(lxml.html.tostring(nav_element, encoding='unicode', pretty_print=True))

                    nav_element.clear()  # Limpiar la navegación en el HTML original
                    self.insert_spinner_and_script(nav_element, root)

                    # Guardar el archivo HTML modificado
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(lxml.html.tostring(root, encoding='unicode', pretty_print=True))

                break  # Procesar solo la primera página
    
    def insert_spinner_and_script(self, nav, tree):
        """Inserta el spinner y el script asincrónico en el HTML usando lxml."""
        # Crear el nodo del spinner
        spinner_div = lxml.html.Element("div", id="loading-spinner", style="display:flex;justify-content:center;align-items:center;height:100px;")
        spinner_img = lxml.html.Element("img", src="/en/bars-rotate-fade.svg", alt="Loading...")
        spinner_div.append(spinner_img)

        # Añadir el spinner a la navegación
        if nav is not None:
            nav.append(spinner_div)

        # Crear el script asíncrono
        script = lxml.html.Element("script")
        script.text = """
        document.addEventListener("DOMContentLoaded", function() {
            var spinner = document.getElementById("loading-spinner");
            var navContainer = document.querySelector("ul.md-nav__list");

            // Use fetch to load the content of nav.html
            fetch('/en/nav.html')
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
        body = tree.xpath('//body')
        if body:
            body[0].append(script)


    def get_html_files_recursively(self, site_dir):
        """ Retrieves all .html files recursively within site_dir. """
        html_files = []
        for root, dirs, files in os.walk(site_dir):
            for file in files:
                if file.endswith('.html') and file != 'nav.html':
                    html_files.append(os.path.join(root, file))
        return html_files

    def clear_navigation_in_all_pages(self, site_dir):
        """ Uses threads to clear the navigation from all pages, leveraging os.walk and ThreadPool. """
        # Recorrer el directorio usando os.walk para encontrar todos los archivos .html
        html_files = self.get_html_files_recursively(site_dir)

        print(f"Starting to clear navigation in {len(html_files)} pages using ThreadPool...")

        # Usar ThreadPoolExecutor y tqdm para procesar en paralelo con barra de progreso
        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(self.clear_navigation, html_files), total=len(html_files)))

    def clear_navigation(self, file_path):
        """ Clears the navigation in a specific HTML page. """
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = lxml.html.parse(f)
            root = tree.getroot()

        # Encontrar el elemento <ul> con la clase 'md-nav__list'
        nav_div = root.xpath("//ul[@class='md-nav__list']")
        if nav_div:
            nav_element = nav_div[0]  # Seleccionamos el primer <ul> encontrado
            nav_element.clear()  # Limpiar la navegación

            # Insertar el spinner y el script
            self.insert_spinner_and_script(nav_element, root)

            # Guardar el archivo HTML modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(lxml.html.tostring(root, encoding='unicode', pretty_print=True))
