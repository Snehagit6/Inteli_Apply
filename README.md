# Inteli_Apply

Agentic AI system to search and apply jobs with tailored resume


# System design
                 ┌────────────────────┐
                 │  User Request       │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │ Agent Orchestrator │
                 └─────────┬──────────┘
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
             Resume      Search      Job
              Tool        Tool      Details
                │          │          │
                │       Playwright    │
                │          │          │
                ▼          ▼          ▼
           Candidate     JobCard   JobDetails
             Profile
                │          │          │
                └──────────┼──────────┘
                           ▼
                  ┌─────────────────┐
                  │ Matching Agent  │
                  └────────┬────────┘
                           ▼
                   Match Analysis
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          Resume Tailoring      Human Review
                 │                   │
                 └─────────┬─────────┘
                           ▼
                   Application Tool
                           │
                       Playwright

<!-- HITL -->
                    
                    
                    SUBMIT APPLICATION
                            │
                            ▼
                     Human Approval
                            │
                     ┌──────┴──────┐
                     │             │
                   Approve       Reject
                     │
                     ▼
                  Submit