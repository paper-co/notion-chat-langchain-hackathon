import os
import time
import shutil
import requests
import json
from dotenv import load_dotenv
load_dotenv('../.env')


NOTION_SECRET = os.getenv('NOTION_SECRET')
headers = {
    "Notion-Version": "2022-06-28",
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Content-Type": "application/json",
}

def get_page_from_api(page_id, folder_path="", debugging_data=False):
    URL_PAGE = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(URL_PAGE, headers=headers)

    if response.status_code == 200:

        # TODO: extract propoerties from page
        page = json.loads(response.text)
        page_title = ""
        for key, prop in page['properties'].items():
            if prop['type'] == 'title':
                page_title = prop['title'][0]['plain_text']

        page_folder_name = page_title.replace(" ", "_")
        if folder_path != "":
            page_folder_name = os.path.join(folder_path, page_folder_name)
        print(f"Creating folder {page_folder_name} for page {page_title} with page id {page_id}...")

        if os.path.exists(page_folder_name):
            shutil.rmtree(page_folder_name) # Remove existing folder and its contents
        os.mkdir(page_folder_name)

        raw_data_path = ""
        if debugging_data:
            raw_data_path = os.path.join(page_folder_name, "raw")
            if os.path.exists(raw_data_path):
                shutil.rmtree(raw_data_path) # Remove existing folder and its contents
            print(f"Creating folder {raw_data_path}")
            os.mkdir(raw_data_path)

            with open(os.path.join(raw_data_path, f"page_data_{page_id}.json"), 'w') as f:
                f.write(response.text)

        page_data = "# " + page_title + "\n\n"
        for property_label, pg_property in page['properties'].items():
            propery_text = get_page_property(property_label, pg_property)
            if propery_text is not None:
                page_data += f"{propery_text}\n"
        # Extract content from page (blocks):
        page_data += get_block_data_from_api(page_id, 'page', debugging_data=debugging_data, folder_path=page_folder_name)

        # Create a file within the subfolder
        file_path = os.path.join(page_folder_name, f"page_text_{page_id}.md")
        with open(file_path, "w") as file:
            file.write(page_data)

    else:
        print(f"Error: {response.text}")

def get_page_property(property_label, pg_property):

    if pg_property['type'] == "rich_text":
        texts = [text['plain_text'] for text in pg_property['rich_text']]
        texts = '\n'.join(texts)
        return f'### {property_label}:\n{texts}\n'

    # TODO: add other types of properties


def get_block_data_from_api(block_id, type, debugging_data=False, level=0, folder_path=""):
    URL_BLOCK = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(URL_BLOCK, headers=headers)

    if response.status_code == 200:
        block_children = json.loads(response.text)['results']

        if debugging_data:
            raw_file_path = os.path.join(folder_path, "raw", f"block_{type}_{block_id}.json")
            with open(raw_file_path, 'w') as f:
                f.write(response.text)

        # TODO: blocks properties to check: has_children, archived, type
        block_text = ""
        previous_child_type = "" # useful for table formatting
        for child in block_children:
            print(f"{'- '*level}Processing child block {child['id']}...") if debugging_data else None
            child_type = child['type']
            content = child[child_type]
            if child_type == "child_page":
                block_text += f"{content['title']}\n"
                # TODO: call get_page_from_api and append to the current sub-pages of the block which appends to their parents subpages, till the next page up
                get_page_from_api(child['id'], folder_path=folder_path, debugging_data=debugging_data)
                previous_child_type = child_type
                continue
            if child_type == "child_database":
                # TODO: call get_page_from_api and append to the current sub-pages of the block which appends to their parents subpages, till the next page up
                block_text += f"{content['title']}\n"
                previous_child_type = child_type
                continue
            if child_type == "table_row":
                cells = content['cells']
                cells_texts = []
                for cell in cells:
                    cell_text = [text['plain_text'] for text in cell]
                    cells_texts.append(" ".join(cell_text))
                block_text += f"| {' | '.join(cells_texts)} |\n"
                if previous_child_type != "table_row":
                    block_text += "| --- " * len(cells) + "|\n"
                previous_child_type = child_type
                continue

            rich_text = content.get('rich_text', None)
            if rich_text is not None:
                plain_texts = [text['plain_text'] for text in rich_text]
                #print(plain_texts)
                plain_text = " ".join(plain_texts)
                block_text += f"{plain_text}\n"
            if child['has_children']:
                grand_children_text = get_block_data_from_api(child['id'], child['type'], debugging_data, level=level+1, folder_path=folder_path)
                # sleep for 0.33 seconds to avoid exceeding the API rate limit (3 requests per second)
                time.sleep(0.33)
                block_text += f"{grand_children_text}\n"
            previous_child_type = child_type
        return block_text

    else:
        print(f"Error: {response.text}")




if __name__ == '__main__':
    #page_id = '8983f31939254c76af1858c0e141dc0f' # Internal Customization Tool
    page_id = '6877998bca2c4a17acc9868e66704e0e' # Acquire Squad
    get_page_from_api(page_id, debugging_data=True)
    #block_id = "8983f319-3925-4c76-af18-58c0e141dc0f" # page
    #block_id = "927ad88d-2bfa-4936-810f-916b000dc9d2" # colum_list
    #block_id = "a50f3fde-09d2-453c-9569-be295663fdc3" # column
    #block_id = "93a99699-ef68-47d1-ba7b-8499197e2a95" # column_list
    #block_id = "3fa87dd3-5849-4073-867d-4dfdf93f2c32" # column (this is the one that has children with their data)

    #block_id = "56ec988d-af86-462f-88e6-7e49618aa3ce" # callout --> this one I can get data from: callout/rich_text[0]/plain_text
    #block_id = "f2ae5d8a-5de4-4967-981d-c276cfea6616" # callout  "       "       "         "
    #block_id = "31e464cc-c3c9-42ea-a300-defc54926400" # paragraph  "       "       "         "  : paragraph/rich_text[0]/plain_text

    block_id = "fd3b96f2-4e73-4464-ab6e-1ea79b894586"

    #block_data = get_block_data_from_api(block_id, "table", debugging_data=True)
    #print(block_data)


