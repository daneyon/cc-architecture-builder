---
id: visualization-workflow
title: Data Visualization Design Workflow
category: reference
tags: [visualization, data-viz, perception, iterative-design, nested-model]
summary: Hybrid visualization design workflow synthesizing Yau's data-viz process, Cleveland-McGill visual encoding effectiveness, and Munzner's nested model. Advisory reference for planning dashboards, charts, or visualization-heavy deliverables.
depends_on: []
related: [planning-implementation, product-design-cycle]
complexity: foundational
last_updated: 2026-04-22
estimated_tokens: 1200
source: CAB-curated synthesis (Yau 2013, Cleveland-McGill 1984, Munzner 2014); relocated from skills/planning-implementation/references/ in Phase 2.6 of impl-plan-ux-log-tracker-2026-04-22.md
confidence: A
review_by: 2026-10-22
---

# Data Visualization Design Workflow

Hybrid of Nathan Yau's Data Visualization Process, Cleveland and McGill's Visual Encoding Framework, and Munzner's Nested Model for Visualization Design. This workflow will guide you from acquiring the data to implementing the visualization while ensuring perceptual effectiveness and an iterative design process.


**1. Define the Problem (Domain Situation)**
   - **Goal:** Clearly define the problem or the insight you want to derive from your data. Understand your audience, the questions you're answering, and the decisions the visualization will inform.
   - **Actions:**
     - Identify key questions or problems.
     - Clarify the purpose and context of the visualization.
     - Establish who the audience is and what their needs are.

   *Source: Munzner's Nested Model (Domain Situation).*

---

**2. Acquire and Parse Data (Data Acquisition and Preparation)**
   - **Goal:** Gather and clean the data to ensure it’s ready for visualization.
   - **Actions:**
     - Acquire relevant data (e.g., text, tables, etc.).
     - Clean and preprocess the data (e.g., parsing text, handling missing values).
     - Organize the data into a structured format suitable for analysis and visualization.

   *Source: Yau's Data Visualization Process (Acquire and Parse).*

---

**3. Filter and Abstract Data (Data/Task Abstraction)**
   - **Goal:** Extract the key aspects of the data needed for the visualization, focusing on what is most relevant to the problem.
   - **Actions:**
     - Filter the data to remove irrelevant details.
     - Abstract the data to focus on the key insights, patterns, or trends.
     - Define the tasks your visualization will support (e.g., comparison, trend identification, etc.).

   *Source: Munzner's Nested Model (Data Abstraction) & Yau's Process (Filter).*

---

**4. Analyze and Explore (Mining for Insights)**
   - **Goal:** Analyze the abstracted data for key trends, patterns, outliers, or insights that you want to visualize.
   - **Actions:**
     - Perform exploratory data analysis (e.g., statistical analysis, text analysis, clustering).
     - Identify important relationships, patterns, or anomalies in the data.
     - Refine your understanding of what insights need to be highlighted in the visualization.

   *Source: Yau's Process (Mine).*

---

**5. Choose the Right Visual Encoding (Encoding Design)**
   - **Goal:** Select the most effective visual representations for your data based on human perception.
   - **Actions:**
     - Map data dimensions to visual properties like position, length, angle, and color.
     - Choose appropriate chart types (e.g., bar charts, scatterplots, heatmaps) based on the data.
     - Ensure visual encodings are perceptually accurate and easy to interpret.

   *Source: Cleveland & McGill's Visual Encoding Framework.*

---

**6. Design Interaction and Layout (Interaction and Interface Design)**
   - **Goal:** Enhance the usability and interactivity of your visualization, making it more engaging and dynamic.
   - **Actions:**
     - Decide on interaction features like zooming, filtering, or tooltips.
     - Arrange the visual elements to ensure a clean and coherent layout.
     - Consider user interaction flow and how users will engage with the data.

   *Source: Munzner's Nested Model (Visual Encoding/Interaction Design).*

---

**7. Implement Visualization (Visual Representation)**
   - **Goal:** Build the visualization using the chosen visual encodings and interaction designs.
   - **Actions:**
     - Use appropriate tools (e.g., D3.js, Tableau, Power BI, etc.) to construct the visualizations.
     - Test the performance of the visualization, ensuring it is responsive and efficient.

   *Source: Yau's Process (Represent) & Munzner's Model (Algorithm Level).*

---

**8. Iterate and Refine (Evaluation)**
   - **Goal:** Evaluate the effectiveness of the visualization and improve it based on feedback and further insights.
   - **Actions:**
     - Gather feedback from users or stakeholders.
     - Iterate through design revisions to enhance clarity, accuracy, and user experience.
     - Continuously refine the visualization based on evolving data or new requirements.

   *Source: Munzner's Model (Iterative Design).*

---

**Summary of the Workflow Steps:**
1. **Define the Problem (Domain Situation)** – Understand the problem and audience.
2. **Acquire and Parse Data (Data Acquisition)** – Gather and clean your data.
3. **Filter and Abstract Data (Data/Task Abstraction)** – Focus on the relevant data.
4. **Analyze and Explore (Mining for Insights)** – Discover key insights.
5. **Choose the Right Visual Encoding (Encoding Design)** – Select effective visual encodings.
6. **Design Interaction and Layout (Interaction and Interface Design)** – Plan interactions and layout.
7. **Implement Visualization (Representation)** – Build and deploy the visualization.
8. **Iterate and Refine (Evaluation)** – Improve based on feedback and usage.