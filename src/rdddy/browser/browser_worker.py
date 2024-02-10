import asyncio
import asyncio
from asyncio import subprocess
from asyncio.subprocess import Process
import psutil


from playwright.async_api import async_playwright
import pyperclip

from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from rdddy.browser.browser_domain import *

from rdddy.messages import *
from loguru import logger

LINKEDIN_JOBS_ALERTS_URL = "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=3697926602&distance=25&f_TPR=a1704127314-&f_WT=3%2C2&geoId=102448103&keywords=senior%20staff%20engineer&origin=JOB_ALERT_IN_APP_NOTIFICATION&savedSearchId=1735387277&sortBy=R"


class BrowserWorker(Actor):
    async def handle_click(self, click_cmd: Click) -> None:
        await self.page.click(
            selector=click_cmd.selector,
            options=click_cmd.options,
            **click_cmd.keyword_args,
        )

    async def handle_goto(self, goto_cmd: Goto) -> None:
        await self.page.goto(
            url=goto_cmd.url, options=goto_cmd.options, **goto_cmd.keyword_args
        )

    async def handle_type(self, type_cmd: TypeText) -> None:
        await self.page.type(
            selector=type_cmd.selector,
            text=type_cmd.text,
            options=type_cmd.options,
            **type_cmd.keyword_args,
        )

    async def handle_send_chatgpt(self, send_cmd: SendChatGPT) -> None:
        SLEEP = 2
        #
        await asyncio.sleep(SLEEP)
        await self.send(self.actor_id, Click(selector="#prompt-textarea"))
        # # pyperclip.copy(send_cmd.prompt)
        # # pyperclip.paste()
        await self.send(
            self.actor_id, TypeText(selector="#prompt-textarea", text=send_cmd.prompt)
        )
        await asyncio.sleep(SLEEP * 5)
        await self.send(self.actor_id, Click(selector='[data-testid="send-button"]'))
        await asyncio.sleep(SLEEP)
        #
        # response = await process_new_responses(self.page)
        # await asyncio.sleep(SLEEP)

        # await self.actor_system.publish(ChatGPTResponse(content=response))
        # await asyncio.sleep(SLEEP)
        # print(send_cmd.prompt)

    async def handle_chatgpt_response(self, response: ChatGPTResponse) -> None:
        logger.info(f"ChatGPT response:\n\n{response}")

    async def handle_find_element(self, find_element_cmd: FindElement) -> None:
        # Implement code to find the element and send ElementFound event
        element_info = await self.page.querySelector(find_element_cmd.selector)
        if element_info:
            await self.publish(ElementFound(content=element_info))
        else:
            # Handle the case when the element is not found
            pass

    async def handle_navigate_back(self, navigate_back_cmd: NavigateBack) -> None:
        await self.page.goBack()
        # Optionally, send a navigation event indicating the back action

    async def handle_navigate_forward(
        self, navigate_forward_cmd: NavigateForward
    ) -> None:
        await self.page.goForward()
        # Optionally, send a navigation event indicating the forward action

    async def handle_reload_page(self, reload_page_cmd: ReloadPage) -> None:
        await self.page.reload()
        # Optionally, send an event indicating that the page has been reloaded

    async def handle_get_page_content(
        self, get_page_content_cmd: GetPageContent
    ) -> None:
        page_content = await self.page.content()
        await self.publish(PageContent(content=page_content))

    async def handle_execute_script(self, execute_script_cmd: ExecuteScript) -> None:
        script_result = await self.page.evaluate(execute_script_cmd.script)
        await self.publish(ScriptResult(result=script_result))

    async def handle_close_browser(self, close_browser_cmd: CloseBrowser) -> None:
        await self.ctx.browser.close()
        await self.publish(BrowserClosed())

    async def handle_set_viewport_size(
        self, set_viewport_size_cmd: SetViewportSize
    ) -> None:
        await self.page.setViewport(
            size={
                "width": set_viewport_size_cmd.width,
                "height": set_viewport_size_cmd.height,
            }
        )
        await self.publish(ViewportSizeSet())


async def main():
    # List of prompts for generating documents

    if not is_command_running(command_to_check):
        print("Starting linkedin browser worker")
        process = await start_chrome_canary()
    else:
        print("Process already running")

    await asyncio.sleep(1)

    async with async_playwright() as p:
        # Connect to an existing instance of Chrome using the connect_over_cdp method.
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")

        # Retrieve the first context of the browser.
        default_context = browser.contexts[0]

        # Retrieve the first page in the context.
        page = default_context.pages[0]

        await page.goto(LINKEDIN_JOBS_ALERTS_URL)

        asys = ActorSystem()

        actor = await asys.actor_of(BrowserWorker, browser=browser, page=page)

        # List of prompts for generating documents
        prompts = [
            "Creating Interactive Data Dashboards: Develop a guide on using streamlitgen to create interactive data dashboards in Streamlit, including real-time updates and user-friendly charts.",
            "Implementing Chatbot Integration: Innovate with a chatbot integration feature in streamlitgen that allows developers to add chatbots to Streamlit apps for enhanced user interaction.",
            "Enhancing Accessibility: Explain how to make Streamlit apps more accessible to users with disabilities using streamlitgen, covering features like screen readers and keyboard navigation.",
            "Real-Time Data Streaming: Document the process of integrating real-time data streaming capabilities into Streamlit apps using streamlitgen, including data source connections and visualization.",
            "Multi-Language Support: Provide instructions on adding multi-language support to Streamlit apps with streamlitgen, accommodating a global user base.",
            "Creating Dynamic Forms: Develop a guide on using streamlitgen to create dynamic and customizable input forms in Streamlit apps, improving user interaction.",
            "Automated Report Generation: Innovate with an automated report generation feature in streamlitgen that enables users to generate professional reports directly from Streamlit apps.",
            "Enhancing Security: Explain best practices for enhancing the security of Streamlit apps using streamlitgen, covering authentication, encryption, and data protection.",
            "Gamification Features: Introduce gamification elements in streamlitgen for creating engaging Streamlit applications with game-like features.",
            "Geospatial Data Visualization: Document how to leverage geospatial data visualization capabilities in Streamlit apps with streamlitgen, including mapping libraries and geospatial data sources.",
            "Streamlit Mobile App Development: Provide a guide on using streamlitgen to develop mobile applications with Streamlit, optimizing layouts and interactions for mobile devices.",
            "Creating Custom Themes: Explain how to create and apply custom themes to Streamlit apps using streamlitgen, allowing for unique and branded app designs.",
            "User Feedback Integration: Innovate with a user feedback integration feature in streamlitgen that enables users to provide feedback directly within Streamlit apps for continuous improvement.",
            "Machine Vision Integration: Document the process of integrating machine vision and image recognition capabilities into Streamlit apps using streamlitgen.",
            "Enhanced Error Handling: Explain best practices for error handling and reporting in Streamlit apps using streamlitgen, ensuring a smooth user experience.",
            "Streamlit Widgets Development: Develop a guide on creating custom Streamlit widgets with streamlitgen, expanding the range of interactive elements in Streamlit apps.",
            "Serverless Deployment: Provide instructions on deploying Streamlit apps as serverless functions using streamlitgen, optimizing scalability and cost-efficiency.",
            "IoT Sensor Data Integration: Explain how to integrate IoT sensor data streams with Streamlit apps using streamlitgen, enabling real-time monitoring and analysis.",
            "Streamlit Analytics Dashboard: Document the process of creating advanced analytics dashboards in Streamlit using streamlitgen, including data connectors and advanced visualizations.",
            "Enhancing User Onboarding: Innovate with a user onboarding feature in streamlitgen that guides new users through app features and functionalities."
            "Define Phase: Describe the importance of clearly defining the problem statement and project goals in a Lean Six Sigma project.",
            "Define Phase: Explain how to identify key stakeholders and gather their input during project initiation.",
            "Define Phase: Outline the steps involved in creating a project charter and its role in project management.",
            "Define Phase: Discuss the significance of defining critical-to-quality (CTQ) parameters in a process.",
            "Define Phase: Describe how to develop a high-level process map to understand the process flow.",
            "Measure Phase: Explain the concept of process capability and how it relates to the Measure phase.",
            "Measure Phase: Discuss the use of data collection plans and data validation in the measurement process.",
            "Measure Phase: Describe the various types of data (e.g., discrete, continuous) and their relevance in Lean Six Sigma.",
            "Measure Phase: Outline the steps to conduct a process capability analysis, including the calculation of Cp, Cpk, Pp, and Ppk.",
            "Measure Phase: Discuss the importance of sampling techniques and selecting the right sample size.",
            "Analyze Phase: Explain the role of data analysis in the Analyze phase of Lean Six Sigma.",
            "Analyze Phase: Describe common data visualization tools and their use in analyzing process data.",
            "Analyze Phase: Discuss hypothesis testing and its application to identify root causes of process variation.",
            "Analyze Phase: Explain techniques like Fishbone diagrams and Pareto analysis for root cause identification.",
            "Analyze Phase: Outline the steps for conducting regression analysis and correlation studies.",
            "Improve Phase: Describe the purpose and principles of brainstorming in Lean Six Sigma projects.",
            "Improve Phase: Explain the concept of Design of Experiments (DOE) and its role in process optimization.",
            "Improve Phase: Discuss strategies for generating and evaluating potential solutions to process problems.",
            "Improve Phase: Outline the steps involved in implementing and piloting process improvements.",
            "Improve Phase: Describe how to develop a control plan to sustain process improvements over time.",
            "Control Phase: Explain the importance of standardization and control in the final phase of Lean Six Sigma.",
            "Control Phase: Discuss the elements of a control plan, including control charts, process monitoring, and response planning.",
            "Control Phase: Describe how to establish process controls and create visual management tools.",
            "Control Phase: Explain the significance of mistake-proofing (poka-yoke) in maintaining process stability.",
            "Control Phase: Discuss the handover process and documentation for the successful completion of a Lean Six Sigma project.",
        ]

        # Broadcast SendChatGPT events for each prompt
        for prompt in prompts:
            url = "https://chat.openai.com/g/g-JWcKIFe74-bucky-v10133/c/28ccc59a-0dc5-46da-9dee-f37d71781beb"
            # url = "https://chat.openai.com/"
            await asys.publish(Goto(url=url))
            await asyncio.sleep(3)
            await asys.publish(
                SendChatGPT(
                    prompt=f"Write the chapter contents like a Python enterprise architect MBBB. Full text not a summary. {prompt}. Create chapter using streamlitgen and TRIZ methodology. Combine this with the rest of what we have discussed to synthesize innovation implementation and deployment using CLI help. Add detailed section on adding to marketplace and generating revenue."
                )
            )
            await asyncio.sleep(90)

        while True:
            await asyncio.sleep(1)

        links = await page.query_selector_all(".job-card-container__link")

        for link in links:
            await link.click()


if __name__ == "__main__":
    asyncio.run(main())
