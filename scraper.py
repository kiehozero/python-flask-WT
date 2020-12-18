from requests_html import HTMLSession

class JobScrape:
    def __init__(self, site_name):
        """
        Having the job site in a list means we can check on initialisation and throw an error if the site is not available.
        """

        sites = [{"monster": {
                "url": "https://www.monster.ie/jobs/search/",
                "query_format": "?q={keywords}&where={city}&cy={country}",
                "results": "#ResultsContainer",
                "not_found": ".pivot.block"}
              },
              
             {"indeed": {
                 "url": "https://ie.indeed.com/jobs", "query_format": "q={keywords}&l={city}", "results": "#resultsCol",}
             }]
    
        try: 
            self.site_data = [site[site_name] for site in sites if site_name in site][0]
            self.site_name = site_name

        except IndexError:
            raise ValueError(f"{site_name} is not found or not supported yet.")

    def _format_monster():
        pass

    def _format_indeed():
        pass

    def _get_description():
        pass

    def _scrape_site(self, city, country, keywords):
        """
        Private method to scrape the supplied site.
        """

        s = HTMLSession()

        keywords = "+".join(keywords.split(","))

        base_url = self.site_data["url"]

        query = self.site_data["query_format"].replace("{keywords}", keywords).replace("{city}", city).replace("{country}", country)

        r = s.get(f"{base_url}{query}")

        if r.html.find(self.site_data["not_found"]):
            return None
        else:
            return r.html.find(self.site_data["results"], first=True)

    def get_jobs(self, city, country, keywords, desc=True):
        """
        Main class method. Calls the scraper and formats the results based on the selected site.
        """

        jobs = self._scrape_site(city, country, keywords)

        if self.site_name.lower() == "monster":
            return self._format_monster(jobs, desc) if jobs else None