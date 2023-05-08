{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMM/VJZS8Fxwkx3HtlBtQXo",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/aby1802/Azure-Stream-Analytics-for-Real-Time-Cab-Service-Monitoring/blob/main/streamlit_app2.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "FNAHDBKnlkgC",
        "outputId": "a0fcb062-5835-4b2b-c8de-50fb6de5e893"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing app.py\n"
          ]
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import pytesseract\n",
        "from pdf2image import convert_from_path\n",
        "import pandas as pd\n",
        "import re\n",
        "\n",
        "# Set Tesseract OCR path\n",
        "pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'\n",
        "\n",
        "# Set Tesseract language\n",
        "pytesseract_lang = 'kan'\n",
        "pytesseract_config = '--psm 6'\n",
        "\n",
        "def extract_data(text):\n",
        "    data = {}\n",
        "    lines = text.split('\\n')\n",
        "    lines = [line for line in lines if line.strip()]\n",
        "    for line in lines:\n",
        "        if re.match(r'^\\w{10}$', line):\n",
        "            data['id'] = line\n",
        "        elif 'ವಯಸ್ಸು :' in line:\n",
        "            data['age_gender'] = line\n",
        "        elif 'ಮನೆಯ ಸಂಖ್ಯೆ:' in line:\n",
        "            data['house_number'] = line\n",
        "        elif 'ಹೆಸರು:' in line:\n",
        "            data['name'] = line\n",
        "        elif 'ತಂದೆಯ ಹೆಸರು:' in line:\n",
        "            data['father_name'] = line\n",
        "    return data\n",
        "\n",
        "def process_pdf(file_path):\n",
        "    data_list = []\n",
        "    pages = convert_from_path(file_path, dpi=300)\n",
        "    for page in pages:\n",
        "        text = pytesseract.image_to_string(page, lang=pytesseract_lang, config=pytesseract_config)\n",
        "        data_list.append(extract_data(text))\n",
        "    return pd.DataFrame(data_list)\n",
        "\n",
        "def main():\n",
        "    st.title(\"PDF Data Extraction\")\n",
        "    st.write(\"Upload a PDF file and extract data from it.\")\n",
        "\n",
        "    # Upload file\n",
        "    uploaded_file = st.file_uploader(\"Choose a PDF file\", type=[\"pdf\"])\n",
        "    if uploaded_file is not None:\n",
        "        # Process PDF file\n",
        "        df = process_pdf(uploaded_file)\n",
        "        \n",
        "        # Display extracted data\n",
        "        st.write(\"Extracted Data:\")\n",
        "        st.dataframe(df)\n",
        "\n",
        "        # Download CSV file\n",
        "        csv_data = df.to_csv(index=False, encoding='utf-8-sig')\n",
        "        st.download_button(\"Download CSV\", data=csv_data, file_name=\"output.csv\")\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    main()\n"
      ]
    }
  ]
}