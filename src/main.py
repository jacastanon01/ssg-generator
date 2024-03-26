import sys
import os
import shutil

from src.block_markdown import markdown_to_blocks, markdown_to_html_node


def main() -> None:
    sourcedir, destination = format_paths()
    copy_contents(sourcedir, destination)
    generate_page("content/test.md", "template.html", "public/index.html")


def format_paths() -> tuple[str, str]:
    """Return absolute paths of static and public directories
    to be used in copy_contents function"""
    abs_path = os.getcwd()

    if os.path.exists(f"{abs_path}/public"):
        shutil.rmtree(f"{abs_path}/public")

    source = os.path.join(abs_path, "static")
    if not os.path.exists(source):
        raise NotADirectoryError("static directory does not exist in src")
    destination = os.path.join(abs_path, "public")

    return source, destination


def copy_contents(source: str, destination: str) -> None:
    """Copy contents from source directory into destination directory"""
    listdirs = os.listdir(
        source
    )  # list all items in the source directory for processing

    for item in listdirs:
        # join paths for static and public folders
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            # copy static file to public directory
            shutil.copyfile(source_path, destination_path)
        else:
            if not os.path.exists(destination_path):
                # create directory
                os.makedirs(destination_path)
            # recursively copy nested directories and their contents
            copy_contents(source_path, destination_path)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    title = ""
    for block in blocks:
        if block.startswith("# "):
            title = "".join(block.split("\n")[0].lstrip("#"))
            break
    else:
        raise Exception("No h1 header found in markdown")

    return title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Generate html page from markdown"""
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path} as template..."
    )
    # read markdown and html files and save to variables
    from_markdown, html_template = "", ""
    with open(from_path, "r") as f:
        from_markdown = f.read()
    with open(template_path, "r") as f:
        html_template = f.read()
    # generate html from markdown
    content = markdown_to_html_node(from_markdown)
    title = extract_title(from_markdown)
    # replace title and content with content
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", content.to_html())
    # write newly generated html into destination file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html_template)


if __name__ == "__main__":
    main()
