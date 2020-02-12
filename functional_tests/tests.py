from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):



    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def setUp(self):
        self.browser = webdriver.Firefox() 

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):
        # Edit has heard about a cool new online to-do app. She goes 
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text 
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fiching lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        # Edith wonders wether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that efect
        # self.fail('Finish the test!')
        # She visits that URL -her to-do list is still there
        
        # The page updates again, and now shows both items on her list


        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_al_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now  a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is comming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Francis visits the home page, There is  no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body'.text)
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting thean Edith...
        inputbox = self.browser.find_element_by+id('id_new_item')
        inputbox.send_keys('Buy mik')
        inputbox.send_keys(Key.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        # Francis gets his own unique URLD
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        selfassertNotEqual(francis_list_url, edith_list_url)

        # Again, thereis no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNtoIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfed, they both go back to sleep
         
        



