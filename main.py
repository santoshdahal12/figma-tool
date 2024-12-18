import json
import time
import os

import urllib3
import requests

FIGMA_API_URL = "https://api.figma.com/v1/files"
FIGMA_TOKEN = os.getenv("figma_token")
FILE_ID = os.getenv("figma_file_id")

VDS_IDENTIFIER = "[VDS]"

urllib3.disable_warnings()


def fetch_figma_file(file_id, token):
    """
    Fetch the Figma file JSON using the Figma API.

    Args:
        file_id (str): Figma file ID.
        token (str): Figma personal access token.

    Returns:
        dict: The JSON data of the Figma file.
    """
    headers = {"X-FIGMA-TOKEN": token}
    response = requests.get(f"{FIGMA_API_URL}/{file_id}/components", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch Figma file. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None


# not used right now , but good for nested component search
def find_components(node, components=[]):
    """
    Recursively traverse the Figma JSON structure to find all components.

    Args:
        node (dict): Current node in the JSON tree.
        components (list): List to collect component names or details.

    Returns:
        list: A list of components found in the file.
    """
    if node.get("type"):
        # Append component details to the list
        components.append({
            "name": node.get("name"),
            "id": node.get("id")
        })

    # Recursively traverse child nodes if they exist
    for child in node.get("children", []):
        find_components(child, components)

    return components


def filter_vds_components(components):
    """
        Filters components where any 'name' key value starts with '[VDS]' in the top-level,
        'containing_frame', or 'containingStateGroup'.
        """
    filtered = []
    for component in components:
        if (
                component.get("name", "").startswith(VDS_IDENTIFIER) or
                component.get("containing_frame", {}).get("name", "").startswith(VDS_IDENTIFIER) or
                component.get("containing_frame", {}).get("containingStateGroup", {}).get("name", "").startswith(
                    VDS_IDENTIFIER)
        ):
            filtered.append(component)
    return filtered


if __name__ == '__main__':

    start_time = time.time()

    # Fetch the Figma file
    figma_data = fetch_figma_file(FILE_ID, FIGMA_TOKEN)

    if figma_data and figma_data.get("meta"):
        vds_components = filter_vds_components(figma_data["meta"]["components"])
        with open("vds-components.json", "w") as file:
            json.dump(vds_components, file, indent=4)

    # total execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
