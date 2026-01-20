# Microsoft Foundry Agent Integration Skill

A GitHub Copilot skill for integrating Microsoft Foundry agent applications into your projects.

## What's in This Directory

This directory contains a complete GitHub Copilot skill that teaches how to call Microsoft Foundry agents.

### Core Files

- **SKILL.md** - The main skill definition with YAML frontmatter and detailed instructions
- **GETTING_STARTED.md** - Step-by-step setup and usage guide
- **README.md** - This file

### Example Code

- **example_python.py** - Python implementation using Azure AI SDK
  - Simple agent calls
  - Streaming responses
  - Multi-turn conversations
  
- **example_typescript.ts** - TypeScript implementation using REST API
  - Fetch API integration
  - Async/await patterns
  - Error handling

### Configuration

- **.env.example** - Template for environment variables
- **requirements.txt** - Python dependencies
- **package.json** - Node.js dependencies

### Utilities

- **validate_skill.py** - Validation script to check skill format

## Quick Start

1. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Foundry endpoint and deployment name
   ```

2. **Choose your language:**

   **Python:**
   ```bash
   pip install -r requirements.txt
   python example_python.py
   ```

   **TypeScript:**
   ```bash
   npm install
   npm start
   ```

3. **See GETTING_STARTED.md for detailed instructions**

## How GitHub Copilot Uses This Skill

When this skill is present in your repository (in `.github/skills/foundry-agent/`), GitHub Copilot can:

1. **Reference it automatically** when you ask questions about Foundry integration
2. **Use code examples** as templates for generating new code
3. **Follow best practices** outlined in the skill documentation
4. **Understand context** about your Foundry setup

### Example Prompts

Try asking GitHub Copilot:
- "Use the foundry-agent skill to create a new agent client"
- "How do I call my Foundry agent with streaming?"
- "Show me how to handle errors when calling Foundry agents"
- "Create a multi-turn conversation with my Foundry agent"

## Validation

To validate that the skill is properly formatted:

```bash
python validate_skill.py
```

Expected output:
```
✓ Skill validation passed!
```

## Customization

Feel free to adapt this skill for your specific needs:

1. **Add your own examples** - Include code specific to your Foundry agents
2. **Update instructions** - Add your team's best practices
3. **Include tools** - Add helper scripts or utilities
4. **Extend documentation** - Add FAQs or troubleshooting guides

## File Structure

```
foundry-agent/
├── SKILL.md                  # Main skill definition (required)
├── GETTING_STARTED.md        # Setup guide
├── README.md                 # This file
├── example_python.py         # Python examples
├── example_typescript.ts     # TypeScript examples
├── requirements.txt          # Python deps
├── package.json              # Node.js deps
├── .env.example              # Config template
└── validate_skill.py         # Validation tool
```

## Requirements

### For Using the Skill with Copilot
- GitHub Copilot subscription
- Repository with this skill in `.github/skills/foundry-agent/`

### For Running Examples
- Microsoft Foundry project with published agent
- Azure credentials
- Python 3.8+ or Node.js 18+ (depending on which example you use)

## Support and Resources

- **SKILL.md** - Complete skill documentation with all integration patterns
- **GETTING_STARTED.md** - Detailed setup and troubleshooting
- [Microsoft Foundry Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [GitHub Copilot Skills Docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## License

MIT License - See LICENSE file in repository root
