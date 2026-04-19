generate_cad_prototype_tool = {
    "name": "generate_cad_prototype",
    "description": "Generates a 3D wireframe prototype based on a user's description. Use this when the user asks to 'visualize', 'prototype', 'create a wireframe', or 'design' something in 3D.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "prompt": {
                "type": "STRING",
                "description": "The user's description of the object to prototype."
            }
        },
        "required": ["prompt"]
    }
}




write_file_tool = {
    "name": "write_file",
    "description": "Writes content to a file at the specified path. Overwrites if exists.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "The path of the file to write to."
            },
            "content": {
                "type": "STRING",
                "description": "The content to write to the file."
            }
        },
        "required": ["path", "content"]
    }
}

read_directory_tool = {
    "name": "read_directory",
    "description": "Lists the contents of a directory.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "The path of the directory to list."
            }
        },
        "required": ["path"]
    }
}

read_file_tool = {
    "name": "read_file",
    "description": "Reads the content of a file.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "The path of the file to read."
            }
        },
        "required": ["path"]
    }
}

open_file_tool = {
    "name": "open_file",
    "description": "Opens a file using the default application for that file type on the user's PC (e.g., PDF viewer, image viewer, text editor). Use when the user asks to 'open', 'show', or 'view' a specific file.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "The absolute or relative path to the file to open."
            }
        },
        "required": ["path"]
    }
}

open_browser_tool = {
    "name": "open_browser",
    "description": "Opens a URL or website in the user's default browser with all their logins and bookmarks. Use for 'open Google', 'go to YouTube', 'open Gmail', 'search X on Chrome', etc. This is different from run_web_agent — this just opens the browser for the user to interact with.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "The URL to open. If the user says 'open Google', use 'https://www.google.com'. If they say 'search X', use 'https://www.google.com/search?q=X'."
            }
        },
        "required": ["url"]
    }
}

open_app_tool = {
    "name": "open_app",
    "description": "Launches an application on the user's PC by name. Use when the user says 'open VS Code', 'launch Spotify', 'open calculator', etc.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "app_name": {
                "type": "STRING",
                "description": "The name or command of the application to launch (e.g., 'code', 'spotify', 'gnome-calculator', 'notepad')."
            }
        },
        "required": ["app_name"]
    }
}

set_volume_tool = {
    "name": "set_system_volume",
    "description": "Sets the system audio output volume to a percentage (0-100). Use when the user says 'set volume to X%', 'lower the volume', 'mute', etc.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "percent": {
                "type": "INTEGER",
                "description": "Volume level from 0 (mute) to 100 (max)."
            }
        },
        "required": ["percent"]
    }
}

list_processes_tool = {
    "name": "list_processes",
    "description": "Lists the currently running processes on the user's PC, sorted by CPU or memory usage. Use when the user asks 'what's using my CPU?', 'show running processes', etc.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "sort_by": {
                "type": "STRING",
                "description": "Sort by 'cpu' or 'memory'. Defaults to 'cpu'."
            },
            "limit": {
                "type": "INTEGER",
                "description": "Maximum number of processes to return. Defaults to 10."
            }
        }
    }
}

kill_process_tool = {
    "name": "kill_process",
    "description": "Terminates a running process by its PID or name. Use carefully — only when the user explicitly asks to kill or close a process.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "pid": {
                "type": "INTEGER",
                "description": "Process ID to terminate. Use this if you know the PID."
            },
            "name": {
                "type": "STRING",
                "description": "Process name to terminate (kills first match). Use if PID is unknown."
            }
        }
    }
}

take_screenshot_tool = {
    "name": "take_screenshot",
    "description": "Captures a screenshot of the user's screen and sends it so ORION can see what's on the display. Use when the user says 'take a screenshot', 'show me my screen', or when visual context of the screen is needed for a task.",
    "parameters": {
        "type": "OBJECT",
        "properties": {}
    }
}

move_file_tool = {
    "name": "move_file",
    "description": "Moves or renames a file or folder from one location to another.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "source": {
                "type": "STRING",
                "description": "The source file or folder path."
            },
            "destination": {
                "type": "STRING",
                "description": "The destination path (new location or new name)."
            }
        },
        "required": ["source", "destination"]
    }
}

delete_file_tool = {
    "name": "delete_file",
    "description": "Permanently deletes a file. Use with caution — only when the user explicitly confirms deletion.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "The path to the file to delete."
            }
        },
        "required": ["path"]
    }
}

tools_list = [{"function_declarations": [
    generate_cad_prototype_tool,
    write_file_tool,
    read_directory_tool,
    read_file_tool,
    open_file_tool,
    open_browser_tool,
    open_app_tool,
    set_volume_tool,
    list_processes_tool,
    kill_process_tool,
    take_screenshot_tool,
    move_file_tool,
    delete_file_tool,
]}]


