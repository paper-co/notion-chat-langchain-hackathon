# A ChatBot for Your Notion Knowledge Base

Create a simple chatbot for question-answering your Notion knowledge base/docs using Openai, Typescript, LangChain and Pinecone.

[Tutorial video](https://www.youtube.com/watch?v=prbloUGlvLE)

## 📊 Example Data

This repo uses a Notion template of the support docs from [cron](https://cronhq.notion.site/Cron-Calendar-5625be54feac4e13a75b10271b65ddb7) - a next-generation calendar for professionals and teams

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
![Screen Shot 2023-05-17 at 2 22 12 PM](https://github.com/paper-co/notion-chat-langchain-hackathon/assets/25120457/1bd4a8a6-41de-4047-9a5f-f1ca55522bb2)



## Deployment

You can deploy this app to the cloud with [Vercel](https://vercel.com) ([Documentation](https://nextjs.org/docs/deployment)).

## Credit

This repo is inspired by [notion-qa](https://github.com/hwchase17/notion-qa)
