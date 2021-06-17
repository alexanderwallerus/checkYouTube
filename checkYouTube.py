#check youtube channels for new videos
##############################################################################################
from selenium import webdriver
from selenium.common import exceptions as seleExceptions

options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1000, 1080)

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
    
    xPath = '//div[@class="style-scope ytd-grid-video-renderer"]'
    firstVidDiv = driver.find_element_by_xpath(xPath)
    vidName = firstVidDiv.find_element_by_xpath('//a[@id="video-title"]')
    return vidName.text

with open('channels.csv') as f:
    channels = f.readlines()

print(f'checking {len(channels)} channels:')
for i, channel in enumerate(channels):
    channel = channel.rstrip()
    channel = channel.split(',')
    while len(channel)>3:           #there was a , in the title
        channel[2] += ',' + channel[3]
        channel = channel[:-1]
    channelUrl = 'https://www.youtube.com/' + channel[1] + '/videos'
    
    #compare this old title with the newest video
    newestVid = getVidFromChannel(channelUrl)
    #replace utf characters
    newestVid = newestVid.encode('ascii', errors='ignore') #'replace' would make unicode
    newestVid = newestVid.decode('ascii', errors='ignore') #chars into '?'
    if i % 10 == 0 and i != 0:
        print()    
    print(f'{i}', end=' ')
    if not channel[2] == newestVid:
        print(f'\n{channel[0]} has a new video: {newestVid}')
        print(f'channel url: {channelUrl}')
        
    #replace each last video with the most current last video  
    channel[2] = newestVid
    channel = ','.join(channel) + '\n'
    channels[i] = channel

driver.quit()
#update the list
with open('channels.csv', 'w') as f:
    f.writelines(channels)





