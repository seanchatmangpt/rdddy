import dspy
from dspy import Signature, InputField, OutputField


class SparsePrimingRepresentation(Signature):
    """
    Create a distilled essence of input information as Sparse Priming Representation (SPR) for activating latent space in LLMs.
    """

    input_information = InputField(
        desc="Detailed information, concepts, or knowledge to be transformed."
    )
    latent_abilities_activation = InputField(
        desc="Target latent abilities or content in LLMs to be activated."
    )

    distilled_spr = OutputField(
        desc="Condensed SPR content comprising statements, assertions, associations, concepts, analogies, and metaphors."
    )


class SPRWriterSignature(Signature):
    """
    Transform detailed information into Sparse Priming Representation (SPR) for advanced NLP tasks.
    """

    input_information = InputField(desc="Detailed information provided by the user.")
    distilled_spr = OutputField(
        desc="Condensed list of statements, concepts, and metaphors for LLM priming."
    )


output = """Enterprise grade generative conversational AI framework and infrastructure suite, CALM system for 
contextual conversation understanding and dialogue management, Flows for simplifying dialogue management, Enterprise 
Search for rapid scope expansion, foundational capabilities for analytics, security, and observability, deployment 
options including on-premises or fully managed service, built-in Multi-Channel Connectors and OpenTelemetry-based 
tracing for integration and performance monitoring, conversation analytics pipeline and Real-Time Markers for 
tracking and visualizing performance."""


context = """RASA PRO

Elevate Your Conversational AI Excellence
An enterprise grade generative conversational AI framework and infrastructure suite to help you scale, secure, and monitor your AI assistant.

Talk with Sales
Simplify Complexity with CALM
CALM stands for Conversational AI with Language Models. It’s a generative AI native approach to building contextual AI assistants in Rasa Pro. With the core modules below, your AI Assistant can leverage language models to better understand and help your customers.

Dialogue Understanding
Cutting-edge contextual conversation understanding
Leverage language models to navigate nuanced customer journeys
Handle common conversational patterns such as digression, correction, and disambiguation out of the box
Contextual Dialogue Manager
Design and define user journeys and business processes with Flows
Together with Dialogue Understanding, activate, and navigate between Flows based on customer requests
Ensure customers are only exposed to pre-defined user journeys
CALM system
REPHRASE RESPONSES

Contextual Response Rephraser
Out of scope is now in scope. Try our Contextual Response Rephraser and never leave your users hanging again with the words “I don’t understand”.

Response Rephraser
Read more
SIMPLIFY DIALOGUE

Flows
Simplify Dialogue Management with Flows. Define user journeys in the form of modular step-by-step conversation flows that can be activated and linked with CALM.

Flows
Read more
EXPAND SCOPE WITH SEARCH

Enterprise Search
Expand your scope rapidly with Enterprise Search. Accurately answer questions in conversation from a knowledge base.


Read more
Foundational Rasa Pro Capabilities
Extend our open source framework with analytics, security and observability capabilities.

Secure
Enterprise-grade security and privacy controls to keep your data, and your customer’s data safe.

PII Data Management solution to secure customer data and remain compliant
Daily Security Scanning to ship regularly patched Docker images
Secrets Management powered by Vault

Test
Assess the quality of your Rasa Assistant performance to ensure each new release is confidently deployed with:

End-to-End Testing for comprehensive acceptance and integration testing
Load Testing Guidelines to demonstrate the resources required for Rasa Assistants operating at scale
E2E Testing flow
Deploy
Advance your deployment capabilities with Rasa Pro.

Deploy on-premises or in your private cloud with our Kubernetes Helm charts
Or choose Rasa-as-a-Service for a fully managed service running the Rasa Platform in your preferred cloud

Integrate
Built-in Multi-Channel Connectors plus endpoints to connect with databases, APIs, voice IVRs, and other data sources.


Observe
Resolve performance issues faster and identify bottlenecks through OpenTelemetry-based tracing.


Analyze
Track and visualize Rasa Assistant performance.

Use our conversation analytics pipeline to track assistant metrics in the tooling (BI tools, data warehouses) of your choice
Add Real-Time Markers to track key moments in your customer journeys for targeted analysis

RASA PRO
Rasa Pro Solution Sheet
Read more about all of the features and capabilities of Rasa Pro, our pro-code conversational AI framework and infrastructure suite.

Download the Solution Sheet"""


def main():
    lm = dspy.OpenAI(max_tokens=2000)
    dspy.settings.configure(lm=lm)

    cot = (
        dspy.ChainOfThought(SparsePrimingRepresentation)
        .forward(input_information=context)
        .distilled_spr
    )

    print(cot)


if __name__ == "__main__":
    main()
