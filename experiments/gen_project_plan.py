from jinja2 import Template
from pydantic import BaseModel

from utils.create_prompts import create_data


class ProjectDetails(BaseModel):
    project_name: str
    project_duration: str
    project_methodology: str
    project_objectives: str
    AI_templates: str
    meta_templates: str
    scaffolding: str
    blueprints: str
    rapid_development: str
    innovation: str
    project_initiation: str
    project_plan: str
    timelines: str
    milestones: str
    resource_allocation: str
    project_scope_document: str


def render_project_template(project_details: ProjectDetails):
    template_str = """
    {{ project_details.project_name }}
    Project Overview:
    A {{ project_details.project_duration }} project aimed at developing an {{ project_details.project_methodology }}-driven full-stack website, harnessing the methodologies of Design for Lean Six Sigma (DFLSS). {{ project_details.project_objectives }} of custom code generation and prompt engineering will be utilized. This strategy emphasizes the integration of {{ project_details.AI_templates }}, {{ project_details.meta_templates }}, {{ project_details.scaffolding }}, and {{ project_details.blueprints }} to ensure {{ project_details.rapid_development }} and {{ project_details.innovation }}.

    Week 1: {{ project_details.project_initiation }}
    Objective: Establish project foundations and detailed planning.
    • Host a kickoff meeting to define project objectives, utilizing AI-powered templates for effective planning.
    • Develop a comprehensive {{ project_details.project_plan }} including {{ project_details.timelines }}, {{ project_details.milestones }}, and {{ project_details.resource_allocation }}.
    Deliverable: Detailed {{ project_details.project_scope_document }} and scope document.
    """

    template = Template(template_str)
    rendered_template = template.render(project_details=project_details.dict())

    return rendered_template


# Example usage:

import asyncio

pr = """**Press Release: Introducing the Future of Competitive Intelligence - The Game-Changing Website That Redefines Market Strategy**

**FOR IMMEDIATE RELEASE**

**[City, Date]** - In a groundbreaking development set to transform the landscape of competitive intelligence, we are thrilled to announce the launch of our state-of-the-art Competitive Intelligence Website. This revolutionary platform is meticulously designed to empower businesses to not only track their competitors but to outsmart and outperform them in the ever-evolving market.

**Revolutionizing Competitive Strategy**

Our Competitive Intelligence Website is a culmination of cutting-edge technology and in-depth market insights. It is tailored to equip sales teams with the tools they need to comprehensively analyze competitors and craft winning strategies.

**Key Features:**

- **Advanced Competitor Monitoring**: Leveraging AI, our website offers real-time tracking of competitors’ activities, ensuring that businesses are always a step ahead.
- **Interactive Battle Cards**: We offer dynamic and customizable battle cards that vividly compare products and services against competitors, highlighting unique selling points and key differentiators.
- **AI-Powered Summarization and Importance Scoring**: Distill crucial information from a sea of data with our AI-driven summarization and importance scoring tools.
- **Actionable Insights Right to Your Inbox**: Get high-priority competitive insights directly delivered, allowing sales teams to focus on strategic decision-making.
- **Comprehensive Resource Library**: Access our extensive collection of templates, reports, and guides to enhance your competitive intelligence strategy.

**Empowering Businesses to Lead**

"Our mission was to create a platform that not only simplifies competitive intelligence but transforms it into an impactful strategic tool," says the CEO. "With our website, businesses can now harness the full potential of their market data to make informed, winning decisions."

**Stay Ahead, Stay Informed**

In today's fast-paced business environment, understanding and anticipating competitor moves is crucial. Our Competitive Intelligence Website doesn't just provide data - it offers a roadmap to victory.

**Availability:**

The Competitive Intelligence Website is available now. We invite businesses to experience the future of market strategy and competitive analysis.

**Contact:**

For more information on how our platform can revolutionize your competitive strategy, please contact [Contact Information].

---

**About Us:**

[Company Name] is at the forefront of competitive intelligence solutions, dedicated to providing innovative tools and insights that empower businesses to excel in their markets.

**END**"""


async def main():
    data = await create_data(prompt=pr, cls=ProjectDetails)
    details = ProjectDetails(**data)
    project_template = render_project_template(details)
    print(project_template)


if __name__ == "__main__":
    asyncio.run(main())
