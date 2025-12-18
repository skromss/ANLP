# Lab 2: Multi-Agent Music Tutor

## Overview
This project implements a **Multi-Agent System (MAS)** as a **Musical Tutor**. It helps users with music theory, practice planning, and chord information using specialized agents.

## Features
*   **Router Agent**: Classifies queries into Theory, Practice, or General categories.
*   **Music Theory Agent**: Explains concepts like scales, intervals, and history using a local knowledge base.
*   **Practice Coach Agent**: Generates random practice routines and looks up chord notes.
*   **General Agent**: Handles casual conversation.

## Architecture
Stateful graph with explicit routing:
Stateful graph with explicit routing:

```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD;
    __start__([Start]):::first
    router(Router)
    theory_agent(Theory Agent)
    practice_agent(Practice Agent)
    general_agent(General Agent)
    tools(Tools)
    __end__([End]):::last
    
    __start__ --> router;
    
    router -.->|Theory| theory_agent;
    router -.->|Practice| practice_agent;
    router -.->|General| general_agent;
    
    theory_agent -.-> __end__;
    theory_agent -.->|Call Tool| tools;
    
    practice_agent -.-> __end__;
    practice_agent -.->|Call Tool| tools;
    
    tools -.-> theory_agent;
    tools -.-> practice_agent;
    
    general_agent --> __end__;
    
    classDef default fill:#f2f0ff,line-height:1.2
    classDef first fill-opacity:0
    classDef last fill:#bfb6fc
```

## Usage
```bash
python notebooks/demo.py
```
