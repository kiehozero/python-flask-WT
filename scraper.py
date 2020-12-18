from requests_html import HTMLSession

class JobScrape():
   
    def __init__(self, site_name):
        """
        Having the job site in a list means we can check on initialisation and throw an error if the site is not available.
        """

        sites = [{"monster": {
                "url": "https://www.monster.ie/jobs/search/",
                "query_format": "?q={keywords}&where={city}&cy={country}",
                "results": "#ResultsContainer",
                "not_found": ".pivot.block", 
                "desc_text": "[name=\"sanitizedHtml\"]"}
              },
              
             {"indeed": {
                 "url": "https://ie.indeed.com/jobs", "query_format": "q={keywords}&l={city}", "results": "#resultsCol",}
             }]
    
        try: 
            self.site_data = [site[site_name] for site in sites if site_name in site][0]
            self.site_name = site_name

        except IndexError:
            raise ValueError(f"{site_name} is not found or not supported yet.")

    def _format_monster(self, results, desc):
        """
        Non-public method to return jobs in the given format of title, company, url, description (optional).
        """

        job_summaries = []

        cards = results.find(".card-content .summary")
        """Omits the first=true parameter so we get all results."""

        for card in cards:
            job = {}
            job["title"] = card.find(".title a", first=True).text
            job["company"] = card.find(".company .name", first=True).text
            url = card.find(".title a", first=True)
            job["url"] = url.attrs["href"]
            if desc:
                job["description"] = self._get_description(url.attrs["href"])

            job_summaries.append(job)

        return job_summaries

    def _format_indeed():
        pass

    def _get_description(self, url):
        """
        Private function to retrieve the job description
        """

        s = HTMLSession()

        r = s.get(url)

        result = r.html.find(self.site_data["desc_text"], first=True)

        return result.text if result else "No description available."

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