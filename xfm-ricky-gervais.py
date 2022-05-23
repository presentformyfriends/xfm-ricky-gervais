#! python3

from pytube import YouTube
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os


def createURL(season, episode):
    url = ("https://www.therickygervaisshow.com/xfm-vault/s"+season+"e"+episode)
    return url


def driverConfig():
    options = Options()
    options.add_argument('-headless') # Set driver to be headless
    driver = webdriver.Firefox(options=options, service_log_path=os.devnull) # Define driver, no logs
    return driver


def getYouTubeLink(driver, url):
    driver.get(url) # Load url
    try:
        src = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='plyr__video-wrapper plyr__video-embed']/iframe"))).get_attribute("src")
        videoID = src[src.find('embed')+6:src.find('?autoplay')].strip() # Scrape video ID
        link = ("https://www.youtube.com/watch?v=" + videoID) # Create link
        return link
    except (NoSuchElementException, TimeoutException):
        print("ERROR getYouTubeLink function")


def downloadVideo(folder, url, link):
    try:
        yt = YouTube(link)
        stream_url = yt.streams.get_highest_resolution()
        stream_url.download(folder)
        print(url + " Download completed!")
    except:
        print("ERROR downloadVideo function")


def download(driver, season, first, last):
    folder =  f"{os.getenv('USERPROFILE')}\\Downloads\\XFM The Ricky Gervais Show\\XFM The Ricky Gervais Show Season {str(int(season))}"
    for e in range(first, last):
        url = createURL(season, str(e).zfill(2))
        link = getYouTubeLink(driver, url)
        downloadVideo(folder, url, link)


def rename(path, filename, newname):
    renamed = 0
    untouched = 0
    print("\nRunning rename function...\n")
    if os.path.isdir(path):
        globpath = path.glob("*")
        for filepath in globpath:
            if os.path.isfile(filepath) and os.path.basename(filepath) == filename:
                basedir = os.path.dirname(filepath)
                new_filepath = os.path.join(basedir + "\\" + newname)
                try:
                    os.rename(filepath, new_filepath)
                    renamed += 1
                    print("\'" + filename + "\' \nRENAMED TO:\n\'" + newname + "\'\n")
                except FileExistsError:
                    print("ERROR rename function: File already exists\n")
            else:
                untouched += 1
                continue
        if renamed == 1:
            print(f"{renamed} file successfully renamed!\n")
        elif renamed > 1:
            print(f"{renamed} files successfully renamed!\n")
        else:
            print("ERROR rename function: Nothing to rename\n")
##        print("Files renamed: ", renamed)
##        print("Files not renamed: ", untouched)
    else:
        print("ERROR rename function: Folder path invalid\n")


def renameFiles():
    path = Path(f"{os.getenv('USERPROFILE')}\\Downloads\\XFM The Ricky Gervais Show\\XFM The Ricky Gervais Show Season 2")
    # Rename S2E02 file
    filename = "Ricky Gervais XFM Show - Series 2 Episode 2.mp4"
    newname = "XFM The Ricky Gervais Show Series 2 Episode 2.mp4"
    rename(path, filename, newname)
    # Rename S2E18 file
    filename = "XFM The Ricky Gervais Xmas Show Series 2 Episode 18 - A Diddy Man Prostitute.mp4"
    newname = "XFM The Ricky Gervais Show Series 2 Episode 18 - A Diddy Man Prostitute (Xmas Show).mp4"
    rename(path, filename, newname)



### Configure driver
driver = driverConfig()

### SEASON 1 (23 episodes) ###
download(driver, "01", 1, 24)

### SEASON 2 (51 episodes) ###
download(driver, "02", 1, 52)
renameFiles() # Rename S2E02 and S2E18 to keep them in sequential order

### SEASON 3 (12 episodes) ###
download(driver, "03", 1, 13)

### SEASON 4 (6 episodes) ###
download(driver, "04", 1, 7)

# Quit driver
driver.quit()
