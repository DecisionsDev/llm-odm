import camelot
from langchain.document_loaders import PyPDFLoader
import warnings
import os
import requests

def camelot_parse(pdf: str):
    pdf_loader = PyPDFLoader(pdf)
    document=pdf_loader.load()
    print(document)
    warnings.simplefilter('ignore')
    for page in range(1,len(document)+1):
        tables = camelot.read_pdf(pdf,flavor='stream',pages=f'{page}')
        if tables.n > 0:
            print(str(f'page.{page}.csv'))
            i=0
            for subtable in tables:
                print(subtable.parsing_report)
                print(len(subtable.df.columns))
                if(len(subtable.df.columns)>1) and subtable.parsing_report['accuracy'] > 90.0:
                    print(str(f'Generate page.{page}-{i}.csv'))
                    subtable.to_csv(f'{datadir}/page.{page}-{i}.csv')
                    i=i+1     

pdffile = 'docs/ABSF-en.pdf'
datadir="data"
# Download the file if it's does not exist
if(not os.path.exists(pdffile)):
    # Download the file
    url = 'https://www.chase.com/content/dam/chase-ux/documents/personal/checking/ABSF-en.pdf'
    os.mkdir('docs')
    with open(pdffile, 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)
# Create datadir
if(not os.path.exists(datadir)):
    os.mkdir(datadir)
    print("% s created successfully" % datadir)
camelot_parse(pdffile)

    