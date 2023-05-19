# Docugami - a ChatBot for Your Notion Knowledge Base
<img src="https://github.com/paper-co/notion-chat-langchain-hackathon/assets/25120457/6729c3d1-e0c6-47ca-9df7-bf13b90f4758" width="75%"></img>


Create a simple chatbot for question-answering your Notion knowledge base/docs using Openai, Typescript, LangChain and Pinecone.

[Tutorial video](https://www.youtube.com/watch?v=prbloUGlvLE)

## 📊 Example Data

Example data can be exported from notion as Markdown/CSV with 'everything including subpages' selected; or you can use the Pinecode Index we've already populated for instructional purposes. Please message Riley or Eduardo for Pinecone API access.

## Development

1. Clone the repo
2. Install packages

```
pnpm install
```

3. Set up your `.env` file

- Copy `.env.example` into `.env`
  Your `.env` file should look like this:

```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX_NAME=
```

- Visit [openai](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) and [pinecone](https://www.pinecone.io/) to retrieve API keys and insert into your `.env` file.


### This step no longer applies as Riley put it in the env file on 5-17-23

4. In the `config` folder, go into `pinecone-index.ts` and replace `PINECONE_INDEX_NAME` with the index name in your pinecone dashboard.

## 🧑 Instructions for ingesting your own dataset

### Your Pinecone index should should be Metric type 'cosine' with the Dimensions of 1536, or it will not work. As follows -
![Screen Shot 2023-05-17 at 11 18 46 AM](https://github.com/paper-co/notion-chat-langchain-hackathon/assets/25120457/9ab09a7c-22fe-4827-a8cc-5ba368efde77)


Export your dataset from Notion. You can do this by clicking on the three dots in the upper right hand corner and then clicking `Export`.

Follow these Notion instructions: [Exporting your content](https://www.notion.so/help/export-your-content)

When exporting, make sure to select the `Markdown & CSV` format option.

Select `Everything`, `include subpages` and `Create folders for subpages.` Then click `Export`

This will produce a `.zip` file in your Downloads folder. Move the `.zip` file into the root of this repository.

Either unzip the folder using 7-Zip (or WinZip) or run the following Unix/Linux command to unzip the zip file (replace the `Export...` with your own file name).

```shell
unzip Export-d3adfe0f-3131-4bf3-8987-a52017fc1bae.zip -d Notion_DB
```

You should see a `Notion_DB` folder in your root folder that contains markdown files and folders of your knowledge base.

## Ingest data

Now we need to `ingest` your docs. In **very** simple terms, ingesting is the process of converting your docs into numbers (embedding) that can be easily stored and analyzed for similarity searches.

```bash
npm run ingest

```

## Running the app

Run your local dev environment `npm run dev`.

Use the search bar to ask a question about your docs.

Simple.


## Screenshots
![Screen Shot 2023-05-18 at 2 02 48 PM](https://github.com/paper-co/notion-chat-langchain-hackathon/assets/25120457/9784e84e-fcf5-47ab-93eb-7e85369eb9ec)

## Tailwind notes for DevOps/non front end folks
Always put images in the public folder located in this repo. You can view the docugami.png code as a reference. You can also always
extend the theme within the [tailwind.config.cjs](https://github.com/paper-co/notion-chat-langchain-hackathon/blob/main/tailwind.config.cjs) to
add more things like a background image, or edit.

If you need to add a css class you can edit [base.css](https://github.com/paper-co/notion-chat-langchain-hackathon/blob/main/styles/base.css)


## Deployment

You can deploy this app to the cloud with [Vercel](https://vercel.com) ([Documentation](https://nextjs.org/docs/deployment)).

## Notion Extraction Module (Python)

This module offers an automated and customizable way to extract data from Notion. It’s written in Python so it can be easily used to schedule and orchestrate periodic data extraction with Airflow, for example, which offers a UI to monitor data extraction status, as well as important mechanisms such as auto-retry, in case the Notion API is not available or we reach some API limit.

#### What has been done so far
The script receives a Notion page ID and extracts all of its content, as well as its sub-pages content, creating a folder hierarchy that represents the pages hierarchy. It also formats the output in Markdown, so the final files are .md files.

#### How to execute it
  - go to folder `notion-data-extraction`
  - create and activate a Python virtual env
  - install the dependencies in the virtual env, from the requirements.txt file
  - edit file notion_extraction.py to add the id of your root Notion page at the end of the file in variable page_id (TODO: receive this as a parameter instead)
  - run python notion_extraction.py from this folder (or from the folder you want the data to be stored, adjusting the path of the python script)

### TODO
  - [ ] Retrieve people’s names from page properties (e.g. Squads’ PM)
  - [ ] Retrieve data and pages from pages’s children databases
  - [ ] Tie in the python script to automatically populate the Markdown data, and trigger typescript to ingest it.
  - [ ] Retrieve only pages which have been edited since the last extraction
  - [ ] Possible pure TS implementation for notion extraction?
  - [ ] Export/ingest all data from Initiatives page

## Credit

This repo is inspired by [notion-qa](https://github.com/hwchase17/notion-qa)
