import os
import openai
import re
from collections import OrderedDict
import requests, PyPDF2
from io import BytesIO
  
openai.api_key = os.environ["OPENAI_API_KEY"]

def getTLDRfromURL():
    # creating a pdf file object 
    url = input("Enter the pdf url: ") 
    response = requests.get(url)
    my_raw_data = response.content

    final_text = ""

    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfFileReader(data)

        # Iterate through pages (max of 15 to save money)
        for page in range(min(read_pdf.getNumPages(), 15)):
            ai_text = read_pdf.getPage(page).extractText()

            response = openai.Completion.create(
                engine="davinci",
                prompt=ai_text + "\n\ntl;dr:",
                temperature=0.3,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            final_text += response["choices"][0]["text"]


    "\n".join(list(OrderedDict.fromkeys(final_text.split("\n"))))
    final_text = final_text.replace('Click to expand... ', '')
    final_text = final_text.replace('\n\n', '\n')
    final_text = re.sub(r'^\\s+|[\\s&&[^\\r\\n]](?=\\s|$)|\\s+\\z', '', final_text)

    return final_text

if __name__ == "main":
    response = getTLDRfromURL()
    print(response)