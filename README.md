# hack-weekends-2023
A language translation tool which will convert the mappings and transformations rules defined in CSV data directly into ready-to-run SQL queries, saving time taken to on-board new-customers, or even convert new payers data into standard data models.

## QueryBridge

#### Your SQL writing wingman!
***QueryBridge*** takes in human-readable prompts and generates SQL transformations, helping **Innovaccer**'s data-ingestion teams systematically build their SQL queries and write them faster!

Powered by ***OpenAI's*** `GPT-3.5-turbo` language model.

## Instructions
Clone this repo - 

```git clone https://https://gitlab.innovaccer.com/aseem.raghav/querybridge.git```

Install dependencies -

`pip install -r requirements.txt`

Run QueryBridge on Streamlit's UI -

`streamlit run query_bridge/streamlit_app.py`

Voila! QueryBridge UI is now set-up on your local.

<video controls width="640" height="360">
  <source src="demo/QueryBridge Demo-1.mp4" type="video/mp4">
  QueryBridge Demo Screen Recording
</video>

To view the Demo video, go [here](https://github.com/A-Raghav/hack-weekends-2023/blob/main/demo/QueryBridge%20Demo-1.mp4)
