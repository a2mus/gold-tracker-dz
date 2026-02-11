---
name: mcp-builder
description: |
  Guide for creating high-quality MCP (Model Context Protocol) servers that enable
  LLMs to interact with external services through well-designed tools.
  Use when building MCP servers to integrate external APIs or services,
  whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services
through well-designed tools. The quality of an MCP server is measured by how well it enables
LLMs to accomplish real-world tasks.

---

## High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools**:
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools
can be more convenient for specific tasks, while comprehensive coverage gives agents
flexibility to compose operations.

**Tool Naming and Discoverability**:
Clear, descriptive tool names help agents find the right tools quickly. Use consistent
prefixes (e.g., `github_create_issue`, `github_list_repos`).

**Response Format**:
- Use **Markdown** for human-readable responses (status updates, explanations)
- Use **JSON** for structured data that will be parsed programmatically
- Consider what information the LLM needs to make decisions

#### 1.2 Research the API

Before implementation:
1. Read API documentation thoroughly
2. Identify core endpoints and authentication methods
3. Note rate limits and pagination patterns
4. Understand error responses

#### 1.3 Plan Tool Design

For each tool:
- **Name**: Descriptive, consistent naming (verb_noun pattern)
- **Description**: Clear explanation of what it does and when to use it
- **Parameters**: Required vs optional, clear types and constraints
- **Response**: What the LLM needs to know

---

### Phase 2: Implementation

#### 2.1 Python Implementation (FastMCP)

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("my-service")

class CreateItemParams(BaseModel):
    """Parameters for creating a new item."""
    name: str = Field(..., description="Name of the item")
    description: str = Field(None, description="Optional description")

@mcp.tool
async def create_item(params: CreateItemParams) -> str:
    """
    Create a new item in the service.
    
    Use this when you need to add a new item to the system.
    Returns the created item's ID and details.
    """
    # Implementation
    result = await api.create(params.name, params.description)
    return f"Created item: {result.id} - {result.name}"
```

#### 2.2 TypeScript Implementation (MCP SDK)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";
import { z } from "zod";

const server = new Server({
  name: "my-service",
  version: "1.0.0"
});

const CreateItemSchema = z.object({
  name: z.string().describe("Name of the item"),
  description: z.string().optional().describe("Optional description")
});

server.registerTool({
  name: "create_item",
  description: "Create a new item in the service. Use when adding new items.",
  inputSchema: CreateItemSchema,
  handler: async (params) => {
    const result = await api.create(params.name, params.description);
    return { content: [{ type: "text", text: `Created: ${result.id}` }] };
  }
});
```

---

### Phase 3: Review and Test

#### 3.1 Quality Checklist

- [ ] All tools have clear, descriptive names
- [ ] All tools have helpful descriptions
- [ ] Parameters are well-documented with types
- [ ] Error handling is comprehensive
- [ ] Responses are formatted appropriately
- [ ] Authentication is handled securely
- [ ] Rate limits are respected

#### 3.2 Testing

Test each tool:
1. **Happy path**: Normal usage scenarios
2. **Edge cases**: Empty inputs, large inputs, special characters
3. **Error cases**: Invalid inputs, API errors, auth failures
4. **Integration**: Tools working together in sequences

---

### Phase 4: Create Evaluations

Create evaluation questions that test:
- Basic functionality of each tool
- Complex workflows requiring multiple tools
- Error handling and edge cases
- Real-world use cases

---

## Best Practices

### Tool Design

1. **Single Responsibility**: Each tool does one thing well
2. **Clear Names**: `service_verb_noun` pattern
3. **Helpful Descriptions**: Explain when and why to use the tool
4. **Sensible Defaults**: Optional parameters have good defaults
5. **Informative Responses**: Return what the LLM needs to continue

### Error Handling

```python
@mcp.tool
async def risky_operation(params: Params) -> str:
    try:
        result = await api.call(params)
        return format_success(result)
    except AuthError:
        return "Error: Authentication failed. Please check credentials."
    except RateLimitError:
        return "Error: Rate limit exceeded. Please wait before retrying."
    except ApiError as e:
        return f"Error: API returned error - {e.message}"
```

### Security

- Never expose API keys in responses
- Validate all inputs before processing
- Use environment variables for secrets
- Implement appropriate access controls

---

## Reference Documentation

### Core MCP Documentation
- MCP Protocol: `https://modelcontextprotocol.io`
- Best Practices: Tool naming, response formats, pagination

### SDK Documentation
- Python SDK: `https://github.com/modelcontextprotocol/python-sdk`
- TypeScript SDK: `https://github.com/modelcontextprotocol/typescript-sdk`

---

## Keywords

mcp, model context protocol, api integration, tools, fastmcp, typescript sdk, python sdk, server development
