import os
import subprocess
import shutil
from zipfile import ZipFile
import xml.etree.ElementTree as ET

def get_component_directories_from_xml():
    """
    Parse the appian-component-plugin.xml file to extract component rule-names.
    Returns a list of component names.
    """
    xml_file = "appian-component-plugin.xml"
    components = []

    try:
        print(f"Parsing {xml_file} for component rule-names...")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Find all <component> tags and extract the rule-name attribute
        for component in root.findall("component"):
            rule_name = component.get("rule-name")
            if rule_name:
                components.append(rule_name)

        print(f"Found components in XML: {', '.join(components)}")
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        exit(1)

    return components

def run_parcel_build(component_name):
    """Run the Parcel build process for a specific component."""
    try:
        print(f"Building component: {component_name}...")
        print("Cleaning dist folder...")
        if os.path.exists("dist"):
            shutil.rmtree("dist")  # Delete the dist folder

        print("Running Parcel build...")
        # Dynamically locate the npx binary
        npx_binary = shutil.which("npx")
        if not npx_binary:
            raise FileNotFoundError("npx binary not found. Ensure Node.js and npx are installed.")

        # Build the specific component
        component_path = f"{component_name}/v1/index.html"
        subprocess.run([npx_binary, "parcel", "build", component_path, "--public-url", "./"], check=True)
        print(f"Parcel build for {component_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during Parcel build for {component_name}: {e}")
        return False
    except FileNotFoundError as e:
        print(f"npx binary not found: {e}")
        exit(1)

def add_appian_sdk_placeholder():
    file_path = os.path.join("dist", "index.html")
    try:
        print(f"Modifying {file_path}...")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if '<script src="APPIAN_JS_SDK_URI"></script>' not in content:
            content = content.replace(
                "</body>",
                '    <script src="APPIAN_JS_SDK_URI"></script>\n</body>'
            )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Successfully modified {file_path}.")
        return True
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
        return False

def copy_files_for_component(component_name):
    try:
        output_dir = os.path.join("output", component_name, "v1")

        # Create the component output directory
        os.makedirs(output_dir, exist_ok=True)

        # Copy all files from dist to output/component/v1
        for file_name in os.listdir("dist"):
            full_file_name = os.path.join("dist", file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, output_dir)

        # Copy the component properties file if it exists
        properties_file = f"{component_name}_en_US.properties"
        properties_path = os.path.join(component_name, "v1", properties_file)
        if os.path.exists(properties_path):
            shutil.copy(properties_path, output_dir)
        else:
            print(f"Warning: Properties file not found: {properties_path}")

        print(f"Files for {component_name} copied successfully.")
        return True
    except Exception as e:
        print(f"Error copying files for {component_name}: {e}")
        return False

def zip_output_files():
    """Zip all files in the output directory, excluding existing .zip files."""
    try:
        project_name = "appian-component-library"  # Name of the project
        zip_file_name = f"{project_name}.zip"
        output_dir = "output"
        zip_file_path = os.path.join(output_dir, zip_file_name)

        # Create the zip file
        print(f"Creating zip file: {zip_file_path}...")
        with ZipFile(zip_file_path, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    if not file.endswith(".zip"):  # Exclude existing zip files
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_dir)  # Preserve relative paths
                        zipf.write(file_path, arcname)

        print(f"Zip file created successfully: {zip_file_path}")
        return True
    except Exception as e:
        print(f"Error creating zip file: {e}")
        return False

if __name__ == "__main__":
    # Clean the output directory at the start
    print("Cleaning output directory...")
    if os.path.exists("output"):
        shutil.rmtree("output")  # Delete the output folder
    os.makedirs("output", exist_ok=True)
    
    # Copy the plugin XML file once at the beginning
    if os.path.exists("appian-component-plugin.xml"):
        shutil.copy("appian-component-plugin.xml", "output")
        print("Copied appian-component-plugin.xml to output directory.")
    else:
        print("Warning: appian-component-plugin.xml not found!")
    
    # Get all component directories from the XML file
    components = get_component_directories_from_xml()
    
    # Process each component
    success_count = 0
    for component in components:
        print(f"\n{'='*50}\nProcessing component: {component}\n{'='*50}")
        
        if run_parcel_build(component):
            if add_appian_sdk_placeholder():
                if copy_files_for_component(component):
                    success_count += 1
    
    # Create the final zip file if at least one component was processed successfully
    if success_count > 0:
        print(f"\nSuccessfully processed {success_count} out of {len(components)} components.")
        zip_output_files()
        if os.path.exists("dist"):
            print("Cleaning up dist folder...")
            shutil.rmtree("dist")
            
    else:
        print("\nNo components were successfully processed.")
        exit(1)