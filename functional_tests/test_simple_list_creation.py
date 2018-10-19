#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's
        # hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # wait for refresh
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_fow_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # the page updates again, and now shows both items on her lists
        time.sleep(1)  # wait for refresh
        self.check_fow_row_in_list_table('1: Buy peacock feathers')
        self.check_fow_row_in_list_table(
            '2: Use peacock feathers to make a fly'
        )

