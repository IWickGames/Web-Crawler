class crawler:    
    def crawlUrl(self, starterUrl, layers, debug=True):
        import os
        import asyncio
        import async_timeout
        import threading

        self.extractedUrlList = []
        self.testedUrlList = []
        self.discoveredUrls = []

        async def getUrls(url):
            from bs4 import BeautifulSoup, SoupStrainer
            import requests
            urlList = []
            validUrls = []

            async with async_timeout.timeout(1.5):
                try:
                    for link in BeautifulSoup(requests.get(url, timeout=2).text, "html.parser").find_all("a"):
                        urlList.append(link.get("href"))
                except:
                    return urlList

                for testURL in urlList:
                    if testURL:
                        if testURL.startswith("http"):
                            validUrls.append(testURL)
            return validUrls
        
        async def extractor(url):
            includeUrl(url)
            async with async_timeout.timeout(1.5):
                for extUrl in await getUrls(url):
                    if not extUrl in self.extractedUrlList and not extUrl in self.testedUrlList and not extUrl in self.discoveredUrls:
                        self.extractedUrlList.append(extUrl)
                self.extractedUrlList.remove(url)
                self.testedUrlList.append(url)

        def includeUrl(url):
            if not url in self.discoveredUrls:
                self.discoveredUrls.append(url)

        def urlSaveState():
            l = []
            for i in self.extractedUrlList:
                if not i in self.testedUrlList:
                    l.append(i)
            return l

        self.testedUrlList.append(starterUrl)

        for returnUrl in asyncio.run(getUrls(starterUrl)):
                includeUrl(returnUrl)
                self.extractedUrlList.append(returnUrl)

        layer = 1
        for _ in range(layers):
            save = urlSaveState()
            
            amount = 0
            for url in save:
                while threading.active_count()-1 >= 500:
                    pass
                threading.Thread(target=asyncio.run, args=(extractor(url),)).start()
                if debug:
                    print(f"Running Threads: {threading.active_count()-1}/Que:{len(save)-amount} | Layer: {layer} | Disconvered Urls: {len(self.discoveredUrls)}", end="         \r")
                amount += 1

            while threading.active_count()-1 != 0:
                if debug:
                    print(f"Running Threads: {threading.active_count()-1} | Layer: {layer} | Disconvered Urls: {len(self.discoveredUrls)}", end="         \r")
                pass
            layer += 1
        
        print("")
        
        return self.discoveredUrls
