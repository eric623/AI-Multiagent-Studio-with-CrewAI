from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class ResearchCrew:
    """A crew for conducting research,
       summarizing findings, and fact-checking"""

    agents_config = 'C:\\Users\\Utilisateur\\Desktop\BE\\Fichiers\\Les_projets\\AI_agents_Courses\\Partie1\\Agentic_system101\\config\\agents.yaml'
    tasks_config = 'C:\\Users\\Utilisateur\\Desktop\BE\\Fichiers\\Les_projets\\AI_agents_Courses\\Partie1\\Agentic_system101\\config\\tasks.yaml'


    def __init__(self):
        self.search_tool = SerperDevTool()
    
    @agent
    def research_agent(self) -> Agent:
        return Agent(
        config=self.agents_config['research_agent'],
        tools=[self.search_tool],
    )

    @agent
    def summarization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarization_agent'],
        )

    @agent
    def fact_checker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker_agent'],
            tools=[self.search_tool],
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            tools=[self.search_tool],
        )

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task']
        )

    @task
    def fact_checking_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_checking_task'],
            tools=[self.search_tool]
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )