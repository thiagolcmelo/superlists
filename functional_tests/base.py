#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import unittest

# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        staging_server_url = os.environ.get("STAGING_SERVER")
        if staging_server_url:
            cls.server_url = 'http://' + staging_server_url
            cls.live_server_url = ""
            return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def enter_item_and_submit(self, item):
        input_elem = self.get_item_input_box()
        input_elem.send_keys(item)
        input_elem.send_keys(Keys.ENTER)
        time.sleep(1)
