from app.tools.project_tools import get_project_brief, list_project_images
from app.tools.memory_tools import search_memory, get_all_memory, save_to_memory
from app.tools.image_tools import generate_image, analyze_image

# All tools list - passed to Gemini
ALL_TOOLS = [
    get_project_brief,
    list_project_images,
    search_memory,
    get_all_memory,
    save_to_memory,
    generate_image,
    analyze_image,
]

# Tool executor - maps function name to actual function
TOOL_MAP = {
    "get_project_brief": get_project_brief,
    "list_project_images": list_project_images,
    "search_memory": search_memory,
    "get_all_memory": get_all_memory,
    "save_to_memory": save_to_memory,
    "generate_image": generate_image,
    "analyze_image": analyze_image,
}
