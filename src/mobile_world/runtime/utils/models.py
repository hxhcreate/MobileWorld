# models.py
"""Pydantic models for FastAPI server requests and responses."""

from typing import Any, Literal

from pydantic import BaseModel, field_validator

# Action type constants
ANSWER = "answer"
CLICK = "click"
DOUBLE_TAP = "double_tap"
FINISHED = "finished"
INPUT_TEXT = "input_text"
KEYBOARD_ENTER = "keyboard_enter"
LONG_PRESS = "long_press"
NAVIGATE_BACK = "navigate_back"
NAVIGATE_HOME = "navigate_home"
OPEN_APP = "open_app"
SCROLL = "scroll"
STATUS = "status"
SWIPE = "swipe"
UNKNOWN = "unknown"
WAIT = "wait"
DRAG = "drag"
ASK_USER = "ask_user"
MCP = "mcp"
ENV_FAIL = "error_env"
DEFAULT_IMAGE = "ghcr.io/tongyi-mai/mobile_world:latest"
DEFAULT_NAME_PREFIX = "mobile_world_env"
_ACTION_TYPES = (
    CLICK,
    DOUBLE_TAP,
    SCROLL,
    SWIPE,
    INPUT_TEXT,
    NAVIGATE_HOME,
    NAVIGATE_BACK,
    KEYBOARD_ENTER,
    OPEN_APP,
    STATUS,
    WAIT,
    LONG_PRESS,
    ANSWER,
    FINISHED,
    UNKNOWN,
    DRAG,
    ASK_USER,
    MCP,
)

_SCROLL_DIRECTIONS = ("left", "right", "down", "up")

# Keys of JSON action
ACTION_TYPE = "action_type"
INDEX = "index"
X = "x"
Y = "y"
TEXT = "text"
DIRECTION = "direction"
APP_NAME = "app_name"
GOAL_STATUS = "goal_status"
START_X = "start_x"
START_Y = "start_y"
END_X = "end_x"
END_Y = "end_y"
ACTION_KEYS = [
    ACTION_TYPE,
    INDEX,
    X,
    Y,
    TEXT,
    DIRECTION,
    APP_NAME,
    GOAL_STATUS,
    START_X,
    START_Y,
    END_X,
    END_Y,
]


class JSONAction(BaseModel):
    """Represents a parsed JSON action.

    Example:
        result_json = {'action_type': 'click', 'x': 100, 'y': 200}
        action = JSONAction(**result_json)

    Attributes:
        action_type: The action type.
        index: The index to click, if action is a click. Either an index or a <x, y>
            should be provided. See x, y attributes below.
        x: The x position to click, if the action is a click.
        y: The y position to click, if the action is a click.
        text: The text to type, if action is type.
        direction: The direction to scroll, if action is scroll.
        goal_status: If the status is a 'status' type, indicates the status of the goal.
        app_name: The app name to launch, if the action type is 'open_app'.
        keycode: Keycode actions are necessary for an agent to interact with complex
            UI elements (like large textareas) that can't be accessed or controlled by
            simply taping, ensuring precise control over navigation and selection in
            the interface.
        clear_text: Whether to clear the text field before typing.
        start_x: The x position to start drag, if the action is a drag.
        start_y: The y position to start drag, if the action is a drag.
        end_x: The x position to end drag, if the action is a drag.
        end_y: The y position to end drag, if the action is a drag.
    """

    action_type: str | None = None
    index: str | int | None = None
    x: int | None = None
    y: int | None = None
    text: str | None = None
    direction: str | None = None
    goal_status: str | None = None
    app_name: str | None = None
    keycode: str | None = None
    clear_text: bool | None = None
    start_x: int | None = None
    start_y: int | None = None
    end_x: int | None = None
    end_y: int | None = None
    action_name: str | None = None
    action_json: dict | None = None

    @field_validator("action_type")
    @classmethod
    def validate_action_type(cls, v: str | None) -> str | None:
        """Validate action type is valid."""
        if v is not None and v not in _ACTION_TYPES:
            raise ValueError(f"Invalid action type: {v}")
        return v

    @field_validator("index")
    @classmethod
    def validate_index(cls, v: str | int | None) -> int | None:
        """Convert index to int if needed."""
        if v is not None:
            return int(v)
        return v

    @field_validator("x", "y", mode="before")
    @classmethod
    def validate_coordinates(cls, v: int | float | None) -> int | None:
        """Convert float coordinates to int if needed."""
        if v is not None:
            return round(v)
        return v

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str | None) -> str | None:
        """Validate scroll direction is valid."""
        if v is not None and v not in _SCROLL_DIRECTIONS:
            raise ValueError(f"Invalid scroll direction: {v}")
        return v

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, v: Any) -> str | None:
        """Convert text to string if needed."""
        if v is not None and not isinstance(v, str):
            return str(v)
        return v

    @field_validator("keycode")
    @classmethod
    def validate_keycode(cls, v: str | None) -> str | None:
        """Validate keycode format."""
        if v is not None and not v.startswith("KEYCODE_"):
            raise ValueError(f"Invalid keycode: {v}")
        return v

    def model_post_init(self, __context: Any) -> None:
        """Additional validation after model initialization."""
        if self.index is not None:
            if self.x is not None or self.y is not None:
                raise ValueError("Either an index or a <x, y> should be provided.")

    def __eq__(self, other: object) -> bool:
        """Compare two JSONActions."""
        if not isinstance(other, JSONAction):
            return False
        return _compare_actions(self, other)

    def __ne__(self, other: object) -> bool:
        """Check if two JSONActions are not equal."""
        return not self.__eq__(other)


def _compare_actions(a: JSONAction, b: JSONAction) -> bool:
    """Compares two JSONActions.

    Args:
        a: The first action.
        b: The second action.

    Returns:
        If the actions are equal.
    """
    # Ignore cases for app_name and text.
    if a.app_name is not None and b.app_name is not None:
        app_name_match = a.app_name.lower() == b.app_name.lower()
    else:
        app_name_match = a.app_name == b.app_name

    if a.text is not None and b.text is not None:
        text_match = a.text.lower() == b.text.lower()
    else:
        text_match = a.text == b.text

    # Compare the non-metadata fields.
    return (
        app_name_match
        and text_match
        and a.action_type == b.action_type
        and a.index == b.index
        and a.x == b.x
        and a.y == b.y
        and a.keycode == b.keycode
        and a.direction == b.direction
        and a.goal_status == b.goal_status
        and a.start_x == b.start_x
        and a.start_y == b.start_y
        and a.end_x == b.end_x
        and a.end_y == b.end_y
    )


APP_DICT = {
    "桌面": "com.google.android.apps.nexuslauncher",
    "Contacts": "com.google.android.contacts",
    "Settings": "com.android.settings",
    "设置": "com.android.settings",
    "Clock": "com.google.android.deskclock",
    "Maps": "com.google.android.apps.maps",
    "Chrome": "com.android.chrome",
    "Calendar": "org.fossify.calendar",
    "files": "com.google.android.documentsui",
    "Gallery": "gallery.photomanager.picturegalleryapp.imagegallery",
    "淘店": "com.testmall.app",
    "Taodian": "com.testmall.app",
    "Mattermost": "com.mattermost.rnbeta",
    "Mastodon": "org.joinmastodon.android.mastodon",
    "Mail": "com.gmailclone",
    "SMS": "com.google.android.apps.messaging",
    "Camera": "com.android.camera2",
}

COMMON_CN_APP_DICT = {
    "淘宝": "com.taobao.taobao",
    "淘宝闪购": "com.taobao.taobao",
    "高德地图": "com.autonavi.minimap",
    "饿了么": "me.ele",
}


# FastAPI Server Models
class InstanceInfo(BaseModel):
    docker_port_local: int | None = None
    container_id: str | None = None


class InitRequest(BaseModel):
    device: str = "emulator-5554"
    type: Literal["cmd", "docker"] = "cmd"
    instance: InstanceInfo | None = None


class ScreenshotQuery(BaseModel):
    device: str
    prefix: str | None = None
    return_b64: bool = False


class XMLQuery(BaseModel):
    device: str
    prefix: str | None = None
    mode: Literal["uia", "ac"] = "uia"  # uia: get_xml; ac: get_ac_xml
    return_content: bool = False


class StepRequest(BaseModel):
    """Request for executing a step action."""

    device: str
    action: JSONAction


class TaskOperationRequest(BaseModel):
    task_name: str
    req_device: str


# Client Response Models
class Response(BaseModel):
    """Response model for client operations."""

    status: str
    message: str


class SmsRequest(BaseModel):
    device: str
    sender: str
    message: str


class TaskCallbackRequest(BaseModel):
    """Request for saving task callback data."""

    device: str
    callback_data: dict[str, Any]


class Observation(BaseModel):
    screenshot: Any
    accessibility_tree: Any = None
    ask_user_response: str | None = None
    tool_call: Any | None = None


# Environment/Docker Models
class ContainerInfo(BaseModel):
    """Information about a Docker container."""

    name: str
    status: str | None = None
    running: bool = False
    started_at: str | None = None
    image: str | None = None
    backend_port: int | None = None
    viewer_port: int | None = None
    vnc_port: int | None = None
    adb_port: int | None = None


class ContainerConfig(BaseModel):
    """Configuration for launching a container."""

    name: str
    backend_port: int
    viewer_port: int
    vnc_port: int
    adb_port: int = 5556
    image: str = DEFAULT_IMAGE
    dev_mode: bool = False
    enable_vnc: bool = False
    env_file_path: Any | None = None  # Path
    dev_src_path: Any | None = None  # Path


class LaunchResult(BaseModel):
    """Result of launching a container."""

    name: str
    backend_port: int
    viewer_port: int
    adb_port: int
    vnc_port: int
    success: bool = False
    ready: bool = False
    error_message: str | None = None


class PrerequisiteCheckResult(BaseModel):
    """Result of a single prerequisite check."""

    name: str
    passed: bool
    message: str
    details: str | None = None


class PrerequisiteCheckResults(BaseModel):
    """Results of all prerequisite checks."""

    checks: list[PrerequisiteCheckResult]

    @property
    def all_passed(self) -> bool:
        """Return True if all checks passed."""
        return all(c.passed for c in self.checks)

    @property
    def passed_count(self) -> int:
        """Return count of passed checks."""
        return sum(1 for c in self.checks if c.passed)

    @property
    def failed_count(self) -> int:
        """Return count of failed checks."""
        return sum(1 for c in self.checks if not c.passed)


class ImageStatus(BaseModel):
    """Status of a Docker image."""

    image: str
    exists_locally: bool
    local_digest: str | None = None
    remote_digest: str | None = None
    needs_update: bool = False
    error: str | None = None
