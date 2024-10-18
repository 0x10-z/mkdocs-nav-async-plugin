import os
import time
import shutil
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class NavAsyncPlugin(BasePlugin):

    def on_post_build(self, config):
        """
        Executes once the entire site is generated.
        Extracts the navigation from one page and applies it to the rest,
        using threads to clear the navigation from all pages and add a spinner.
        """
        start_time = time.time()

        site_dir = config['site_dir']
        nav_file_path = os.path.join(site_dir, 'nav.html')
        svg_src = os.path.join(os.path.dirname(__file__), 'loading_icons', 'bars-rotate-fade.svg')
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
                    soup = BeautifulSoup(f, 'html.parser')

                print(f"Taking nav from: {file_path}")
                nav_div = soup.find('ul', {'class': 'md-nav__list'})  # Find the navigation

                if nav_div:
                    # Save the navigation to a separate file
                    with open(nav_file_path, 'w', encoding='utf-8') as nav_file:
                        nav_file.write(str(nav_div))
                    nav_div.clear()  # Clear the navigation in the original HTML
                    self.insert_spinner_and_script(nav_div, soup)

                    # Save the modified HTML file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))

                break  # Process only the first page

    def insert_spinner_and_script(self, nav, soup):
        """ Inserts the loading spinner and the asynchronous script into the page's HTML. """
        # Create the spinner elements and the navigation placeholder
        spinner_div = soup.new_tag('div', id='loading-spinner', style='display:flex;justify-content:center;align-items:center;height:100px;')
        spinner_img = soup.new_tag('img', src='/en/bars-rotate-fade.svg', alt='Loading...')
        spinner_div.append(spinner_img)

        # Create the asynchronous loading script
        script_tag = soup.new_tag('script')
        script_tag.string = '''
        document.addEventListener("DOMContentLoaded", function() {
            var spinner = document.getElementById("loading-spinner");
            var navContainer = document.querySelector("ul.md-nav__list");

            // Show the spinner while the navigation is loading

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
                    // spinner.style.display = "none";  // Hide the spinner once loaded
                    console.log("Navigation loaded");
                })
                .catch(function(error) {
                    console.error('Error loading navigation:', error);
                    spinner.style.display = "none";  // Hide the spinner even if there's an error
                });
        });
        '''

        # Insert the spinner, placeholder, and script into the HTML body
        if nav:
            nav.append(spinner_div)
        soup.body.append(script_tag)

    def get_html_files_recursively(self, site_dir):
        """ Retrieves all .html files recursively within site_dir. """
        html_files = []
        for root, dirs, files in os.walk(site_dir):
            for file in files:
                if file.endswith('.html') and file != 'nav.html':
                    html_files.append(os.path.join(root, file))
        return html_files

    def clear_navigation_in_all_pages(self, site_dir):
        """ Uses threads to clear the navigation from the rest of the pages. """
        html_files = self.get_html_files_recursively(site_dir)
        print(f"Starting to clear navigation in pages using ThreadPool ({len(html_files)} files)...")

        # Use ThreadPoolExecutor to clear the navigation in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(self.clear_navigation, html_files[1:])

    def clear_navigation(self, file_path):
        """ Clears the navigation in a specific HTML page. """
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        nav_div = soup.find('ul', {'class': 'md-nav__list'})
        if nav_div:
            nav_div.clear()
        
        self.insert_spinner_and_script(nav_div, soup)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
