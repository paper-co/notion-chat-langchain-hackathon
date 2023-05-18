import os
import time
import os
import requests
from pprint import pprint
import json
from dotenv import load_dotenv
load_dotenv('../.env')


NOTION_SECRET = os.getenv('NOTION_SECRET')
headers = {
    "Notion-Version": "2022-06-28",
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Content-Type": "application/json",
}

def get_page_from_api(page_id, folder_path=""):
    URL_PAGE = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(URL_PAGE, headers=headers)

    if response.status_code == 200:
        with open(f'page_data_{page_id}.json', 'w') as f:
            f.write(response.text)

        # TODO: extract propoerties from page
        page = json.loads(response.text)
        page_title = ""
        for key, prop in page['properties'].items():
            if prop['type'] == 'title':
                page_title = prop['title'][0]['plain_text']

        page_foler_name = page_title.replace(" ", "_")
        if folder_path != "":
            page_foler_name = os.path.join(folder_path, page_foler_name)
        print(f"Creating foler {page_foler_name} for page {page_title} with page id {page_id}...")
        os.mkdir(page_foler_name)

        # Extract content from page (blocks):
        page_data = get_block_data_from_api(page_id)

        # Create a file within the subfolder
        file_path = os.path.join(page_foler_name, f"page_data_{page_id}.txt")
        with open(file_path, "w") as file:
            file.write(page_data)

    else:
        print(f"Error: {response.text}")


def get_block_data_from_api(block_id, debugging_data=False, level=0):
    URL_PAGE = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(URL_PAGE, headers=headers)

    if response.status_code == 200:
        if debugging_data:
            with open(f'block_data_{block_id}.json', 'w') as f:
                f.write(response.text)
        # load response into a json object
        block_children = json.loads(response.text)['results']
        # TODO: blocks properties to check: has_children, archived, type
        block_text = ""
        for child in block_children:
            print(f"{'-'*level}Processing child block {child['id']}...") if debugging_data else None
            child_type = child['type']
            content = child[child_type]
            if child_type == "child_page":
                block_text += f"{content['title']}\n"
                # TODO: call get_page_from_api and append to the current sub-pages of the block which appends to their parents subpages, till the next page up
                continue
            if child_type == "child_database":
                # TODO: call get_page_from_api and append to the current sub-pages of the block which appends to their parents subpages, till the next page up
                block_text += f"{content['title']}\n"
                continue
            if len(content) > 0:
                #print(f"CONTENT: {content}")
                rich_text = content['rich_text']
                #print(rich_text)
                plain_texts = [text['plain_text'] for text in rich_text]
                #print(plain_texts)
                plain_text = " ".join(plain_texts)
                block_text += f"{plain_text}\n"
            if child['has_children']:
                grand_children_text = get_block_data_from_api(child['id'], debugging_data, level+1)
                # sleep for 0.33 seconds to avoid exceeding the API rate limit (3 requests per second)
                time.sleep(0.33)
                block_text += f"{grand_children_text}\n"
        return block_text

    else:
        print(f"Error: {response.text}")




if __name__ == '__main__':
    page_id = '8983f31939254c76af1858c0e141dc0f' # Internal Customization Tool
    get_page_from_api(page_id)
    #block_id = "8983f319-3925-4c76-af18-58c0e141dc0f" # page
    #block_id = "927ad88d-2bfa-4936-810f-916b000dc9d2" # colum_list
    #block_id = "a50f3fde-09d2-453c-9569-be295663fdc3" # column
    #block_id = "93a99699-ef68-47d1-ba7b-8499197e2a95" # column_list
    #block_id = "3fa87dd3-5849-4073-867d-4dfdf93f2c32" # column (this is the one that has children with their data)

    #block_id = "56ec988d-af86-462f-88e6-7e49618aa3ce" # callout --> this one I can get data from: callout/rich_text[0]/plain_text
    #block_id = "f2ae5d8a-5de4-4967-981d-c276cfea6616" # callout  "       "       "         "
    #block_id = "31e464cc-c3c9-42ea-a300-defc54926400" # paragraph  "       "       "         "  : paragraph/rich_text[0]/plain_text


    #block_data = get_block_data_from_api(block_id, debugging_data=True)
    #print(block_data)


