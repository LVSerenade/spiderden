# PC Part Picker Spiders
These spiders can crawl the website [pc part picker](https://pcpartpicker.com/) for the information on the CPU and the memory parts.
If you use the crawlers be gentle on the website (delay of 1sec for download), faster than that you will get blocked.

# What they can scrape
- [CPU](https://pcpartpicker.com/products/cpu/) -> `cpu_spider.py` = cpu
- [CPU Cooler](https://pcpartpicker.com/products/cpu-cooler/) -> `cpu_cooler_spider.py` = cpucooler
- [Motherboard](https://pcpartpicker.com/products/motherboard/) -> `motherboard_spider.py` = motherboard
- [Memory](https://pcpartpicker.com/products/memory/) -> `memory_spider.py` = memory
- [Storage](https://pcpartpicker.com/products/internal-hard-drive/) -> `storage_spider.py` = storage
- [Video Card](https://pcpartpicker.com/products/video-card/) -> `video_card_spider.py` = videocard
- [Power Supply](https://pcpartpicker.com/products/power-supply/) -> `power_supply_spider.py` = powersupply
- [Case](https://pcpartpicker.com/products/case/) -> `case_spider.py` = case

# Requirements
- Python 3.7 and above
- Pip

# How to use

1. Open up your terminal and `cd` into the spiderden folder, make sure that you have Python 3 installed with pip.
2. Create a virtual environment and activate it (_optional_)
3. run `pip install -r requirements.txt` (_might take a while_)
4. go into the pc_part_picker folder by doing `cd pc_part_picker`
5. run the spider you want by doing `scrapy crawl _____ -o ______.csv` where the first blank is the name of the spider you want to launch and the second blank is the name of your output. The name of the spider are listed above in the _What they can scrape_ section.
6. Wait for the spider to finish running.

You can of course edit the code to fit your needs.

# How it work
The first step the crawlers undertake is to get the list of all the part on the website:

![Step 0 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_0.png)

Then it get all the links to the complete part information and it gather the information from there.
The first thing it fetch on the page is the rating of the part, which is conveniently located on the banner:

![Step 1 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_1.png)

Then it fetch the list of prices that are gathered from vendors:

![Step 2 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_2.png)

Finally the spider take the reviews that are given by the pc part community and the specification of the part:

![Step 3 of how it work](https://github.com/yacineMahdid/spiderden/blob/master/media/pc_part_picker/target_3.png)

# Dataset Composition:
## CPU 
- manufacturer
- model	
- part #	
- core count	
- core clock	
- boost clock	
- tdp	
- series	
- microarchitecture	
- core family	
- socket	
- integrated graphics	
- maximum supported memory	
- ecc support	
- packaging	
- includes cpu cooler	
- l1 cache	
- l2 cache	
- l3 cache	
- lithography	
- simultaneous multithreading	
- prices	
- rating	
- reviews

_Not all fields are always filled, even for the price, rating and reviews_

## Memory
- manufacturer
- part #
- speed
- type
- modules
- price / gb
- color
- cas latency
- voltage
- timing
- ecc / registered
- heat spreader
- prices
- rating

_Similarly some of the fields are empty for some data points_

# Note
The dataset generated from the spiders is in a very raw format as the spider stored the data as it was shown on the page after the html was stripped off. There is some pre-processing that should be done on the dataset before being useable. However, I didn't want to bias the dataset with a specific pre-processing methodology.

The difficulty of scraping this website is not high, but not easy either. They have various measure in place that stop the crawlers (like loading the important part with a second post call after the page as loaded) and checking if the frequency of the ip address making the request is human possible. If you don't throttle the frequency a Captcha will stop you and you will get a rate limit.

# Contribution
Screenshots taken from [pc part picker](https://pcpartpicker.com/) at 2020-01-11.
