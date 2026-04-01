from google import genai
from google.genai import types
from app.config import settings
from app.tools import TOOL_MAP
from app.db.repositories import message_repo
from app.db.repositories import memory_repo

client = genai.Client(api_key=settings.gemini_api_key)

def run_chat(project_id: str, conversation_id: str, user_message: str) -> str:

    # Load conversation history
    history = []
    past_messages = message_repo.get_conversation_messages(conversation_id)
    for msg in past_messages:
        if msg["role"] in ("user", "assistant"):
            history.append(types.Content(
                role="user" if msg["role"] == "user" else "model",
                parts=[types.Part(text=msg["content"])]
            ))

    # Load memory context
    memories = memory_repo.get_all_memory(project_id)
    memory_context = ""
    if memories:
        memory_context = "\n\nProject Memory:\n"
        for m in memories:
            memory_context += f"- {m['key']}: {m['value']}\n"

    system_instruction = f"""You are an AI project assistant.
Current Project ID: {project_id}
Always use get_project_brief tool first to understand the project.
Use search_memory and get_all_memory to recall stored knowledge.
Use save_to_memory to remember important things.
Use generate_image when user asks to create an image.
Use analyze_image when user asks to analyze an image.
{memory_context}"""

    # Build tools from TOOL_MAP functions
    tools = types.Tool(function_declarations=[
        _make_declaration(fn) for fn in TOOL_MAP.values()
    ])

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[tools]
    )

    # Add user message to history
    history.append(types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    ))

    # Tool loop
    max_iterations = 5
    for _ in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=config
        )

        candidate = response.candidates[0].content
        history.append(candidate)

        # Check for tool calls
        tool_parts = [p for p in candidate.parts if p.function_call]
        if not tool_parts:
            break

        # Execute all tool calls
        tool_results = []
        for part in tool_parts:
            fn_name = part.function_call.name
            fn_args = dict(part.function_call.args)
            print(f"[Tool Call] {fn_name}({fn_args})")

            if fn_name in TOOL_MAP:
                result = TOOL_MAP[fn_name](**fn_args)
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            tool_results.append(types.Part(
                function_response=types.FunctionResponse(
                    name=fn_name,
                    response={"result": str(result)}
                )
            ))

        history.append(types.Content(role="user", parts=tool_results))

    # Extract final text
    final_reply = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            final_reply += part.text

    return final_reply if final_reply else "I couldn't generate a response."


def _make_declaration(fn):
    """Auto-generate function declaration from Python function"""
    import inspect
    sig = inspect.signature(fn)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        properties[name] = {"type": "string", "description": f"{name} parameter"}
        if param.default is inspect.Parameter.empty:
            required.append(name)

    return types.FunctionDeclaration(
        name=fn.__name__,
        description=fn.__doc__ or fn.__name__,
        parameters=types.Schema(
            type="OBJECT",
            properties={k: types.Schema(type="STRING") for k in properties},
            required=required
        )
    )