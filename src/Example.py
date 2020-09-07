import webCrawler #Imports the crawler library from the current directory

c = webCrawler.crawler() #Creates Crawler Instance

#starterUrl is your beginner url
#Layers is how deep you want the crawler to go into the website
#The more layers you go into the longer the crawler will take to complete

#Function returns a list of all the urls the crawler found

#Debug defaults to TRUE if not entered, change to false to not display any information about
#the current progress of the scrape(I would suggest you keep debug on as it allows you to see progress and know it has not frozen)
listUrl = c.crawlUrl(starterUrl="https://www.youtube.com/watch?v=Sagg08DrO5U", layers=4, debug=True)

#Print out the stored scraped urls in the vairable listURL
print(listUrl)
