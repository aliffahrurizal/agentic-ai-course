https://docs.crewai.com/concepts/planning
* youtube video link: https://youtu.be/DpQw0DP7dE8?t=505
# Before enabling planning

1. run command in terminal `crewai run`

Agents sequential Tasks

```markdown
# Agent: AI LLMs Senior Data Researcher
## Task: Conduct a thorough research about AI LLMs Make sure you find any interesting and relevant information given the current year is 2025.
```

```markdown
# Agent: AI LLMs Reporting Analyst
## Task: Review the context you got and expand each topic into a full section for a report. Make sure the report is detailed and contains any and all relevant information.

```

# After enabling planning

Agents sequential Tasks

```markdown
[2025-03-06 20:35:45][INFO]: Planning the crew execution
# Agent: AI LLMs Senior Data Researcher
## Task: Conduct a thorough research about AI LLMs Make sure you find any interesting and relevant information given the current year is 2025.
1. **Information Gathering:** The AI LLMs Senior Data Researcher will begin by searching for information regarding AI LLMs in 2025. This will encompass advancements, trends, challenges, and breakthroughs. Sources include academic databases, industry publications, tech news outlets, AI research blogs, and conference proceedings.
2. **Trend Identification:** The researcher will then identify key trends and innovations in LLMs expected to be prominent in 2025. Examples may include advancements in model size, training techniques, multi-modality, energy efficiency, or specific application areas.
3. **Competitive Landscape Analysis:** The researcher will analyze the competitive landscape by identifying key players and their contributions to AI LLMs. This involves examining leading tech companies, research institutions, and open-source projects.
4. **Ethical Considerations:** Explore ethical considerations surrounding LLMs. This includes concerns about bias, misinformation, job displacement, and responsible AI development.
5. **Application Areas:** Examine diverse application areas of LLMs in 2025. These may include healthcare, finance, education, customer service, creative content generation, and scientific research.
6. **Future Predictions:** Make informed predictions about the future of AI LLMs, considering factors such as technological progress, market dynamics, and societal impact.
7. **Documentation:** Create a detailed list of the 10 most relevant bullet points about AI LLMs. This will serve as the task output for the next agent.
8. **Review and Refine:** The researcher will review the list to ensure accuracy, relevance, and conciseness. This may involve cross-referencing information and making necessary revisions.

```

```markdown
# Agent: AI LLMs Reporting Analyst
## Task: Review the context you got and expand each topic into a full section for a report. Make sure the report is detailed and contains any and all relevant information.
1. **Context Review:** The AI LLMs Reporting Analyst will carefully review the 10 bullet points provided by the AI LLMs Senior Data Researcher.
2. **Topic Expansion:** For each bullet point, the analyst will conduct further research to gather more detailed information. This may involve consulting additional sources, conducting literature reviews, and analyzing data.
3. **Section Drafting:** The analyst will draft a full section for each topic, incorporating the expanded information. Each section will include an introduction, supporting details, examples, and conclusions.
4. **Report Structuring:** The analyst will structure the report in a logical and coherent manner, with clear headings and subheadings. This ensures that the report is easy to read and understand.
5. **Content Enrichment:** Enrich the report with relevant statistics, case studies, and real-world examples to support the key findings.
6. **Formatting and Style:** Format the report in markdown, ensuring that it is visually appealing and easy to read. Use appropriate fonts, headings, and spacing.
7. **Review and Editing:** The analyst will thoroughly review and edit the report to ensure accuracy, clarity, and completeness. This may involve correcting grammatical errors, clarifying ambiguous statements, and adding missing information.
8. **Finalization:** Generate the final report, formatted as markdown, ready for distribution or presentation.


```