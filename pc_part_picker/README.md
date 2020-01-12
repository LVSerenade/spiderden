# PC Part Picker Spider
These spiders can crawl the website [pc part picker](https://pcpartpicker.com/) for the information on the CPU and the memory parts.
If you use the crawlers be gentle on the website (delay of 1sec for download), faster than that you will get blocked.

# How it work
The first step the memory or the cpu crawler undertake is to get the list of all the part on the website:

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
Also, the dataset is in a very raw format as the spider stored the data as it was shown on the page after the html was stripped off. There is some pre-processing that should be done on the dataset before being useable. However, I didn't want to bias the dataset with a specific pre-processing methodology.
