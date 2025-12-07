"""
Context Engineering Visual Prompts - PRO VERSION
Refined for Gemini 3 Pro Image with explicit text rendering requirements

Optimized for:
- Accurate text rendering (no misspellings)
- Clear visual hierarchy
- Minimal text, maximum clarity
- Professional technical diagram aesthetic
"""

CONTEXT_ENGINEERING_PROMPTS_PRO = [
    # 1. Context Engineering Stack (REFINED)
    """Professional technical diagram: Seven stacked horizontal bars forming a layer stack.
    Each bar has distinct color, icon on left, and label text on right.

    From TOP to BOTTOM:
    Bar 7: Blue (#2196F3) | Gear icon | Text: "SYSTEM PROMPT" (all caps, bold)
    Bar 6: Purple (#9C27B0) | Network icon | Text: "SEMANTIC CONTEXT" (all caps, bold)
    Bar 5: Green (#4CAF50) | Database icon | Text: "RETRIEVED KNOWLEDGE" (all caps, bold)
    Bar 4: Yellow (#FFC107) | Chat bubble icon | Text: "CONVERSATION MEMORY" (all caps, bold)
    Bar 3: Orange (#FF9800) | Wrench icon | Text: "TOOL CONTEXT" (all caps, bold)
    Bar 2: Pink (#E91E63) | User icon | Text: "USER PREFERENCES" (all caps, bold)
    Bar 1: Red (#F44336) | Question mark icon | Text: "CURRENT QUERY" (all caps, bold)

    Right side: Vertical upward arrow labeled "Context Assembly Flow"
    White background, clean modern style, high contrast text.""",

    # 2. RAG 2.0 Pipeline (REFINED)
    """Horizontal flowchart showing RAG pipeline, left to right with 8 connected boxes:

    Box 1: Blue rounded rectangle | Text: "Query Input"
    Box 2: Purple rectangle | Text: "Query Understanding" | Subtext: "Intent + Entities"
    Box 3: Green cylinder | Text: "Semantic Search"
    Box 4: Orange cylinder | Text: "Keyword Search"
    Box 5: Purple diamond | Text: "Fusion" (merge point from boxes 3+4)
    Box 6: Gold rectangle | Text: "Reranking" | Star icons
    Box 7: Teal rectangle | Text: "Context Assembly"
    Box 8: Green rounded rectangle | Text: "Response Generation"

    Arrows connect each step. Clean technical flowchart style, white background.""",

    # 3. Context Optimization Comparison (REFINED)
    """Side-by-side bar chart comparison with two vertical bars:

    LEFT BAR (Inefficient):
    Title: "Before Optimization"
    Red border, divided into 4 segments:
    - Top 30%: Dark gray | Label: "Irrelevant Data"
    - Next 25%: Gray | Label: "Redundant History"
    - Next 30%: Light gray | Label: "All Tool Schemas"
    - Bottom 15%: Light green | Label: "Useful Context"
    Footer: "Cost: $0.50 | Latency: 3.2s" (red text)

    RIGHT BAR (Optimized):
    Title: "After Optimization"
    Green border, divided into 4 segments:
    - Top 50%: Bright green | Label: "Relevant Data"
    - Next 20%: Medium green | Label: "Summarized History"
    - Next 15%: Light green | Label: "Relevant Tools Only"
    - Bottom 15%: Blue | Label: "Cached System Prompt"
    Footer: "Cost: $0.12 | Latency: 0.8s" (green text)

    Large arrow between bars labeled "76% cost reduction"
    White background, clear labels, high contrast.""",

    # 4. MCP Three-Tier Architecture (REFINED)
    """Three-tier architecture diagram, top to bottom:

    TIER 1 (Top): Large blue gradient box labeled "LLM Agent"
    Inside: Three model names: "Claude | GPT-4 | Gemini" (evenly spaced)

    TIER 2 (Middle): Purple gradient band labeled "Model Context Protocol (MCP)"
    Three connected components: "Client" → "Protocol Layer" → "Discovery"
    Bidirectional arrows between components

    TIER 3 (Bottom): Five MCP servers in a row:
    Server 1: Green database icon | Label: "Database"
    Server 2: Orange cloud icon | Label: "API"
    Server 3: Yellow folder icon | Label: "Files"
    Server 4: Red terminal icon | Label: "Code"
    Server 5: Blue envelope icon | Label: "Email"

    Dotted lines connect MCP layer to each server
    Security shield icons on each connection
    White background, clean modern style.""",

    # 5. Attention Heatmap (REFINED)
    """Horizontal bar diagram showing attention pattern:

    Top: Single horizontal bar (1000px wide, 100px tall) representing context window
    Label above: "Context Window: 10,000 tokens"

    Bar divided into regions with gradient overlay:
    - Left 20%: Bright green/yellow gradient | Label: "High Attention"
    - Middle 60%: Orange to red gradient | Label: "Low Attention (Lost in Middle)"
    - Right 20%: Bright green/yellow gradient | Label: "High Attention"

    Warning icon in middle section with text: "Critical info placed here may be invisible"

    Below: U-shaped graph showing "Recall Probability" (y-axis) vs "Position in Context" (x-axis)
    Danger zone (middle) shaded red

    Clean data visualization style, clear labels.""",

    # 6. Memory Strategies Grid (REFINED)
    """2x2 grid layout with four memory management approaches:

    TOP LEFT:
    Title: "Sliding Window"
    Icon: Rectangle with moving highlight window
    Pro: "Simple, recent context" (green checkmark)
    Con: "Loses old data" (red X)

    TOP RIGHT:
    Title: "Summarization"
    Icon: Multiple boxes compressing into one
    Pro: "Preserves history" (green checkmark)
    Con: "Information loss" (red X)

    BOTTOM LEFT:
    Title: "Memory Blocks"
    Icon: Stacked blocks with priority numbers
    Pro: "Structured, prioritized" (green checkmark)
    Con: "Complex setup" (red X)

    BOTTOM RIGHT:
    Title: "Hybrid (Best)"
    Icon: Compressed old blocks plus full recent blocks
    Pro: "Production-ready" (green checkmark)
    Pro: "Best of both worlds" (green checkmark)

    Each quadrant: white background, clear borders, consistent icons.""",

    # 7. Agentic RAG Decision Tree (REFINED)
    """Flowchart showing adaptive retrieval:

    Start: Blue rounded box | Text: "Query Input"
    ↓
    Decision: Purple diamond | Text: "Assess Complexity"

    Three branches:

    LEFT BRANCH (Simple):
    Green path → Box: "Single-Shot Retrieval" → Box: "Generate Response" → End

    MIDDLE BRANCH (Complex):
    Orange path → Box: "Plan Multi-Step" → Three sequential boxes:
    "Step 1: Retrieve" → "Step 2: Retrieve" → "Step 3: Retrieve"
    → Box: "Synthesize Results" → Box: "Generate Response" → End

    RIGHT BRANCH (Ambiguous):
    Yellow path → Box: "Request Clarification" → Oval: "User Clarifies"
    → Box: "Targeted Retrieval" → Box: "Generate Response" → End

    Each path uses distinct color throughout
    Clear arrows, simple boxes, white background.""",

    # 8. Security Layers Diagram (REFINED)
    """Security diagram showing attack vs defense:

    LEFT SIDE (Attack):
    Red theme
    Box: "Malicious Input" | Contains: "Ignore previous instructions..."
    Red arrow pointing right →
    Box: "Vulnerable System" | Red outline | Skull icon

    CENTER (Defense):
    Five layered shields (stacked):
    Shield 1 (Blue): "Input Validation"
    Shield 2 (Green): "Boundary Markers"
    Shield 3 (Purple): "Instruction Hierarchy"
    Shield 4 (Orange): "Output Validation"
    Shield 5 (Red): "Tool Permissions"

    Red attack arrow hits shields, blocked ✗

    RIGHT SIDE (Secured):
    Green theme
    Box: "Validated Input" | Green outline
    Green arrow →
    Box: "Protected System" | Green checkmark icon

    Clear color coding: red = danger, green = safe.""",

    # 9. ROI Metrics Dashboard (REFINED)
    """Dashboard with 6 metric cards in 2 rows:

    ROW 1:
    Card 1: "Cost per Request"
    Before: $0.50 (red, large)
    After: $0.12 (green, large)
    Change: ↓ 76% (green arrow)

    Card 2: "Average Latency"
    Before: 3.2s (red)
    After: 0.9s (green)
    Change: ↓ 72% (green arrow)

    Card 3: "Hallucination Rate"
    Before: 18% (red)
    After: 4% (green)
    Change: ↓ 78% (green arrow)

    ROW 2:
    Card 4: "User Satisfaction"
    Before: 68% (orange)
    After: 89% (green)
    Change: ↑ 21% (green arrow)

    Card 5: "Context Utilization"
    Before: 45% (orange)
    After: 87% (green)
    Change: ↑ 42% (green arrow)

    Card 6: "Monthly Savings"
    Amount: $8,500 (large green text)
    Subtext: "Based on 50K requests/month"

    Clean dashboard grid, white background, clear metrics.""",

    # 10. Tool Chaining Sequence (REFINED)
    """Horizontal workflow diagram showing tool chain:

    Start: Blue speech bubble | Text: "User: Send email to CA customers"
    ↓
    Box: "Agent Plans" | Purple background
    List inside:
    "1. Search users"
    "2. Get emails"
    "3. Send bulk email"
    ↓

    TOOL 1: Green rounded box | Database icon
    Label: "search_users"
    Input: "active, CA"
    Output: "1,245 user IDs" →

    TOOL 2: Orange rounded box | Contacts icon
    Label: "get_user_emails"
    Input: "1,245 IDs"
    Output: "1,245 emails" →

    TOOL 3: Red rounded box | Envelope icon
    Label: "send_bulk_email"
    Input: "1,245 emails + message"
    Output: "Sent: 1,245" →

    End: Green rounded box | Checkmark icon
    Text: "Success: 1,245 emails sent"

    Clear data flow arrows, labeled inputs/outputs, white background.""",
]

# Prompting best practices applied:
# 1. Explicit text spelling ("SYSTEM PROMPT" all caps, bold)
# 2. Clear color specifications (#HEX codes)
# 3. Exact icon descriptions
# 4. Precise layout instructions
# 5. Reduced text complexity
# 6. High contrast requirements
# 7. Clean backgrounds specified

if __name__ == "__main__":
    print(f"Total PRO Prompts: {len(CONTEXT_ENGINEERING_PROMPTS_PRO)}")
    print("\nRefined for Gemini 3 Pro Image:")
    print("- Explicit text rendering requirements")
    print("- Clear color specifications")
    print("- Precise icon and layout instructions")
    print("- High contrast, minimal text")
    for i, prompt in enumerate(CONTEXT_ENGINEERING_PROMPTS_PRO, 1):
        print(f"\n{i}. {prompt[:80]}...")
