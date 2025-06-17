from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from research_crew.tools.custom_tool import WebSearchTool, WebScraperTool


@CrewBase
class ResearchCrew():
    """ResearchCrew crew"""

    def __init__(self):
        # Initialize tools
        self.web_search_tool = WebSearchTool()
        self.web_scraper_tool = WebScraperTool()

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.web_search_tool, self.web_scraper_tool],
            verbose=True
        )

    @agent
    def writer(self)-> Agent:
        return Agent(
            config = self.agents_config['writer'],
            verbose=True
        )

    @agent
    def editor(self)->Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Create the ResearchCrew crew"""
        return Crew(
            agents=self.agents,
            tasks = self.tasks,
            process=Process.sequential,
            verbose=True
        )
