import json
import bs4

datas = json.load(open("output.json"))

html = {}

for data in datas:
    doc = bs4.BeautifulSoup(data["context"])
    for button in doc.find_all(attrs = {'role': 'button'}):
        button.decompose()
    html[data['event_type']] = str(doc)
    print(doc.text)

open('out.html', 'w').write('\n\n\n\n'.join(o[0] + "\n" + o[1] for o in html.items()))
