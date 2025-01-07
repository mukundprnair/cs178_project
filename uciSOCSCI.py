import functions

URL = "https://www.socsci.uci.edu/profiles.php"
# Change this to False if you want the full names of professors
LAST_NAMES = True

soup = functions.get_soup(URL)

faculty_info = soup.find_all('div', class_='faculty-info')
valid_faculty_info =[]
for div in faculty_info:
    first_li = div.find("li").text
    if not ('Lecturer' in first_li or 'Emeritus' in first_li or 'Emerita' in first_li):
        valid_faculty_info.append(div)


print(valid_faculty_info[0])
names = []
emails = []
for fac_div in valid_faculty_info:
    email = fac_div.find("ul", class_='post-meta').find('a')
    name = fac_div.find("h4")
    if email is None:
        continue
    names.append(name.text)
    emails.append(email.text)

functions.write(emails, names, 'uciSOCSCI', LAST_NAMES)
