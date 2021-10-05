from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import csv



URL = 'https://stackoverflow.com/questions'
WEBDRIVER = 'driver/chromedriver'
OPTIONS = Options()
OPTIONS.add_argument('--headless')
DRIVER = Chrome(WEBDRIVER, options=OPTIONS)

#CSV writer
csv_file = open('unanswered_list.csv', 'w')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()


#Selenium scrapper
def get_q(pages, tag):
    URL = 'https://stackoverflow.com/questions'
    display_dict = {}
    while_counter = 1
    while while_counter < int(pages):
        DRIVER.get(URL)
        print(DRIVER)
        questions = DRIVER.find_elements_by_class_name("question-summary")
        for question in questions:
            try:
                status = question.find_element_by_class_name("unanswered")
            except:
                status = None
            try:
                tags = question.find_element_by_link_text(f'{tag}')
            except:
                tags = None
            if status and tags:
                q_text = question.find_element_by_class_name('question-hyperlink').text
                link = question.find_element_by_class_name('question-hyperlink').get_attribute('href')
                dictwriter.writerow({'question': q_text, 'link': link})
                display_dict[q_text] = link
        while_counter += 1
        URL = DRIVER.find_element_by_link_text('Next').get_attribute('href')
    return display_dict