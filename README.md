# OSINT Detective Agent

> **Harnessing frontier AI models to revolutionize open-source intelligence gathering and analysis**

An autonomous AI agent powered by Claude that conducts sophisticated OSINT investigations, combining multiple intelligence-gathering tools to profile individuals across the internet. This project explores how cutting-edge language models can orchestrate complex investigative workflows, synthesize disparate data sources, and generate actionable intelligence—capabilities that improve with each generation of frontier models.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## Purpose

**OSINT Detective Agent** demonstrates the transformative potential of AI agents in intelligence gathering and analysis. By equipping autonomous agents with professional OSINT tools, we're exploring:

- **AI-powered investigation workflows**: How frontier models can orchestrate multi-tool investigations autonomously
- **Emergent analytical capabilities**: Leveraging the increasing intelligence of models like Claude to discover patterns, make deductions, and generate insights that go beyond simple data aggregation
- **Scalable intelligence**: As we add more tools and techniques, more capable models unlock proportionally better detective work and profiling

**The Vision**: Continue expanding the agent's toolkit—adding geolocation analysis, image intelligence, and advanced profiling techniques—so that as AI models grow more sophisticated, they can conduct investigations rivaling human analysts.

---

## Features

### Current Capabilities

- **Email Intelligence**: Discover all online accounts associated with an email address
- **Username Tracking**: Map social media presence across 400+ platforms
- **Gmail Deep Dive**: Extract Google account metadata, map reviews, calendar events, and activity patterns
- **Intelligent Analysis**: AI-driven profiling that deduces:
  - Geographic locations and travel patterns from review data
  - Interests, hobbies, and potential occupation from platform choices
  - Behavioral patterns and online activity levels
- **Comprehensive Reports**: Auto-generated markdown investigation reports with cross-referenced findings
- **False Positive Filtering**: Smart filtering of known unreliable results

### Why These Tools?

After extensive testing of dozens of OSINT packages and frameworks, **Holehe**, **Sherlock**, and **GHunt** emerged as the gold standard:

- **Low false negative rates** - They actually find what's there
- **Active maintenance** - Regularly updated to counter platform changes
- **Proven reliability** - Battle-tested in real-world OSINT operations
- **Complementary coverage** - Together they provide comprehensive internet footprint mapping

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- [pipx](https://pipx.pypa.io/) (recommended for Sherlock)
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Installation

#### 1. Clone the Repository (with submodules)

```bash
git clone --recurse-submodules https://github.com/yourusername/osint-detective-agent.git
cd osint-detective-agent
```

> **Important**: GHunt is included as a submodule, so you **must** use `--recurse-submodules` when cloning.

#### 2. Install OSINT Tools

**Sherlock** (Username to Social Media):
```bash
pipx install sherlock-project
```

**Holehe** (Email to Accounts):
```bash
pip3 install holehe
```

**GHunt** (Gmail Intelligence):
```bash
cd GHunt
# Follow the installation instructions in GHunt/README.md
# You'll need to run `ghunt login` after installation to authenticate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure API Key

Create a `.env` file in the project root:

```bash
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

---

## Usage

### Basic Investigation

```bash
python detective.py "Investigate user john_doe with email johndoe@gmail.com"
```

### Example Queries

**Email-focused investigation:**
```bash
python detective.py "Profile the email target@example.com"
```

**Username-focused investigation:**
```bash
python detective.py "Find all social media for username cyber_sleuth"
```

**Combined investigation:**
```bash
python detective.py "Deep dive on user alice_wonder, email alice@gmail.com"
```

### What Happens During an Investigation

1. **Tool Verification**: Agent checks that all OSINT tools are installed
2. **Intelligence Gathering**: Runs Holehe, Sherlock, and GHunt in parallel
3. **Data Collection**: Saves all raw outputs to `output/` directory
4. **Analysis Phase**: AI reads and cross-references all data sources
5. **Report Generation**: Creates comprehensive markdown report in `reports/` directory

---

## Contributing

**Contributions are highly welcome!** This project is at the intersection of AI and security research—there's enormous potential for innovation.

### Priority Areas

1. **Image Analysis Integration**
   - Geolocation from photos (landmark recognition, metadata extraction)
   - Facial recognition integration
   - Visual OSINT tools (reverse image search APIs)

2. **Additional OSINT Tools**
   - Low false-negative rate is critical
   - Must be actively maintained
   - Should provide unique data not covered by existing tools

### Planned Enhancements

- Image Intelligence: Geolocation analysis from photos, facial recognition integration
- Leaked Credential Databases: Integration with breach aggregators (HaveIBeenPwned API)
- Phone Number Intelligence: Reverse phone lookup and carrier information
- Historical Snapshots: Wayback Machine integration for digital archaeology

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-capability`)
3. Make your changes with clear commit messages
4. Test thoroughly (especially tool reliability)
5. Submit a pull request with detailed description

**Guidelines:**
- Ensure any new tools have demonstrably low false negative rates
- Document tool selection rationale
- Update SKILL.md with new tool procedures
- Add error handling for tool failures

---

## Ethical Considerations & Legal Disclaimer

**This tool is for educational and authorized security research purposes only.**

### Responsible Use

- **DO**: Use for authorized penetration testing, security research, or investigating your own digital footprint
- **DO**: Obtain proper authorization before investigating individuals
- **DO**: Respect privacy laws and regulations in your jurisdiction
- **DON'T**: Use for stalking, harassment, or unauthorized surveillance
- **DON'T**: Use for identity theft or social engineering attacks
- **DON'T**: Violate platform Terms of Service at scale

**The developers of this tool are not responsible for misuse.** OSINT techniques access publicly available information, but aggregating and analyzing such data may have legal implications depending on your jurisdiction and use case.


---

## Acknowledgments

- **Anthropic** - For Claude and the Agent SDK enabling autonomous investigations
- **Holehe, Sherlock, GHunt developers** - For building reliable OSINT tools
- **OSINT Community** - For pioneering open-source intelligence techniques

---

<div align="center">

**Built with intelligence, for the future of intelligence gathering**

Star this repo if you find it interesting!

</div>