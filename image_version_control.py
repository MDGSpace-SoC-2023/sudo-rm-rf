# image_version_control.py
import os
from PIL import Image
import click
import networkx as nx
import numpy as np
from skimage.metrics import structural_similarity as ssim

class ImageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.parent_v=None

    def add_parent(self,image_path):
        if self.parent_v is None:
            self.graph.add_node(
                1,
                image_path=image_path,
                version_number=1,

            )
        else:
            raise Exception("Parent version already exist")
            

    def add_version(self, parent_version, image_path):
        version_id = len(self.graph.nodes) + 1
        self.graph.add_node(
            version_id,
            image_path=image_path,
            version_number=version_id,
            parent_version=parent_version
        )

        if parent_version is not None:
            self.graph.add_edge(parent_version, version_id)

    def visualize_graph(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')

def image_changed(image_path1, image_path2):
    image1 = np.array(Image.open(image_path1))
    image2 = np.array(Image.open(image_path2))

    if image1.shape != image2.shape:
        return True

    return not np.array_equal(image1, image2)

image_graph = ImageGraph()

@click.group()
def cli():
    pass


@cli.command()
@click.option("--image-path", type=click.Path(exists=True), help="Path to the image file")
def parentadd(image_path):
    if image_path is None or not os.path.isfile(image_path):
        click.echo("Error: Invalid image path.")
        return
    image_graph.add_parent(image_path)
    click.echo(f"Node created with parent version XX and image path: {image_path}")


@cli.command()
@click.argument("parent_version", default=None)
@click.option("--image-path", type=click.Path(exists=True), help="Path to the image file")
def create(parent_version, image_path):
    if image_path is None or not os.path.isfile(image_path):
        click.echo("Error: Invalid image path.")
        return

    image_graph.add_version(parent_version, image_path)
    click.echo(f"Node created with parent version {parent_version} and image path: {image_path}")

@cli.command()
@click.argument("version")
@click.option("--image-path", type=click.Path(exists=True), help="Path to the image file")
def commit(version, image_path):
    if version not in image_graph.graph.nodes:
        click.echo(f"Error: Version {version} does not exist.")
        return

    parent_version = max(image_graph.graph.predecessors(version), default=None)

    if parent_version is not None:
        if image_path is None or not os.path.isfile(image_path):
            click.echo("Error: Invalid image path.")
            return

        if image_changed(image_graph.graph.nodes[parent_version]['image_path'], image_path):
            image_graph.add_version(parent_version, image_path)
            click.echo(f"Committed new version {version} with image: {image_path}")
        else:
            click.echo("No changes detected. Skipping commit.")
    else:
        click.echo("Error: Cannot commit the initial version.")

@cli.command()
def visualize():
    image_graph.visualize_graph()
    click.echo("Visualized the graph (close the window to exit).")

if __name__ == "__main__":
    cli()
