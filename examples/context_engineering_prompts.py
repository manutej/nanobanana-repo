"""
Context Engineering Visual Prompts
Generated from comprehensive research for webinar on Context Engineering

These prompts create technical diagrams and architectural visualizations
for the webinar: "Your LLM App Isn't Failing Because of the Model.
It's Failing Because of the Context."
"""

CONTEXT_ENGINEERING_PROMPTS = [
    # 1. Context Engineering Stack
    """Technical architecture diagram showing 7 stacked rectangular layers with distinct colors and icons.
    From top to bottom: Layer 7 (blue) 'SYSTEM PROMPT' with gears icon, Layer 6 (purple) 'SEMANTIC CONTEXT'
    with knowledge graph icon, Layer 5 (green) 'RETRIEVED KNOWLEDGE RAG' with database icon, Layer 4 (yellow)
    'CONVERSATION MEMORY' with chat bubbles, Layer 3 (orange) 'TOOL CONTEXT' with wrench icon, Layer 2 (pink)
    'USER PREFERENCES' with user profile icon, Layer 1 (red) 'CURRENT QUERY' with question mark. Vertical arrow
    on right showing data flow from bottom to top. Clean modern professional style, white background.""",

    # 2. RAG 2.0 Pipeline
    """Horizontal flowchart diagram showing RAG 2.0 pipeline from left to right. Start with 'Query Input'
    rounded rectangle in blue, flowing to 'Query Understanding' box with bullet points, then splitting into
    parallel 'Semantic Search' green cylinder and 'Keyword Search' orange cylinder, converging to 'Fusion'
    purple diamond, then 'Reranking' gold rectangle with stars, 'Context Assembly' teal rectangle, 'Generation'
    pink cloud with brain icon, 'Validation' red shield icon, ending with 'Response' green rounded rectangle.
    Clean lines, modern icons, white background, professional technical style.""",

    # 3. Context Window Optimization
    """Side-by-side comparison diagram showing inefficient vs optimized context usage. LEFT: Large rectangle
    labeled 'Inefficient Context' with red border showing 30% gray 'Irrelevant Data', 25% light gray 'Redundant
    History', 20% medium gray 'All Tool Schemas', 15% green 'Useful Context', with Token Cost $0.50 and Latency
    3.2s below. RIGHT: Same sized rectangle labeled 'Optimized Context' with green border showing 50% bright
    green 'Relevant Data', 20% light green 'Summarized History', 15% medium green 'Relevant Tools', 10% blue
    'Cached System Prompt', with Token Cost $0.12 and Latency 0.8s below. Arrow between showing transformation.
    Modern clean style with clear color coding.""",

    # 4. MCP Architecture
    """Three-tier architecture diagram showing LLM integration via Model Context Protocol. TOP: Large rounded
    rectangle 'LLM Agent' in blue gradient containing Claude, GPT-4, Gemini text. MIDDLE: Purple gradient band
    'Model Context Protocol' with 'MCP Client', 'Protocol Layer', 'Discovery & Routing' connected by bidirectional
    arrows. BOTTOM: Five MCP servers in a row - 'Database Server' green cylinder icon, 'API Server' orange cloud
    icon, 'File System Server' yellow folder icon, 'Code Execution Server' red terminal icon, 'Email Server' blue
    envelope icon. Dotted lines connecting protocol layer to each server with security shield icons. Modern clean
    technical diagram style, white background.""",

    # 5. Lost in the Middle Effect
    """Horizontal bar diagram representing context window with attention heatmap. Top bar labeled 'Context Window
    10,000 tokens' divided into segments. Heatmap overlay: beginning 20% in bright green/yellow (high attention),
    middle 60% in orange to red gradient with warning icon and annotation 'Critical information placed here may be
    invisible', end 20% in bright green/yellow (high attention). Below: U-shaped graph showing 'Recall Probability'
    vs 'Position in Context' with danger zone shaded in middle. Clean data visualization style, clear color gradient,
    professional aesthetic.""",

    # 6. Memory Management Strategies
    """2x2 grid layout showing four memory management strategies. TOP LEFT: 'Sliding Window' with diagram of rectangle
    with moving window highlighted, Pros: Simple recent context, Cons: Loses old context. TOP RIGHT: 'Summarization'
    with multiple boxes compressing into smaller box, Pros: Preserves history saves tokens, Cons: Information loss.
    BOTTOM LEFT: 'Memory Blocks' with stacked labeled blocks with priority numbers, Pros: Structured prioritized,
    Cons: Complex implementation. BOTTOM RIGHT: 'Hybrid Window plus Summary' with compressed old blocks plus full
    recent blocks, Pros: Best of both production-ready, Cons: Moderate complexity. Each quadrant has icon, simple
    diagram, bullet points. Clean grid layout, consistent styling, white background.""",

    # 7. Agentic RAG Decision Flow
    """Flowchart showing adaptive retrieval strategy selection. Start: 'Query Input' blue rounded rectangle flows
    to 'Agent Assesses Complexity' purple diamond splitting into three branches. LEFT: 'Simple Query' green flows
    to 'Single-Shot Retrieval' to 'Generate Response' green rounded. MIDDLE: 'Complex Multi-Hop' orange flows to
    'Plan Multi-Step' to 'Execute Step 1' 'Execute Step 2' 'Execute Step 3' connected rectangles to 'Synthesize
    Results' to 'Generate Response' orange rounded. RIGHT: 'Ambiguous' yellow flows to 'Request Clarification' to
    'User Clarifies' oval to 'Targeted Retrieval' to 'Generate Response' yellow rounded. Each branch visually
    distinct color, clear decision points, modern flowchart style.""",

    # 8. Prompt Injection Security
    """Security diagram showing attack and defense layers. LEFT: 'Attack Vector' red theme with 'Malicious User Input'
    dark red box containing 'Ignore previous instructions' text, red arrow to 'Vulnerable System' red outline with
    compromised output and skull icon. CENTER: 'Defense Layers' with shield icon showing 5 colored shields stacked -
    Layer 1 blue 'Input Validation', Layer 2 green 'Boundary Markers', Layer 3 purple 'Instruction Hierarchy', Layer 4
    orange 'Output Validation', Layer 5 red 'Tool Permissions'. RIGHT: 'Secured System' green theme with 'Validated
    Input' light green box flowing to properly structured context to safe output with checkmark. Arrows showing attack
    blocked at each layer. Security-focused visual style.""",

    # 9. ROI Dashboard
    """Dashboard layout with 6 metric cards in 2 rows showing before/after context engineering. ROW 1: Card 1 'Cost
    per Request' Before $0.50 red After $0.12 green with down arrow 76%, Card 2 'Average Latency' Before 3.2s red
    After 0.9s green down 72%, Card 3 'Hallucination Rate' Before 18% red After 4% green down 78%. ROW 2: Card 4
    'User Satisfaction' Before 68% yellow After 89% green up 21%, Card 5 'Context Utilization' Before 45% orange
    After 87% green up 42%, Card 6 'Monthly Savings' $8,500 saved large green based on 50K requests per month.
    Clean dashboard style, clear metrics, green/red color coding for improvements.""",

    # 10. Tool Chaining Workflow
    """Horizontal workflow diagram showing tool chain execution. 'User Query' blue speech bubble 'Send promotional
    email to active CA customers' flows to 'Agent Plans Workflow' purple brain icon with numbered list: 1 Search
    users, 2 Get emails, 3 Send bulk email. Flows to TOOL 1 'search_users' green database icon Input 'active
    customers in California' Output 'user_ids: 1245 users' arrow to TOOL 2 'get_user_emails' orange contacts
    icon Input 'user_ids from Tool 1' Output 'emails: 1245 emails' arrow to TOOL 3 'send_bulk_email' red envelope
    icon Input 'emails from Tool 2 plus subject plus body' Output 'sent: 1245 emails' flows to 'Success Response'
    green checkmark 'Successfully sent to 1245 customers'. Data flow arrows between tools, each tool as rounded
    rectangle with icon and labeled inputs/outputs. Clean workflow diagram style.""",
]

if __name__ == "__main__":
    print(f"Total Context Engineering Prompts: {len(CONTEXT_ENGINEERING_PROMPTS)}")
    print("\nPrompts:")
    for i, prompt in enumerate(CONTEXT_ENGINEERING_PROMPTS, 1):
        print(f"\n{i}. {prompt[:100]}...")
