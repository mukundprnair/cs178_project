import functions

URL = "https://merage.uci.edu/research-faculty/faculty-directory/index.html"
# Change this to False if you want the full names of professors
LAST_NAMES = True

soup = functions.get_soup(URL)
emails = []
names = []

deptRows = soup.find_all('tr', class_='deptRow')
print(type(deptRows[0].children))
for row in deptRows:
    children = row.find_all('td', recursive=False)
    # each children element is a <td>
    if (len(children) <= 2 or
            'teaching' in children[0].text or
            'emerita' in children[0].text
            or 'emeritus' in children[0].text):
        continue
    email = children[-1].find('a', recursive=True).get('href').split(':')[1].strip()
    if email == '':
        continue
    names.append(children[0].find('a', recursive=True).text)
    emails.append(children[-1].find('a', recursive=True).get('href').split(':')[1].strip())

functions.write(emails, names, 'uciBusiness', LAST_NAMES)
