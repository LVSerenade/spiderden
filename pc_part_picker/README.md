# PC Part Picker Spider
This spiders can crawl the website [pc part picker](https://pcpartpicker.com/) for the information on cases, fan, cpu, cpu cooler, memory, motherboard, external hard drive etc..
If you use the crawlers be gentle on the website (delay of 1sec for download), faster than that you will get blocked.

# What they can scrape
Here is the final dataset the spiders can scrape : [S3 Bucket Link]()
It includes data from all of these categories of product:
- case
- case accessory
- case fan
- cpu
- cpu cooler
- external hard drive
- fan controller 
- headphones
- internal hard drive
- keyboard
- laptop
- memory
- monitor
- motherboard
- mouse
- optical drive
- os
- power supply
- software
- sound card
- thermal paste
- ups
- video card
- wired network card
- wireless network card

An important point to note is that this website is dynamic and the content vary from time to time. If you want an up to date version of the data you will need to run the crawler again.

# Requirements
- Python 3
- Pip

# How to use

1. Open up your terminal and `cd` into the spiderden folder, make sure that you have Python 3 installed with pip.
2. Create a virtual environment and activate it (_optional_)
3. run `pip install -r requirements.txt` (_might take a while_)
4. go into the pc_part_picker folder by doing `cd pc_part_picker`
5. run the spider you want by doing `scrapy crawl parts`. This will take a while with the current configuration and will output a json named all_parts.json which contain all parts. 
6. If you want separate csv files per category run `convert_csv.py`. There are different specificaitons per category so having everything into one CSV wasn't possible.

You can of course edit the code to fit your needs.

# How it work
The first step the crawlers undertake is to get the list of all the part category on the website. 
Then it use these category pages to get a list of all the parts that matches a given category:

![Step 0 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_0.png)

Then it get all the links to the complete part information and it gather the information from there.
The first thing it fetch on the page is the rating of the part, which is conveniently located on the banner:

![Step 1 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_1.png)

Then it fetch the list of prices that are gathered from vendors:

![Step 2 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_2.png)

Finally the spider take the reviews that are given by the pc part community and the specification of the part:

![Step 3 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_3.png)

# Dataset Composition:
Total Number of Parts Scraped : **39668** parts

## Breakdown of parts per category:
- cpu : 1213 parts
- ups : 658 parts
- thermal-paste : 103 parts
- fan-controller : 36 parts
- case-fan : 1495 parts
- case-accessory : 8 parts
- laptop : 307 parts
- external-hard-drive : 319 parts
- monitor : 2770 parts
- software : 143 parts
- os : 56 parts
- optical-drive : 217 parts
- power-supply : 2027 parts
- case : 3880 parts
- video-card : 4178 parts
- internal-hard-drive : 3788 parts
- speakers : 195 parts
- mouse : 1949 parts
- keyboard : 2262 parts
- headphones : 2289 parts
- wireless-network-card : 303 parts
- wired-network-card : 120 parts
- sound-card : 71 parts
- memory : 7127 parts
- motherboard : 3043 parts
- cpu-cooler : 1111 parts


The fields per category are highly variable however, three fields are always there: **price**, **rating** and **reviews**
_Not all fields are always filled, even for the price, rating and reviews_

# Note
The dataset generated from the spider is in a very raw format as the spider stored the data as it was shown on the page after the html was stripped off. There is some pre-processing that should be done on the dataset before being useable. However, I didn't want to bias the dataset with a specific pre-processing methodology.

The difficulty of scraping this website is not high, but not easy either. They have various measure in place that stop the crawlers (like loading the important part with a second post call after the page as loaded) and checking if the frequency of the ip address making the request is human possible. If you don't throttle the frequency a Captcha will stop you and you will get a rate limit.

# Contribution
Screenshots taken from [pc part picker](https://pcpartpicker.com/) at 2020-01-11.
