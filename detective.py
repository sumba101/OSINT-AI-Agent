"""
OSINT Detective Agent

An AI-powered OSINT investigation tool using Claude Agent SDK.
Investigates individuals based on email addresses and usernames using:
- Holehe: Email-to-account discovery
- Sherlock: Username-to-social-media mapping  
- GHunt: Gmail account intelligence

Usage:
    python detective.py "Investigate user john_doe with email john@gmail.com"
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# Load environment variables
load_dotenv()

# Ensure output directories exist
Path("output").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# System prompt for the OSINT Detective Agent
SYSTEM_PROMPT = """You are an OSINT (Open Source Intelligence) Detective Agent.

Your mission: Investigate individuals based on email addresses and/or usernames provided, then generate a comprehensive intelligence report.

## CRITICAL FIRST STEP: TOOL VERIFICATION

Before doing ANYTHING else, you MUST verify that ALL THREE CLI tools are installed and accessible.

Run these commands one by one:
1. holehe --help
2. sherlock --help
3. ghunt --help

### Interpreting Results

**Tool IS available**: You'll see help documentation with usage, options, etc.

**Tool is NOT available**: You'll see error messages like:
- "'holehe' is not recognized as an internal or external command" (Windows CMD)
- "The term 'holehe' is not recognized as the name of a cmdlet" (PowerShell)
- "holehe: command not found" (Linux/Mac)

### MANDATORY REQUIREMENT: ALL TOOLS MUST BE AVAILABLE

If ANY of the three tools (holehe, sherlock, ghunt) is not available:

1. **STOP IMMEDIATELY** - Do not proceed with the investigation
2. **Report clearly** which tool(s) are missing
3. **Provide installation instructions**:
   - holehe: `pip install holehe`
   - sherlock: `pip install sherlock-project`
   - ghunt: `pip install ghunt` then run `ghunt login`
4. **End your response** - Do not attempt partial investigation

Example error response format:
```
❌ INVESTIGATION CANNOT PROCEED

Tool Availability Check:
- ✅ holehe: Available
- ❌ sherlock: NOT INSTALLED
- ✅ ghunt: Available

Missing tool(s): sherlock

Installation instructions:
  pip install sherlock-project

Please install all missing tools and run the investigation again.
```

---

## IF ALL TOOLS ARE AVAILABLE: Investigation Protocol

Once all tools are verified, follow the detailed investigation procedures documented in the OSINT Investigation Skill (SKILL.md).

### Your Investigation Should:

1. **Extract identifiers** from the user query (emails, usernames)
2. **Run appropriate CLI tools** following SKILL.md procedures
3. **Save all outputs to files** in the output/ directory
4. **Read and analyze** all output files, including any JSON files created by GHunt
5. **Apply filters** to remove false positives (see SKILL.md blacklist)
6. **Generate comprehensive report** in reports/ directory following the template in SKILL.md

### Intelligence Analysis Expectations:

Your final report should demonstrate deep analytical thinking:

- **Location Intelligence**: Use GHunt map review locations and calendar data to deduce:
  - Places the person has been or frequently visits
  - Travel patterns and frequency (heavy traveler vs. local)
  - Geographic home base or areas of activity
  - Potential work/home locations based on review patterns

- **Interest & Occupation Profiling**: Analyze discovered accounts/domains to infer:
  - Hobbies and interests (gaming, photography, fitness, etc.)
  - Professional field or occupation (if domains are highly indicative like GitHub, LinkedIn, industry forums)
  - Skill levels and expertise areas
  - Community involvement and social patterns

- **Cross-Platform Patterns**: Identify connections and consistencies across different data sources

Support all conclusions with specific evidence from the collected data. Be analytical, not just descriptive.
"""


async def run_investigation(query: str):
    """Run the OSINT investigation agent."""
    
    # Configure agent options
    options = ClaudeAgentOptions(
        model="claude-haiku-4-20250514",  # Claude Haiku 4.5
        # model="claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 (alternative for complex investigations)
        permission_mode="bypassPermissions",  # No human approval needed for tool execution
        setting_sources=["project"],           # Load skills from .claude/skills/
        allowed_tools=["Bash", "Write", "Read", "Glob", "Grep"],
        system_prompt=SYSTEM_PROMPT
    )
    
    print()
    print("=" * 60)
    print("  🔍 OSINT Detective Agent")
    print("=" * 60)
    print(f"\nQuery: {query}")
    print()
    print("-" * 60)
    print()
    
    try:
        async with ClaudeSDKClient(options=options) as client:
            # Send the query to the agent
            await client.query(prompt=query)
            
            # Stream and process the response
            async for message in client.receive_response():
                msg_type = type(message).__name__
                
                if msg_type == "AssistantMessage":
                    # Print text content from assistant
                    if hasattr(message, "content"):
                        for block in message.content:
                            if hasattr(block, "text"):
                                print(block.text, end="", flush=True)
                
                elif msg_type == "ToolUseMessage":
                    # Show which tool is being used
                    tool_name = getattr(message, "name", "unknown")
                    print(f"\n🔧 Using tool: {tool_name}", flush=True)
                
                elif msg_type == "ToolResultMessage":
                    print("   ✓ Complete", flush=True)
        
        print()
        print("-" * 60)
        print("\n✅ Investigation complete.")
        print("   Check the reports/ directory for the final report.")
        print("   Check the output/ directory for raw tool outputs.")
        
    except Exception as e:
        print(f"\n❌ Error during investigation: {e}")
        raise


def main():
    """Main entry point."""
    
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print()
        print("❌ Error: ANTHROPIC_API_KEY not found.")
        print()
        print("Please set your API key:")
        print("  - Create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        print("  - Or set environment variable: export ANTHROPIC_API_KEY=your-key")
        print()
        print("Get your API key at: https://console.anthropic.com/settings/keys")
        print()
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print()
        print("OSINT Detective Agent")
        print("=" * 40)
        print()
        print("Usage:")
        print('  python detective.py "<investigation query>"')
        print()
        print("Examples:")
        print('  python detective.py "Investigate user john_doe with email johndoe@gmail.com"')
        print('  python detective.py "Find information on email test@example.com"')
        print('  python detective.py "Profile the username cyber_sleuth"')
        print()
        sys.exit(1)
    
    # Get the query from command line
    query = sys.argv[1]
    
    # Run the investigation
    asyncio.run(run_investigation(query))


if __name__ == "__main__":
    main()