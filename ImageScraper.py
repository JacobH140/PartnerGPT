# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable


import os
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable


def scrape_images(search_keys, number_of_images=2):
    def worker_thread(search_key):

        image_scraper = GoogleImageScraper(webdriver_path, image_path, search_key, number_of_images, headless,
                                           min_resolution, max_resolution)
        image_urls.append(image_scraper.find_image_urls())
        # image_scraper.save_images(image_urls)

        # Release resources
        del image_scraper

    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'Google-Image-Scraper-master/webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'Google-Image-Scraper-master/photos'))

    # search keys given as array: ["cat","t-shirt","apple","orange","pear","fish"]

    #Parameters
    # number_of_images                   Desired number of images
    headless = True                    # True = No Chrome GUI
    min_resolution = (0, 0)            # Minimum desired image resolution
    max_resolution = (9999, 9999)      # Maximum desired image resolution
    max_missed = 1000                    # Max number of failed images before exit
    number_of_workers = 1              # Number of "workers" used

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    image_urls = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)

    return image_urls
