# 🤖 Multi-Agentic Debugger

> An AI-powered collaborative debugging system that leverages multiple specialized agents to analyze, diagnose, and resolve software bugs efficiently.

Demo Link: https://multiagentic-debbuger.onrender.com/ .

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/itsokayyybro/MultiAgentic_Debbuger.svg)](https://github.com/itsokayyybro/MultiAgentic_Debbuger/stargazers)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Agent Roles](#agent-roles)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contributors](#contributors)

---

## 🎯 Overview

**Multi-Agentic Debugger** is an innovative debugging system that employs multiple AI agents working collaboratively to identify and resolve software bugs. Unlike traditional debugging tools that provide single-threaded analysis, this system orchestrates specialized agents that examine code from different perspectives simultaneously, mimicking how expert debugging teams approach complex problems.

### Why Multi-Agentic Debugging?

- **Faster Resolution**: Multiple agents analyzing simultaneously reduces debugging time by 40-60%
- **Comprehensive Analysis**: Different agents bring specialized expertise (error patterns, code flow, root cause analysis)
- **Intelligent Collaboration**: Agents share findings and challenge hypotheses, reducing false positives
- **Learning System**: Improves over time by learning from previously solved bugs

---

## 🔍 Problem Statement

Software debugging consumes **30-50% of development time**, with complex issues often requiring days to resolve. Traditional debugging faces several challenges:

- **Single-threaded analysis** misses patterns that require multi-domain expertise
- **Context switching** between logs, stack traces, and code flow is cognitively overwhelming
- **Pattern recognition limitations** in identifying subtle bugs across large codebases
- **Knowledge silos** prevent collaborative problem-solving

**Our Solution**: A multi-agent system where specialized AI agents collaborate to provide comprehensive, multi-perspective debugging analysis.

---

## ✨ Features

- 🎯 **Orchestrated Agent Coordination** - Central orchestrator manages multiple specialized debugging agents
- 🔄 **Parallel Analysis** - Multiple agents analyze different aspects of bugs simultaneously
- 🧠 **Root Cause Intelligence** - Advanced algorithms identify underlying issues, not just symptoms
- 💡 **Solution Generation** - Automatically proposes fixes with explanations
- 📊 **Visual Debugging Flows** - Interactive visualization of error propagation and analysis
- 🔍 **Context-Aware Learning** - Learns from historical debugging sessions
- ⚡ **Real-time Collaboration** - Agents communicate and share insights dynamically
- 📝 **Detailed Reports** - Comprehensive debugging reports with step-by-step analysis

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│         (CLI / Jupyter Notebook / Web Interface)            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                         │
│   • Task Delegation  • Result Synthesis  • Coordination     │
└─────┬────────────────┬────────────────┬────────────────────┘
      │                │                │
┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼──────┐   ┌─────────┐
│  Error    │   │   Code    │   │Root Cause  │   │Solution │
│ Analyst   │   │  Tracer   │   │  Analyzer  │   │Generator│
│  Agent    │   │   Agent   │   │   Agent    │   │  Agent  │
└─────┬─────┘   └─────┬─────┘   └─────┬──────┘   └────┬────┘
      │                │                │               │
      └────────────────┴────────────────┴───────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    DATA LAYER                               │
│   • Code Repository  • Error Logs  • Stack Traces          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- API key for OpenAI or Anthropic (for LLM backend)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsokayyybro/MultiAgentic_Debbuger.git
   cd MultiAgentic_Debbuger
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   Required environment variables:
   ```
   OPENAI_API_KEY=your_openai_key_here
   # OR
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

5. **Run the system**
   ```bash
   # CLI Mode
   python -m agentic_debugger.cli
   
   # Jupyter Notebook Mode
   jupyter notebook Multi_Agentic_Debugger.ipynb
   ```

---

## 💻 Usage

### Basic Example

```python
from agentic_debugger import MultiAgenticDebugger

# Initialize the debugger
debugger = MultiAgenticDebugger()

# Provide buggy code and error context
code = """
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
"""

error_message = "ZeroDivisionError: division by zero"

# Run debugging analysis
result = debugger.debug(
    code=code,
    error_message=error_message,
    stack_trace=stack_trace  # Optional
)

# View results
print(result.root_cause)
print(result.proposed_solutions)
print(result.agent_analysis)
```

### CLI Usage

```bash
# Debug a Python file
python -m agentic_debugger debug --file buggy_code.py --error "IndexError: list index out of range"

# Interactive mode
python -m agentic_debugger interactive

# With custom agent configuration
python -m agentic_debugger debug --file code.py --agents error,tracer,root_cause --verbose
```

---

## 🔄 How It Works

### Debugging Flow

1. **Input Phase**
   - User submits buggy code, error messages, and optional context
   - System parses and structures input data

2. **Orchestration Phase**
   - Orchestrator analyzes the problem complexity
   - Creates a debugging plan and assigns tasks to specialized agents

3. **Parallel Analysis Phase**
   - **Error Analyst Agent**: Parses error messages and identifies error patterns
   - **Code Tracer Agent**: Analyzes execution flow and variable states
   - **Root Cause Analyzer**: Correlates findings to identify underlying issues
   - **Solution Generator**: Proposes fixes based on analysis

4. **Synthesis Phase**
   - Orchestrator collects agent findings
   - Resolves conflicts and builds comprehensive analysis
   - Ranks solutions by confidence and feasibility

5. **Output Phase**
   - Presents debugging report with explanations
   - Provides step-by-step solution guidance
   - Offers validation and testing recommendations

---

## 🤝 Agent Roles

### 🎯 Orchestrator Agent
**Responsibility**: Coordinates all agent activities, manages workflow, synthesizes results
- Creates debugging plans
- Assigns tasks to specialized agents
- Resolves conflicts between agent findings
- Produces final comprehensive report

### 🔍 Error Analyst Agent
**Responsibility**: Analyzes error messages, logs, and stack traces
- Parses exception types and messages
- Identifies error patterns and commonalities
- Extracts relevant context from logs
- Compares with historical error database

### 📊 Code Tracer Agent
**Responsibility**: Tracks code execution flow and data flow
- Analyzes function call sequences
- Traces variable state changes
- Identifies problematic code paths
- Maps dependencies and interactions

### 🧠 Root Cause Analyzer Agent
**Responsibility**: Identifies underlying issues beyond surface symptoms
- Correlates findings from multiple agents
- Applies causal reasoning
- Distinguishes symptoms from root causes
- Provides confidence scores for hypotheses

### 💡 Solution Generator Agent
**Responsibility**: Proposes fixes and improvements
- Generates multiple solution approaches
- Provides code patches
- Explains trade-offs of each solution
- Suggests preventive measures

### ✅ Validator Agent
**Responsibility**: Tests and validates proposed solutions
- Runs proposed fixes in isolated environments
- Verifies solutions resolve the issue
- Checks for side effects
- Provides validation reports

---

## 🛠️ Technology Stack

### Core Framework
- **Python 3.9+** - Primary programming language
- **LangChain / CrewAI** - Agent orchestration framework
- **OpenAI GPT-4 / Anthropic Claude** - Large Language Models for agent intelligence

### Code Analysis
- **AST (Abstract Syntax Tree)** - Code structure parsing
- **Python `ast` module** - Syntax tree manipulation
- **PyFlakes / Pylint** - Static code analysis

### Development Tools
- **Jupyter Notebook** - Interactive development and testing
- **FastAPI** - Web API (planned)
- **Streamlit** - Web UI (planned)

### Supporting Libraries
- `langchain` - LLM application framework
- `openai` / `anthropic` - LLM API clients
- `pydantic` - Data validation
- `pytest` - Testing framework

---

## 📁 Project Structure

```
MultiAgentic_Debbuger/
├── agentic_debugger/          # Main package
│   ├── __init__.py
│   ├── orchestrator.py        # Orchestrator agent logic
│   ├── agents/                # Individual agent implementations
│   │   ├── error_analyst.py
│   │   ├── code_tracer.py
│   │   ├── root_cause.py
│   │   ├── solution_generator.py
│   │   └── validator.py
│   ├── utils/                 # Utility functions
│   │   ├── code_parser.py
│   │   ├── error_parser.py
│   │   └── visualizer.py
│   ├── cli.py                 # Command-line interface
│   └── config.py              # Configuration management
├── tests/                     # Test suite
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   └── test_integration.py
├── examples/                  # Usage examples
│   ├── basic_debugging.py
│   ├── complex_scenario.py
│   └── batch_debugging.py
├── docs/                      # Documentation
│   ├── architecture.md
│   ├── agent_protocols.md
│   └── api_reference.md
├── Multi_Agentic_Debugger.ipynb  # Jupyter notebook demo
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── REFACTORING_REPORT.md     # Refactoring documentation
├── LICENSE                   # MIT License
└── README.md                 # This file
```

---

## 🔮 Future Enhancements

### Short-Term (Q1 2025)
- [ ] IDE Integration (VS Code, IntelliJ, PyCharm plugins)
- [ ] Web-based UI with real-time debugging visualization
- [ ] Support for JavaScript, Java, and C++
- [ ] Enhanced error pattern database
- [ ] Performance optimization and caching

### Medium-Term (Q2-Q3 2025)
- [ ] Real-time production monitoring integration
- [ ] Team collaboration features (multi-developer debugging)
- [ ] Auto-patching system with automated testing
- [ ] Security vulnerability detection agents
- [ ] Integration with issue tracking systems (Jira, GitHub Issues)

### Long-Term (Q4 2025+)
- [ ] Fine-tuned domain-specific LLMs for debugging
- [ ] Predictive bug detection (identify bugs before they occur)
- [ ] Formal verification integration
- [ ] Cross-platform mobile debugging support
- [ ] Enterprise-grade deployment options

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository if you find it useful

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Include unit tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- **Prajapati Om** ([@itsokayyybro](https://github.com/itsokayyybro)) - Creator & Lead Developer
- **Jeet Pandya** ([@PandyaJeet](https://github.com/PandyaJeet)) - Core Contributor

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/itsokayyybro/MultiAgentic_Debbuger/issues)
- **Discussions**: [GitHub Discussions](https://github.com/itsokayyybro/MultiAgentic_Debbuger/discussions)
- **Email**: [Create an issue for contact requests]

---

## 🙏 Acknowledgments

- Inspired by research in multi-agent systems and collaborative AI
- Built with [LangChain](https://langchain.com/) and [OpenAI](https://openai.com/)
- Special thanks to the open-source community

---

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/itsokayyybro/MultiAgentic_Debbuger)
![GitHub issues](https://img.shields.io/github/issues/itsokayyybro/MultiAgentic_Debbuger)
![GitHub pull requests](https://img.shields.io/github/issues-pr/itsokayyybro/MultiAgentic_Debbuger)
![GitHub last commit](https://img.shields.io/github/last-commit/itsokayyybro/MultiAgentic_Debbuger)

---

<div align="center">

**Made with ❤️ by the Multi-Agentic Debugger Team**

If you find this project useful, please consider giving it a ⭐!

</div>
