import os
import openai
import re
from collections import OrderedDict
import requests, PyPDF2
from io import BytesIO
  
openai.api_key = os.environ["OPENAI_API_KEY"]

# creating a pdf file object 
# pdfFileObj = open('iOS14_iPadOS14.pdf', 'rb') 

url = input("Enter the pdf url: ") 


# url = 'https://www.blv.admin.ch/dam/blv/de/dokumente/lebensmittel-und-ernaehrung/publikationen-forschung/jahresbericht-2017-2019-oew-rr-rasff.pdf.download.pdf/Jahresbericht_2017-2019_DE.pdf'
response = requests.get(url)
my_raw_data = response.content

# creating a pdf reader object 

# for pageNum in range(pdfFile.getNumPages()):
#     currentPage = pdfFile.getPage(pageNum).extractText()
#     print(currentPage)

# printing number of pages in pdf file 
# print(pdfReader.numPages) 
  
# creating a page object 
# pageObj = pdfReader.getPage(0) 
  
# extracting text from page 
# pageText = pageObj.extractText()
# final_text = "If you don't like the terms, don't use the software. Apple reserves all rights not expressly granted to you.\n\n- You are not buying the software, you are buying a license to use it.\n\n- You are not buying the hardware, you are buying a license to use it.\n\n- You are not buying the phone, you are buying a license to use it.\n\n- The license agreement is for the software that comes with your device. If you buy a new device, you get a new license. If you restore your device from a backup, you get a new license. If you update your device, you get a new license. If you buy a used device, Apple is not responsible for any damage you do to your device. You are responsible for any damage you do to your device.\n\n\nThis is a legal document and is not intended to be a substitute for professional legal advice. You agree to these terms by using your device.\n\nClick to expand... If you don't like the EULA, don't buy the product.\n\nClick to expand... You agree to the license by using the device. You agree to the terms of the license when you install the update. You agree to the terms of the license when you set up the device.\n\nClick to expand... You agree to this license when you use your iPhone, iPad, or iPod touch. If you don't agree, you can return it within 14 days for a refund.\n\n\n2. Additional Terms.\n\n\n(a) You shall be authorized to use the Apple Software only on an iOS or You agree to Apple's license terms when you use your iPhone, iPad, or iPod touch. If you have a problem with your device, you can return it. If you have a problem with the software, you can return it. If you have a problem with the software and the device, you can return them both.Amans-MacBook-Pro:GPT3_Experiments amankishore$ python3 tldr_foruser.py  You agree to this license when you use your device.\n\nClick to expand... You agree to this license if you use your iPhone, iPad or iPod touch.\n\n\nAPPLE PAY SUPPLEMENTAL TERMS\n\nTHE APPLE PAY SUPPLEMENTAL TERMS ARE ADDITIONAL TO THE APPLE PAY TERMS OF SALE SET FORTH BELOW, AND ARE You can't use it for anything other than personal use. You agree to this license when you accept the terms of the license on your device. You agree to the terms of this license when you install an update to the iOS. You agree to the terms of this license when you use an app that has a separate license. You agree to the terms of this You agree to this license by using your device. You agree to any updates to this license by using your device.\n\n2. Scope of License\n\n(a) This License allows you to use the Apple Software on any Device that you own or control. (b) You may You agree to this license when you use your iPhone/iPad/iPod touch. Apple owns the software, not you. You only have a license to use it, not ownership.\n\nClick to expand... If you use your iPhone, iPad or iPod touch, you agree to the terms of this license.\n\n\n2. Scope of License(a) The license granted to you for the Apple Software is limited to a non-transferable license to use the Apple Software on an iOS Product that you own You agree to the terms of this license by using your device. If you don't agree, you can return your device within the return period to the Apple Store or authorized distributor where you obtained it for a refund, subject to Apple's return policy.\n\n\niOS and iPadOS Software License Agreement\n\n If you don't agree to the terms, don't use the device. You agree to the terms of the license when you use the software. If you don't agree, you can't use the software.\n\n\n2. What is the license?"
final_text = ""

with BytesIO(my_raw_data) as data:
    read_pdf = PyPDF2.PdfFileReader(data)

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

print(final_text)