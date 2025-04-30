import streamlit as st
import pandas as pd
import os, openai, sqlparse

from utils import messages

openai.api_key = "OPENAI_API_KEY"


def write_user_content(src, dest, transf, additional):
    if len(transf) == 0:
        transf = "No transformation"
    prompt_item = f"Write a SQL query for transforming {src} into {dest}, and apply the following transformation:\n{transf}. {additional}"

    return prompt_item


def return_assistant_output(user_content):
    messages.append({"role": "user", "content": user_content})
    answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return answer["choices"][0]["message"]["content"]


def save_data(data: pd.DataFrame, filename: str = "data_cache"):
    if not os.path.exists("cache"):
        os.mkdir("cache")

    try:
        data.to_csv(f"cache/{filename}.csv", index=False)
    except Exception as error:
        print(f"save_data operation failed due to error: {error}")


def add_data(src, dest, transf, addi, filename):
    try:
        data = pd.read_csv(f"cache/{filename}.csv")
    except:
        data = pd.DataFrame(
            {
                "source_column": [],
                "destination_column": [],
                "transformation": [],
                "additional_remarks": [],
                "suggestion": [],
            }
        )
    temp_df = pd.DataFrame(
        {
            "source_column": [src],
            "destination_column": [dest],
            "transformation": [transf],
            "additional_remarks": [addi],
            "suggestion": [""],
        }
    )
    data = pd.concat([data, temp_df]).reset_index(drop=True)
    save_data(data=data, filename=filename)
    return data


def make_suggestions_on_all(data: pd.DataFrame, filename: str):
    new_data = data.copy()
    new_data.fillna("", inplace=True)

    for i, row in new_data.iterrows():
        if row["suggestion"] == "":
            prompt = write_user_content(
                src=row["source_column"],
                dest=row["destination_column"],
                transf=row["transformation"],
                additional=row["additional_remarks"],
            )
            assistant_output = return_assistant_output(prompt)
            assistant_output = sqlparse.format(assistant_output, reindent=True)
            new_data.loc[i, "suggestion"] = assistant_output

        else:
            continue

    if not new_data.equals(data):
        save_data(data=new_data, filename=filename)

    return new_data


def sql_query_output(data):
    contents_list = []

    for suggestion in data.suggestion:
        contents_list.append(suggestion)

    contents_string = ", ".join(contents_list)
    sql_query = f"select {contents_string} from your_table;"

    try:
        sql_query = sqlparse.format(sql_query, reindent=True)
    except:
        pass

    return sql_query


def run_query_bridge():
    # Sidebar
    with st.sidebar:
        add_radio = st.radio("Navigator", ("Home", "Playground"))

    # Home
    st.title("QueryBridge")
    st.subheader("Your SQL writing wingman!")
    st.write(
        """***QueryBridge*** takes in human-readable prompts and generates SQL transformations, helping **Innovaccer**'s data-ingestion teams systematically build their SQL queries and write them faster!
        \nPowered by ***OpenAI's*** `GPT-3.5-turbo` language model."""
    )

    if add_radio == "Home":
        filename = "data_cache_home"
        # empty cache if exists
        try:
            os.remove(f"cache/{filename}.csv")
        except:
            pass

        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            cols = dataframe.columns

            if set(cols) == set(
                [
                    "source_column",
                    "destination_column",
                    "transformation",
                    "additional_remarks",
                ]
            ):
                st.write("Data preview -")
                st.write(dataframe)
                dataframe["suggestion"] = ""

                if st.button("Generate SQL query"):
                    try:
                        dataframe_cache = pd.read_csv(f"cache/{filename}.csv")

                    except:
                        with st.spinner(
                            "Please wait while QueryBridge builds your query..."
                        ):
                            dataframe_cache = make_suggestions_on_all(
                                dataframe, filename
                            )

                    sql_query = sql_query_output(dataframe_cache)
                    st.code(sql_query)
                    st.download_button(
                        label="Download SQL query",
                        data=sql_query,
                        file_name="data.sql",
                        mime="text/sql",
                    )

            else:
                st.error("Unable to proceed. Please check if column names are correct")

    elif add_radio == "Playground":
        st.subheader(add_radio)
        filename = "data_cache_playground"

        # FORM
        with st.form(key="my_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                source_column = st.text_input(
                    "Enter source column",
                    help="The name of the column in the source-table.",
                    placeholder="Example: ADMTG_DGNS_CD",
                )

            with col2:
                destination_column = st.text_input(
                    "Enter destination column",
                    help="The name of the column in the Innovaccer's destination table",
                    placeholder="Example: ad",
                )

            transformation = st.text_area(
                "Enter the transformation",
                help="Human readable context for transformation from source-column(s) to destination-column (in L2 tables).",
                placeholder="Example: Return an empty string if value is either '~' or 'blank'",
            )
            expander = st.expander("Additional Instructions (optional)")
            additional_instructions = expander.text_area(
                "Enter additional instructions for transformation",
                help='For example - `If not blank, coalesce with " "`',
                placeholder="coalesce with '' to remove any NULL value",
            )

            submitted = st.form_submit_button("Submit")

        if submitted:
            if (len(source_column) == 0) or (len(destination_column) == 0):
                st.error("Please enter Source and Destination column fields.")

            else:
                data = add_data(
                    source_column,
                    destination_column,
                    transformation,
                    additional_instructions,
                    filename=filename,
                )

        try:
            data = pd.read_csv(f"cache/{filename}.csv")
            new_data = make_suggestions_on_all(data=data, filename=filename)

            if not new_data.equals(data):
                save_data(data=new_data, filename=filename)

            if st.button("Delete History"):
                os.remove(f"cache/{filename}.csv")
                st.info("History deleted")
            else:
                st.write(new_data)
                sql_query = sql_query_output(new_data)
                st.code(sql_query)
                st.download_button(
                    label="Download SQL query",
                    data=sql_query,
                    file_name="data.sql",
                    mime="text/sql",
                )

        except:
            pass


if __name__ == "__main__":
    run_query_bridge()
