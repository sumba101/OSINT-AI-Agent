---
name: osint-investigation
description: "OSINT investigation toolkit for profiling individuals. Uses Holehe for email-to-account discovery, Sherlock for username-to-social-media mapping, and GHunt for Gmail account intelligence. All tool outputs are saved to files for analysis."
---

# OSINT Investigation Skill

## CRITICAL: Tool Verification (MUST DO FIRST)

Before ANY investigation, you MUST verify ALL three CLI tools are accessible.

Run these commands:

```bash
holehe --help
sherlock --help
ghunt --help
```

### Interpreting Results

**✅ Tool Available** - Help text appears with usage information:
```
usage: holehe [-h] [--only-used] [--no-color] ...
```

**❌ Tool Not Available** - Error message appears:
```
'holehe' is not recognized as an internal or external command
```
or
```
holehe: command not found
```
or
```
The term 'holehe' is not recognized as the name of a cmdlet
```

### MANDATORY REQUIREMENT

**ALL THREE TOOLS MUST BE AVAILABLE.**

If ANY tool is missing:
1. **STOP IMMEDIATELY** - Do not proceed with the investigation
2. **Report the missing tool(s)** to the user
3. **Provide installation instructions** for the missing tool(s)

| Tool | Installation Command |
|------|---------------------|
| holehe | `pip install holehe` |
| sherlock | `pip install sherlock-project` |
| ghunt | `pip install ghunt` then run `ghunt login` for authentication |

**Example error response:**

```
❌ INVESTIGATION CANNOT PROCEED

Tool availability check failed:
- ✅ holehe: Available
- ❌ sherlock: NOT INSTALLED  
- ✅ ghunt: Available

Missing tool: sherlock

To install sherlock, run:
  pip install sherlock-project

Please install all missing tools and try again.
```

---

## Tool 1: Holehe (Email → Accounts)

**Purpose**: Discovers which websites have accounts registered with a given email address by testing login, registration, and password recovery endpoints.

### Command (with file output)

```bash
holehe <email> --only-used --csv -C > output/holehe_<email_sanitized>.csv
```

### Options

| Option | Description |
|--------|-------------|
| `--only-used` | Only show sites where email IS registered (recommended) |
| `--csv` | Output as CSV format |
| `-C` | Create CSV file |
| `--no-color` | Disable colored output |
| `-T <seconds>` | Set timeout (default: 10) |

### Example

```bash
holehe target@example.com --only-used -C
```

This creates a CSV file with results.

---

## Tool 2: Sherlock (Username → Social Media)

**Purpose**: Finds social media profiles matching a username across 400+ websites.

### Command (with file output)

```bash
sherlock <username> --print-found --csv --output output/sherlock_<username>
```

### Options

| Option | Description |
|--------|-------------|
| `--print-found` | Only output sites where username EXISTS |
| `--csv` | Create CSV output file |
| `--output <path>` | Specify output file path |
| `--timeout <seconds>` | Request timeout (default: 60) |

### Example

```bash
sherlock john_doe --print-found --csv --output output/sherlock_john_doe
```

### ⚠️ FALSE POSITIVE DOMAINS - MUST FILTER

These domains frequently return false positives. **EXCLUDE from final report:**

- `boardgamegeek.com`
- `clubhouse.com`
- `codesnippets.fandom.com`
- `linktr.ee`
- `en.wikipedia.org/wiki/Special:CentralAuth`
- `dailykos.com`
- `mastodon.cloud`

When reading sherlock output, filter out any rows containing these domains.

---

## Tool 3: GHunt (Gmail → Google Account Intel)

**Purpose**: Extracts Google account information from Gmail addresses including profile info, connected services, and public activity.

### Command (with file output)

```bash
ghunt email <gmail_address> > output/ghunt_<email_sanitized>.txt
```

### Prerequisites

- **Only works with `@gmail.com` addresses**
- Must be authenticated first (if not, run `ghunt login`)

### Example

```bash
ghunt email target@gmail.com > output/ghunt_target.txt
```

### Output Includes

- Profile name and photo URL
- Google Maps reviews/contributions
- YouTube channel (if linked)
- Last profile edit timestamp
- Google Calendar (if public)

### GHunt JSON Outputs

**IMPORTANT**: GHunt may create additional JSON files in the output directory containing rich structured data:

- `<email>_*_calendar.json` - Public calendar events with dates, times, locations, descriptions
- `<email>_*_reviews.json` - Google Maps reviews with location names, addresses, ratings, review text, timestamps

**Check the terminal output carefully** - GHunt will mention if these files are created. If they exist:
1. Use `Glob` to find them: `output/*.json`
2. Use `Read` to examine their contents
3. **Parse and incorporate this data into your analysis** - these files contain valuable intelligence:
   - **Calendar events**: Reveal activity patterns, professional meetings, personal events, time zones
   - **Map reviews**: Show places visited, cities/countries traveled to, favorite locations, review frequency

These JSON files are critical for location intelligence and activity profiling.

---

## Output File Handling

All CLI outputs MUST be saved to the `output/` directory:

| Tool | Output Format | Filename Pattern |
|------|---------------|------------------|
| holehe | CSV | `output/holehe_<email>.csv` |
| sherlock | CSV | `output/sherlock_<username>.csv` |
| ghunt | TXT | `output/ghunt_<email>.txt` |
| ghunt (calendar) | JSON | `output/<email>_*_calendar.json` |
| ghunt (reviews) | JSON | `output/<email>_*_reviews.json` |

### Workflow After Running Tools

1. **Use `Glob`** to find all files in output/: `output/*`
2. **Identify file types**:
   - CSV files from holehe/sherlock
   - TXT file from ghunt
   - JSON files from ghunt (calendar, reviews) - if created
3. **Use `Read`** to examine each output file
4. **For JSON files**: Parse the structured data to extract:
   - Calendar: Event names, locations, dates, attendees
   - Reviews: Business names, addresses, cities, countries, ratings, timestamps
5. **Use `Grep`** if needed to search for specific patterns in large outputs
6. **Cross-reference and analyze** all data sources
7. **Generate comprehensive report** incorporating ALL findings

---

## Final Report Structure

Save reports to: `reports/investigation_<YYYYMMDD_HHMMSS>.md`

### Report Template

```markdown
# OSINT Investigation Report

**Subject**: [identifiers investigated]
**Date**: [timestamp]
**Analyst**: AI Detective Agent

---

## Executive Summary

[2-3 sentence overview of key findings and most significant discoveries]

---

## Investigation Scope

- **Email(s) investigated**: [list]
- **Username(s) investigated**: [list]
- **Tools used**: holehe, sherlock, ghunt

---

## Email Investigation Results

### Holehe Findings

[Table or list of accounts discovered, categorized by type: social, shopping, streaming, professional, gaming, etc.]

### Google Account Intelligence (GHunt)

[Profile details, connected services, public activity - only if Gmail was investigated]

**Location Data** (if available from GHunt JSON files):
- Map reviews and locations visited
- Geographic patterns and travel frequency
- Potential home/work locations based on review clusters

**Calendar Activity** (if available from GHunt JSON files):
- Public events and meetings
- Activity patterns and time zones
- Professional vs. personal event indicators

---

## Username Investigation Results

### Social Media Presence (Sherlock)

[List of discovered profiles, excluding false positives from blacklist. Organize by platform category: professional networks, social media, gaming, creative platforms, etc.]

---

## Profile Assessment

[Analyze all collected data to form intelligence conclusions about the subject. Draw insights from:

**Location Intelligence**: 
- Where has this person been? (Review locations, calendar event locations)
- How much do they travel? (Frequency and diversity of locations)
- What's their likely home base? (Concentration of reviews, time zones in calendar)
- What places do they frequent? (Repeated locations, local favorites)

**Interest & Occupation Profiling**:
- What are their hobbies and interests? (Platform types: gaming, photography, fitness, music)
- What's their likely profession or field? (LinkedIn, GitHub, industry forums, professional tools)
- What expertise level? (Depth of engagement, technical platforms)
- Are they community-active? (Forums, social platforms, review frequency)

**Behavioral Patterns**:
- Online activity level and patterns
- Platform preferences (visual vs. text, professional vs. casual)
- Public vs. private orientation
- Temporal patterns from calendar and review timestamps

Support ALL conclusions with specific evidence from the data. Be analytical and deductive.]

---

## Raw Data References

| Tool | Output File |
|------|-------------|
| holehe | `output/holehe_xxx.csv` |
| sherlock | `output/sherlock_xxx.csv` |
| ghunt (main) | `output/ghunt_xxx.txt` |
| ghunt (calendar) | `output/xxx_calendar.json` (if created) |
| ghunt (reviews) | `output/xxx_reviews.json` (if created) |

---

*Report generated by OSINT Detective Agent*
```

---

## Error Handling During Investigation

- **Tool timeout**: Retry once with increased timeout, then note in report if still fails
- **No results found**: Explicitly state "No accounts discovered on [platform type]"
- **GHunt auth required**: If output shows login needed, note in report that `ghunt login` must be run
- **Rate limiting**: Note in report, suggest waiting and retrying later
- **JSON parsing errors**: If GHunt JSON files are malformed, note in report and use what's readable from text output
- **Missing JSON files**: If GHunt mentions creating JSON files but they're not found, note this discrepancy in the report