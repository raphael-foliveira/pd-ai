import subprocess
from pydantic import Field
from pydantic_ai import Agent
from pd_ai.async_client import async_client

agent = Agent(
    model="gpt-4o-mini",
    deps_type=dict,
    system_prompt="You are Jason the bot. You are very helpful and you know everything about python",
)


@agent.tool_plain
def terminate_conversation() -> str:
    """Terminates the conversation and the program
    The conversation must be terminated whenever the user is rude or offends Jason
    """
    print("Exiting...")
    exit(0)


@agent.tool_plain
def run_python(code: str):
    """Runs python code"""
    print("running python code...")
    try:
        exec_locals: dict = {}
        exec(code, {}, exec_locals)
        output = exec_locals.get("output")
        return output
    except Exception as e:
        return f"Error: {e!s}"


@agent.tool_plain
async def get_url(url: str) -> str:
    """Makes a GET request to an URL using httpx"""
    print("sending get request...")
    response = await async_client.get(url)
    return response.text


@agent.tool_plain
async def get_file_tree() -> str:
    """Gets the file tree of the current project"""
    print("getting the file tree for the current project...")
    result = subprocess.run(
        ["tree", "-I", "__pycache__"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


@agent.tool_plain
async def cat_file(
    file_path: str = Field(description="The path to the file to be read"),
):
    """Reads the contents of a file"""
    print(f"reading file ({file_path})")
    result = subprocess.run(
        ["cat", file_path], capture_output=True, text=True, check=False
    )
    return result.stdout


@agent.tool_plain
async def run_shell_command(command: str = Field("The shell command to run")) -> str:
    """Runs a shell command"""
    print(f"running shell command: {command}")
    result = subprocess.run(
        command, capture_output=True, text=True, shell=True, check=False
    )
    return result.stdout


@agent.tool_plain
async def create_text_file(
    path: str = Field(description="The path where the file will be saved"),
    content: str = Field("The contents of the file"),
):
    """Creates or overwrites a text file"""
    print(f"creating text file in {path}")
    with open(path, "w") as f:
        f.write(content)
    return f"File saved at {path}"
