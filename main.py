from PIL import Image
import io

class Version:
    def __init__(self, version_id, changes, commit_message="", parent=None):
        self.version_id = version_id
        self.changes = changes
        self.commit_message = commit_message
        self.parent = parent
        self.children = []
        self.images = {}

    def add_image(self, image_name, image_data):
        self.images[image_name] = image_data

    def get_image(self, image_name):
        return self.images.get(image_name)

class ImageVersionControlSystem:
    def __init__(self):
        self.versions = {}

    def create_version(self, version_id, changes, commit_message="", image_changes=None):
        if version_id in self.versions:
            print(f"Error: Version {version_id} already exists.")
            return

        parent_version = self.get_latest_version()
        new_version = Version(version_id, changes, commit_message, parent_version)

        if image_changes:
            for image_name, image_data in image_changes.items():
                new_version.add_image(image_name, image_data)

        if parent_version:
            parent_version.add_child(new_version)
9
        self.versions[version_id] = new_version
        print(f"Created version {version_id} with changes: {changes}, Commit Message: {commit_message}")

    def get_latest_version(self):
        if not self.versions:
            return None
        return max(self.versions.values(), key=lambda v: v.version_id)

    def print_version_history(self, version=None, indent=0):
        if version is None:
            version = self.get_latest_version()

        if version:
            print("  " * indent + f"Version {version.version_id}: {version.changes}")
            for child in version.children:
                self.print_version_history(child, indent + 1)

# Example usage with image changes:
image_vc_system = ImageVersionControlSystem()

# Open and read image files
image1 = Image.open("image1.jpg")
image2 = Image.open("image2.jpg")

# Convert images to bytes
image_data1 = io.BytesIO()
image1.save(image_data1, format="JPEG")

image_data2 = io.BytesIO()
image2.save(image_data2, format="JPEG")

# Create versions with image changes
image_vc_system.create_version(1, "Initial commit", "First commit", {"image1.jpg": image_data1.getvalue()})
image_vc_system.create_version(2, "Modify image1", "Fix bug", {"image1.jpg": image_data1.getvalue()})
image_vc_system.create_version(3, "Add image2", "Add feature", {"image2.jpg": image_data2.getvalue()})

# Print the version history
image_vc_system.print_version_history()
