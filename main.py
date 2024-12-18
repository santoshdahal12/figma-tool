import json
import csv
import time

import urllib3
import requests

FIGMA_API_URL = "https://api.figma.com/v1/files"
FIGMA_TOKEN = "<>"
FILE_ID = "<>"

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
    response = requests.get(f"{FIGMA_API_URL}/{file_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch Figma file. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None


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


if __name__ == '__main__':

    start_time = time.time()

    # Fetch the Figma file
    figma_data = fetch_figma_file(FILE_ID, FIGMA_TOKEN)

    if figma_data:
        # # Load the JSON file from json
        with open("figma.json", "w") as file:
            json.dump(figma_data, file, indent=4)
        #
        # # Start traversal from the document root
        # components = find_components(figma_data.get("document"))
        #
        # # Output the components found
        # print(f"Found {len(components)} components:")
        # # Save the components to a new JSON file
        # with open("components_list2.json", "w", encoding="utf-8") as output_file:
        #     json.dump(components, output_file, indent=4, ensure_ascii=False)
        #
        # # Save the components to a CSV file
        # csv_file_name = "components_list2.csv"
        # with open(csv_file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=["name", "id"])
        #     writer.writeheader()
        #     writer.writerows(components)

    # total execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
