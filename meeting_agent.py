import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai.process import Process
from crewai_tools import SerperDevTool
import os

# Streamlit app setup
st.set_page_config(page_title="AI Meeting Agent 📝", layout="wide")
st.title("AI Meeting Preparation Agent 📝")

# Sidebar for API keys
st.sidebar.header("API Keys")
anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

# Check if all API keys are set
if anthropic_api_key and serper_api_key:
    # # Set API keys as environment variables
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    claude = LLM(model="claude-sonnet-4-20250514", temperature= 0.7, api_key=anthropic_api_key)
    search_tool = SerperDevTool()

    # Input fields - Your Company Context
    st.header("Your Company Details")
    your_company_name = st.text_input("Your Company Name:", help="Enter your organization's name")
    your_company_description = st.text_area(
        "Your Company Description:", 
        help="Briefly describe what your company does, key products/services, and unique value proposition",
        height=100
    )
    
    # Meeting Perspective
    meeting_perspective = st.radio(
        "Your Role in This Meeting:",
        ["Provider/Seller (We are pitching or offering services)", 
         "Customer/Buyer (We are evaluating or purchasing services)"],
        help="This helps tailor the strategy to your position in the negotiation"
    )
    
    st.header("Meeting Details")
    company_name = st.text_input("Client Company Name:", help="The company you're meeting with")
    meeting_objective = st.text_input("Meeting Objective:", help="e.g., 'Content partnership deal', 'Vendor evaluation'")
    attendees = st.text_area("Attendees and Their Roles (one per line):", help="Include names and titles")
    meeting_duration = st.number_input("Meeting Duration (minutes):", min_value=15, max_value=180, value=60, step=15)
    focus_areas = st.text_input("Specific Areas of Focus or Concerns:", help="e.g., 'Pricing', 'Technical integration', '3D rendering quality'")

    # Define perspective-specific context
    if "Provider/Seller" in meeting_perspective:
        perspective_context = f"""
        CRITICAL CONTEXT: You are preparing for a meeting where YOUR COMPANY ({your_company_name}) is the PROVIDER/SELLER.
        Your company offers: {your_company_description}
        
        Your goal is to:
        1. Identify gaps or pain points at {company_name} that YOUR company can solve
        2. Position YOUR capabilities as solutions to THEIR challenges
        3. Prepare responses that showcase YOUR value proposition
        4. Anticipate objections they might have about price, quality, or capabilities
        5. Build a persuasive narrative for why they should choose YOU
        """
    else:
        perspective_context = f"""
        CRITICAL CONTEXT: You are preparing for a meeting where YOUR COMPANY ({your_company_name}) is the CUSTOMER/BUYER.
        Your company needs: {your_company_description}
        
        Your goal is to:
        1. Evaluate if {company_name} can reliably meet YOUR requirements
        2. Identify potential risks, quality issues, or red flags
        3. Prepare tough questions to vet THEIR capabilities
        4. Understand negotiation leverage points for pricing and terms
        5. Build criteria to determine if THEY are the right partner for YOU
        """

    # Define the agents
    context_analyzer = Agent(
        role='Meeting Context Specialist',
        goal='Analyze and summarize key background information for the meeting',
        backstory='You are an expert at quickly understanding complex business contexts and identifying critical information.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
        tools=[search_tool]
    )

    industry_insights_generator = Agent(
        role='Industry Expert',
        goal='Provide in-depth industry analysis and identify key trends',
        backstory='You are a seasoned industry analyst with a knack for spotting emerging trends and opportunities.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
        tools=[search_tool]
    )

    strategy_formulator = Agent(
        role='Meeting Strategist',
        goal='Develop a tailored meeting strategy and detailed agenda',
        backstory='You are a master meeting planner, known for creating highly effective strategies and agendas.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
    )

    executive_briefing_creator = Agent(
        role='Communication Specialist',
        goal='Synthesize information into concise and impactful briefings',
        backstory='You are an expert communicator, skilled at distilling complex information into clear, actionable insights.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
    )

    # Define the tasks
    context_analysis_task = Task(
        description=f"""
        {perspective_context}
        
        Analyze the context for the meeting with {company_name}, considering:
        1. The meeting objective: {meeting_objective}
        2. The attendees: {attendees}
        3. The meeting duration: {meeting_duration} minutes
        4. Specific focus areas or concerns: {focus_areas}
        
        YOUR COMPANY CONTEXT:
        - Company Name: {your_company_name}
        - What We Do: {your_company_description}
        - Our Role: {"We are offering/selling services" if "Provider/Seller" in meeting_perspective else "We are evaluating/buying services"}

        Research {company_name} thoroughly, including:
        1. Recent news and press releases
        2. Key products or services
        3. Major competitors
        4. Financial stability and market position
        
        CRITICAL: Frame all findings in terms of how they relate to OUR position. If we are the seller, identify their pain points. If we are the buyer, identify their reliability indicators.
        
        Provide a comprehensive summary of your findings, highlighting the most relevant information for the meeting context.
        Format your output using markdown with appropriate headings and subheadings.
        """,
        agent=context_analyzer,
        expected_output="A detailed analysis of the meeting context and company background, including recent developments, financial performance, and relevance to the meeting objective from YOUR company's perspective, formatted in markdown with headings and subheadings."
    )

    industry_analysis_task = Task(
        description=f"""
        {perspective_context}
        
        Based on the context analysis for {company_name} and the meeting objective: {meeting_objective}, provide an in-depth industry analysis:
        1. Identify key trends and developments in the industry
        2. Analyze the competitive landscape
        3. Highlight potential opportunities and threats
        4. Provide insights on market positioning
        
        YOUR COMPANY CONTEXT:
        - Company Name: {your_company_name}
        - What We Do: {your_company_description}
        - Our Role: {"We are offering/selling services" if "Provider/Seller" in meeting_perspective else "We are evaluating/buying services"}

        CRITICAL: If we are the SELLER, identify market gaps where OUR solution fits. If we are the BUYER, identify market risks or better alternatives we should consider.
        
        Ensure the analysis is relevant to the meeting objective and attendees' roles.
        Format your output using markdown with appropriate headings and subheadings.
        """,
        agent=industry_insights_generator,
        expected_output="A comprehensive industry analysis report from YOUR company's perspective, including trends, competitive landscape, opportunities, threats, and strategic positioning for YOUR role in the partnership, formatted in markdown with headings and subheadings."
    )

    strategy_development_task = Task(
        description=f"""
        {perspective_context}
        
        Using the context analysis and industry insights, develop a tailored meeting strategy and detailed agenda for the {meeting_duration}-minute meeting with {company_name}. Include:
        1. A time-boxed agenda with clear objectives for each section
        2. Key talking points for each agenda item
        3. Suggested speakers or leaders for each section
        4. Potential discussion topics and questions to drive the conversation
        5. Strategies to address the specific focus areas and concerns: {focus_areas}
        
        YOUR COMPANY CONTEXT:
        - Company Name: {your_company_name}
        - What We Do: {your_company_description}
        - Our Role: {"We are offering/selling services" if "Provider/Seller" in meeting_perspective else "We are evaluating/buying services"}

        CRITICAL STRATEGY ALIGNMENT:
        {"- Focus on building rapport and demonstrating value proposition" if "Provider/Seller" in meeting_perspective else "- Focus on due diligence questions and negotiation leverage"}
        {"- Allocate time for handling objections and closing" if "Provider/Seller" in meeting_perspective else "- Allocate time for technical vetting and pricing negotiation"}
        {"- Position YOUR company as the solution to THEIR problems" if "Provider/Seller" in meeting_perspective else "- Position YOUR requirements and ensure THEY can meet YOUR standards"}

        Ensure the strategy and agenda align with the meeting objective: {meeting_objective}
        Format your output using markdown with appropriate headings and subheadings.
        """,
        agent=strategy_formulator,
        expected_output="A detailed meeting strategy and time-boxed agenda optimized for YOUR role (seller or buyer), including objectives, key talking points, and role-specific strategies, formatted in markdown with headings and subheadings."
    )

    executive_brief_task = Task(
        description=f"""
        {perspective_context}
        
        Synthesize all the gathered information into a comprehensive yet concise executive brief for the meeting with {company_name}. Create the following components:

        1. A detailed one-page executive summary including:
           - Clear statement of the meeting objective
           - YOUR COMPANY ({your_company_name}) overview and what you bring to the table
           - THEIR COMPANY ({company_name}) background and key attendees
           - Critical intelligence about {company_name} and relevant industry context
           - Top 3-5 strategic goals for the meeting FROM YOUR PERSPECTIVE
           - Brief overview of the meeting structure and key topics to be covered

        2. An in-depth list of key talking points, each supported by:
           - Relevant data or statistics
           - Specific examples or case studies
           - {"How YOUR capabilities solve THEIR problems" if "Provider/Seller" in meeting_perspective else "How THEIR capabilities meet YOUR requirements"}
           - {"Value proposition and differentiation from competitors" if "Provider/Seller" in meeting_perspective else "Due diligence points and risk assessment"}

        3. Anticipate and prepare for potential questions:
           {"- Questions THEY will ask YOU about pricing, capabilities, timeline, and guarantees" if "Provider/Seller" in meeting_perspective else "- Questions YOU should ask THEM about quality, reliability, support, and references"}
           - Craft thoughtful, data-driven responses to each question
           - {"Prepare objection handling for common concerns" if "Provider/Seller" in meeting_perspective else "Prepare tough vetting questions with specific metrics"}
           - Include any supporting information or additional context that might be needed

        4. Strategic recommendations and next steps:
           - Provide 3-5 actionable recommendations based on the analysis
           - {"Clear path to closing the deal or securing commitment" if "Provider/Seller" in meeting_perspective else "Clear evaluation criteria and vendor selection process"}
           - Outline clear next steps for implementation or follow-up
           - Suggest timelines or deadlines for key actions
           - Identify potential challenges or roadblocks and propose mitigation strategies
        
        YOUR COMPANY CONTEXT:
        - Company Name: {your_company_name}
        - What We Do: {your_company_description}
        - Our Role: {"PROVIDER/SELLER - We are pitching our solution" if "Provider/Seller" in meeting_perspective else "CUSTOMER/BUYER - We are evaluating their solution"}

        CRITICAL: The entire brief must be written from the perspective of {your_company_name} meeting with {company_name}. 
        {"All 'we/our' references should be about YOUR company selling TO them." if "Provider/Seller" in meeting_perspective else "All 'we/our' references should be about YOUR company buying FROM them."}
        
        Ensure the brief is comprehensive yet concise, highly actionable, and precisely aligned with the meeting objective: {meeting_objective}. 
        The document should be structured for easy navigation and quick reference during the meeting.
        Format your output using markdown with appropriate headings and subheadings.
        """,
        agent=executive_briefing_creator,
        expected_output="A comprehensive executive brief written from YOUR company's perspective, clearly distinguishing between YOUR role and THEIR role, including summary, key talking points optimized for your position (seller or buyer), Q&A preparation with role-appropriate questions, and strategic recommendations, formatted in markdown with main headings (H1), section headings (H2), and subsection headings (H3) where appropriate. Use bullet points, numbered lists, and emphasis (bold/italic) for key information."
    )

    # Create the crew
    meeting_prep_crew = Crew(
        agents=[context_analyzer, industry_insights_generator, strategy_formulator, executive_briefing_creator],
        tasks=[context_analysis_task, industry_analysis_task, strategy_development_task, executive_brief_task],
        verbose=True,
        process=Process.sequential
    )

    # Run the crew when the user clicks the button
    if st.button("Prepare Meeting"):
        with st.spinner("AI agents are preparing your meeting..."):
            result = meeting_prep_crew.kickoff()        
        st.markdown(result)

    st.sidebar.markdown("""
    ## How to use this app:
    1. Enter your API keys in the sidebar.
    2. Provide your company details and meeting perspective.
    3. Enter the client company information and meeting details.
    4. Click 'Prepare Meeting' to generate your comprehensive meeting preparation package.

    The AI agents will work together to:
    - Analyze the client company context and background
    - Provide industry insights and competitive positioning
    - Develop a tailored meeting strategy based on YOUR role (seller/buyer)
    - Create an executive brief with perspective-appropriate talking points

    This process may take a few minutes. Please be patient!
    """)
else:
    st.warning("Please enter all API keys in the sidebar before proceeding.")