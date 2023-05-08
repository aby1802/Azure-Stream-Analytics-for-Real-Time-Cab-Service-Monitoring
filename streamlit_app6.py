{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPGVzJ9oTcTSyryE59V2sxZ",
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
        "<a href=\"https://colab.research.google.com/github/aby1802/Azure-Stream-Analytics-for-Real-Time-Cab-Service-Monitoring/blob/main/streamlit_app6.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 373
        },
        "id": "FNAHDBKnlkgC",
        "outputId": "6fc8b451-5721-471d-c6df-dc1fda521bd7"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-ce7f725d4662>\u001b[0m in \u001b[0;36m<cell line: 1>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpytesseract\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mpdf2image\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mconvert_from_path\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mre\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
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
        "    main()\n",
        "\n",
        "\n"
      ]
    }
  ]
}