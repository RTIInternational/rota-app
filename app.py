from functools import partial
from pathlib import Path

from pandas import DataFrame, read_csv, read_excel
import streamlit as st
from more_itertools import ichunked
from stqdm import stqdm

from onnx_model_utils import predict, predict_bulk, max_pred_bulk, RELEASE_TAG
from download import download_link

PRED_BATCH_SIZE = 8


st.set_page_config(page_title="ROTA", initial_sidebar_state="collapsed")

st.markdown(Path("readme.md").read_text())

with st.beta_expander("View Model Details"):
    st.markdown(Path("model_details.md").read_text())
    st.markdown(f"Model Version: `{RELEASE_TAG}`")

st.markdown("## ✏️ Single Coder Demo")
input_text = st.text_input(
    "Input Offense",
    value="FRAUDULENT USE OF A CREDIT CARD OR DEBT CARD >= $25,000",
)

predictions = predict(input_text)

st.markdown("Predictions")
labels = ["Charge Category"]
st.dataframe(
    DataFrame(predictions[0])
    .assign(
        confidence=lambda d: d["score"].apply(lambda d: round(d * 100, 0)).astype(int)
    )
    .drop("score", axis="columns")
)

st.markdown("---")
st.markdown("## 📑 Bulk Coder")
st.warning(
    "⚠️ *Note:* Your input data will be deduplicated"
    " on the selected column to reduce computation requirements."
    " You will need to re-join the results on your offense text column."
)
st.markdown("1️⃣ **Upload File**")
uploaded_file = st.file_uploader("Bulk Upload", type=["xlsx", "csv"])

file_readers = {"csv": read_csv, "xlsx": partial(read_excel, engine="openpyxl")}

if uploaded_file is not None:
    for filetype, reader in file_readers.items():
        if uploaded_file.name.endswith(filetype):
            df = reader(uploaded_file)
            file_name = uploaded_file.name
    del uploaded_file
    st.write("2️⃣ **Select Column of Offense Descriptions**")
    string_columns = list(df.select_dtypes("object").columns)
    longest_column = max(
        [(df[c].str.len().mean(), c) for c in string_columns], key=lambda x: x[0]
    )[1]

    selected_column = st.selectbox(
        "Select Column",
        options=list(string_columns),
        index=string_columns.index(longest_column),
    )
    original_length = len(df)
    df_unique = df.drop_duplicates(subset=[selected_column]).copy()
    del df
    st.markdown(
        f"Uploaded Data Sample `(Deduplicated. N Rows = {len(df_unique)}, Original N = {original_length})`"
    )
    st.dataframe(df_unique.head(20))
    st.write(f"3️⃣ **Predict Using Column: `{selected_column}`**")

    column = df_unique[selected_column].copy()
    del df_unique
    if st.button(f"Compute Predictions"):
        input_texts = (value for _, value in column.items())

        n_batches = (len(column) // PRED_BATCH_SIZE) + 1

        bulk_preds = []
        for batch in stqdm(
            ichunked(input_texts, PRED_BATCH_SIZE),
            total=n_batches,
            desc="Bulk Predict Progress",
        ):
            batch_preds = predict_bulk(batch)
            bulk_preds.extend(batch_preds)

        pred_df = column.to_frame()
        max_preds = max_pred_bulk(bulk_preds)
        pred_df["charge_category_pred"] = [p["label"] for p in max_preds]
        pred_df["charge_category_pred_confidence"] = [
            int(round(p["score"] * 100, 0)) for p in max_preds
        ]
        del column
        del bulk_preds
        del max_preds

        # # TODO: Add all scores

        st.write("**Sample Output**")
        st.dataframe(pred_df.head(100))

        tmp_download_link = download_link(
            pred_df,
            f"{file_name}-ncrp-predictions.csv",
            "⬇️ Download as CSV",
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)
