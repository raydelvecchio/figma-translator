from .constants import Config
from .utils import createFile, runCommand
from .downloader import FigmaDownloader
from .generator import UIGenerator
import shutil
import os
from tqdm import tqdm

class FigmaTranslator:
    def __init__(self, project_name: str, test_environment: bool = True) -> None:
        self.project_name = project_name.lower()
        self.test_environment = test_environment
        self.downloader = FigmaDownloader()
        self.generator = UIGenerator()

        if test_environment:
            self._setup_test_environment()

    def _setup_test_environment(self):
        print("BEGINNING ENVIRONMENT SETUP...\n")
        
        # won't regenerate the test environmet if we use the same name!
        if os.path.exists(os.path.join(Config.ENVIRONMENTS_FOLDER, self.project_name)):
            print(f"Project '{self.project_name}' already exists. Finishing setup.")
            return

        steps = [
            ("Creating environments folder", self._create_environments_folder),
            ("Changing to environments folder", lambda: os.chdir(Config.ENVIRONMENTS_FOLDER)),
            ("Setting up the project", lambda: runCommand(f"yarn create react-app {self.project_name}")),
            ("Changing to project folder", lambda: os.chdir(self.project_name)),
            ("Installing dependencies", lambda: runCommand("yarn add bootstrap react-bootstrap @popperjs/core")),
            ("Installing additional dependencies", lambda: runCommand("yarn add -D tailwindcss@latest postcss@latest autoprefixer@latest react-icons")),
            ("Initializing tailwind", lambda: runCommand("npx tailwindcss init -p")),
            ("Setting up Bootstrap CSS and JS", self._setup_bootstrap),
            ("Updating tailwind config", self._update_tailwind_config),
            ("Updating index.css", self._update_index_css),
            ("Updating App.js", self._update_app_js),
            ("Deleting unnecessary files", self._delete_unnecessary_files),
            ("Going back to main directory", lambda: os.chdir(os.path.dirname(os.path.dirname(os.getcwd()))))
        ]

        for _, step_function in tqdm(steps, desc="Setting up test environment"):
            step_function()

        print("Project environment setup complete!\n")
        print(f"To start the development server, run:")
        print(f"cd {Config.ENVIRONMENTS_FOLDER}/{self.project_name}")
        print("yarn start")
        print("\nYOUR PROJECT IS BEING GENERATED SHORTLY...\n")

    def _create_environments_folder(self):
        if not os.path.exists(Config.ENVIRONMENTS_FOLDER):
            os.makedirs(Config.ENVIRONMENTS_FOLDER)

    def _update_tailwind_config(self):
        createFile('tailwind.config.js', '''
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
        ''')

    def _update_index_css(self):
        createFile('src/index.css', '''
@tailwind base;
@tailwind components;
@tailwind utilities;
        ''')

    def _setup_bootstrap(self):
        # Update index.js to import Bootstrap CSS and JS
        index_js_content = '''
        import React from 'react';
        import ReactDOM from 'react-dom/client';
        import './index.css';
        import App from './App';
        import 'bootstrap/dist/css/bootstrap.min.css';
        import 'bootstrap/dist/js/bootstrap.bundle.min.js';

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
        );
        '''
        createFile('src/index.js', index_js_content)

    def _update_app_js(self):
        createFile('src/App.js', '''
import './App.css';
// TODO: your imports here

function App() {
    return (
        <></>  // TODO: your components here
    );
}

export default App;
        ''')

    def _delete_unnecessary_files(self):
        unnecessary_files = ['src/logo.svg', 'src/App.test.js', 'src/setupTests.js', 
                             'public/logo192.png', 'public/logo512.png', 'public/robots.txt', 'public/manifest.json']
        for file in unnecessary_files:
            if os.path.exists(file):
                os.remove(file)

    def translate(self, figma_file_id: str, output_image_filename: str):
        """
        Translates a Figma file into code! Writes the output to a file. The main entrypoint for this!
        """
        print(f"Translating {figma_file_id} to code...")
        if not output_image_filename.lower().endswith('.png'):
            output_image_filename += '.png'
        
        image_filenames = self.downloader.downloadFigmaFileImages(file_id=figma_file_id, filename=output_image_filename)
        code_filenames = [self.generator.getCodeForImage(ifn) for ifn in image_filenames]
        
        if self.test_environment:
            self._setup_project_environment(code_filenames)
        else:
            print("Code files generated:")
            for code_file in code_filenames:
                print(f"- {code_file}")
        print()

    def _setup_project_environment(self, code_filenames):
        project_src_folder = os.path.join(Config.ENVIRONMENTS_FOLDER, self.project_name, 'src')
        os.makedirs(project_src_folder, exist_ok=True)
        
        app_js_path = os.path.join(project_src_folder, 'App.js')
        imports, components = [], []
        
        for code_file in code_filenames:
            shutil.copy(code_file, project_src_folder)
            component_name = self._extract_component_name(code_file)
            filename = os.path.basename(code_file)
            imports.append(f"import {component_name} from './{filename}';")
            components.append(f"<{component_name} />")
        
        self._update_app_js_content(app_js_path, imports, components)
        
        print(f"Code files copied to {project_src_folder} and integrated into App.js")

        project_dir = os.path.join(Config.ENVIRONMENTS_FOLDER, self.project_name)
        print(f"Changing directory to {project_dir}")
        os.chdir(project_dir)
        
        print("Starting the development server...")
        runCommand("yarn start")

    def _extract_component_name(self, code_file):
        with open(code_file, 'r') as f:
            content = f.read()
            export_line = [line for line in content.split('\n') if line.startswith('export default')][0]
            return export_line.split()[2].rstrip(';')

    def _update_app_js_content(self, app_js_path, imports, components):
        with open(app_js_path, 'r+') as f:
            content = f.read()
            content = content.replace("// TODO: your imports here", f"{'\n'.join(imports)}\n//TODO: your imports here")
            content = content.replace("<></>  // TODO: your components here", f"{components[0]}\n//TODO: your components here" if components else "")
            f.seek(0)
            f.write(content)
            f.truncate()
