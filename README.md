# checkYouTube

## Check a provided list of youtube channels for new videos since the last check

A quick python script to check youtube channels for new videos.

## How to use

* The script needs selenium installed (pip install selenium)
* And it needs geckodriver.exe next to itself in its folder (or accessible in the PATH). Geckodriver is the driver of firefox and can be downloaded here https://github.com/mozilla/geckodriver/releases i.e. as geckodriver-vX.XX.X-win64.zip for 64-bit windows.
* You also need to create a channels.csv file in this folder, in which you can enter your channels of interest. Each channel can be entered as 3 comma separated strings:
  * First a name for the channel.
  * Then the channel identifier from the URL of the channel videos. This is the URL part between https://www.youtube.com/ and /videos. I.e. for The Coding Train https://www.youtube.com/user/shiffman/videos this would be **user/shiffman**.
  * an arbitrary word or letter - the script will overwrite it with the title of the most recent video.

If you want to for example have the script check for a new video on the channels 3Blue1Brown, Veritasium, and Michael Reeves, your channels.csv file would look like this:

```
3blue1brown,channel/UCYO_jab_esuFRV4b17AJtAw,x
veritasium,c/veritasium,x
michael reeves,channel/UCtHaxi4GTYDpJgMSGy7AeSw,x
```

Once you run the script it will look at the provided channels and report back if the most recent video doesn't match what it found the last time it ran.