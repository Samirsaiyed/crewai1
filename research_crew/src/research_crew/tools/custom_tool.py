from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import os

class WebSearchInput(BaseModel):
    """Input schema for WebSearchTool."""
    query: str = Filed(..., description="Search query to find information")

class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Search the web for current information on any topic"
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        """Execute web search using Serper API"""
        try:
            url = "https://google.serper.dev/search"

            payload = {
                'q': query,
                'num': 5
            }

            headers = {
                'X-API-KEY': os.getenv('SERPER_API_KEY'),
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=payload, headers=headers)
            results = response.json()

            # Format results
            search_results = []
            if 'organic' in results:
                for result in results['organic'][:5]:
                    search_results.append(f"Title: {result.get('title', 'N/A')}\n"
                    f"Link: {result.get('link','N/A')}\n"
                    f"Snippet: {result.get('snippet','N/A')}\n")

            return f"Search Results for '{query}' : \n\n" + "\n---\n".join(search_results)

        except Exception as e:
            return f"Error performing search: {str(e)}"

class WebScraperInput(BaseModel):
    """Input schema for WebScraper Tool"""
    url: str = Field(..., description="URL to scrape content from")

class WebScraperTool(BaseModel):
    name: str = "Web Scraper Tool"
    description: str = "Extract content from web pages for detailed analysis"
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, url:str)->str:
        """Scrape content from a given URL"""

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script","style"]):
                script.decompose()

            # get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            # Limit text length
            if len(text) > 3000:
                text = text[:3000] + "..."

            return f"Content from {url}:\n\n{text}"

        except Exception as e:
            return f"Error scrapping {url}: {str(e)}"
            
    

