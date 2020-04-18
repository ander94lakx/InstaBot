from selenium import webdriver
from time import sleep
from getpass import getpass
import urllib.request


class InstaBot:
    def __init__(self, username, pw):
        print("Starting...")
        self.driver = webdriver.Firefox(executable_path="./geckodriver.exe")
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        
        print("Loggin in...")
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Ahora no')]")\
            .click()
        sleep(2)

    def scroll_down_to_bottom(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_pictures(self):
        # Step 1: Take the links for all the images of a user
        print("Getting links for all the images...")
        links = self.get_pictures_links()

        i = 1
        # Get image for every link:
        for link in links:
            print("Image ", i, " of ", len(links))
            self.get_picture(link)
            sleep(10)
            i += 1

    
    def get_pictures_links(self):
        # Go to logged user's profile
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)

        # List with all the images of one user
        links = []

        # Start the scrolling process in order to star getting links
        # (DOM only contains the current loaded set of tiles, removint the ones that are not being showed at the moment)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(2)

            # Get the current set of <a></a> tags and save the links in href attribute
            links_elements = self.driver.find_elements_by_xpath('//a[contains(@href,"p/")]')

            for elem in links_elements:
                links.append(elem.get_attribute('href'))

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # The process sometimes saves duplicate values because of "lazy loading tiles" mecanism,
        # so it is neccesary to delete duplicates
        links = list(set(links))
        return links


    def get_picture(self, link):
        self.driver.get(link)
        sleep(2)
        try:
            # Definitively this is not the best way to do this idea
            img_element = self.driver.find_element_by_xpath('//img[contains(@class,"FFVAD")]')
            url = img_element.get_attribute('src')
            time_element = self.driver.find_elements_by_tag_name('time')
            timestamp = time_element[0].get_attribute('datetime')
            if url is not None and timestamp is not None:
                timestamp = timestamp.replace(':', '-')
                timestamp = timestamp.replace('.', '-')
                print(url)
                urllib.request.urlretrieve(url, timestamp + '.jpg')
        except:
            pass


print("Insert your Instagram's username: ")
username = input()
print("Insert your password: ")
password = getpass()
my_bot = InstaBot(username, password)
my_bot.get_pictures()