import re
import functions

# Base URL parts for ICS People directory with filters applied
BASE_URL = "https://ics.uci.edu/people/"
FILTERS = "?filter%5Bemployee_type%5D%5B0%5D=1097&filter%5Bemployee_type%5D%5B1%5D=1143&filter%5Bemployee_type%5D%5B2%5D=1095"

# Change this to False if you want the full names of professors
LAST_NAMES = True


def url_for_page(page: int) -> str:
    # Page 1 has no /page/1/ segment; subsequent pages do
    if page <= 1:
        return f"{BASE_URL}{FILTERS}"
    return f"{BASE_URL}page/{page}/{FILTERS}"


def scrape_page(page: int):
    url = url_for_page(page)
    soup = functions.get_soup(url)

    # Stop condition: page shows 'Nothing found'
    if soup.find(string=re.compile(r"Nothing\s+Found", re.IGNORECASE)):
        print("found 'nothing found' exiting")
        return [], [], False

    mailto_tags = soup.find_all('a', href=lambda h: isinstance(h, str) and h.startswith('mailto:'))
    print("scraping page")

    has_mailtos = bool(mailto_tags)
    if not has_mailtos:
        return [], [], False

    emails = []
    names = []
    seen = set()

    for a in mailto_tags:
        email_text = a.get_text(strip=True)
        if not email_text or '@' not in email_text:
            continue

        # Find the nearest preceding heading that contains the person's name
        heading = a.find_previous(['h2', 'h3', 'h4'])
        if heading is None:
            print("heading is none, skipping")
            continue
        name_text = heading.get_text(strip=True)

        if not name_text:
            continue
    
        # Collect context between heading and email to filter out unwanted titles
        context_text = ''
        if heading is not None:
            bottom_container = heading.parent.parent.find("div", class_="person__bottom-container")
            if bottom_container:
                job_title = bottom_container.find("span", class_="person__job-title")
                if job_title:
                    context_text = job_title.get_text(strip=True)
                else:
                    print("couldn't find job_title")
                    continue
            else:
                print("couldn't find bottom_container")
                continue
        if not context_text:
            print("did not find context_text")


        # print(type(context_text))
        # Only CS department and professor ranks, skip teaching/lecturer/emeritus
        if any(keyword in context_text for keyword in ['Emeritus', 'Emerita', 'Teaching', 'Lecturer']):
            print("skipping ", context_text)
            continue

        # Deduplicate on email
        if email_text.lower() in seen:
            continue
        seen.add(email_text.lower())

        names.append(name_text)
        emails.append(email_text)

    return names, emails, True


def main():
    all_names = []
    all_emails = []

    page = 1
    while True:
        names, emails, has_more = scrape_page(page)
        if not has_more:
            break
        # extend even if this page produced zero filtered results
        all_names.extend(names)
        all_emails.extend(emails)
        page += 1
    print(all_names, all_emails)

    functions.write(all_emails, all_names, 'uciCS', LAST_NAMES)


if __name__ == '__main__':
    main()
