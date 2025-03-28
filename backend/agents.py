from crewai import Agent, Task, Crew
from langchain.tools import Tool
from langchain.utilities import AlphaVantageAPIWrapper
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def create_technical_analyst():
    return Agent(
        role='Technical Analyst',
        goal='Analyze stock data and provide technical insights',
        backstory="""You are an expert stock market analyst with deep knowledge of technical analysis,
        market patterns, and price action. You excel at identifying trends and potential trading opportunities.""",
        verbose=True,
        allow_delegation=False
    )

def create_market_researcher():
    return Agent(
        role='Market Researcher',
        goal='Research market conditions and provide fundamental insights',
        backstory="""You are a seasoned market researcher who specializes in analyzing market conditions,
        company fundamentals, and industry trends. You provide insights based on market research and analysis.""",
        verbose=True,
        allow_delegation=False
    )

def create_analysis_tasks(analyst, researcher, stock_data, user_query):
    tasks = [
        Task(
            description=f"""Analyze the technical aspects of this stock data:
            {stock_data}
            
            Focus on:
            1. Price trends and patterns
            2. Volume analysis
            3. Support and resistance levels
            4. Technical indicators
            
            User question: {user_query}""",
            agent=analyst
        ),
        Task(
            description=f"""Research and analyze market conditions for this stock:
            {stock_data}
            
            Focus on:
            1. Market position and trends
            2. Industry context
            3. Growth potential
            4. Market sentiment
            
            User question: {user_query}""",
            agent=researcher
        )
    ]
    return tasks

def create_analysis_crew(stock_data, user_query):
    try:
        # Create the agents
        analyst = create_technical_analyst()
        researcher = create_market_researcher()
        
        # Create the tasks
        tasks = create_analysis_tasks(analyst, researcher, stock_data, user_query)
        
        # Create and run the crew
        crew = Crew(
            agents=[analyst, researcher],
            tasks=tasks,
            verbose=True
        )
        
        # Get the result
        result = crew.kickoff()
        return result
        
    except Exception as e:
        return f"Error during analysis: {str(e)}" 