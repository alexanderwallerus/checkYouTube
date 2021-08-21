#check youtube channels for new videos
##############################################################################################
from selenium import webdriver
from selenium.common import exceptions as seleExceptions
import os

options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1000, 1080)

#automatically open channels with new videos in firefox
openURL = True
firefoxPath = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

def getVidFromChannel(channelUrl):
    driver.get(channelUrl)
    
    #check if I have to agree to a cookie banner
    ariaLabel = 'Agree to the use of cookies and other data for the purposes described'
    xPath = f'//button[@aria-label="{ariaLabel}"]'
    try:
        agree = driver.find_element_by_xpath(xPath)
        print('cookie banner in the way, clicking it')
        agree.click()
    except seleExceptions.NoSuchElementException:
        #print('no cookie banner in the way')
        pass
    
    firstVidxPath = '//div[@class="style-scope ytd-grid-video-renderer"]'
    firstVidDiv = driver.find_element_by_xpath(firstVidxPath)
    vidTitle = firstVidDiv.find_element_by_xpath('.//a[@id="video-title"]')
    
    #get the video's unique hash from the end of its url
    vidHash = vidTitle.get_attribute('href')
    vidHash = vidHash.split('v=')[1]
    
    return vidTitle.text, vidHash

with open('channels.csv') as f:
    channels = f.readlines()

print(f'checking {len(channels)} channels:')
for i, channel in enumerate(channels):
    channel = channel.rstrip()
    channel = channel.split(',')
    while len(channel)>3:           #there was a , in the title
        channel[2] += ',' + channel.pop(3)
    channelURL = 'https://www.youtube.com/' + channel[1] + '/videos'
    
    #compare the last saved video hash with the newest video's hash
    newestTitle, newestHash = getVidFromChannel(channelURL)
    #remove utf characters
    newestTitle = newestTitle.encode('ascii', errors='ignore') #'replace' would make unicode
    newestTitle = newestTitle.decode('ascii', errors='ignore').rstrip()      #chars into '?'
    if i % 10 == 0 and i != 0:
        print()    
    print(f'{i:>2d}', end=' ')           #2 spaces for up to 2 digits, ">" = aligned right
    if channel[2] != newestHash:
        print(f'\n{channel[0]} has a new video: {newestTitle}')
        print(f'channel url: {channelURL}')
        if openURL:
            os.system(f'""{firefoxPath}" -new-tab "{channelURL}""')
            #yes, os.system() needs those extra surrounding double quotes to correctly use
            #commands which contain a "
        
    #replace each last video with the most current last video  
    channel[2] = newestHash
    channel = ','.join(channel) + '\n'
    channels[i] = channel
        
driver.quit()
#update the list
with open('channels.csv', 'w') as f:
    f.writelines(channels)





