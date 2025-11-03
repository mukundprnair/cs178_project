import functions

URL = "https://www.polisci.uci.edu/people/faculty.php"
# Change this to False if you want the full names of professors
LAST_NAMES = True

soup = functions.get_soup(URL)
emails = []
names = []

faculty_info = soup.find_all("div", class_="faculty-info")
permalink_tags = [div.find('h4') for div in faculty_info]
for tag in permalink_tags:
    anchor_tag = tag.find('a')
    if anchor_tag:
        names.append(anchor_tag.text)
    else:
        names.append(tag.text)

postmeta_tags = [div.find('ul') for div in faculty_info]
for tag in postmeta_tags:
    anchor_tag = tag.find('a')
    if '@' in anchor_tag.text:
        emails.append(anchor_tag.text)


assert len(postmeta_tags) == len(emails)
assert len(permalink_tags) == len(names)

functions.write(emails, names, 'uciPoliSci', LAST_NAMES)

