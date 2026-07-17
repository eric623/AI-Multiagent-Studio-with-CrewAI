# AI MultiAgent Studio

<p align="center">
  <img src="https://raw.githubusercontent.com/eric623/AI-Multiagent-Studio-with-CrewAI/main/Interface.PNG"
       alt="AI MultiAgent Studio Interface"
       width="900"/>
  <br>
  <em>Figure 1 - Streamlit interface integrating the three CrewAI workflows.</em>
</p>

AI MultiAgent Studio is a production-ready Streamlit application that brings together three intelligent multi-agent workflows built with CrewAI. The project demonstrates how autonomous agents can collaborate to perform research, fact-checking, content generation, and long-form writing tasks.

Built as a unified platform, AI MultiAgent Studio showcases modern Agentic AI concepts, including multi-agent orchestration, CrewAI Flows, YAML-based configuration, local LLM deployment with Ollama, and external tool integration such as SerperDev and Firecrawl.

---

## Features

* Unified Streamlit interface for all workflows.
* Multi-agent orchestration with CrewAI.
* Modular YAML-based agent and task configuration.
* Local LLM execution using Ollama (Llama 3.2).
* Web search capabilities with SerperDev.
* Intelligent web scraping with Firecrawl.
* Parallel execution of crews for scalable workflows.
* Production-ready architecture with reusable components.

---

## Workflows

### 1. Multi-Agent Research & Fact-Checking System

An intelligent system that automates:

* Internet research
* Content summarization
* Fact verification

#### Agents

| Agent                    | Role                                          |
| ------------------------ | --------------------------------------------- |
| Internet Researcher      | Finds relevant and up-to-date information.    |
| Content Summarizer       | Produces concise and structured summaries.    |
| Fact-Checking Specialist | Verifies claims and ensures factual accuracy. |

#### Workflow

```text
Topic
   ↓
Research Agent
   ↓
Summarization Agent
   ↓
Fact-Checking Agent
   ↓
Verified Report
```

#### Technologies

* CrewAI
* Ollama (Llama 3.2)
* SerperDevTool
* YAML Configuration

---

### 2. Social Media Content Writer Flow

This workflow automatically converts a blog article or newsletter into social media content.

#### Capabilities

* Scrape web content from a URL.
* Analyze technical articles.
* Generate LinkedIn posts.
* Generate X (Twitter) threads.
* Export content plans as JSON.

#### Agents

| Agent                  | Role                                  |
| ---------------------- | ------------------------------------- |
| Draft Analyzer         | Extracts key ideas and concepts.      |
| Twitter Thread Planner | Generates engaging Twitter/X threads. |
| LinkedIn Post Planner  | Creates professional LinkedIn posts.  |

#### Workflow

```text
Blog URL
   ↓
Firecrawl Scraping
   ↓
Markdown Conversion
   ↓
Draft Analysis
   ↓
Routing
   ├── LinkedIn Post
   └── X Thread
```

#### Technologies

* CrewAI Flows
* Firecrawl
* Python
* JSON
* YAML

---

### 3. Book Writer Flow

A multi-crew system capable of generating an entire book from a single topic.

#### Architecture

##### Outline Crew

| Agent                | Responsibility                                 |
| -------------------- | ---------------------------------------------- |
| Researcher Agent     | Collects information about the topic.          |
| Outline Writer Agent | Generates the book outline and chapter titles. |

##### Chapter Writer Crew

| Agent                | Responsibility                      |
| -------------------- | ----------------------------------- |
| Researcher Agent     | Performs chapter-specific research. |
| Chapter Writer Agent | Writes complete chapters.           |

#### Workflow

```text
Book Topic
    ↓
Outline Crew
    ↓
Book Outline
    ↓
Parallel Chapter Writer Crews
    ↓
Chapter 1
Chapter 2
...
Chapter N
    ↓
Complete Book
```

#### Technologies

* CrewAI
* CrewAI Flows
* SerperDevTool
* YAML
* Python

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/<your-username>/AI_MultiAgent_Studio.git

```

### Install Dependencies

This project uses `uv` for dependency management.

```bash
uv sync

cd AI_MultiAgent_Studio
```

---

## Running the Application

Launch the Streamlit application:

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

## Requirements

* Python 3.11+
* Ollama installed locally
* Llama 3.2 model
* Serper API Key
* Firecrawl API Key
* Streamlit
* CrewAI

---

## Key Concepts Demonstrated

* Multi-Agent Systems
* Agentic AI
* CrewAI Flows
* Multi-Crew Architectures
* YAML Configuration Management
* Web Scraping
* Local LLM Deployment
* Workflow Orchestration
* Parallel Execution
* Streamlit Applications

---

## Author

**AKAKPO Koffi Moïse**

* Interested in Agentic AI, Multi-Agent Systems, Computer Vision, and Applied Artificial Intelligence.

---

> AI MultiAgent Studio demonstrates how modern Agentic AI systems can be designed, orchestrated, and deployed in a production-ready environment using CrewAI, Streamlit, and local LLMs.
