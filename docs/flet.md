### Install Flet with All Features

Source: <https://flet.dev/docs/getting-started>

Installs the Flet package along with all optional dependencies. This command is used after activating a virtual environment (e.g., using venv, Poetry, or uv) to ensure Flet has all necessary components.

```bash
pip install 'flet[all]'
```

```bash
pip install flet[all]
```

--------------------------------

### Install Dependencies with Poetry

Source: <https://flet.dev/docs/getting-started>

Installs all project dependencies defined in `pyproject.toml` using Poetry. The `--no-root` flag prevents Poetry from attempting to install the project package itself.

```bash
poetry install --no-root
```

--------------------------------

### Install libmpv on Linux (WSL)

Source: <https://flet.dev/docs/getting-started>

Installs the libmpv library and development files required for video support in Flet applications on Linux/WSL. It also creates a symbolic link to ensure the library is accessible.

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```

--------------------------------

### Check Flet Version

Source: <https://flet.dev/docs/getting-started>

Displays the currently installed version of the Flet package. This command is useful for verifying the installation and checking compatibility.

```bash
flet --version
```

--------------------------------

### Initialize Project with Poetry

Source: <https://flet.dev/docs/getting-started>

Initializes a new project directory, sets up Poetry for dependency management, and adds Flet with all features as a development dependency. It also specifies the required Python version.

```bash
mkdir my-app
cd my-app
poetry init --dev-dependency='flet[all]' --python='>=3.9' --no-interaction
```

--------------------------------

### Initialize Project with uv

Source: <https://flet.dev/docs/getting-started>

Initializes a new project directory with uv, a fast Python package manager. This command sets up the project structure and creates a `pyproject.toml` file.

```bash
mkdir my-app
cd my-app
uv init
```

--------------------------------

### Install GStreamer on Linux (WSL)

Source: <https://flet.dev/docs/getting-started>

Installs GStreamer components required for audio support in Flet applications on Linux, specifically within a WSL environment. This command ensures that necessary libraries for handling audio streams are available.

```bash
apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools
```

--------------------------------

### Create and Activate venv (Windows)

Source: <https://flet.dev/docs/getting-started>

Commands to create a new directory for your Flet app, navigate into it, set up a Python virtual environment using `venv`, and activate it on Windows. This isolates project dependencies.

```cmd
md first-flet-app
cd first-flet-app
python -m venv .venv
.venv\Scripts\activate
```

--------------------------------

### Create and Activate venv (macOS/Linux)

Source: <https://flet.dev/docs/getting-started>

Commands to create a new directory for your Flet app, navigate into it, set up a Python virtual environment using `venv`, and activate it. This isolates project dependencies.

```bash
mkdir first-flet-app
cd first-flet-app
python3 -m venv .venv
source .venv/bin/activate
```

--------------------------------

### Add Flet Dependency with uv

Source: <https://flet.dev/docs/getting-started>

Adds Flet with all optional features as a development dependency to the project managed by uv. The `--dev` flag specifies it as a development dependency.

```bash
uv add 'flet[all]' --dev
```

--------------------------------

### Run Flet CLI Command with uv

Source: <https://flet.dev/docs/getting-started>

Executes a Flet CLI command (e.g., checking version) within the context of a uv-managed project. This ensures the command runs with the project's isolated dependencies.

```bash
uv run flet --version
```

--------------------------------

### Run Flet CLI Command with Poetry

Source: <https://flet.dev/docs/getting-started>

Executes a Flet CLI command (e.g., checking version) within the context of a Poetry-managed project. This ensures the command runs with the project's isolated dependencies.

```bash
poetry run flet --version
```

--------------------------------

### Create New Flet App using flet create

Source: <https://flet.dev/docs/getting-started/create-flet-app>

This command initializes a new Flet application project. It generates a standard directory structure including a 'src/main.py' file which contains the entry point for your Flet application. Ensure you have Flet installed.

```bash
flet create
```

--------------------------------

### Basic AudioRecorder Example in Python

Source: <https://flet.dev/docs/controls/audiorecorder>

Demonstrates the basic usage of the AudioRecorder control, including starting, stopping, listing devices, checking permissions, pausing, resuming, and playing recorded audio. It utilizes Flet for UI elements and event handling.

```python
import flet as ft

import flet_audio_recorder as ftar
import flet_audio as fta


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title=ft.Text("Audio Recorder"), center_title=True)

    path = "test-audio-file.wav"

    def handle_start_recording(e):
        print(f"StartRecording: {path}")
        audio_rec.start_recording(path)

    def handle_stop_recording(e):
        output_path = audio_rec.stop_recording()
        print(f"StopRecording: {output_path}")
        log.value = f"StopRecording: {output_path}"
        if page.web and output_path is not None:
            page.launch_url(output_path)
        page.update()

    def handle_list_devices(e):
        devices = audio_rec.get_input_devices()
        print(devices)

    def handle_has_permission(e):
        try:
            print(f"HasPermission: {audio_rec.has_permission()}")
            log.value = f"HasPermission: {audio_rec.has_permission()}"
        except Exception as e:
            print(e)
        page.update()

    def handle_pause(e):
        print(f"isRecording: {audio_rec.is_recording()}")
        if audio_rec.is_recording():
            audio_rec.pause_recording()

    def handle_resume(e):
        print(f"isPaused: {audio_rec.is_paused()}")
        if audio_rec.is_paused():
            audio_rec.resume_recording()

    def handle_audio_encoding_test(e):
        for i in list(ft.AudioEncoder):
            print(f"{i}: {audio_rec.is_supported_encoder(i)}")
            page.add(ft.Text(f"audio encoder: {i.name}"))

    def handle_state_change(e):
        print(f"State Changed: {e.data}")

    audio_rec = ftar.AudioRecorder(
        # audio_encoder=ft.AudioEncoder.WAV,
        on_state_changed=handle_state_change,
    )
    audio_play = fta.Audio("non-existent", autoplay=False, volume=6)

    page.overlay.append(audio_play)

    def handle_start_play(e):
        page.add(ft.Text(f"play audio file: {audio_play.src}"))
        audio_play.src = "test-audio-file.wav"
        audio_play.update()
        audio_play.play()

    print(f"audio recorder: {audio_rec}")
    page.overlay.append(audio_rec)
    page.update()
    log = ft.Text(":")

    page.add(
        ft.ElevatedButton("Start Audio Recorder", on_click=handle_start_recording),
        ft.ElevatedButton("Stop Audio Recorder", on_click=handle_stop_recording),
        ft.ElevatedButton("List Devices", on_click=handle_list_devices),
        ft.ElevatedButton("Pause Recording", on_click=handle_pause),
        ft.ElevatedButton("Resume Recording", on_click=handle_resume),
        ft.ElevatedButton("Test AudioEncodings", on_click=handle_audio_encoding_test),
        ft.ElevatedButton("Has Permission", on_click=handle_has_permission),
        ft.ElevatedButton("Play", on_click=handle_start_play),
        ft.ElevatedButton("Pause", on_click=lambda _: audio_play.pause()),
        ft.ElevatedButton("Resume", on_click=lambda _: audio_play.resume()),
        ft.ElevatedButton("Release", on_click=lambda _: audio_play.release()),
        ft.ElevatedButton("Seek 2s", on_click=lambda _: audio_play.seek(2000)),
        log,
    )


ft.app(main)

```

--------------------------------

### Basic Example

Source: <https://flet.dev/docs/controls/cupertinodatepicker>

A basic example demonstrating how to open and use the CupertinoDatePicker.

```APIDOC
## POST /open_cupertino_date_picker

### Description
Opens a CupertinoDatePicker dialog within a bottom sheet.

### Method
POST

### Endpoint
/

### Request Body
```json
{
  "control": "CupertinoBottomSheet",
  "properties": {
    "content": {
      "control": "CupertinoDatePicker",
      "properties": {
        "date_picker_mode": "CupertinoDatePickerMode.DATE_AND_TIME",
        "on_change": "handle_date_change"
      }
    },
    "height": 216,
    "padding": {
      "control": "padding",
      "properties": {
        "only": {
          "top": 6
        }
      }
    }
  }
}
```

### Response

#### Success Response (200)

Indicates the dialog was opened successfully. The actual UI update is handled client-side.

#### Response Example

```json
{
  "status": "success",
  "message": "CupertinoDatePicker opened"
}
```

```

--------------------------------

### AnimatedSwitcher Example

Source: https://flet.dev/docs/controls/animatedswitcher

A live example demonstrating animated switching between two containers with different transition effects.

```APIDOC
## Animated switching between two containers with scale effect

### Description
This example showcases how to use `AnimatedSwitcher` to transition between two `Container` controls using different animation effects like scale, fade, and rotation.

### Method
N/A (This is a code example, not an API endpoint)

### Endpoint
N/A

### Parameters
N/A

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.title = "AnimatedSwitcher examples"

    c1 = ft.Container(
        ft.Text("Hello!", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.Colors.GREEN,
    )
    c2 = ft.Container(
        ft.Text("Bye!", size=50),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.Colors.YELLOW,
    )
    c = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    def scale(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.SCALE
        c.update()

    def fade(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.FADE
        c.update()

    def rotate(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.ROTATION
        c.update()

    page.add(
        c,
        ft.ElevatedButton("Scale", on_click=scale),
        ft.ElevatedButton("Fade", on_click=fade),
        ft.ElevatedButton("Rotate", on_click=rotate),
    )

ft.app(main)
```

### Response

N/A (This is a client-side code example)

### Response Example

N/A

```

--------------------------------

### Sample Flet Application Code

Source: https://flet.dev/docs/publish/web/dynamic-website/hosting/self-hosting

A minimal Flet application that displays 'Hello, world!' on a page. This serves as a basic example to test the hosting setup. The app runs on port 8000 by default.

```python
import flet as ft  

def main(page: ft.Page):  
    page.title = "My Flet app"  
    page.add(ft.Text("Hello, world!"))  

if __name__ == "__main__":  
    ft.app(main)  

```

--------------------------------

### Basic Example

Source: <https://flet.dev/docs/controls/cupertinocontextmenuaction>

A simple example demonstrating the usage of CupertinoContextMenuAction within a CupertinoContextMenu.

```APIDOC
## Basic Example

```python
import flet as ft

def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Image("https://picsum.photos/200/200"),
            actions=[
                ft.CupertinoContextMenuAction(
                    text="Action 1",
                    is_default_action=True,
                    trailing_icon=ft.Icons.CHECK,
                    on_click=lambda e: print("Action 1"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 2",
                    trailing_icon=ft.Icons.MORE,
                    on_click=lambda e: print("Action 2"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 3",
                    is_destructive_action=True,
                    trailing_icon=ft.Icons.CANCEL,
                    on_click=lambda e: print("Action 3"),
                ),
            ],
        )
    )

ft.app(main)
```

```

--------------------------------

### Basic Lottie Animation Example

Source: https://flet.dev/docs/controls/lottie

A simple example demonstrating how to use the Lottie control to display an animation from a URL.

```APIDOC
## Example: Basic Lottie Animation

### Description
This example shows how to instantiate a `Lottie` control with a source URL and add it to the page.

### Method
GET (Implicit for loading assets)

### Endpoint
N/A (Control usage within Flet app)

### Parameters
N/A (Configuration via control properties)

### Request Example
```python
import flet as ft
import flet_lottie as fl

def main(page: ft.Page):
    l = fl.Lottie(
        src="https://raw.githubusercontent.com/xvrh/lottie-flutter/refs/heads/master/example/assets/Logo/LogoSmall.json",
        reverse=False,
        animate=True,
    )
    c1 = ft.Container(content=l, bgcolor=ft.Colors.AMBER_ACCENT, padding=50)
    page.add(c1)

ft.app(target=main)
```

### Response

#### Success Response (200)

- **`Lottie` control instance** - The Lottie animation displayed on the Flet page.

#### Response Example

(Visual rendering of the Lottie animation within the Flet application)

```

--------------------------------

### Image Example

Source: https://flet.dev/docs/controls/image

A live example demonstrating how to use the Image control in Flet, including loading local and remote images.

```APIDOC
## Image Example

### Description
This example showcases the Flet Image control, demonstrating how to display both a local asset image and multiple remote images in a scrollable row.

### Method
```python
import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    images = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.app(main)
```

### Request Body

N/A (This is a client-side control example)

### Response

N/A (This is a client-side control example)

```

--------------------------------

### ResponsiveRow Live Example

Source: https://flet.dev/docs/controls/responsiverow

Provides a complete Python code example demonstrating a dynamic ResponsiveRow that updates on page resize.

```APIDOC
## GET /api/responsive_row_live_example

### Description
This endpoint provides a full Python code example for a live, interactive ResponsiveRow. It includes functionality to display the current page width and updates the layout based on window resizing.

### Method
GET

### Endpoint
/api/responsive_row_live_example

### Parameters
None

### Request Example
(No request body for GET request)

### Response
#### Success Response (200)
- **code** (string) - The Python code for the live ResponsiveRow example.

#### Response Example
```python
import flet as ft

def main(page: ft.Page):
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize

    pw = ft.Text(bottom=50, right=50, style=ft.TextTheme.display_small)
    page.overlay.append(pw)
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
            run_spacing={"xs": 10},
        ),
    )
    page_resize(None)

ft.app(main)
```

```

--------------------------------

### Audio Player with Controls Example

Source: https://flet.dev/docs/controls/audio

An example showcasing the `flet_audio` library to create an audio player with various playback controls like play, pause, seek, volume, and balance.

```APIDOC
## Audio with Playback Controls

### Description
This example demonstrates the usage of the `flet_audio.Audio` control to build a full-featured audio player. It includes buttons for play, pause, resume, release, seeking, volume adjustment, and balance control.

### Method
`fa.Audio`

### Endpoint
N/A (Client-side control)

### Parameters
#### Request Body
- **src** (string) - Required - The URL of the audio file.
- **autoplay** (bool) - Optional - If true, the audio will start playing automatically.
- **volume** (float) - Optional - Initial volume level (0.0 to 1.0).
- **balance** (float) - Optional - Initial stereo balance (-1.0 to 1.0).
- **on_loaded** (function) - Optional - Callback when audio is loaded.
- **on_duration_changed** (function) - Optional - Callback when duration changes.
- **on_position_changed** (function) - Optional - Callback when playback position changes.
- **on_state_changed** (function) - Optional - Callback for audio state changes.
- **on_seek_complete** (function) - Optional - Callback when seek operation completes.

### Request Example
```python
import flet as ft
import flet_audio as fa

url = "https://github.com/mdn/webaudio-examples/blob/main/audio-basics/outfoxing.mp3?raw=true"

def main(page: ft.Page):
    def volume_down(_):
        audio1.volume -= 0.1
        audio1.update()

    def volume_up(_):
        audio1.volume += 0.1
        audio1.update()

    def balance_left(_):
        audio1.balance -= 0.1
        audio1.update()

    def balance_right(_):
        audio1.balance += 0.1
        audio1.update()

    def play(_):
        audio1.play()

    def pause(_):
        audio1.pause()

    def resume(_):
        audio1.resume()

    def release(_):
        audio1.release()

    def seek(_):
        audio1.seek(3000)

    def get_duration(_):
        print("Current duration:", audio1.get_duration())

    def get_position(_):
        print("Current position:", audio1.get_current_position())

    audio1 = fa.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.overlay.append(audio1)
    page.add(
        ft.ElevatedButton("Play", on_click=play),
        ft.ElevatedButton("Pause", on_click=pause),
        ft.ElevatedButton("Resume", on_click=resume),
        ft.ElevatedButton("Release", on_click=release),
        ft.ElevatedButton("Seek 3s", on_click=seek),
        ft.Row(
            [
                ft.ElevatedButton("Volume down", on_click=volume_down),
                ft.ElevatedButton("Volume up", on_click=volume_up),
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton("Balance left", on_click=balance_left),
                ft.ElevatedButton("Balance right", on_click=balance_right),
            ]
        ),
        ft.ElevatedButton("Get duration", on_click=get_duration),
        ft.ElevatedButton("Get current position", on_click=get_position),
    )

ft.app(main)
```

### Response

#### Success Response (200)

N/A (Client-side control)

#### Response Example

N/A

```

--------------------------------

### MenuItemButton Basic Example

Source: https://flet.dev/docs/controls/menuitembutton

A basic example demonstrating the usage of MenuItemButton within a MenuBar to change background colors.

```APIDOC
## Basic Example

### Description
This example shows how to use `MenuItemButton` within a `MenuBar` to allow users to select background colors for a container.

### Method
N/A (UI Component)

### Endpoint
N/A (UI Component)

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Blue"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Green"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Red"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Row([menubar]),
        ft.Container(
            ref=bg_container,
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Text(
                "Choose a bgcolor from the menu",
                style=ft.TextStyle(weight=ft.FontWeight.W_500),
            ),
            alignment=ft.alignment.center,
        ),
    )

ft.app(main)
```

### Response

#### Success Response (200)

N/A (UI Component)

#### Response Example

N/A (UI Component)

```

--------------------------------

### Switch Basic Example

Source: https://flet.dev/docs/controls/switch

A basic example demonstrating the usage of the Switch control with different configurations.

```APIDOC
## Basic Switches

### Code Example

```python
import flet as ft

def main(page):
    def button_clicked(e):
        t.value = f"Switch values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}."
        page.update()

    t = ft.Text()
    c1 = ft.Switch(label="Unchecked switch", value=False)
    c2 = ft.Switch(label="Checked switch", value=True)
    c3 = ft.Switch(label="Disabled switch", disabled=True)
    c4 = ft.Switch(
        label="Switch with rendered label_position='left'",
        label_position=ft.LabelPosition.LEFT,
    )
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(c1, c2, c3, c4, b, t)

ft.app(target=main)
```

### Description

This example showcases four `Switch` controls: an unchecked switch, a checked switch, a disabled switch, and a switch with its label positioned to the left. A button is included to display the current values of all switches when clicked.

```

--------------------------------

### Autoplay Audio Example

Source: https://flet.dev/docs/controls/audio

A Flet example demonstrating how to use the Audio control to autoplay an audio file and control playback with a button.

```APIDOC
## Autoplay Audio

### Description
This example shows how to use the `ft.Audio` control to automatically play an audio file upon loading and provides a button to pause or resume playback.

### Method
`ft.Audio`

### Endpoint
N/A (Client-side control)

### Parameters
#### Request Body
- **src** (string) - Required - The URL of the audio file.
- **autoplay** (bool) - Optional - If true, the audio will start playing automatically.
- **on_state_changed** (function) - Optional - Callback function for audio state changes.

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.title = "Audio Example"

    def change_button(e):
        if e.state == ft.AudioState.PAUSED:
            b.text = "Resume playing"
            b.on_click = lambda e: audio1.resume()

        elif e.state == ft.AudioState.PLAYING:
            b.text = "Pause playing"
            b.on_click = lambda e: audio1.pause()

        b.update()

    audio1 = ft.Audio(
        src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
        autoplay=True,
        on_state_changed=change_button,
    )
    b = ft.ElevatedButton("Pause playing", on_click=lambda _: audio1.pause())

    page.overlay.append(audio1)
    page.add(ft.Text("This is an app with background audio."), b)

ft.app(main)
```

### Response

#### Success Response (200)

N/A (Client-side control)

#### Response Example

N/A

```

--------------------------------

### Get Initial Route in Flet

Source: https://flet.dev/docs/getting-started/navigation-and-routing

Demonstrates how to access and display the initial route of a Flet application. This is useful for understanding the starting point of the user's navigation or deep link. It uses the `page.route` property.

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

ft.app(main, view=ft.AppView.WEB_BROWSER)
```

--------------------------------

### Flet Counter App Example (Python)

Source: <https://flet.dev/docs/index>

A basic Flet application demonstrating a counter with increment and decrement buttons. It uses Flet controls like TextField and IconButton, and handles user interactions with event listeners. Requires the 'flet' library to be installed.

```python
import flet as ft  

def main(page: ft.Page):  
    page.title = "Flet counter example"  
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)  

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)  
        page.update()  

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)  
        page.update()  

    page.add(  
        ft.Row(  
            [  
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),  
                txt_number,  
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),  
            ],  
            alignment=ft.MainAxisAlignment.CENTER,  
        )  
    )  

ft.app(main)  

```

--------------------------------

### Flet Project Structure Example

Source: <https://flet.dev/docs/publish>

Illustrates the minimal directory and file structure expected by the `flet build` command. It highlights `main.py` as the entry point and the optional `assets` directory for application resources and icons.

```text
├── README.md
├── pyproject.toml
└── src
    ├── assets
    │   └── icon.png
    └── main.py

```

--------------------------------

### DropdownM2 with Label and Hint - Flet Python

Source: <https://flet.dev/docs/controls/dropdownm2>

Shows how to configure a DropdownM2 with a descriptive label and a helpful hint text to guide the user. This example utilizes the flet library. It takes label and hint text as configuration and displays a dropdown with selectable options.

```python
import flet as ft


def main(page: ft.Page):
    page.add(
        ft.DropdownM2(
            label="Color",
            hint_text="Choose your favourite color?",
            options=[
                ft.dropdownm2.Option("Red"),
                ft.dropdownm2.Option("Green"),
                ft.dropdownm2.Option("Blue"),
            ],
            autofocus=True,
        )
    )


ft.app(main)

```

--------------------------------

### Start Flet App with Hidden Window and Make Visible

Source: <https://flet.dev/docs/reference/types/window>

This code example shows how to launch a Flet application with its window initially hidden and then make it visible after a delay. It utilizes `ft.AppView.FLET_APP_HIDDEN` to hide the window on startup and then sets `page.window.visible` to `True` after a 3-second pause, followed by a page update.

```python
from time import sleep

import flet as ft


def main(page: ft.Page):

    page.add(ft.Text("Hello!"))
    sleep(3)
    page.window.visible = True
    page.update()


ft.app(main, view=ft.AppView.FLET_APP_HIDDEN)
```

--------------------------------

### Flet GitHub OAuth Authentication Example

Source: <https://flet.dev/docs/cookbook/authentication>

A complete example of setting up and handling GitHub OAuth authentication in a Flet web application. It includes configuring the provider, handling login and logout button clicks, and responding to login/logout events to update the UI.

```python
import os

import flet
from flet import ElevatedButton, LoginEvent, Page
from flet.auth.providers import GitHubOAuthProvider

def main(page: Page):
    provider = GitHubOAuthProvider(
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        redirect_url="http://localhost:8550/oauth_callback",
    )

    def login_button_click(e):
        page.login(provider, scope=["public_repo"])

    def on_login(e: LoginEvent):
        if not e.error:
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    login_button = ElevatedButton("Login with GitHub", on_click=login_button_click)
    logout_button = ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)

flet.app(main, port=8550, view=flet.WEB_BROWSER)

```

--------------------------------

### Python BottomAppBar Example

Source: <https://flet.dev/docs/controls/bottomappbar>

Demonstrates how to create and configure a BottomAppBar in Flet. This example showcases setting the background color, shape, and content, including navigation icons and a placeholder for a floating action button. It utilizes the flet library to build the UI.

```python
import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, shape=ft.CircleBorder()
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.appbar = ft.AppBar(
        title=ft.Text("Bottom AppBar Demo"),
        center_title=True,
        bgcolor=ft.Colors.GREEN_300,
        automatically_imply_leading=False,
    )
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
            ]
        ),
    )

    page.add(ft.Text("Body!"))


ft.app(main)
```

--------------------------------

### Basic CupertinoContextMenu Example in Python

Source: <https://flet.dev/docs/controls/cupertinocontextmenu>

Demonstrates how to create a basic CupertinoContextMenu in Flet. This example shows how to configure the content, enable haptic feedback, and define a list of actions with different properties like default and destructive actions. The `ft.app(main)` function is used to run the Flet application.

```python
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Image("https://picsum.photos/200/200"),
            actions=[
                ft.CupertinoContextMenuAction(
                    text="Action 1",
                    is_default_action=True,
                    trailing_icon=ft.Icons.CHECK,
                    on_click=lambda e: print("Action 1"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 2",
                    trailing_icon=ft.Icons.MORE,
                    on_click=lambda e: print("Action 2"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 3",
                    is_destructive_action=True,
                    trailing_icon=ft.Icons.CANCEL,
                    on_click=lambda e: print("Action 3"),
                ),
            ],
        )
    )


ft.app(main)
```

--------------------------------

### Python: Autoplay Audio with Flet

Source: <https://flet.dev/docs/controls/audio>

Demonstrates how to use the Flet Audio control to autoplay an audio file. This example shows basic setup, state change handling, and integration with a button to pause/resume playback. Autoplay may be restricted in some browsers.

```python
import flet as ft


def main(page: ft.Page):
    page.title = "Audio Example"

    def change_button(e):
        if e.state == ft.AudioState.PAUSED:
            b.text = "Resume playing"
            b.on_click = lambda e: audio1.resume()

        elif e.state == ft.AudioState.PLAYING:
            b.text = "Pause playing"
            b.on_click = lambda e: audio1.pause()

        b.update()

    audio1 = ft.Audio(
        src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
        autoplay=True,
        on_state_changed=change_button,
    )
    b = ft.ElevatedButton("Pause playing", on_click=lambda _: audio1.pause())

    page.overlay.append(audio1)
    page.add(ft.Text("This is an app with background audio."), b)


ft.app(main)

```

--------------------------------

### Basic CupertinoAppBar Example in Python

Source: <https://flet.dev/docs/controls/cupertinoappbar>

Demonstrates how to create a basic iOS-styled application bar using Flet's CupertinoAppBar. This example shows setting the leading icon, background color, trailing icon, and a middle text element. It requires the Flet library. The output is a Flet application with the specified app bar and a simple text body.

```python
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        trailing=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED),
        middle=ft.Text("CupertinoAppBar Example"),
        brightness=ft.Brightness.LIGHT,
    )
    page.add(ft.Text("Body!"))

ft.app(main)
```

--------------------------------

### Install Flet Module (Bash)

Source: <https://flet.dev/docs/index>

Command to install the Flet Python library using pip. This is a prerequisite for running Flet applications. It creates a new virtual environment for Flet.

```bash
pip install flet  

```

--------------------------------

### Flet RadialGradient Container Example

Source: <https://flet.dev/docs/reference/types/radialgradient>

Demonstrates how to create a Container widget with a RadialGradient background using Flet. The gradient transitions between yellow and blue colors. This example requires the Flet library to be installed and imported as 'ft'.

```python
Container(
    gradient=ft.RadialGradient(
       colors=[ft.Colors.YELLOW, ft.Colors.BLUE]
    ),
    width=150,
    height=150,
    border_radius=5
)
```

--------------------------------

### ListTile Example Usage

Source: <https://flet.dev/docs/controls/listtile>

A Python example demonstrating how to use the ListTile control in a Flet application.

```APIDOC
## Python Code Example for ListTile

### Description
This example showcases various configurations of the `ListTile` control, including different states and the inclusion of leading and trailing widgets.

### Language
Python

### Code
```python
import flet as ft

def main(page):
    page.title = "ListTile Examples"
    page.add(
        ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("One-line list tile"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line dense list tile"), dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS),
                            title=ft.Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ft.ListTile(
                            leading=ft.Image(src="/icons/icon-192.png", fit="contain"),
                            title=ft.Text("One-line with leading control"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line with trailing control"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text(
                                "One-line with leading and trailing controls"
                            ),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SNOOZE),
                            title=ft.Text(
                                "Two-line with leading and trailing controls"
                            ),
                            subtitle=ft.Text("Here is a second title."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )
    )

ft.app(main)
```

```

--------------------------------

### Simple AppBar in Python

Source: https://flet.dev/docs/controls/appbar

Demonstrates the creation of a basic AppBar in Flet. This example shows how to set the title, leading icon, background color, and action buttons including a popup menu. It requires the flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "AppBar Example"

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )
    page.add(ft.Text("Body!"))


ft.app(target=main)

```

--------------------------------

### Main Application Setup for Flet Card Game

Source: <https://flet.dev/docs/tutorials/python-solitaire>

The main function initializes the Flet page and adds the Solitaire game instance to it. This sets up the entry point for the Flet application, rendering the game board and its components.

```python
import flet as ft
from solitaire import Solitaire

def main(page: ft.Page):
    
   solitaire = Solitaire()
   
   page.add(solitaire)
   
ft.app(main)
```

--------------------------------

### Basic MenuItemButton Example - Flet Python

Source: <https://flet.dev/docs/controls/menuitembutton>

Demonstrates the basic usage of MenuItemButton within a MenuBar in Flet. This example showcases how to set up menu items with different background colors on hover and handle click and hover events. It requires the flet library.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.padding = 0  
    page.spacing = 0  
    page.theme_mode = ft.ThemeMode.LIGHT  
  
    bg_container = ft.Ref[ft.Container]()  
  
    def handle_color_click(e):  
        color = e.control.content.value  
        print(f"{color}.on_click")  
        bg_container.current.content.value = f"{color} background color"  
        bg_container.current.bgcolor = color.lower()  
        page.update()  
  
    def handle_on_hover(e):  
        print(f"{e.control.content.value}.on_hover")  
  
    menubar = ft.MenuBar(  
        expand=True,  
        controls=[  
            ft.SubmenuButton(  
                content=ft.Text("BgColors"),  
                controls=[  
                    ft.MenuItemButton(  
                        content=ft.Text("Blue"),  
                        leading=ft.Icon(ft.Icons.COLORIZE),  
                        style=ft.ButtonStyle(  
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}  
                        ),  
                        on_click=handle_color_click,  
                        on_hover=handle_on_hover,  
                    ),  
                    ft.MenuItemButton(  
                        content=ft.Text("Green"),  
                        leading=ft.Icon(ft.Icons.COLORIZE),  
                        style=ft.ButtonStyle(  
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}  
                        ),  
                        on_click=handle_color_click,  
                        on_hover=handle_on_hover,  
                    ),  
                    ft.MenuItemButton(  
                        content=ft.Text("Red"),  
                        leading=ft.Icon(ft.Icons.COLORIZE),  
                        style=ft.ButtonStyle(  
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}  
                        ),  
                        on_click=handle_color_click,  
                        on_hover=handle_on_hover,  
                    ),  
                ],  
            ),  
        ],  
    )  
  
    page.add(  
        ft.Row([menubar]),  
        ft.Container(  
            ref=bg_container,  
            expand=True,  
            bgcolor=ft.Colors.SURFACE,  
            content=ft.Text(  
                "Choose a bgcolor from the menu",  
                style=ft.TextStyle(weight=ft.FontWeight.W_500),  
            ),  
            alignment=ft.alignment.center,  
        ),  
    )  
  
  
ft.app(main)  
```

--------------------------------

### Install GStreamer for Flet Audio on Debian/Ubuntu

Source: <https://flet.dev/docs/publish/linux>

Installs the necessary GStreamer libraries required for Flet applications utilizing the `Audio` control. This ensures proper audio playback functionality within the packaged Linux app. It provides commands for both minimal and full installations.

```bash
apt install libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev  

```

```bash
apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio  

```

--------------------------------

### Flet Assist Chip Example

Source: <https://flet.dev/docs/controls/chip>

Demonstrates the creation and functionality of assist chips in Flet. Assist chips feature a leading icon and an on-click event, ideal for contextual and automated actions. This example shows how to handle click events to update the chip's appearance and trigger an external URL.

```python
import flet as ft

def main(page: ft.Page):
    def save_to_favorites_clicked(e):
        e.control.label.value = "Saved to favorites"
        e.control.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        e.control.disabled = True
        page.update()

    def open_google_maps(e):
        page.launch_url("https://maps.google.com")
        page.update()

    save_to_favourites = ft.Chip(
        label=ft.Text("Save to favourites"),
        leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
        bgcolor=ft.Colors.GREEN_200,
        disabled_color=ft.Colors.GREEN_100,
        autofocus=True,
        on_click=save_to_favorites_clicked,
    )

    open_in_maps = ft.Chip(
        label=ft.Text("9 min walk"),
        leading=ft.Icon(ft.Icons.MAP_SHARP),
        bgcolor=ft.Colors.GREEN_200,
        on_click=open_google_maps,
    )

    page.add(ft.Row([save_to_favourites, open_in_maps]))

ft.app(main)

```

--------------------------------

### Basic CupertinoTextField Example

Source: <https://flet.dev/docs/controls/cupertinotextfield>

Demonstrates the creation and basic usage of a CupertinoTextField alongside Material and adaptive text fields. This example shows how to set a placeholder text and style for the CupertinoTextField.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Material text field",
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
        ft.CupertinoTextField(
            placeholder_text="Cupertino text field",
            placeholder_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
        ft.TextField(
            adaptive=True,
            label="Adaptive text field",
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
    )

ft.app(main)
```

--------------------------------

### BarChart with Event Example

Source: <https://flet.dev/docs/controls/barchart>

An example demonstrating how to create and interact with a BarChart, including handling click events to highlight bars.

```APIDOC
## POST /chart/barchart/event

### Description
This endpoint demonstrates the usage of `BarChart` with interactive event handling. When a bar is hovered or clicked, it visually changes and displays a tooltip.

### Method
POST

### Endpoint
`/chart/barchart/event`

### Parameters

#### Query Parameters
None

#### Request Body
None

### Request Example
```json
{
  "message": "This is a sample request for the BarChart event endpoint."
}
```

### Response

#### Success Response (200)

- **chart_data** (object) - The data structure representing the BarChart.
  - **bar_groups** (array) - An array of `BarChartGroup` objects.
  - **bottom_axis** (object) - Configuration for the bottom axis.
  - **on_chart_event** (function) - The event handler function for chart interactions.
  - **interactive** (boolean) - Flag to enable interactive features.

#### Response Example

```json
{
  "chart_data": {
    "bar_groups": [
      {
        "x": 0,
        "bar_rods": [
          {
            "y": 5,
            "hovered": false,
            "width": 22,
            "color": "#FFFFFF",
            "bg_to_y": 20,
            "bg_color": "#81C784"
          }
        ]
      },
      {
        "x": 1,
        "bar_rods": [
          {
            "y": 6.5,
            "hovered": false,
            "width": 22,
            "color": "#FFFFFF",
            "bg_to_y": 20,
            "bg_color": "#81C784"
          }
        ]
      }
      // ... more bar groups
    ],
    "bottom_axis": {
      "labels": [
        {"value": 0, "label": {"text": "M"}},
        {"value": 1, "label": {"text": "T"}}
        // ... more labels
      ]
    },
    "on_chart_event": "function() { ... }",
    "interactive": true
  }
}
```

```

--------------------------------

### Install Zenity on Ubuntu/Debian

Source: https://flet.dev/docs/cookbook/file-picker-and-uploads

This command installs the Zenity package, a dependency for the FilePicker control when running Flet applications on Linux without a browser. Ensure your system's package list is up-to-date before running.

```bash
sudo apt-get install zenity
```

--------------------------------

### Python Virtual Environment and Dependency Installation

Source: <https://flet.dev/docs/publish/web/dynamic-website/hosting/self-hosting>

Commands to create and activate a Python virtual environment, and then install dependencies listed in 'requirements.txt'. This ensures a clean and isolated environment for the Flet application.

```bash
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

```

--------------------------------

### Install Python Dependencies with Poetry

Source: <https://flet.dev/docs/extend/user-extensions>

Installs Python dependencies using Poetry, a dependency management tool. This command reads the `pyproject.toml` file and installs the project's dependencies, ensuring a consistent development environment.

```bash
poetry install  
```

--------------------------------

### Flet Application Entry Point (src/main.py)

Source: <https://flet.dev/docs/getting-started/create-flet-app>

The 'src/main.py' file contains the main function for a Flet application. It defines the application's UI logic within the 'main()' function and initializes the Flet app using 'ft.app()'.

```python
import flet as ft

def main(page: ft.Page):
    # Add UI elements here
    page.add(ft.Text("Hello, Flet!"))

ft.app(target=main)
```

--------------------------------

### Install PyInstaller for Packaging

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Installs the PyInstaller tool, which is a dependency for the `flet pack` command to create standalone executable packages for Flet applications.

```shell
pip install pyinstaller
```

--------------------------------

### Flet Column Horizontal Alignment Example

Source: <https://flet.dev/docs/controls/column>

Demonstrates how to set the horizontal alignment of items within a Flet Column using CrossAxisAlignment. This example shows different alignment options like START, CENTER, and END.

```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_horiz_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    bgcolor=ft.Colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                column_with_horiz_alignment(ft.CrossAxisAlignment.END),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.app(target=main)
```

--------------------------------

### Flet CrossAxisAlignment Usage Example in Python

Source: <https://flet.dev/docs/reference/types/crossaxisalignment>

This Python code demonstrates the usage of the CrossAxisAlignment enum in Flet. It showcases how to align children within a Column, illustrating different alignment values like START, CENTER, and END. The example requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_horiz_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    bgcolor=ft.Colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                column_with_horiz_alignment(ft.CrossAxisAlignment.END),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.app(main)
```

--------------------------------

### Flet Basic Date Picker Example

Source: <https://flet.dev/docs/controls/datepicker>

Demonstrates how to implement a basic DatePicker in Flet. It shows how to open the date picker dialog, handle date changes, and dismissals. This example utilizes Flet's `page.open()` method to display the dialog.

```python
import datetime  
import flet as ft  
  
  
def main(page: ft.Page):  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
  
    def handle_change(e):  
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))  
  
    def handle_dismissal(e):  
        page.add(ft.Text(f"DatePicker dismissed"))  
  
    page.add(  
        ft.ElevatedButton(  
            "Pick date",  
            icon=ft.Icons.CALENDAR_MONTH,  
            on_click=lambda e: page.open(  
                ft.DatePicker(  
                    first_date=datetime.datetime(year=2000, month=10, day=1),  
                    last_date=datetime.datetime(year=2025, month=10, day=1),  
                    on_change=handle_change,  
                    on_dismiss=handle_dismissal,  
                )  
            ),  
        )  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Flet Column Vertical Alignment Example

Source: <https://flet.dev/docs/controls/column>

Demonstrates various vertical alignment options for child controls within a Flet Column. It showcases alignments like START, CENTER, END, SPACE_BETWEEN, SPACE_AROUND, and SPACE_EVENLY.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    def items(count):  
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER_500,  
                )  
            )  
        return items  
  
    def column_with_alignment(align: ft.MainAxisAlignment):  
        return ft.Column(  
            [  
                ft.Text(str(align), size=10),  
                ft.Container(  
                    content=ft.Column(items(3), alignment=align),  
                    bgcolor=ft.Colors.AMBER_100,  
                    height=400,  
                ),  
            ]  
        )  
  
    page.add(  
        ft.Row(  
            [  
                column_with_alignment(ft.MainAxisAlignment.START),  
                column_with_alignment(ft.MainAxisAlignment.CENTER),  
                column_with_alignment(ft.MainAxisAlignment.END),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),  
            ],  
            spacing=30,  
            alignment=ft.MainAxisAlignment.START,  
        )  
    )  
  
  
ft.app(target=main)  


```

--------------------------------

### Basic Placeholder Example - Flet Python

Source: <https://flet.dev/docs/controls/placeholder>

Demonstrates the basic usage of the Flet Placeholder control. This example adds a placeholder that expands to fill available space and uses a random material color. It requires the 'flet' library.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.add(  
        ft.Placeholder(expand=True, color=ft.Colors.random())  # random material color  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Flet PopupMenuButton Example

Source: <https://flet.dev/docs/controls/popupmenubutton>

Demonstrates how to create and use a PopupMenuButton in Flet. This example showcases adding different types of PopupMenuItems, including text-only items, items with icons, custom content, and checkable items. It also includes an event handler for click actions.

```python
import flet as ft  


def main(page: ft.Page):  
    def check_item_clicked(e):
        e.control.checked = not e.control.checked  
        page.update()  

    pb = ft.PopupMenuButton(  
        items=[
            ft.PopupMenuItem(text="Item 1"),  
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, text="Check power"),  
            ft.PopupMenuItem(  
                content=ft.Row(  
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),  
                        ft.Text("Item with a custom content"),  
                    ]
                ),  
                on_click=lambda _: print("Button with custom content clicked!"),  
            ),  
            ft.PopupMenuItem(),  # divider  
            ft.PopupMenuItem(  
                text="Checked item", checked=False, on_click=check_item_clicked  
            ),
        ]  
    )
    page.add(pb)


ft.app(main)
```

--------------------------------

### Display Images with Flet Image Control (Python)

Source: <https://flet.dev/docs/controls/image>

This Python code snippet demonstrates how to use the Flet Image control to display images. It shows how to load local assets and remote URLs, customize image appearance with properties like width, height, fit, and border_radius, and handle multiple images in a scrollable row. This example requires the flet library to be installed.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    images = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.app(main)

```

--------------------------------

### Flet Row Vertical Alignment Example

Source: <https://flet.dev/docs/controls/row>

Demonstrates how to set the vertical alignment of controls within a Flet Row. It showcases `START`, `CENTER`, and `END` alignments by creating rows with different `vertical_alignment` settings.

```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def row_with_vertical_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), vertical_alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=150,
                ),
            ]
        )

    page.add(
        row_with_vertical_alignment(ft.CrossAxisAlignment.START),
        row_with_vertical_alignment(ft.CrossAxisAlignment.CENTER),
        row_with_vertical_alignment(ft.CrossAxisAlignment.END),
    )

ft.app(main)
```

--------------------------------

### Flet Clickable Container Example

Source: <https://flet.dev/docs/controls/container>

Demonstrates how to create clickable Flet Containers, with and without ink effects. This example showcases different configurations for background color, size, and click event handling. It requires the 'flet' library.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.title = "Containers - clickable and not"  
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
  
    page.add(  
        ft.Row(  
            [  
                ft.Container(  
                    content=ft.Text("Non clickable"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.AMBER,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable without Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.GREEN_200,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    on_click=lambda e: print("Clickable without Ink clicked!"),  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable with Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.CYAN_200,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    ink=True,  
                    on_click=lambda e: print("Clickable with Ink clicked!"),  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable transparent with Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    ink=True,  
                    on_click=lambda e: print("Clickable transparent with Ink clicked!"),  
                ),  
            ],  
            alignment=ft.MainAxisAlignment.CENTER,  
        ),  
    )  
  
  
ft.app(main)  
```

--------------------------------

### Basic InteractiveViewer Example

Source: <https://flet.dev/docs/controls/interactiveviewer>

This example demonstrates how to use the InteractiveViewer control to display an image that can be panned and zoomed. It sets minimum and maximum scale values, boundary margins, and event handlers for interaction.

```python
import flet as ft  

def main(page: ft.Page):  
    page.add(  
        ft.InteractiveViewer(  
            min_scale=0.1,  
            max_scale=15,  
            boundary_margin=ft.margin.all(20),  
            on_interaction_start=lambda e: print(e),  
            on_interaction_end=lambda e: print(e),  
            on_interaction_update=lambda e: print(e),  
            content=ft.Image(  
                src="https://picsum.photos/500/500",  
            ),  
        )  
    )  

ft.app(main)  

```

--------------------------------

### Basic ReorderableListView Example in Python

Source: <https://flet.dev/docs/controls/reorderablelistview>

Demonstrates how to implement a ReorderableListView in Flet, showcasing both horizontal and vertical layouts. It includes a basic setup with containers and list tiles, and an event handler for reordering actions. The primary color is set for the reorder handle.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "ReorderableListView Demo"
    page.theme_mode = ft.ThemeMode.DARK

    # the primary color is the color of the reorder handle
    page.theme = page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=ft.Colors.BLUE)
    )

    def handle_reorder(e: ft.OnReorderEvent):
        print(f"Reordered from {e.old_index} to {e.new_index}")

    get_color = lambda i: (
        ft.Colors.ERROR if i % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER
    )

    # horizontal
    h = ft.ReorderableListView(
        expand=True,
        horizontal=True,
        on_reorder=handle_reorder,
        controls=[
            ft.Container(
                content=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                bgcolor=get_color(i),
                margin=ft.margin.symmetric(horizontal=5, vertical=10),
                width=100,
                alignment=ft.alignment.center,
            )
            for i in range(10)
        ],
    )

    # vertical
    v = ft.ReorderableListView(
        expand=True,
        on_reorder=handle_reorder,
        controls=[
            ft.ListTile(
                title=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                leading=ft.Icon(ft.Icons.CHECK, color=ft.Colors.RED),
                bgcolor=get_color(i),
            )
            for i in range(10)
        ],
    )

    page.add(h, v)

ft.app(main)
```

--------------------------------

### Basic Flet WebView Implementation

Source: <https://flet.dev/docs/controls/webview>

A straightforward example demonstrating how to initialize and display a WebView in a Flet application. It loads the 'flet.dev' website and includes basic event handlers for page loading and errors. The `expand=True` property ensures the WebView takes up available space.

```python
import flet as ft
import flet_webview as ftwv


def main(page: ft.Page):
    wv = ftwv.WebView(
        url="https://flet.dev",
        on_page_started=lambda _: print("Page started"),
        on_page_ended=lambda _: print("Page ended"),
        on_web_resource_error=lambda e: print("Page error:", e.data),
        expand=True,
    )
    page.add(wv)


ft.app(main)

```

--------------------------------

### RangeSlider with Event Handling in Python

Source: <https://flet.dev/docs/controls/rangeslider>

This example shows how to implement event handling for a Flet RangeSlider. It defines functions to capture the start, change, and end of the slider interaction. The `on_change_end` event updates a Text control with the final selected range. The slider is configured with minimum and maximum values, and initial start and end values.

```python
import flet as ft

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    def slider_change_start(e):
        print(f"on_change_start: {e.control.start_value}, {e.control.end_value}")

    def slider_is_changing(e):
        print(f"on_change: {e.control.start_value}, {e.control.end_value}")

    def slider_change_end(e):
        print(f"on_change_end: {e.control.start_value}, {e.control.end_value}")
        t.value = f"on_change_end: {e.control.start_value}, {e.control.end_value}"
        page.update()

    t = ft.Text("")

    range_slider = ft.RangeSlider(
        min=0,
        max=50,
        start_value=10,
        end_value=20,
        on_change_start=slider_change_start,
        on_change=slider_is_changing,
        on_change_end=slider_change_end,
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Range slider with events",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                range_slider,
                t,
            ],
        )
    )

ft.app(main)

```

--------------------------------

### Enabling and Managing Flet App Systemd Service

Source: <https://flet.dev/docs/publish/web/dynamic-website/hosting/self-hosting>

Commands to enable and manage the Flet application's systemd service. This includes creating a symbolic link to the service file, starting the service, enabling it to start on boot, and checking its status.

```bash
cd /etc/systemd/system  
sudo ln -s /home/ubuntu/flet-app/flet.service  
sudo systemctl start flet  
sudo systemctl enable flet  
sudo systemctl status flet  

```

--------------------------------

### Dockerfile for Flet Application

Source: <https://flet.dev/docs/publish/web/dynamic-website/hosting/fly-io>

This Dockerfile defines the steps to build a container image for your Flet application. It installs dependencies, copies application code, exposes the necessary port, and sets the entrypoint command.

```dockerfile
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

--------------------------------

### Create basic Hello World app with Flet

Source: <https://flet.dev/docs/tutorials/python-todo>

A simple 'Hello, world!' application using the Flet framework. This example demonstrates the basic structure of a Flet app, including importing the library, defining the main function that takes a page object, adding a text control, and running the app. No external dependencies beyond the 'flet' package are required.

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))

ft.app(main)

```

--------------------------------

### Switch with on_change Event Example

Source: <https://flet.dev/docs/controls/switch>

An example demonstrating how to use the `on_change` event of the Switch control to toggle theme mode.

```APIDOC
## Switch with `on_change` event

### Code Example

```python
import flet as ft

def main(page: ft.Page):
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        c.label = (
            "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        page.update()

    page.theme_mode = ft.ThemeMode.LIGHT
    c = ft.Switch(label="Light theme", on_change=theme_changed)
    page.add(c)

ft.app(target=main)
```

### Description

This example uses a `Switch` control to toggle between light and dark themes for the Flet page. The `on_change` event handler updates the `page.theme_mode` and modifies the switch's label accordingly.

```

--------------------------------

### Flet TextFields with Prefixes and Suffixes

Source: https://flet.dev/docs/controls/textfield

Demonstrates Flet TextFields with various prefixes and suffixes, including text, icons, helper text, and character counters. This example shows how to add visual cues or constraints to the input fields.

```python
import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Textboxes values are:  '{pr.value}', '{sf.value}', '{ps.value}', '{icon.value}'."
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    pr = ft.TextField(label="With prefix", prefix_text="https://")
    sf = ft.TextField(label="With suffix", suffix_text=".com")
    ps = ft.TextField(
        label="With prefix and suffix", prefix_text="https://", suffix_text=".com"
    )
    icon = ft.TextField(
        label="My favorite color",
        icon=ft.Icons.FORMAT_SIZE,
        hint_text="Type your favorite color",
        helper_text="You can type only one color",
        counter_text="{value_length}/{max_length} chars used",
        prefix_icon=ft.Icons.COLOR_LENS,
        suffix_text="...is your color",
        max_length=20,
    )
    page.add(pr, sf, ps, icon, b, t)

ft.app(main)

```

--------------------------------

### Configure .replit for Flet

Source: <https://flet.dev/docs/publish/web/dynamic-website/hosting/replit>

These options in the `.replit` file control package installation behavior. `disableInstallBeforeRun` prevents packages from being installed before each run, and `disableGuessImports` stops the packager from automatically detecting and installing dependencies, though it will still run to install packages when the Repl is executed.

```ini
# Stops the packager from installing packages when running the Repl  
disableInstallBeforeRun = true  
# Stops the packager from guessing and auto-installing packages, but it still runs to install packages when running the Repl  
disableGuessImports = true  
```

--------------------------------

### Install Python Dependencies

Source: <https://flet.dev/docs/extend/user-extensions>

Installs Python dependencies from the project's `pyproject.toml` file. This command is used after making changes to the Python files of the Flet project to ensure all necessary libraries are installed or updated in the virtual environment.

```bash
pip install .  
```

--------------------------------

### Publish Flet App with Pre-release Packages

Source: <https://flet.dev/docs/publish/web/static-website>

Publishes a Flet application and allows `micropip` to install pre-release versions of Python packages. This is achieved by adding the `--pre` flag to the `flet publish` command.

```bash
flet publish <your-flet-app.py> --pre
```

--------------------------------

### AnimatedSwitcher Python Example with Scale, Fade, and Rotate Transitions

Source: <https://flet.dev/docs/controls/animatedswitcher>

This Python code demonstrates how to use the Flet AnimatedSwitcher control to animate transitions between two container widgets. It includes examples of SCALE, FADE, and ROTATION transitions, allowing users to switch between animations via buttons. The example utilizes custom curves and durations for the animations.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "AnimatedSwitcher examples"

    c1 = ft.Container(
        ft.Text("Hello!", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.Colors.GREEN,
    )
    c2 = ft.Container(
        ft.Text("Bye!", size=50),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.Colors.YELLOW,
    )
    c = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    def scale(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.SCALE
        c.update()

    def fade(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.FADE
        c.update()

    def rotate(e):
        c.content = c2 if c.content == c1 else c1
        c.transition = ft.AnimatedSwitcherTransition.ROTATION
        c.update()

    page.add(
        c,
        ft.ElevatedButton("Scale", on_click=scale),
        ft.ElevatedButton("Fade", on_click=fade),
        ft.ElevatedButton("Rotate", on_click=rotate),
    )

ft.app(main)

```

--------------------------------

### CupertinoAlertDialog and Adaptive AlertDialog Example in Python

Source: <https://flet.dev/docs/controls/cupertinoalertdialog>

Demonstrates how to use CupertinoAlertDialog, AlertDialog, and adaptive dialogs in Flet. It shows how to configure actions for each dialog type and how to open them using page.open(). The adaptive dialog example showcases platform-specific action button rendering.

```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    def handle_action_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.text}"))
        # e.control is the clicked action button, e.control.parent is the corresponding parent dialog of the button
        page.close(e.control.parent)

    cupertino_actions = [
        ft.CupertinoDialogAction(
            "Yes",
            is_destructive_action=True,
            on_click=handle_action_click,
        ),
        ft.CupertinoDialogAction(
            text="No",
            is_default_action=False,
            on_click=handle_action_click,
        ),
    ]

    material_actions = [
        ft.TextButton(text="Yes", on_click=handle_action_click),
        ft.TextButton(text="No", on_click=handle_action_click),
    ]

    page.add(
        ft.FilledButton(
            text="Open Material Dialog",
            on_click=lambda e: page.open(
                ft.AlertDialog(
                    title=ft.Text("Material Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=material_actions,
                )
            ),
        ),
        ft.CupertinoFilledButton(
            text="Open Cupertino Dialog",
            on_click=lambda e: page.open(
                ft.CupertinoAlertDialog(
                    title=ft.Text("Cupertino Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=cupertino_actions,
                )
            ),
        ),
        ft.FilledButton(
            text="Open Adaptive Dialog",
            adaptive=True,
            bgcolor=ft.Colors.BLUE_ACCENT,
            on_click=lambda e: page.open(
                ft.AlertDialog(
                    adaptive=True,
                    title=ft.Text("Adaptive Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=(
                        cupertino_actions
                        if page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.MACOS]
                        else material_actions
                    ),
                )
            ),
        ),
    )


ft.app(main)

```

--------------------------------

### Tabs Control - Simple Example

Source: <https://flet.dev/docs/controls/tabs>

Demonstrates the basic usage of the Tabs control with simple text content for each tab.

```APIDOC
## POST /api/tabs/simple

### Description
This endpoint demonstrates the basic usage of the Tabs control with simple text content for each tab.

### Method
POST

### Endpoint
/api/tabs/simple

### Parameters
#### Query Parameters
- **selected_index** (integer) - Optional - The index of the initially selected tab.
- **animation_duration** (integer) - Optional - The duration of the animation in milliseconds when switching between tabs. Defaults to 300.
- **expand** (integer) - Optional - Controls the expansion behavior of the tabs. Defaults to 1.

#### Request Body
- **tabs** (array) - Required - An array of Tab objects to be displayed.
  - **text** (string) - Required - The text label for the tab.
  - **content** (object) - Required - The content to display when the tab is selected.
  - **icon** (string) - Optional - The icon to display for the tab.
  - **tab_content** (object) - Optional - Custom content for the tab's header (e.g., a CircleAvatar).

### Request Example
```json
{
  "selected_index": 1,
  "animation_duration": 300,
  "tabs": [
    {
      "text": "Tab 1",
      "content": {
        "type": "Container",
        "content": {
          "type": "Text",
          "value": "This is Tab 1"
        },
        "alignment": "center"
      }
    },
    {
      "text": "Tab 2",
      "icon": "SETTINGS",
      "content": {
        "type": "Container",
        "content": {
          "type": "Text",
          "value": "This is Tab 2"
        },
        "alignment": "center"
      }
    },
    {
      "tab_content": {
        "type": "CircleAvatar",
        "foreground_image_src": "https://avatars.githubusercontent.com/u/7119543?s=88&v=4"
      },
      "content": {
        "type": "Container",
        "content": {
          "type": "Text",
          "value": "This is Tab 3"
        },
        "alignment": "center"
      }
    }
  ],
  "expand": 1
}
```

### Response

#### Success Response (200)

- **status** (string) - Indicates the success of the operation.

#### Response Example

```json
{
  "status": "success"
}
```

```

--------------------------------

### Flet App Entry Point Initialization

Source: https://flet.dev/docs/tutorials/trello-clone

Initializes the Flet application and sets up the main page with a title, padding, and background color. It then instantiates the `TrelloApp` class and adds it to the page.

```python
import flet as ft

if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Flet Trello clone"
        page.padding = 0
        page.bgcolor = colors.BLUE_GREY_200
        app = TrelloApp(page)
        page.add(app)
        page.update()

    ft.app(main)
```

--------------------------------

### Test Published Flet Web App

Source: <https://flet.dev/docs/publish/web/static-website>

Starts a local HTTP server to test the static website generated by `flet build web`. It serves files from the `build/web` directory. Access the app via `http://localhost:8000`.

```bash
python -m http.server --directory build/web
```

--------------------------------

### Basic Flet Geolocator Example

Source: <https://flet.dev/docs/controls/geolocator>

A Python example demonstrating the basic usage of the Flet Geolocator control. It shows how to initialize the control, handle position changes and errors, request permissions, and retrieve location data. This snippet requires the `flet-geolocator` package.

```python
import flet as ft


async def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("Geolocator Tests"))

    def handle_position_change(e):
        page.add(ft.Text(f"New position: {e.latitude} {e.longitude}"))

    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
        on_position_change=handle_position_change,
        on_error=lambda e: page.add(ft.Text(f"Error: {e.data}")),
    )
    page.overlay.append(gl)

    settings_dlg = lambda handler: ft.AlertDialog(
        adaptive=True,
        title=ft.Text("Opening Location Settings..."),
        content=ft.Text(
            "You are about to be redirected to the location/app settings. "
            "Please locate this app and grant it location permissions."
        ),
        actions=[ft.TextButton(text="Take me there", on_click=handler)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    async def handle_permission_request(e):
        p = await gl.request_permission_async(wait_timeout=60)
        page.add(ft.Text(f"request_permission: {p}"))

    async def handle_get_permission_status(e):
        p = await gl.get_permission_status_async()
        page.add(ft.Text(f"get_permission_status: {p}"))

    async def handle_get_current_position(e):
        p = await gl.get_current_position_async()
        page.add(ft.Text(f"get_current_position: ({p.latitude}, {p.longitude})"))

    async def handle_get_last_known_position(e):
        p = await gl.get_last_known_position_async()
        page.add(ft.Text(f"get_last_known_position: ({p.latitude}, {p.longitude})"))

    async def handle_location_service_enabled(e):
        p = await gl.is_location_service_enabled_async()
        page.add(ft.Text(f"is_location_service_enabled: {p}"))

    async def handle_open_location_settings(e):
        p = await gl.open_location_settings_async()
        page.close(location_settings_dlg)
        page.add(ft.Text(f"open_location_settings: {p}"))

    async def handle_open_app_settings(e):
        p = await gl.open_app_settings_async()
        page.close(app_settings_dlg)
        page.add(ft.Text(f"open_app_settings: {p}"))

    location_settings_dlg = settings_dlg(handle_open_location_settings)
    app_settings_dlg = settings_dlg(handle_open_app_settings)

    page.add(
        ft.Row(
            wrap=True,
            controls=[
                ft.OutlinedButton(
                    "Request Permission",
                    on_click=handle_permission_request,
                ),
                ft.OutlinedButton(
                    "Get Permission Status",
                    on_click=handle_get_permission_status,
                ),
                ft.OutlinedButton(
                    "Get Current Position",
                    on_click=handle_get_current_position,
                ),
                ft.OutlinedButton(
                    "Get Last Known Position",
                    visible=False if page.web else True,
                    on_click=handle_get_last_known_position,
                ),
                ft.OutlinedButton(
                    "Is Location Service Enabled",
                    on_click=handle_location_service_enabled,
                ),
                ft.OutlinedButton(
                    "Open Location Settings",
                    visible=False if page.web else True,
                    on_click=lambda e: page.open(location_settings_dlg),
                ),
                ft.OutlinedButton(
                    "Open App Settings",
                    visible=False if page.web else True,
                    on_click=lambda e: page.open(app_settings_dlg),
                ),
            ],
        )
    )


ft.app(main)

```

--------------------------------

### RangeSlider with Divisions and Labels in Python

Source: <https://flet.dev/docs/controls/rangeslider>

This example demonstrates how to create a RangeSlider with divisions and custom labels in Flet. It configures the slider's minimum and maximum values, initial start and end values, the number of divisions, and colors for different states. The label format is specified to display the value as a percentage.

```python
import flet as ft

def main(page: ft.Page):
    range_slider = ft.RangeSlider(
        min=0,
        max=50,
        start_value=10,
        divisions=10,
        end_value=20,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        label="{value}%",
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Range slider with divisions and labels",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                range_slider,
            ],
        )
    )

ft.app(main)

```

--------------------------------

### Flet Application Structure

Source: <https://flet.dev/docs/getting-started/create-flet-app>

The default directory structure generated by 'flet create'. It includes essential files like 'README.md', 'pyproject.toml', the main application logic in 'src/main.py', and directories for assets and storage.

```directory
├── README.md
├── pyproject.toml
├── src
│   ├── assets
│   │   └── icon.png
│   └── main.py
└── storage
    ├── data
    └── temp
```

--------------------------------

### Flet ExpansionTile Control Example in Python

Source: <https://flet.dev/docs/controls/expansiontile>

This Python code demonstrates how to use the Flet ExpansionTile control to create expandable list items. It shows different configurations for titles, subtitles, background colors, and custom expansion icons. The example also includes an event handler for expansion state changes.

```python
import flet as ft  


def main(page: ft.Page):  
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.spacing = 0  
    page.padding = 0  

    def handle_expansion_tile_change(e):  
        page.open(  
            ft.SnackBar(  
                ft.Text(  
                    f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"  
                ),  
                duration=1000,  
            )  
        )  
        if e.control.trailing:  
            e.control.trailing.name = (  
                ft.Icons.ARROW_DROP_DOWN  
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE  
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE  
            )  
            page.update()  

    page.add(  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 1"),  
            subtitle=ft.Text("Trailing expansion arrow icon"),  
            bgcolor=ft.Colors.BLUE_GREY_200,  
            collapsed_bgcolor=ft.Colors.BLUE_GREY_200,  
            affinity=ft.TileAffinity.PLATFORM,  
            maintain_state=True,  
            collapsed_text_color=ft.Colors.RED,  
            text_color=ft.Colors.RED,  
            controls=[  
                ft.ListTile(  
                    title=ft.Text("This is sub-tile number 1"),  
                    bgcolor=ft.Colors.BLUE_GREY_200,  
                )  
            ],  
        ),  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 2"),  
            subtitle=ft.Text("Custom expansion arrow icon"),  
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),  
            collapsed_text_color=ft.Colors.GREEN,  
            text_color=ft.Colors.GREEN,  
            on_change=handle_expansion_tile_change,  
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],  
        ),  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 3"),  
            subtitle=ft.Text("Leading expansion arrow icon"),  
            affinity=ft.TileAffinity.LEADING,  
            initially_expanded=True,  
            collapsed_text_color=ft.Colors.BLUE_800,  
            text_color=ft.Colors.BLUE_200,  
            controls=[  
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),  
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),  
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),  
            ],  
        ),  
    )  


ft.app(main)  
```

--------------------------------

### Basic Flet TextFields Example

Source: <https://flet.dev/docs/controls/textfield>

Demonstrates the creation and basic usage of multiple Flet TextFields with different configurations such as labels, disabled states, read-only modes, placeholders, and icons. It includes a submit button to display the entered values.

```python
import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb4.value}', '{tb5.value}'."
        page.update()

    t = ft.Text()
    tb1 = ft.TextField(label="Standard")
    tb2 = ft.TextField(label="Disabled", disabled=True, value="First name")
    tb3 = ft.TextField(label="Read-only", read_only=True, value="Last name")
    tb4 = ft.TextField(label="With placeholder", hint_text="Please enter text here")
    tb5 = ft.TextField(label="With an icon", icon=ft.Icons.EMOJI_EMOTIONS)
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(tb1, tb2, tb3, tb4, tb5, b, t)


ft.app(main)

```

--------------------------------

### Simple DataTable Example

Source: <https://flet.dev/docs/controls/datatable>

Demonstrates the basic usage of the DataTable control with columns and rows.

```APIDOC
## DataTable

A Material Design data table.

### Description

This section provides examples of how to create and style a DataTable in Flet.

### Code Example: Simple DataTable

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )

ft.app(main)
```

### Code Example: Styled DataTable

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            width=700,
            bgcolor=ft.Colors.YELLOW,
            border=ft.border.all(2, ft.Colors.RED),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREEN),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
            ],
        ),
    )

ft.app(target=main)
```

```

--------------------------------

### Enable Flet Startup Screen (TOML)

Source: https://flet.dev/docs/publish

Configures the startup screen, shown after the boot screen while third-party packages are unpacked and the app initializes. Similar to the boot screen, it can be enabled globally or per platform, with customizable messages. This configuration corresponds to `[tool.flet.app.startup_screen]` and `[tool.flet.<platform>.app.startup_screen]` sections in `pyproject.toml`.

```toml
[tool.flet.app.startup_screen]
show = true
message = "Starting up the app…"

```

```toml
[tool.flet.android.app.startup_screen]
show = true

```

--------------------------------

### Create New Flet App using poetry

Source: <https://flet.dev/docs/getting-started/create-flet-app>

This command creates a new Flet application using the 'poetry' package manager. 'poetry run' executes the 'flet create' command within the project's virtual environment managed by poetry.

```bash
poetry run flet create
```

--------------------------------

### PaintLinearGradient Usage Example in Flet

Source: <https://flet.dev/docs/reference/types/paintlineargradient>

This snippet demonstrates how to use the PaintLinearGradient class to create a rectangle with a linear gradient fill. It specifies the gradient's start and end points, and the colors to be used. The gradient is applied as a fill style to a cv.Rect object.

```python
cv.Rect(
    10,
    10,
    100,
    100,
    5,
    ft.Paint(
        gradient=ft.PaintLinearGradient(
            (0, 10), (0, 100), colors=[ft.Colors.BLUE, ft.Colors.YELLOW]
        ),
        style=ft.PaintingStyle.FILL,
    ),
)
```

--------------------------------

### Basic ElevatedButton Examples - Python

Source: <https://flet.dev/docs/controls/elevatedbutton>

Demonstrates how to create basic ElevatedButton controls and disabled buttons in Flet. This example shows the fundamental usage of the ElevatedButton and its disabled state.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Basic elevated buttons"

    page.add(
        ft.ElevatedButton(text="Elevated button"),
        ft.Button("Disabled button", disabled=True),
    )

ft.app(main)

```

--------------------------------

### Simple ExpansionPanelList Example in Python

Source: <https://flet.dev/docs/controls/expansionpanel>

Demonstrates how to create and manage a list of expandable panels using Flet's ExpansionPanelList and ExpansionPanel controls. It includes handling panel expansion/collapse events and deleting panels.

```python
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_change(e: ft.ControlEvent):
        print(f"change on panel with index {e.data}")

    def handle_delete(e: ft.ControlEvent):
        panel.controls.remove(e.control.data)
        page.update()

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        elevation=8,
        divider_color=ft.Colors.AMBER,
        on_change=handle_change,
        controls=[
            ft.ExpansionPanel(
                # has no header and content - placeholders will be used
                bgcolor=ft.Colors.BLUE_400,
                expanded=True,
            )
        ],
    )

    colors = [
        ft.Colors.GREEN_500,
        ft.Colors.BLUE_800,
        ft.Colors.RED_800,
    ]

    for i in range(3):
        bgcolor = colors[i % len(colors)]

        exp = ft.ExpansionPanel(
            bgcolor=bgcolor,
            header=ft.ListTile(title=ft.Text(f"Panel {i}"), bgcolor=bgcolor),
        )

        exp.content = ft.ListTile(
            title=ft.Text(f"This is in Panel {i}"),
            subtitle=ft.Text(f"Press the icon to delete panel {i}"),
            trailing=ft.IconButton(ft.Icons.DELETE, on_click=handle_delete, data=exp),
            bgcolor=bgcolor,
        )

        panel.controls.append(exp)

    page.add(panel)


ft.app(main)
```

--------------------------------

### Install MPV for Flet Video on Debian/Ubuntu

Source: <https://flet.dev/docs/publish/linux>

Installs the libmpv development libraries and the `mpv` player, which are required for Flet applications using the `Video` control. This enables proper video playback within the packaged Linux application.

```bash
sudo apt install libmpv-dev mpv  

```

--------------------------------

### Serve Flet Extension Documentation Locally

Source: <https://flet.dev/docs/extend/user-extensions>

Command to serve the documentation for a Flet extension locally using mkdocs, allowing for previewing changes before deployment.

```bash
mkdocs serve
```

--------------------------------

### Create and Navigate Flet Project

Source: <https://flet.dev/docs/getting-started/testing-on-ios>

Generates a new Flet project directory with a basic structure and then changes the current directory into the newly created project. This is the starting point for building a Flet application.

```bash
flet create my-app  
cd my-app  
```

--------------------------------

### Flet IconButton Examples

Source: <https://flet.dev/docs/controls/iconbutton>

Demonstrates creating basic Flet IconButtons with different icons, colors, and click event handlers to open snackbars. It shows how to add these buttons to a page.

```python
import flet as ft  
  

def main(page: ft.Page):  
    page.title = "Icon buttons"  
  
    sby = ft.SnackBar(ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_300))  
    sbn = ft.SnackBar(ft.Icon(ft.Icons.CANCEL, color=ft.Colors.PINK_700))  
    page.add(  
        ft.Row(  
            [  
                ft.IconButton(  
                    icon=ft.Icons.CHECK_CIRCLE,  
                    icon_color=ft.Colors.GREEN_300,  
                    icon_size=40,  
                    tooltip="Yep",  
                    on_click=lambda e: page.open(sby),  
                ),  
                ft.IconButton(  
                    icon=ft.Ico n.CANCEL,  
                    icon_color=ft.Colors.PINK_700,  
                    icon_size=40,  
                    tooltip="Nope",  
                    on_click=lambda e: page.open(sbn),  
                ),  
            ],  
            alignment=ft.MainAxisAlignment.CENTER,  
        ),  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Install Pillow for Icon Conversion

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Installs the Pillow library, which is necessary for PyInstaller to convert PNG icons to platform-specific formats (.ico for Windows, .icns for macOS) when packaging Flet applications.

```shell
pip install pillow
```

--------------------------------

### Create Flet Project Command

Source: <https://flet.dev/docs/publish>

Shows the command to create a new Flet project with the recommended structure. This command initializes a new directory with essential files for a Flet application.

```bash
flet create myapp

```

--------------------------------

### Install Rosetta 2 on macOS

Source: <https://flet.dev/docs/publish/macos>

Installs Rosetta 2, which is required for Flutter to run on Apple Silicon Macs. This command needs to be executed with administrator privileges.

```shell
sudo softwareupdate --install-rosetta --agree-to-license
```

--------------------------------

### List Installed Provisioning Profiles (Shell)

Source: <https://flet.dev/docs/publish/ios>

This command allows you to list all installed provisioning profiles on your macOS system. It iterates through the provisioning profiles directory, extracts the Name and UUID for each profile using security and xmllint, and then formats the output for easy readability.

```bash
for profile in ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision; do security cms -D -i "$profile" | grep -E -A1 '<key>(Name|UUID)</key>' | sed -n 's/.*<string>\(.*\)<\/string>/\1/p' | paste -d ' | ' - -; done
```

--------------------------------

### Install Flet Package

Source: <https://flet.dev/docs/getting-started/testing-on-ios>

Installs or upgrades the Flet package to the latest version using pip. This command ensures you have the most recent features and bug fixes for Flet development.

```bash
pip install flet --upgrade  
```

--------------------------------

### Basic CupertinoActivityIndicator Example in Python

Source: <https://flet.dev/docs/controls/cupertinoactivityindicator>

Demonstrates how to create and display a basic CupertinoActivityIndicator in Flet. This example shows setting the radius and color of the indicator. It requires the flet library.

```python
import flet as ft  

def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT  

    page.add(
        ft.CupertinoActivityIndicator(
            radius=50,
            color=ft.Colors.RED,
            animating=True,
        )
    )

ft.app(main)
```

--------------------------------

### Basic Flet TimePicker Example

Source: <https://flet.dev/docs/controls/timepicker>

Demonstrates how to implement a basic TimePicker in Flet. This example shows how to open the dialog, handle selection changes, dismissals, and entry mode changes. It requires the Flet library.

```python
import flet as ft  


def main(page: ft.Page):  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  

    def handle_change(e):  
        page.add(ft.Text(f"TimePicker change: {time_picker.value}"))  

    def handle_dismissal(e):  
        page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))  

    def handle_entry_mode_change(e):  
        page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))  

    time_picker = ft.TimePicker(  
        confirm_text="Confirm",  
        error_invalid_text="Time out of range",  
        help_text="Pick your time slot",  
        on_change=handle_change,  
        on_dismiss=handle_dismissal,  
        on_entry_mode_change=handle_entry_mode_change,  
    )  

    page.add(  
        ft.ElevatedButton(  
            "Pick time",  
            icon=ft.Icons.TIME_TO_LEAVE,  
            on_click=lambda _: page.open(time_picker),  
        )  
    )  


ft.app(main)  

```

--------------------------------

### Basic CupertinoButton Example

Source: <https://flet.dev/docs/controls/cupertinobutton>

Demonstrates the creation of different styles of CupertinoButton, including normal, filled, and disabled states. It also shows how ElevatedButton can adapt to a CupertinoButton appearance on Apple platforms. The example requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.CupertinoButton(
            content=ft.Text(
                "Normal CupertinoButton",
                color=ft.CupertinoColors.DESTRUCTIVE_RED,
            ),
            bgcolor=ft.CupertinoColors.LIGHT_BACKGROUND_GRAY,
            opacity_on_click=0.3,
            on_click=lambda e: print("Normal CupertinoButton clicked!"),
        ),
        ft.CupertinoButton(
            content=ft.Text("Filled CupertinoButton", color=ft.Colors.YELLOW),
            bgcolor=ft.Colors.PRIMARY,
            alignment=ft.alignment.top_left,
            border_radius=ft.border_radius.all(15),
            opacity_on_click=0.5,
            on_click=lambda e: print("Filled CupertinoButton clicked!"),
        ),
        ft.CupertinoButton(
            content=ft.Text("Disabled CupertinoButton"),
            bgcolor=ft.Colors.PRIMARY,
            disabled=True,
            alignment=ft.alignment.top_left,
            opacity_on_click=0.5,
        ),
        ft.ElevatedButton(
            adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
            bgcolor=ft.CupertinoColors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.Icons.FAVORITE, color="pink"),
                    ft.Text("ElevatedButton+adaptive"),
                ],
                tight=True,
            ),
        ),
    )

ft.app(main)
```

--------------------------------

### AppVeyor CI Configuration for Flet Packaging

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

This configuration file (`appveyor.yml`) defines the CI workflow for packaging a Flet application. It specifies build steps including installing dependencies, running `flet pack` for different platforms, and uploading the resulting artifacts. It assumes the presence of a `GITHUB_TOKEN` environment variable for publishing to GitHub releases.

```yaml
version: '{build}'

build:
  # Build the project, but don't run tests on AppVeyor
  # If you need tests to run on AppVeyor, uncomment the following line:
  # test: true

# Install dependencies and run flet pack
install:
  # Install Python (if not already installed)
  # - ps: "$ProgressPreference = 'SilentlyContinue'; Install-ChocolateyPackage Python3 -y"
  # Add Python to PATH
  # - set PATH=%%PYTHON3%%;%%PYTHON3%%\Scripts;!PATH!
  # Install pip requirements
  - pip install -r requirements.txt
  # Install Flet and PyInstaller
  - pip install flet[packaging]

# Build and package the app for Windows, macOS, and Ubuntu
build_script:
  # Package for Windows
  - flet pack -d -v
  # Package for macOS
  # - flet pack -d -m -v
  # Package for Ubuntu
  # - flet pack -d -l -v

# Upload artifacts (e.g., zip/tar app bundles)
artifacts:
  - path: dist\*
    name: FletApp-Windows
  # - path: dist/your_app_macOS.zip
  #   name: FletApp-macOS
  # - path: dist/your_app_linux.tar.gz
  #   name: FletApp-Linux

# Deploy to GitHub Releases (requires GITHUB_TOKEN)
# Only deploy when a new tag is pushed
deploy:
  - provider: GitHub
    release: '$(appveyor_repo_tag_name)'
    description: 'Release $(appveyor_repo_tag_name)'
    auth_token:
      secure: "$(GITHUB_TOKEN)"
    artifact: FletApp-Windows
    # artifact: FletApp-macOS
    # artifact: FletApp-Linux
    draft: false
    prerelease: false
    on: TAG

```

--------------------------------

### Flet LineChart: Single Toggle Example

Source: <https://flet.dev/docs/controls/linechart>

This Python code demonstrates the creation and interaction of a Flet LineChart. It includes defining two datasets, configuring chart axes and grid lines, and implementing a toggle function to switch between datasets and interactivity. The chart is designed to be responsive and visually informative.

```python
import flet as ft  
  
  
class State:
    toggle = True  
  
  
s = State()  
  
  
def main(page: ft.Page):  
    data_1 = [  
        ft.LineChartData(  
            data_points=[  
                ft.LineChartDataPoint(0, 3),  
                ft.LineChartDataPoint(2.6, 2),  
                ft.LineChartDataPoint(4.9, 5),  
                ft.LineChartDataPoint(6.8, 3.1),  
                ft.LineChartDataPoint(8, 4),  
                ft.LineChartDataPoint(9.5, 3),  
                ft.LineChartDataPoint(11, 4),  
            ],  
            stroke_width=5,  
            color=ft.Colors.CYAN,  
            curved=True,  
            stroke_cap_round=True,  
        )  
    ]  
  
    data_2 = [  
        ft.LineChartData(  
            data_points=[  
                ft.LineChartDataPoint(0, 3.44),  
                ft.LineChartDataPoint(2.6, 3.44),  
                ft.LineChartDataPoint(4.9, 3.44),  
                ft.LineChartDataPoint(6.8, 3.44),  
                ft.LineChartDataPoint(8, 3.44),  
                ft.LineChartDataPoint(9.5, 3.44),  
                ft.LineChartDataPoint(11, 3.44),  
            ],  
            stroke_width=5,  
            color=ft.Colors.CYAN,  
            curved=True,  
            stroke_cap_round=True,  
        )  
    ]  
  
    chart = ft.LineChart(  
        data_series=data_1,  
        border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),  
        horizontal_grid_lines=ft.ChartGridLines(  
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1  
        ),  
        vertical_grid_lines=ft.ChartGridLines(  
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1  
        ),  
        left_axis=ft.ChartAxis(  
            labels=[  
                ft.ChartAxisLabel(  
                    value=1,  
                    label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD),  
                ),  
                ft.ChartAxisLabel(  
                    value=3,  
                    label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD),  
                ),  
                ft.ChartAxisLabel(  
                    value=5,  
                    label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD),  
                ),  
            ],  
            labels_size=40,  
        ),  
        bottom_axis=ft.ChartAxis(  
            labels=[  
                ft.ChartAxisLabel(  
                    value=2,  
                    label=ft.Container(  
                        ft.Text(  
                            "MAR",  
                            size=16,  
                            weight=ft.FontWeight.BOLD,  
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),  
                        ),  
                        margin=ft.margin.only(top=10),  
                    ),  
                ),  
                ft.ChartAxisLabel(  
                    value=5,  
                    label=ft.Container(  
                        ft.Text(  
                            "JUN",  
                            size=16,  
                            weight=ft.FontWeight.BOLD,  
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),  
                        ),  
                        margin=ft.margin.only(top=10),  
                    ),  
                ),  
                ft.ChartAxisLabel(  
                    value=8,  
                    label=ft.Container(  
                        ft.Text(  
                            "SEP",  
                            size=16,  
                            weight=ft.FontWeight.BOLD,  
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),  
                        ),  
                        margin=ft.margin.only(top=10),  
                    ),  
                ),  
            ],  
            labels_size=32,  
        ),  
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),  
        min_y=0,  
        max_y=6,  
        min_x=0,  
        max_x=11,  
        # animate=5000,  
        expand=True,  
    )  
  
    def toggle_data(e):  
        if s.toggle:  
            chart.data_series = data_2  
            chart.interactive = False  
        else:  
            chart.data_series = data_1  
            chart.interactive = True  
        s.toggle = not s.toggle  
        chart.update()  
  
    page.add(ft.ElevatedButton("avg", on_click=toggle_data), chart)  
  
  
ft.app(main)  
```

--------------------------------

### Initialize Fly.io App

Source: <https://flet.dev/docs/publish/web/dynamic-website/hosting/fly-io>

This command creates and initializes a new Fly.io application. Replace `<your-app-name>` with your desired application name.

```bash
fly apps create --name <your-app-name>
```

--------------------------------

### Run Flet App for iOS Development

Source: <https://flet.dev/docs/getting-started/testing-on-ios>

Starts the Flet development server, enabling live preview of the Flet application on an iOS device. The `--ios` flag specifically targets iOS deployment.

```bash
flet run --ios  
```

--------------------------------

### Flet Margin Usage Examples

Source: <https://flet.dev/docs/reference/types/margin>

Demonstrates various ways to apply margins to Flet containers using the Margin class's helper methods. This includes applying margins to all sides, symmetric margins, and margins to specific sides. The examples show how to instantiate Margin objects and assign them to a container's margin property.

```python
container_1.margin = margin.all(10)
container_2.margin = 20 # same as margin.all(20)
container_3.margin = margin.symmetric(vertical=10)
container_4.margin = margin.only(left=10)
```

--------------------------------

### Flet Padding Examples

Source: <https://flet.dev/docs/reference/types/padding>

Demonstrates various ways to apply padding to Flet containers using the `Padding` class and its helper methods. This includes applying uniform padding, symmetric padding, and padding to specific sides.

```python
container_1.padding = ft.padding.all(10)
container_2.padding = 20
container_3.padding = ft.padding.symmetric(horizontal=10)
container_4.padding=padding.only(left=10)
```

--------------------------------

### Flet PermissionHandler Basic Example

Source: <https://flet.dev/docs/controls/permissionhandler>

This Python code demonstrates the basic usage of the PermissionHandler control in Flet. It shows how to initialize the control, add it to the page overlay, and implement functions to check, request, and open app settings for microphone permissions. The example utilizes Flet's UI elements like OutlinedButton and Text to display the status and results of permission operations.

```python
import flet as ft

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("PermissionHandler Tests"))
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    def check_permission(e):
        o = ph.check_permission(e.control.data)
        page.add(ft.Text(f"Checked {e.control.data.name}: {o}"))

    def request_permission(e):
        o = ph.request_permission(e.control.data)
        page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))

    def open_app_settings(e):
        o = ph.open_app_settings()
        page.add(ft.Text(f"App Settings: {o}"))

    page.add(
        ft.OutlinedButton(
            "Check Microphone Permission",
            data=ft.PermissionType.MICROPHONE,
            on_click=check_permission,
        ),
        ft.OutlinedButton(
            "Request Microphone Permission",
            data=ft.PermissionType.MICROPHONE,
            on_click=request_permission,
        ),
        ft.OutlinedButton(
            "Open App Settings",
            on_click=open_app_settings,
        ),
    )

ft.app(main)

```

--------------------------------

### Verify Flet CLI Installation

Source: <https://flet.dev/docs/getting-started/testing-on-ios>

Checks if the Flet command-line interface (CLI) is installed and accessible in the system's PATH. This confirms that Flet commands can be executed directly from the terminal.

```bash
flet --version  
```

--------------------------------

### Python Pagelet Example with Appbar, BottomAppBar, and Drawer

Source: <https://flet.dev/docs/controls/pagelet>

This example demonstrates how to create a Flet Pagelet control. It includes a custom AppBar, a BottomAppBar with action buttons, and an end drawer that can be opened via a FloatingActionButton. The Pagelet itself is configured with specific dimensions and background colors.

```python
import flet as ft  

def main(page: ft.Page):  
    def open_pagelet_end_drawer(e):  
        pagelet.show_drawer(ed)  
  
    ed = ft.NavigationDrawer(  
        controls=[  
            ft.NavigationDrawerDestination(  
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"  
            ),  
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_COMMENT, label="Item 2"),  
        ],  
    )  
    pagelet = ft.Pagelet(  
        appbar=ft.AppBar(  
            title=ft.Text("Pagelet AppBar Title"), bgcolor=ft.Colors.AMBER_ACCENT  
        ),  
        content=ft.Container(ft.Text("Pagelet Body"), padding=ft.padding.all(16)),  
        bgcolor=ft.Colors.AMBER_100,  
        bottom_app_bar=ft.BottomAppBar(  
            bgcolor=ft.Colors.BLUE,  
            shape=ft.NotchShape.CIRCULAR,  
            content=ft.Row(  
                controls=[  
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),  
                    ft.Container(expand=True),  
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),  
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),  
                ]  
            ),  
        ),  
        end_drawer=ed,  
        floating_action_button=ft.FloatingActionButton(  
            "Open", on_click=open_pagelet_end_drawer, shape=ft.CircleBorder()  
        ),  
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,  
        width=400,  
        height=400,  
    )  

    page.add(pagelet)  


ft.app(main)  
```

--------------------------------

### Basic CupertinoPicker Example in Python

Source: <https://flet.dev/docs/controls/cupertinopicker>

Demonstrates how to use the CupertinoPicker to create an iOS-style selection dialog. It allows users to pick a fruit from a list, with the selected fruit displayed and updated in real-time. This example utilizes Flet's CupertinoBottomSheet to present the picker.

```python
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    selected_fruit_ref = ft.Ref[ft.Text]()
    fruits = [
        "Apple",
        "Mango",
        "Banana",
        "Orange",
        "Pineapple",
        "Strawberry",
    ]

    def handle_picker_change(e):
        selected_fruit_ref.current.value = fruits[int(e.data)]
        page.update()

    cupertino_picker = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_picker_change,
        controls=[ft.Text(value=f) for f in fruits],
    )

    page.add(
        ft.Row(
            tight=True,
            controls=[
                ft.Text("Selected Fruit:", size=23),
                ft.TextButton(
                    content=ft.Text(value=fruits[3], ref=selected_fruit_ref, size=23),
                    style=ft.ButtonStyle(color=ft.Colors.BLUE),
                    on_click=lambda e: page.open(
                        ft.CupertinoBottomSheet(
                            cupertino_picker,
                            height=216,
                            padding=ft.padding.only(top=6),
                        )
                    ),
                ),
            ],
        ),
    )


ft.app(main)

```

--------------------------------

### Basic CupertinoContextMenuAction Example in Python

Source: <https://flet.dev/docs/controls/cupertinocontextmenuaction>

This Python code demonstrates how to create and use CupertinoContextMenuAction controls within a Flet application. It shows how to define actions with text, icons, and click handlers, and how to style them as default or destructive actions. The example uses the Flet framework to build a simple UI with an image that triggers a context menu when long-pressed.

```python
import flet as ft

def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Image("https://picsum.photos/200/200"),
            actions=[
                ft.CupertinoContextMenuAction(
                    text="Action 1",
                    is_default_action=True,
                    trailing_icon=ft.Icons.CHECK,
                    on_click=lambda e: print("Action 1"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 2",
                    trailing_icon=ft.Icons.MORE,
                    on_click=lambda e: print("Action 2"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 3",
                    is_destructive_action=True,
                    trailing_icon=ft.Icons.CANCEL,
                    on_click=lambda e: print("Action 3"),
                ),
            ],
        )
    )

ft.app(main)
```

--------------------------------

### Publish Flet App as a Static Website

Source: <https://flet.dev/docs/publish/web/static-website>

Publishes a Flet application to a standalone static website. The output is placed in the `./dist` directory. Optional arguments allow for pre-release package installation, specifying asset directories, application metadata, base URL, web renderer, and URL routing strategy.

```bash
flet publish <your-flet-app.py>
```

--------------------------------

### Install APK to Android Device using ADB

Source: <https://flet.dev/docs/publish/android>

This command uses the Android Debug Bridge (ADB) tool to install an APK file onto a connected Android device or emulator. Ensure ADB is in your system's PATH or provide the full path to the executable.

```bash
adb install <path-to-your.apk>

```

--------------------------------

### MenuButton Properties

Source: <https://flet.dev/docs/controls/submenubutton>

Details on the configurable properties of the MenuButton control.

```APIDOC
## MenuButton Properties

### `alignment_offset`

The offset of the menu relative to the alignment origin determined by `MenuStyle.alignment` on the `style` attribute.

### `clip_behavior`

Whether to clip the content of this control or not.
Value is of type `ClipBehavior` and defaults to `ClipBehavior.HARD_EDGE`.

### `content`

The child control to be displayed in the middle portion of this button.
Typically this is the button's label, using a `Text` control.

### `controls`

A list of controls that appear in the menu when it is opened.
Typically either `MenuItemButton` or `SubMenuButton` controls.
If this list is empty, then the button for this menu item will be disabled.

### `leading`

An optional control to display before the `content`.
Typically an `Icon` control.

### `menu_style`

Customizes this menu's appearance.
Value is of type `MenuStyle`.

### `style`

Customizes this button's appearance.
Value is of type `ButtonStyle`.

### `trailing`

An optional control to display after the `content`.
Typically an `Icon` control.
```

--------------------------------

### Assist Chips Example

Source: <https://flet.dev/docs/controls/chip>

Demonstrates the creation and functionality of Assist Chips, which are chips with a leading icon and an on_click event, used for dynamic and contextual automated actions.

```APIDOC
## Assist Chips

### Description
Assist chips are designed to represent smart or automated actions that appear dynamically and contextually within a user interface. They typically feature a leading icon and respond to click events.

### Method
Not applicable (this is a UI control example, not an API endpoint).

### Endpoint
Not applicable.

### Parameters
Not applicable.

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    def save_to_favorites_clicked(e):
        e.control.label.value = "Saved to favorites"
        e.control.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        e.control.disabled = True
        page.update()

    def open_google_maps(e):
        page.launch_url("https://maps.google.com")
        page.update()

    save_to_favourites = ft.Chip(
        label=ft.Text("Save to favourites"),
        leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
        bgcolor=ft.Colors.GREEN_200,
        disabled_color=ft.Colors.GREEN_100,
        autofocus=True,
        on_click=save_to_favorites_clicked,
    )

    open_in_maps = ft.Chip(
        label=ft.Text("9 min walk"),
        leading=ft.Icon(ft.Icons.MAP_SHARP),
        bgcolor=ft.Colors.GREEN_200,
        on_click=open_google_maps,
    )

    page.add(ft.Row([save_to_favourites, open_in_maps]))

ft.app(main)
```

### Response

Not applicable (this is a UI control example).

#### Success Response (200)

Not applicable.

#### Response Example

Not applicable.

```

--------------------------------

### Load Custom Packages in Flet App (Pyodide)

Source: https://flet.dev/docs/publish/web/static-website

Demonstrates how to load custom Python packages from PyPI during app startup within a Pyodide environment (like Flet web apps). It utilizes `micropip` to install packages, such as 'regex', directly within the Flet app. This is essential when running Flet apps in a browser environment.

```python
import sys

if sys.platform == "emscripten": # check if run in Pyodide environment
    import micropip
    await micropip.install("regex")

```

--------------------------------

### Install APK to Specific Android Device using ADB

Source: <https://flet.dev/docs/publish/android>

This command installs an APK file onto a specific Android device when multiple devices are connected to the computer. The `<device>` identifier can be obtained using the `adb devices` command.

```bash
adb -s <device> install <path-to-your.apk>

```

--------------------------------

### Flet Flashlight Control Example

Source: <https://flet.dev/docs/controls/flashlight>

This Python code demonstrates how to use the Flet Flashlight control. It initializes the flashlight, adds it to the page's overlay, and provides a button to toggle the flashlight's state.

```python
import flet as ft

def main(page: ft.Page):
    flashlight = ft.Flashlight()
    page.overlay.append(flashlight)
    page.add(ft.TextButton("toggle", on_click=lambda _: flashlight.toggle()))

ft.app(main)

```

--------------------------------

### Create New Flet App using uv

Source: <https://flet.dev/docs/getting-started/create-flet-app>

This command creates a new Flet application using the 'uv' package manager. 'uv run' executes the 'flet create' command within the context managed by uv, ensuring dependencies are handled correctly.

```bash
uv run flet create
```

--------------------------------

### ListTile Examples in Python

Source: <https://flet.dev/docs/controls/listtile>

This Python code demonstrates various configurations of the ListTile control in Flet. It showcases one-line, dense, selected, and multi-line list tiles with leading and trailing icons or images, as well as popup menus.

```python
import flet as ft

def main(page):
    page.title = "ListTile Examples"
    page.add(
        ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("One-line list tile"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line dense list tile"), dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS),
                            title=ft.Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ft.ListTile(
                            leading=ft.Image(src="/icons/icon-192.png", fit="contain"),
                            title=ft.Text("One-line with leading control"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line with trailing control"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text(
                                "One-line with leading and trailing controls"
                            ),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SNOOZE),
                            title=ft.Text(
                                "Two-line with leading and trailing controls"
                            ),
                            subtitle=ft.Text("Here is a second title."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )
    )


ft.app(main)

```

--------------------------------

### Basic CupertinoSlidingSegmentedButton Example

Source: <https://flet.dev/docs/controls/cupertinoslidingsegmentedbutton>

Demonstrates how to create and use a basic CupertinoSlidingSegmentedButton in Flet. This example shows how to set the selected index, thumb color, and handle change events. It requires the flet library.

```python
import flet as ft  
  
  
def main(page):
    page.title = "CupertinoSlidingSegmentedButton example"
    page.theme_mode = ft.ThemeMode.LIGHT  
  
    def handle_change(e):
        print(f"selected_index: {e.data}")
        page.open(ft.SnackBar(ft.Text(f"segment {int(e.data) + 1} chosen")))
  
    page.add(
        ft.CupertinoSlidingSegmentedButton(
            selected_index=1,
            thumb_color=ft.Colors.BLUE_400,
            on_change=handle_change,
            controls=[
                ft.Text("One"),
                ft.Text("Two"),
                ft.Text("Three"),
            ],
        ),
    )


ft.app(main)
```

--------------------------------

### Flet Multiline TextFields Example

Source: <https://flet.dev/docs/controls/textfield>

Illustrates the use of multiline TextFields in Flet. This includes standard multiline fields, disabled ones with pre-filled content, and fields that automatically adjust height with a maximum line limit.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(label="standard", multiline=True),
        ft.TextField(
            label="disabled",
            multiline=True,
            disabled=True,
            value="line1\nline2\nline3\nline4\nline5",
        ),
        ft.TextField(
            label="Auto adjusted height with max lines",
            multiline=True,
            min_lines=1,
            max_lines=3,
        ),
    )

ft.app(main)

```

--------------------------------

### Initialize fly.io Configuration

Source: <https://flet.dev/docs/tutorials/trello-clone>

Creates a fly.toml configuration file for your project. This command prompts you for details to set up your application's deployment configuration on fly.io.

```bash
fly launch
```

--------------------------------

### CircleAvatar Examples in Python

Source: <https://flet.dev/docs/controls/circleavatar>

Demonstrates various ways to use the CircleAvatar control, including displaying profile images, handling image loading errors, showing initials, using icons, customizing colors, and adding online status indicators. It requires the 'flet' library.

```python
import flet as ft

def main(page):
    # a "normal" avatar with background image
    a1 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with failing foreground image and fallback text
    a2 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with icon, aka icon with inverse background
    a3 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.ABC),
    )
    # avatar with icon and custom colors
    a4 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.WARNING_ROUNDED),
        color=ft.Colors.YELLOW_200,
        bgcolor=ft.Colors.AMBER_700,
    )
    # avatar with online status
    a5 = ft.Stack(
        [
            ft.CircleAvatar(
                foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
            ),
            ft.Container(
                content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                alignment=ft.alignment.bottom_left,
            ),
        ],
        width=40,
        height=40,
    )
    page.add(a1, a2, a3, a4, a5)


ft.app(main)
```

--------------------------------

### Flet ProgressRing Determinate and Indeterminate Example

Source: <https://flet.dev/docs/controls/progressring>

Demonstrates how to use the Flet ProgressRing control to display both determinate and indeterminate progress. The determinate indicator updates its value from 0.0 to 1.0, while the indeterminate indicator shows a continuous animation. This example requires the flet library.

```python
from time import sleep
import flet as ft

def main(page: ft.Page):
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
    prl = ft.Text("Wait for the completion...")
    page.add(
        ft.Text("Circular progress indicator", style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Row([pr, prl]),
        ft.Text(
            "Indeterminate cicrular progress", style=ft.TextThemeStyle.HEADLINE_SMALL
        ),
        ft.Column(
            [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    for i in range(0, 101):
        pr.value = i * 0.01
        sleep(0.1)
        if i == 100:
            prl.value = "Finished!"
        page.update()

ft.app(main)

```

--------------------------------

### Flet VerticalDivider Example

Source: <https://flet.dev/docs/controls/verticaldivider>

Demonstrates how to use the VerticalDivider control in a Flet application to create visual separators within a Row. It showcases different configurations for width and color. This example requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.Container(
                    bgcolor=ft.Colors.ORANGE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    bgcolor=ft.Colors.BROWN_400,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(width=1, color="white"),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(width=9, thickness=3),
                ft.Container(
                    bgcolor=ft.Colors.GREEN_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )

ft.app(main)
```

--------------------------------

### Flet Alignment Usage Examples

Source: <https://flet.dev/docs/reference/types/alignment>

Demonstrates how to apply pre-defined and custom alignments to Flet containers using the Alignment class. This is useful for controlling the positioning of UI elements within their parent containers. The examples show setting alignment to center, top_left, and a custom Alignment object.

```python
container_1.alignment = ft.alignment.center
container_2.alignment = ft.alignment.top_left
container_3.alignment = ft.Alignment(-0.5, -0.5)
```

--------------------------------

### Flet MainAxisAlignment Usage Example in Python

Source: <https://flet.dev/docs/reference/types/mainaxisalignment>

Demonstrates the usage of Flet's MainAxisAlignment enum to control the alignment of items within a Column. The code creates several columns, each with a different MainAxisAlignment, and displays them in a Row. This example requires the 'flet' library.

```python
import flet as ft  
  
def main(page: ft.Page):  
    def items(count):
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER_500,  
                )  
            )  
        return items  
  
    def column_with_alignment(align: ft.MainAxisAlignment):  
        return ft.Column(  
            [  
                ft.Text(str(align), size=10),  
                ft.Container(  
                    content=ft.Column(items(3), alignment=align),  
                    bgcolor=ft.Colors.AMBER_100,  
                    height=400,  
                ),  
            ]  
        )  
  
    page.add(  
        ft.Row(  
            [  
                column_with_alignment(ft.MainAxisAlignment.START),  
                column_with_alignment(ft.MainAxisAlignment.CENTER),  
                column_with_alignment(ft.MainAxisAlignment.END),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),  
            ],  
            spacing=30,  
            alignment=ft.MainAxisAlignment.START,  
        )  
    )  
  
ft.app(main)  
```

--------------------------------

### Flet CupertinoRadio Basic Example

Source: <https://flet.dev/docs/controls/cupertinoradio>

Demonstrates how to use CupertinoRadio within a Flet RadioGroup to allow users to select a single favorite color. It includes standard Material Design Radio and Adaptive Radio for comparison. The example utilizes Flet's event handling for button clicks to display the selected value.

```python
import flet as ft

def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    cg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.CupertinoRadio(
                    value="red",
                    label="Red - Cupertino Radio",
                    active_color=ft.Colors.RED,
                    inactive_color=ft.Colors.RED,
                ),
                ft.Radio(
                    value="green",
                    label="Green - Material Radio",
                    fill_color=ft.Colors.GREEN,
                ),
                ft.Radio(
                    value="blue",
                    label="Blue - Adaptive Radio",
                    adaptive=True,
                    active_color=ft.Colors.BLUE,
                ),
            ]
        )
    )

    page.add(ft.Text("Select your favorite color:"), cg, b, t)

ft.app(main)
```

--------------------------------

### Flet Card with Buttons Example (Python)

Source: <https://flet.dev/docs/controls/card>

This Python code snippet demonstrates how to create a Flet Card control. The card contains a ListTile with an icon, title, and subtitle, followed by a Row of TextButtons. The example utilizes Flet's layout controls and theming.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.title = "Card Example"  
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.add(  
        ft.Card(  
            content=ft.Container(  
                content=ft.Column(  
                    [  
                        ft.ListTile(  
                            leading=ft.Icon(ft.Icons.ALBUM),  
                            title=ft.Text("The Enchanted Nightingale"),  
                            subtitle=ft.Text(  
                                "Music by Julie Gable. Lyrics by Sidney Stein."  
                            ),  
                            bgcolor=ft.Colors.GREY_400,  
                        ),  
                        ft.Row(  
                            [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],  
                            alignment=ft.MainAxisAlignment.END,  
                        ),  
                    ]  
                ),  
                width=400,  
                padding=10,  
            ),  
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,  
        )  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Build Flet App for Linux

Source: <https://flet.dev/docs/publish/linux>

This command initiates the process of packaging a Flet application into a standalone Linux executable. It requires the Flet CLI to be installed and run on a Linux environment. The output is a distributable Linux application.

```bash
flet build linux

```

--------------------------------

### Basic Flet Slider Example

Source: <https://flet.dev/docs/controls/slider>

Demonstrates the creation of basic and disabled Flet Slider controls. It shows how to initialize a slider and set its disabled state.

```python
import flet as ft

def main(page):
    page.add(
        ft.Text("Default slider:"),
        ft.Slider(),
        ft.Text("Default disabled slider:"),
        ft.Slider(disabled=True),
    )

ft.app(main)
```

--------------------------------

### Create New Flet App from Template

Source: <https://flet.dev/docs/reference/cli/create>

This command generates a new Flet application structure using a specified template. It requires an output directory and supports optional arguments for project name, description, and template type. The default template is 'app'.

```bash
flet create [-h] [-v] [--project-name PROJECT_NAME] [--description DESCRIPTION] [--template {app,extension}] output_directory
```

--------------------------------

### Simple BottomSheet Example in Python

Source: <https://flet.dev/docs/controls/bottomsheet>

This example demonstrates how to create and display a simple modal bottom sheet using Flet. It includes a button to open the bottom sheet and a dismiss button within the sheet. The `on_dismiss` event handler is also shown, which adds a text to the page when the sheet is dismissed. This requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "BottomSheet example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def bs_dismissed(e):
        page.add(ft.Text("Bottom sheet dismissed"))

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Here is a bottom sheet!"),
                    ft.ElevatedButton("Dismiss", on_click=lambda _: page.close(bs)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=50,
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)
    page.add(
        ft.ElevatedButton("Display bottom sheet", on_click=lambda e: page.open(bs))
    )


ft.app(target=main)

```

--------------------------------

### Flet Web: Configure URL Strategy

Source: <https://flet.dev/docs/getting-started/navigation-and-routing>

This example shows how to configure the URL strategy for Flet web applications. You can choose between 'path' (default) or 'hash' strategies by passing the `route_url_strategy` parameter to the `flet.app()` function.

```python
ft.app(main, route_url_strategy="hash")
```

--------------------------------

### MenuButton Events

Source: <https://flet.dev/docs/controls/submenubutton>

Details on the event handlers available for the MenuButton control.

```APIDOC
## MenuButton Events

### `on_blur`

Fired when this button loses focus.

### `on_close`

Fired when the menu is closed.

### `on_focus`

Fired when the button receives focus.

### `on_hover`

Fired when the button is hovered.

### `on_open`

Fired when the menu is opened.
```

--------------------------------

### Flet Canvas Bezier Curve Example

Source: <https://flet.dev/docs/controls/canvas>

Demonstrates drawing complex shapes using Bezier curves with the cv.Path control in Flet Canvas. This example creates two distinct shapes with different colors and opacities.

```python
import math

import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    cp = cv.Canvas(
        [
            cv.Path(
                [
                    cv.Path.MoveTo(25, 125),
                    cv.Path.QuadraticTo(50, 25, 135, 35, 0.35),
                    cv.Path.QuadraticTo(75, 115, 135, 215, 0.6),
                    cv.Path.QuadraticTo(50, 225, 25, 125, 0.35),
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.FILL,
                    color=ft.Colors.PINK_400,
                ),
            ),
            cv.Path(
                [
                    cv.Path.MoveTo(85, 125),
                    cv.Path.QuadraticTo(120, 85, 165, 75, 0.5),
                    cv.Path.QuadraticTo(120, 115, 165, 175, 0.3),
                    cv.Path.QuadraticTo(120, 165, 85, 125, 0.5),
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.FILL,
                    color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_400),
                ),
            ),
        ],
        width=float("inf"),
        expand=True,
    )

    page.add(cp)


ft.app(main)
```

--------------------------------

### Badge Example for NavigationBar in Python

Source: <https://flet.dev/docs/reference/types/badge>

Demonstrates how to use the Flet Badge control to display notifications or counts on icons within a NavigationBar. It shows different configurations for badges with and without text.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Badge example"

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon_content=ft.Icon(
                    ft.Icons.EXPLORE,
                    badge=ft.Badge(small_size=10),
                ),
                label="Explore",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE,
                label="Commute",
            ),
            ft.NavigationBarDestination(
                icon_content=ft.Icon(
                    ft.Icons.PHONE,
                    badge="10",
                )
            ),
        ]
    )
    page.add(ft.Text("Body!"))


ft.app(main)
```

--------------------------------

### NavigationRail Widget Documentation

Source: <https://flet.dev/docs/controls/navigationrail>

Documentation for the NavigationRail widget, including its properties, examples, and configuration.

```APIDOC
## NavigationRail Widget

A material widget that is meant to be displayed at the left or right of an app to navigate between a small number of views, typically between three and five.

### Properties

- **`bgcolor`** (Color) - Sets the color of the Container that holds all of the NavigationRail's contents.
- **`destinations`** (list[NavigationRailDestination]) - Defines the appearance of the button items. Must be a list of two or more `NavigationRailDestination` instances.
- **`elevation`** (float) - Controls the size of the shadow below the NavigationRail. Defaults to `0.0`.
- **`extended`** (bool) - Indicates that the NavigationRail should be in the extended state. The extended state has a wider rail container, and the labels are positioned next to the icons. `min_extended_width` can be used to set the minimum width of the rail when it is in this state. The rail will implicitly animate between the extended and normal state. If the rail is going to be in the extended state, then the `label_type` must be set to `none`. Defaults to `False`.
- **`group_alignment`** (float) - The vertical alignment for the group of destinations within the rail. The value must be between `-1.0` and `1.0`. Defaults to `-1.0`.
- **`indicator_color`** (Color) - The color of the navigation rail's indicator.
- **`indicator_shape`** (OutlinedBorder) - The shape of the navigation rail's indicator. Defaults to `StadiumBorder()`.
- **`label_type`** (NavigationRailLabelType) - Defines the layout and behavior of the labels for the default, unextended navigation rail. When a navigation rail is extended, the labels are always shown. Defaults to `None` - no labels are shown.
- **`leading`** (Control) - An optional leading control in the rail that is placed above the destinations. Its location is not affected by `group_alignment`.
- **`min_extended_width`** (float) - The final width when the animation is complete for setting `extended` to `True`. Defaults to `256`.
- **`min_width`** (float) - The smallest possible width for the rail regardless of the destination's icon or label size. Defaults to `72`. This value also defines the min width and min height of the destinations.
- **`selected_index`** (int) - The index into `destinations` for the current selected `NavigationRailDestination` or `None` if no destination is selected.
- **`selected_label_text_style`** (TextStyle) - The `TextStyle` of a destination's label when it is selected. When a destination is not selected, `unselected_label_text_style` will instead be used.

### Example Usage

```python
import flet as ft

def main(page: ft.Page):
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(
            icon=ft.Icons.CREATE, text="Add", on_click=lambda e: print("FAB clicked!")
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="First",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Settings_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.app(target=main)
```

```

--------------------------------

### Configure macOS Entitlements in pyproject.toml

Source: https://flet.dev/docs/publish/macos

Defines macOS entitlements for the Flet application within the `pyproject.toml` file. This example shows how to enable the 'photos-library' entitlement.

```toml
[tool.flet.macos]
entitlement."com.apple.security.personal-information.photos-library" = true
```

--------------------------------

### Serve Flet App with Daphne (Shell)

Source: <https://flet.dev/docs/publish/web/dynamic-website>

Command to run a Flet web app using Daphne, an ASGI protocol server. This command is suitable for serving Flet applications that have been exported as ASGI apps, typically from a file named `main.py`.

```shell
daphne -b 0.0.0.0 -p 8000 main:app
```

--------------------------------

### Basic CupertinoActionSheetAction Example in Python

Source: <https://flet.dev/docs/controls/cupertinoactionsheetaction>

This example demonstrates the basic usage of CupertinoActionSheetAction within a CupertinoActionSheet. It shows how to define title, message, cancel action, and various other actions (default, normal, destructive). The actions are triggered by an on_click event handler. Dependencies: flet library.

```python
import flet as ft

def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.content.value}"))
        page.close(bottom_sheet)

    action_sheet = ft.CupertinoActionSheet(
        title=ft.Row(
            [ft.Text("Title"), ft.Icon(ft.Icons.BEDTIME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        message=ft.Row(
            [ft.Text("Description"), ft.Icon(ft.Icons.AUTO_AWESOME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        cancel=ft.CupertinoActionSheetAction(
            content=ft.Text("Cancel"),
            on_click=handle_click,
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("Default Action"),
                is_default_action=True,
                on_click=handle_click,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Normal Action"),
                on_click=handle_click,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Destructive Action"),
                is_destructive_action=True,
                on_click=handle_click,
            ),
        ],
    )

    bottom_sheet = ft.CupertinoBottomSheet(action_sheet)

    page.add(
        ft.CupertinoFilledButton(
            "Open CupertinoBottomSheet",
            on_click=lambda e: page.open(bottom_sheet),
        )
    )

ft.app(main)
```

--------------------------------

### Set Minimum SDK Version in pyproject.toml

Source: <https://flet.dev/docs/publish/android>

This configuration in `pyproject.toml` sets the minimum Android API level (version) required for your Flet app to install and run. Apps will not be installable on devices with a lower Android version. The default is 21.

```toml
[tool.flet.android]
min_sdk_version = 21

```

--------------------------------

### Flet AutofillGroup Basic Example in Python

Source: <https://flet.dev/docs/controls/autofillgroup>

Demonstrates how to group several TextField controls within an AutofillGroup to leverage autofill suggestions. This example utilizes different AutofillHint values for Name, Email, Phone Number, Street Address, and Postal Code.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.AutofillGroup(
            ft.Column(
                controls=[
                    ft.TextField(
                        label="Name",
                        autofill_hints=ft.AutofillHint.NAME,
                    ),
                    ft.TextField(
                        label="Email",
                        autofill_hints=[ft.AutofillHint.EMAIL],
                    ),
                    ft.TextField(
                        label="Phone Number",
                        autofill_hints=[ft.AutofillHint.TELEPHONE_NUMBER],
                    ),
                    ft.TextField(
                        label="Street Address",
                        autofill_hints=ft.AutofillHint.FULL_STREET_ADDRESS,
                    ),
                    ft.TextField(
                        label="Postal Code",
                        autofill_hints=ft.AutofillHint.POSTAL_CODE,
                    ),
                ]
            )
        )
    )

# run with 'flet run -w'
ft.app(main)
```

--------------------------------

### Build a Simple To-Do App with Flet

Source: <https://flet.dev/docs/getting-started/flet-controls>

This example provides a functional To-Do list application using Flet. It includes a `TextField` for new tasks and an `ElevatedButton` to add them. The `add_clicked` function handles adding new checkboxes with task names to the page and clearing the input field. Requires `flet`.

```python
import flet as ft

def main(page):
    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        new_task.update()

    new_task = ft.TextField(hint_text="What's needs to be done?", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))

ft.app(main)
```

--------------------------------

### Flet CupertinoAlertDialog Example

Source: <https://flet.dev/docs/controls/cupertinodialogaction>

This example demonstrates how to create and display a CupertinoAlertDialog with two actions (Yes and No) using Flet. The dialog includes a title, content, and dismiss handler, with actions that print messages and close the dialog when clicked. It utilizes CupertinoDialogAction for the action buttons.

```python
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def dialog_dismissed(e):
        page.add(ft.Text("Dialog dismissed"))

    def handle_action_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.text}"))
        page.close(cupertino_alert_dialog)

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
        on_dismiss=dialog_dismissed,
        actions=[
            ft.CupertinoDialogAction(
                text="Yes",
                is_destructive_action=True,
                on_click=handle_action_click,
            ),
            ft.CupertinoDialogAction(
                text="No", is_default_action=True, on_click=handle_action_click
            ),
        ],
    )

    page.add(
        ft.CupertinoFilledButton(
            text="Open CupertinoAlertDialog",
            on_click=lambda e: page.open(cupertino_alert_dialog),
        )
    )


ft.app(main)
```

--------------------------------

### Create Flet LineChart with Multiple Data Series

Source: <https://flet.dev/docs/controls/linechart>

This snippet demonstrates the creation of a Flet LineChart control. It includes defining multiple data series with varying styles, such as line color, stroke width, curvature, and below-line background color. The example also configures the chart's border and the left y-axis with custom labels.

```python
import flet as ft

class State:
    toggle = True

s = State()

def main(page: ft.Page):
    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 1.5),
                ft.LineChartDataPoint(5, 1.4),
                ft.LineChartDataPoint(7, 3.4),
                ft.LineChartDataPoint(10, 2),
                ft.LineChartDataPoint(12, 2.2),
                ft.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=8,
            color=ft.Colors.LIGHT_GREEN,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 2.8),
                ft.LineChartDataPoint(7, 1.2),
                ft.LineChartDataPoint(10, 2.8),
                ft.LineChartDataPoint(12, 2.6),
                ft.LineChartDataPoint(13, 3.9),
            ],
            color=ft.Colors.PINK,
            below_line_bgcolor=ft.Colors.with_opacity(0, ft.Colors.PINK),
            stroke_width=8,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 2.8),
                ft.LineChartDataPoint(3, 1.9),
                ft.LineChartDataPoint(6, 3),
                ft.LineChartDataPoint(10, 1.3),
                ft.LineChartDataPoint(13, 2.5),
            ],
            color=ft.Colors.CYAN,
            stroke_width=8,
            curved=True,
            stroke_cap_round=True,
        ),
    ]

    data_2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 4),
                ft.LineChartDataPoint(5, 1.8),
                ft.LineChartDataPoint(7, 5),
                ft.LineChartDataPoint(10, 2),
                ft.LineChartDataPoint(12, 2.2),
                ft.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=4,
            color=ft.Colors.with_opacity(0.5, ft.Colors.LIGHT_GREEN),
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 2.8),
                ft.LineChartDataPoint(7, 1.2),
                ft.LineChartDataPoint(10, 2.8),
                ft.LineChartDataPoint(12, 2.6),
                ft.LineChartDataPoint(13, 3.9),
            ],
            color=ft.Colors.with_opacity(0.5, ft.Colors.PINK),
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.PINK),
            stroke_width=4,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 3.8),
                ft.LineChartDataPoint(3, 1.9),
                ft.LineChartDataPoint(6, 5),
                ft.LineChartDataPoint(10, 3.3),
                ft.LineChartDataPoint(13, 4.5),
            ],
            color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN),
            stroke_width=4,
            stroke_cap_round=True,
        ),
    ]

    chart = ft.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text("1m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text("2m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=3,
                    label=ft.Text("3m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=4,
                    label=ft.Text("4m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Text("5m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=6,
                    label=ft.Text("6m", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(

```

--------------------------------

### Advanced ResponsiveRow Example with Multiple Breakpoints and Controls in Flet

Source: <https://flet.dev/docs/controls/responsiverow>

This example showcases a complex ResponsiveRow layout with multiple containers and text fields. It demonstrates how to set different column spans for various breakpoints (xs, md, lg) and also includes a responsive text field layout that adjusts to medium screen sizes ('md'). The page also includes a resize listener to update a text display with the current page width.

```python
import flet as ft


def main(page: ft.Page):
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize

    pw = ft.Text(bottom=50, right=50, style=ft.TextTheme.display_small)
    page.overlay.append(pw)
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
            run_spacing={"xs": 10},
        ),
    )
    page_resize(None)


ft.app(main)
```

--------------------------------

### Serve Flet App with Hypercorn (Shell)

Source: <https://flet.dev/docs/publish/web/dynamic-website>

Command to run a Flet web app using Hypercorn, an ASGI web server. This command assumes the Flet app has been exported as an ASGI app and is contained in a file named `main.py`.

```shell
hypercorn main:app --bind 0.0.0.0:8000
```

--------------------------------

### Flet Filter Chip Example

Source: <https://flet.dev/docs/controls/chip>

Illustrates the implementation of filter chips in Flet. Filter chips are designed to filter content based on tags or descriptive words in their labels and utilize the on-select event. This example shows how to dynamically create filter chips for amenities and update the page upon selection.

```python
import flet as ft

def main(page: ft.Page):
    def amenity_selected(e):
        page.update()

    title = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Amenities")])
    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]
    amenity_chips = []

    for amenity in amenities:
        amenity_chips.append(
            ft.Chip(
                label=ft.Text(amenity),
                bgcolor=ft.Colors.GREEN_200,
                disabled_color=ft.Colors.GREEN_100,
                autofocus=True,
                on_select=amenity_selected,
            )
        )

    page.add(title, ft.Row(amenity_chips))

ft.app(main)

```

--------------------------------

### Install flet-lottie for Lottie Control

Source: <https://flet.dev/docs/controls/lottie>

To use the Lottie control in your Flet application, you need to add the `flet-lottie` package to your project's dependencies. This is typically done in the `pyproject.toml` file under the `[project]` section. Ensure you specify the correct version of Flet and flet-lottie.

```toml
[project]
...
dependencies = [
  "flet==0.27.6",
  "flet-lottie==0.1.0",
]


```

--------------------------------

### ShaderMask Control Documentation

Source: <https://flet.dev/docs/controls/shadermask>

Detailed documentation for the ShaderMask control, including its properties and usage examples.

```APIDOC
## ShaderMask Control

A control that applies a mask generated by a shader to its child.

### Description

This control applies a visual mask, typically created by a shader (like a gradient), to its child control. It's useful for effects such as fading edges or applying custom visual overlays.

### Properties

#### `blend_mode`
- **Type**: `BlendMode`
- **Default**: `BlendMode.MODULATE`
- **Description**: Specifies the blending mode used when applying the shader to the `content`. This determines how the shader's color and alpha values interact with the child's original appearance.

#### `border_radius`
- **Type**: `BorderRadius`
- **Description**: Defines the radius for the corners of the mask. This can be used to apply rounded corners to the masked area.

#### `content`
- **Type**: `Control`
- **Description**: The child control that will be masked by the shader. This is the element whose appearance will be modified by the `shader` property.

#### `shader`
- **Type**: `Gradient`
- **Description**: A gradient object that defines the mask to be applied. This shader determines the transparency and color overlay on the `content`.
```

--------------------------------

### Initialize Solitaire Class for Drag Start in Flet

Source: <https://flet.dev/docs/tutorials/python-solitaire>

This Python code defines a `Solitaire` class to store the starting `top` and `left` coordinates of a draggable control. The `start_drag` function is an event handler for `on_pan_start` that captures these initial positions before the drag occurs. An instance of `Solitaire` is created to manage these positions.

```python
class Solitaire:
   def __init__(self):
       self.start_top = 0
       self.start_left = 0

solitaire = Solitaire()

def start_drag(e: ft.DragStartEvent):
    solitaire.start_top = e.control.top
    solitaire.start_left = e.control.left
    e.control.update()

```

--------------------------------

### RadioGroup Basic Example

Source: <https://flet.dev/docs/controls/radio>

Demonstrates a basic RadioGroup with multiple radio options and a submit button to display the selected value.

```APIDOC
## RadioGroup Basic Example

### Description
This example shows a simple `RadioGroup` where users can select one color from a list of options (Red, Green, Blue). A submit button displays the chosen color in a Text control.

### Method
N/A (Client-side Flet app)

### Endpoint
N/A (Client-side Flet app)

### Parameters
N/A

### Request Example
```python
import flet as ft

def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    cg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="red", label="Red"),
                ft.Radio(value="green", label="Green"),
                ft.Radio(value="blue", label="Blue"),
            ]
        )
    )

    page.add(ft.Text("Select your favorite color:"), cg, b, t)

ft.app(main)
```

### Response

N/A

```

--------------------------------

### Hosting Multiple Flet Apps

Source: https://flet.dev/docs/publish/web/dynamic-website

Demonstrates how to mount multiple Flet applications under different paths on the same domain using FastAPI.

```APIDOC
## Hosting Multiple Flet Apps

### Description
This example shows how to host several Flet applications under the same domain by mounting them to different URL paths within a single FastAPI application.

### Method
`app.mount(path, app)`

### Endpoint
`/` and `/sub-app/` (example paths)

### Request Body
N/A

### Request Example
```python
import flet as ft
import flet.fastapi as flet_fastapi

async def root_main(page: ft.Page):
    await page.add_async(ft.Text("This is root app!"))

async def sub_main(page: ft.Page):
    await page.add_async(ft.Text("This is sub app!"))

app = flet_fastapi.FastAPI()

# Mount sub-application first
app.mount("/sub-app", flet_fastapi.app(sub_main))
# Mount root application last, as it acts as a catch-all
app.mount("/", flet_fastapi.app(root_main))
```

### Warning

Ensure that sub-applications are mounted *before* the root Flet app. The root app is typically configured with a catch-all handler for `index.html` and SPA routing, so mounting it last prevents it from intercepting requests intended for sub-applications. Also, note the trailing slash in the sub-app mount path (`/sub-app/`). Omitting it may lead to requests being routed to the root app.

```

--------------------------------

### Basic CupertinoFilledButton Example - Python

Source: https://flet.dev/docs/controls/cupertinofilledbutton

Demonstrates the basic usage of CupertinoFilledButton in Flet. This button displays text and has a click handler that prints a message. It requires the 'flet' library.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.add(  
        ft.CupertinoFilledButton(  
            content=ft.Text("CupertinoFilled"),  
            opacity_on_click=0.3,  
            on_click=lambda e: print("CupertinoFilledButton clicked!"),  
        ),  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Python ShakeDetector Example

Source: <https://flet.dev/docs/controls/shakedetector>

This Python code demonstrates how to use the ShakeDetector control. It initializes the detector with custom shake parameters and appends it to the page's overlay. An event handler prints a message when a shake is detected. Dependencies include the 'flet' library.

```python
import flet as ft  

def main(page: ft.Page):  
    shd = ft.ShakeDetector(  
        minimum_shake_count=2,  
        shake_slop_time_ms=300,  
        shake_count_reset_time_ms=1000,  
        on_shake=lambda _: print("SHAKE DETECTED!"),  
    )  
    page.overlay.append(shd)  

    page.add(ft.Text("Program body"))  


ft.app(main)  

```

--------------------------------

### Running flet build Command

Source: <https://flet.dev/docs/publish>

Demonstrates the basic usage of the 'flet build' command, specifying the target platform. The command can be run from the Flet app directory or with an explicit path to the Python app.

```bash
# Build for a specific target platform from the app directory
flet build <target_platform>

# Build for a specific target platform with a path to the Python app
flet build <target_platform> <path_to_python_app>
```

--------------------------------

### Create Simple Tabs with Flet

Source: <https://flet.dev/docs/controls/tabs>

Demonstrates how to create a basic set of tabs in Flet. This example initializes a Tabs control with three tabs, each containing simple text content. It utilizes Flet's Tab and Container controls for layout and presentation. The selected index and animation duration are configured.

```python
import flet as ft

def main(page: ft.Page):
  
    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Tab 2",
                icon=ft.Icons.SETTINGS,
                content=ft.Container(
                    content=ft.Text("This is Tab 2"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                tab_content=ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/7119543?s=88&v=4"
                ),
                content=ft.Container(
                    content=ft.Text("This is Tab 3"), alignment=ft.alignment.center
                ),
            ),
        ],
        expand=1,
    )

    page.add(t)


ft.app(main)
```

--------------------------------

### Create a Basic Elevated Button in Flet

Source: <https://flet.dev/docs/getting-started/flet-controls>

This example shows the creation of a simple `ElevatedButton` with text. Buttons are fundamental interactive controls in Flet that can trigger actions when clicked. Requires the `flet` library.

```python
import flet as ft

btn = ft.ElevatedButton("Click me!")
page.add(btn)
```

--------------------------------

### Basic DropdownM2 Example - Flet Python

Source: <https://flet.dev/docs/controls/dropdownm2>

Demonstrates the fundamental usage of the DropdownM2 control, allowing users to select an option and display the chosen value upon button click. It requires the flet library. Inputs are the dropdown options, and output is the selected value displayed as text.

```python
import flet as ft


def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Dropdown value is:  {dd.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    dd = ft.DropdownM2(
        width=100,
        options=[
            ft.dropdownm2.Option("Red"),
            ft.dropdownm2.Option("Green"),
            ft.dropdownm2.Option("Blue"),
        ],
    )
    page.add(dd, b, t)


ft.app(main)

```

--------------------------------

### Flet SafeArea Example: Basic Counter

Source: <https://flet.dev/docs/controls/safearea>

This Python snippet demonstrates the usage of the `SafeArea` control in Flet. It embeds a `Text` control displaying a counter within a `Container`, which is then placed inside a `SafeArea`. The `SafeArea` ensures that the counter is not obscured by system UI elements. The example includes a floating action button to increment the counter.

```python
import flet as ft


class State:
    counter = 0


def main(page: ft.Page):
    state = State()

    def add_click(e):
        state.counter += 1
        counter.value = str(state.counter)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=add_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter := ft.Text("0", size=50),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)

```

--------------------------------

### Running Packaged Flet Apps on Different OS

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Demonstrates how to run the packaged Flet application executable on macOS, Windows, and Linux after it has been created using `flet pack`.

```shell
open dist/your_program.app # On macOS
```

```shell
dist\your_program.exe # On Windows
```

```shell
dist/your_program # On Linux
```

--------------------------------

### Basic CupertinoSegmentedButton Example in Python

Source: <https://flet.dev/docs/controls/cupertinosegmentedbutton>

Demonstrates how to create and use a basic CupertinoSegmentedButton in Flet. This example shows setting the initial selected index, selected color, and handling the on_change event to print the selected index. It utilizes Flet's control system for building the UI.

```python
import flet as ft


def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.CupertinoSegmentedButton(
            selected_index=1,
            selected_color=ft.Colors.RED_400,
            on_change=lambda e: print(f"selected_index: {e.data}"),
            controls=[
                ft.Text("One"),
                ft.Container(
                    padding=ft.padding.symmetric(10, 30),
                    content=ft.Text("Two"),
                ),
                ft.Container(
                    padding=ft.padding.symmetric(5, 10),
                    content=ft.Text("Three"),
                ),
            ],
            padding=ft.padding.symmetric(20, 50),
        ),
    )


ft.app(main)

```

### Make Flet App Window Transparent

Source: <https://flet.dev/docs/reference/types/window>

This snippet demonstrates how to make the Flet application window and its background transparent. It achieves this by setting `page.window.bgcolor` and `page.bgcolor` to transparent, and also hides the window's title bar and frame. This is useful for creating custom, floating UI elements.

```python
import flet as ft

def main(page: ft.Page):
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.left = 400
    page.window.top = 200
    page.add(ft.ElevatedButton("I'm a floating button!"))

ft.app(main)
```

--------------------------------

### Move Window with WindowDragArea in Python

Source: <https://flet.dev/docs/controls/windowdragarea>

This Python example demonstrates how to use the WindowDragArea control to make an application window draggable, maximizable, and restorable. It requires the Flet library. The code hides the default title bar and adds a WindowDragArea that occupies the available space, allowing users to interact with the window by dragging this area. An IconButton is included to close the window.

```python
import flet as ft

def main(page: ft.Page):
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True

    page.add(
        ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(
                        ft.Text(
                            "Drag this area to move, maximize and restore application window."
                        ),
                        bgcolor=ft.Colors.AMBER_300,
                        padding=10,
                    ),
                    expand=True,
                ),
                ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: page.window.close()),
            ]
        )
    )

ft.app(main)
```

--------------------------------

### Start Flet App with Hidden Window and Make Visible

Source: <https://flet.dev/docs/reference/types/window>

This code example shows how to launch a Flet application with its window initially hidden and then make it visible after a delay. It utilizes `ft.AppView.FLET_APP_HIDDEN` to hide the window on startup and then sets `page.window.visible` to `True` after a 3-second pause, followed by a page update.

```python
from time import sleep

import flet as ft


def main(page: ft.Page):

    page.add(ft.Text("Hello!"))
    sleep(3)
    page.window.visible = True
    page.update()


ft.app(main, view=ft.AppView.FLET_APP_HIDDEN)
```

--------------------------------

### Force Close App Window with Confirmation Dialog (Python)

Source: <https://flet.dev/docs/reference/types/window>

Demonstrates how to use the `page.window.destroy()` method to force the closing of an app window. It integrates with `page.window.prevent_close = True` to implement a confirmation dialog before exiting. This is useful for preventing accidental closure of applications.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "MyApp"

    def window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)
            page.update()

    page.window.prevent_close = True
    page.window.on_event = window_event

    def yes_click(e):
        page.window.destroy()

    def no_click(e):
        page.close(confirm_dialog)
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(ft.Text('Try exiting this app by clicking window\'s "Close" button!'))

ft.app(main)
```

--------------------------------

### Style Result Text (Flet)

Source: <https://flet.dev/docs/tutorials/python-calculator>

Shows how to style a `Text` control in Flet by setting its `color` and `size` properties.  This example sets the result text to white with a size of 20.

```python
result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
```

--------------------------------

### Handle Page Resize Event in Flet

Source: <https://flet.dev/docs/controls/page>

This event handler is triggered when the browser or native OS window containing a Flet app is resized. The event handler receives a WindowResizeEvent object containing information about the new window dimensions. It can be used to dynamically adjust UI elements based on the available space.

```python
def page_resized(e):
    print("New page size:", page.window.width, page.window_height)

page.on_resized = page_resized
```

--------------------------------

### ResponsiveColumn Spanning with Breakpoints in Flet

Source: <https://flet.dev/docs/controls/responsiverow>

Illustrates how to define column spans for different screen breakpoints using a dictionary. This example shows columns that take up 6 units on small screens ('sm') and are configured to adapt to varying screen sizes.

```python
import flet as ft

ft.ResponsiveRow([
    ft.Column(col={"sm": 6}, controls=[ft.Text("Column 1")]),
    ft.Column(col={"sm": 6}, controls=[ft.Text("Column 2")])
])
```

--------------------------------

### Enabling Developer Mode in Windows Settings

Source: <https://flet.dev/docs/publish/windows>

When building Flet apps for Windows, you might encounter an error related to symlink support, requiring Developer Mode to be enabled. This command opens the relevant Windows settings page.

```powershell
start ms-settings:developers
```

--------------------------------

### Build Windows Application with Flet CLI

Source: <https://flet.dev/docs/publish/windows>

The `flet build windows` command is used to create a Windows executable from your Flet application. This process requires specific prerequisites to be met on the Windows environment.

```bash
flet build windows
```

--------------------------------

### Configure Android Split APKs in pyproject.toml

Source: <https://flet.dev/docs/publish/android>

This configuration in `pyproject.toml` tells Flet CLI to split the fat APK into smaller APKs for each platform architecture. This is useful for reducing APK size and is an alternative to using the `--split-per-abi` command-line option.

```toml
[tool.flet.android]
split_per_abi = true

```

--------------------------------

### Packaging Assets with `flet pack` (Windows)

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Includes additional data files or folders, such as assets, into the Flet application package. This command is specifically for Windows, using a semicolon as a separator for the source and destination paths.

```shell
flet pack your_program.py --add-data "assets;assets"
```

--------------------------------

### Build Flet Web App with Color Emojis

Source: <https://flet.dev/docs/publish/web/static-website>

Builds a Flet web application that includes support for color emojis. This increases the application size due to the inclusion of a larger emoji font file.

```bash
flet build web --use-color-emoji
```

--------------------------------

### Set Page Title

Source: <https://flet.dev/docs/controls/page>

Sets the title of the browser or native OS window for the Flet application. The `page.update()` method must be called to apply the change.

```python
page.title = "My awesome app"
page.update()
```

--------------------------------

### Define FletSpinkit Color and Size Properties in Python

Source: <https://flet.dev/docs/extend/user-extensions>

Defines 'color' and 'size' properties for the FletSpinkit control in Python. It utilizes ConstrainedControl and includes setter/getter methods for these properties, specifying their types and how they are set using Flet's attribute system.

```python
from enum import Enum  
from typing import Any, Optional  

from flet.core.constrained_control import ConstrainedControl  
from flet.core.control import OptionalNumber  
from flet.core.types import ColorEnums, ColorValue  


class FletSpinkit(ConstrainedControl):  
    """
    FletSpinkit Control.  
    """

    def __init__(  
        self,  
        #  
        # Control  
        #  
        opacity: OptionalNumber = None,  
        tooltip: Optional[str] = None,  
        visible: Optional[bool] = None,  
        data: Any = None,  
        #  
        # ConstrainedControl  
        #  
        left: OptionalNumber = None,  
        top: OptionalNumber = None,  
        right: OptionalNumber = None,  
        bottom: OptionalNumber = None,  
        #  
        # FletSpinkit specific  
        #  
        color: Optional[ColorValue] = None,  
        size: OptionalNumber = None,  
    ):
        ConstrainedControl.__init__(  
            self,  
            tooltip=tooltip,  
            opacity=opacity,  
            visible=visible,  
            data=data,  
            left=left,  
            top=top,  
            right=right,  
            bottom=bottom,  
        )  

        self.color = color  
        self.size = size  

    def _get_control_name(self):  
        return "flet_spinkit"  

    # color  
    @property  
    def color(self) -> Optional[ColorValue]:  
        return self.__color  

    @color.setter  
    def color(self, value: Optional[ColorValue]):  
        self.__color = value  
        self._set_enum_attr("color", value, ColorEnums)  

    # size  
    @property  
    def size(self):  
        return self._get_attr("size")  

    @size.setter  
    def size(self, value):  
        self._set_attr("size", value)  
```

--------------------------------

### Publish Flet App with HTML Web Renderer

Source: <https://flet.dev/docs/publish/web/static-website>

Publishes a Flet application using the 'html' web renderer instead of the default 'canvaskit'. This can reduce the application size and may be preferable in certain environments. The `--web-renderer html` option selects this renderer.

```bash
flet publish <your-flet-app.py> --web-renderer html
```

--------------------------------

### Advanced ResponsiveRow Example with Multiple Breakpoints and Controls in Flet

Source: <https://flet.dev/docs/controls/responsiverow>

This example showcases a complex ResponsiveRow layout with multiple containers and text fields. It demonstrates how to set different column spans for various breakpoints (xs, md, lg) and also includes a responsive text field layout that adjusts to medium screen sizes ('md'). The page also includes a resize listener to update a text display with the current page width.

```python
import flet as ft


def main(page: ft.Page):
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize

    pw = ft.Text(bottom=50, right=50, style=ft.TextTheme.display_small)
    page.overlay.append(pw)
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
            run_spacing={"xs": 10},
        ),
    )
    page_resize(None)


ft.app(main)
```

--------------------------------

### Display Flet Icons with Different Colors and Sizes (Python)

Source: <https://flet.dev/docs/controls/icon>

This Python code snippet demonstrates how to create and display Flet Icon controls with customizable colors and sizes. It utilizes the flet library and shows how to set icon names, colors using predefined constants or hex codes, and specific sizes. No external dependencies beyond the flet library are required.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.Icon(name=ft.Icons.FAVORITE, color=ft.Colors.PINK),
                ft.Icon(name=ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN_400, size=30),
                ft.Icon(name=ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE, size=50),
                ft.Icon(name="settings", color="#c1c1c1"),
            ]
        )
    )

ft.app(main)
```

--------------------------------

### Access FletSpinkit Color and Size Properties in Dart

Source: <https://flet.dev/docs/extend/user-extensions>

Demonstrates how to access 'color' and 'size' properties from a Flet control in Dart. It uses helper methods like `attrColor` and `attrDouble` to retrieve these values and applies them to a Flutter SpinKit widget.

```dart
import 'package:flet/flet.dart';  
import 'package:flutter/material.dart';  
import 'package:flutter_spinkit/flutter_spinkit.dart';  

class FletSpinkitControl extends StatelessWidget {  
  final Control? parent;  
  final Control control;  

  const FletSpinkitControl({  
    super.key,  
    required this.parent,  
    required this.control,  
  });  

  @override  
  Widget build(BuildContext context) {  
    var color = control.attrColor("color", context);  
    var size = control.attrDouble("size");  
    Widget myControl = SpinKitRotatingCircle(  
      color: color,  
      size: size ?? 100,  
    );  


    return constrainedControl(context, myControl, parent, control);  
  }
}
```

--------------------------------

### Basic Rive Animation Display in Python

Source: <https://flet.dev/docs/controls/rive>

This Python code demonstrates how to display a Rive animation using the Flet framework. It takes a URL for the Rive file and optionally displays a progress bar while loading. The animation can be sized using width and height properties.

```python
import flet as ft  


def main(page):  
    page.add(  
        ft.Rive(  
            "https://cdn.rive.app/animations/vehicles.riv",  
            placeholder=ft.ProgressBar(),  
            width=300,  
            height=200,  
        )  
    )  


ft.app(main)  
```

--------------------------------

### Use FletSpinkit with Custom Color and Size in Python App

Source: <https://flet.dev/docs/extend/user-extensions>

Shows how to integrate the custom FletSpinkit control into a Flet application. It demonstrates setting the 'color' and 'size' properties of the FletSpinkit widget within a Stack layout.

```python
import flet as ft  

from flet_spinkit import FletSpinkit  


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  

    page.add(  
        ft.Stack(  
            [  
                ft.Container(height=200, width=200, bgcolor=ft.Colors.BLUE_100),  
                FletSpinkit(  
                    opacity=0.5,  
                    tooltip="Spinkit tooltip",  
                    top=0,  
                    left=0,  
                    color=ft.Colors.YELLOW,  
                    size=150,  
                ),  
            ]  
        )  
    )  


ft.app(main)
```

--------------------------------

### Create and Activate venv (Windows)

Source: <https://flet.dev/docs/getting-started>

Commands to create a new directory for your Flet app, navigate into it, set up a Python virtual environment using `venv`, and activate it on Windows. This isolates project dependencies.

```cmd
md first-flet-app
cd first-flet-app
python -m venv .venv
.venv\Scripts\activate
```

--------------------------------

### Flet Text Control: Custom Styles

Source: <https://flet.dev/docs/controls/text>

Demonstrates various custom text styles in Flet using the Text control. It showcases different font sizes, colors, background colors, font weights, italic settings, and text selection. It also includes examples of limiting text to a single line with an ellipsis and limiting text to a specific number of lines or dimensions.

```python
import flet as ft  

def main(page: ft.Page):  
    page.title = "Text custom styles"  
    page.scroll = ft.ScrollMode.ADAPTIVE  

    page.add(  
        ft.Text("Size 10", size=10),  
        ft.Text("Size 30, Italic", size=30, color=ft.Colors.PINK_600, italic=True),  
        ft.Text(  
            "Size 40, w100",  
            size=40,  
            color=ft.Colors.WHITE,  
            bgcolor=ft.Colors.BLUE_600,  
            weight=ft.FontWeight.W_100,  
        ),  
        ft.Text(  
            "Size 50, Normal",  
            size=50,  
            color=ft.Colors.WHITE,  
            bgcolor=ft.Colors.ORANGE_800,  
            weight=ft.FontWeight.NORMAL,  
        ),  
        ft.Text(  
            "Size 60, Bold, Italic",  
            size=50,  
            color=ft.Colors.WHITE,  
            bgcolor=ft.Colors.GREEN_700,  
            weight=ft.FontWeight.BOLD,  
            italic=True,  
        ),  
        ft.Text(  
            "Size 70, w900, selectable",  
            size=70,  
            weight=ft.FontWeight.W_900,  
            selectable=True,  
        ),  
        ft.Text(  
            "Limit long text to 1 line with ellipsis",  
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,  
        ),  
        ft.Text(  
            "Proin rutrum, purus sit amet elementum volutpat, nunc lacus vulputate orci, cursus ultrices neque dui quis purus. Ut ultricies purus nec nibh bibendum, eget vestibulum metus various. Duis convallis maximus justo, eu rutrum libero maximus id. Donec ullamcorper arcu in sapien molestie, non pellentesque tellus pellentesque. Nulla nec tristique ex. Maecenas euismod nisl enim, a convallis arcu laoreet at. Ut at tortor finibus, rutrum massa sit amet, pulvinar velit. Phasellus diam lorem, viverra vitae leo vitae, consequat suscipit lorem.",  
            max_lines=1,  
            overflow=ft.TextOverflow.ELLIPSIS,  
        ),  
        ft.Text(  
            "Limit long text to 2 lines and fading",  
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,  
        ),  
        ft.Text(  
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",  
            max_lines=2,  
        ),  
        ft.Text(  
            "Limit the width and height of long text",  
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,  
        ),  
        ft.Text(  
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",  
            width=700,  
            height=100,  
        ),  
    )  


ft.app(main)  
```

--------------------------------

### Create and Activate Virtual Environment (Windows)

Source: <https://flet.dev/docs/getting-started/testing-on-ios>

This snippet shows the commands to create a Python virtual environment using `venv` and activate it on Windows systems. This is essential for isolating project dependencies.

```batch
python.exe -m venv .venv  
.venv\Scripts\activate.bat  
```

--------------------------------

### Customize OAuth Complete Page HTML in Flet

Source: <https://flet.dev/docs/cookbook/authentication>

This snippet shows how to customize the HTML content displayed to the user after a successful OAuth authorization. It involves defining an HTML string with a script to close the window and a message for the user, then passing it to the `page.login()` method. This is applicable to Flet desktop and web apps.

```python
complete_page_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Signed in to MyApp</title>
  </head>
<body>
  <script type="text/javascript">
      window.close();
  </script>
  <p>You've been successfully signed in! You can close this tab or window now.</p>
</body>
</html>
"""

page.login(
    provider,
    complete_page_html=complete_page_html,
)
```

--------------------------------

### Run Flet App Locally (Bash)

Source: <https://flet.dev/docs/index>

Command to run a Flet application in a native OS window. This executes the specified Python script using the Flet runtime.

```bash
flet run counter.py  

```

--------------------------------

### Animate Container Properties with Flet

Source: <https://flet.dev/docs/cookbook/animations>

Enables implicit animation of container properties such as size, background color, and border style by setting Container.animate. This allows for smooth visual transitions when properties change.

```python
import flet as ft

def main(page: ft.Page):

    c = ft.Container(
        width=150,
        height=150,
        bgcolor="red",
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
    )

    def animate_container(e):
        c.width = 100 if c.width == 150 else 150
        c.height = 50 if c.height == 150 else 150
        c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.update()

    page.add(c, ft.ElevatedButton("Animate container", on_click=animate_container))

ft.app(main)

```

--------------------------------

### Customize Tabs Appearance with TabsTheme

Source: <https://flet.dev/docs/reference/types/tabstheme>

Demonstrates how to apply a custom theme to Tabs controls in a Flet application using the TabsTheme class. This includes setting divider color, indicator color and size, label colors, and overlay colors for different states.

```python
page.theme = ft.Theme(  
    tabs_theme=ft.TabsTheme(  
        divider_color=ft.Colors.BLUE,  
        indicator_color=ft.Colors.RED,  
        indicator_tab_size=True,  
        label_color=ft.Colors.GREEN,  
        unselected_label_color=ft.Colors.AMBER,  
        overlay_color={  
            ft.MaterialState.FOCUSED: ft.Colors.with_opacity(0.2, ft.Colors.GREEN),  
            ft.MaterialState.DEFAULT: ft.Colors.with_opacity(0.2, ft.Colors.PINK),  
        },  
    )  
)

```

--------------------------------

### Flet Clickable Container Example

Source: <https://flet.dev/docs/controls/container>

Demonstrates how to create clickable Flet Containers, with and without ink effects. This example showcases different configurations for background color, size, and click event handling. It requires the 'flet' library.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.title = "Containers - clickable and not"  
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
  
    page.add(  
        ft.Row(  
            [  
                ft.Container(  
                    content=ft.Text("Non clickable"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.AMBER,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable without Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.GREEN_200,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    on_click=lambda e: print("Clickable without Ink clicked!"),  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable with Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    bgcolor=ft.Colors.CYAN_200,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    ink=True,  
                    on_click=lambda e: print("Clickable with Ink clicked!"),  
                ),  
                ft.Container(  
                    content=ft.Text("Clickable transparent with Ink"),  
                    margin=10,  
                    padding=10,  
                    alignment=ft.alignment.center,  
                    width=150,  
                    height=150,  
                    border_radius=10,  
                    ink=True,  
                    on_click=lambda e: print("Clickable transparent with Ink clicked!"),  
                ),  
            ],  
            alignment=ft.MainAxisAlignment.CENTER,  
        ),  
    )  
  
  
ft.app(main)  
```

--------------------------------

### Install Pillow for Icon Conversion

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Installs the Pillow library, which is necessary for PyInstaller to convert PNG icons to platform-specific formats (.ico for Windows, .icns for macOS) when packaging Flet applications.

```shell
pip install pillow
```

--------------------------------

### Trigger Flet Log Display with Exit Code

Source: <https://flet.dev/docs/publish>

This code snippet shows how to terminate a Flet application and trigger the display of the console log. By calling `sys.exit(100)`, the Flet framework will automatically display the accumulated log content in a scrollable window. Any other exit code will terminate the app without displaying the log.

```python
import sys

sys.exit(100)

```

--------------------------------

### Run Flet App as Desktop

Source: <https://flet.dev/docs/getting-started/running-app>

Executes a Flet application as a desktop application. It can run the default `main.py` in the current directory or a specified script file path. The app launches in a native OS window.

```bash
flet run
flet run [script]
flet run /Users/JohnSmith/Documents/projects/flet-app
flet run counter.py
```

--------------------------------

### Page Spacing Property

Source: <https://flet.dev/docs/controls/page>

The `spacing` property controls the vertical spacing between controls placed on the Page. It defaults to 10 virtual pixels and is applied when the page alignment is set to 'start', 'end', or 'center'.

```APIDOC
## Page Spacing Property

### Description
Vertical spacing between controls on the Page. Default value is 10 virtual pixels. Spacing is applied only when `alignment` is set to `start`, `end` or `center`.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
page.spacing = 20
page.add(
    ft.Text("First item"),
    ft.Text("Second item")
)
page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Flet Stack Offset Transformation Example

Source: https://flet.dev/docs/controls

Illustrates the use of the `offset` transformation within a Flet `Stack`. The `offset` property applies a translation transformation before painting a control, scaled to the control's size, allowing for precise positioning adjustments within a stack.

```python
import flet as ft  

def main(page: ft.Page):

    page.add(
        ft.Stack(
            [
                ft.Container(
                    bgcolor="red",
                    width=100,
                    height=100,
                    left=100,
                    top=100,
                    offset=ft.transform.Offset(-1, -1),
                )
            ],
            width=1000,
            height=1000,
        )
    )

ft.app(main)

```

--------------------------------

### Customize Page Transitions with PageTransitionsTheme in Flet

Source: <https://flet.dev/docs/reference/types/pagetransitionstheme>

This example demonstrates how to customize page transition animations for different platforms using Flet's PageTransitionsTheme. It shows how to set specific transitions for Android, iOS, macOS, Linux, and Windows within a Flet application's theme.

```python
page.theme = ft.Theme(
    page_transitions=ft.PageTransitionsTheme(
        android=ft.PageTransitionTheme.OPEN_UPWARDS,
        ios=ft.PageTransitionTheme.CUPERTINO,
        macos=ft.PageTransitionTheme.FADE_UPWARDS,
        linux=ft.PageTransitionTheme.ZOOM,
        windows=ft.PageTransitionTheme.NONE
    )
)

```

--------------------------------

### Running Packaged Flet Apps on Different OS

Source: <https://flet.dev/docs/cookbook/packaging-desktop-app>

Demonstrates how to run the packaged Flet application executable on macOS, Windows, and Linux after it has been created using `flet pack`.

```shell
open dist/your_program.app # On macOS
```

```shell
dist\your_program.exe # On Windows
```

```shell
dist/your_program # On Linux
```

--------------------------------

### Generate Base64 from File Content (Windows PowerShell)

Source: <https://flet.dev/docs/controls/image>

This PowerShell command enables users on Windows to convert the content of a file (such as an image) into a Base64 encoded string. The `Get-Content` cmdlet reads the file as bytes, and `ConvertTo-Base64String` performs the encoding. This generated string can then be utilized in applications that require Base64 image data.

```powershell
[convert]::ToBase64String((Get-Content -path "your_file_path" -Encoding byte))
```

--------------------------------

### Basic Flet WebView Implementation

Source: <https://flet.dev/docs/controls/webview>

A straightforward example demonstrating how to initialize and display a WebView in a Flet application. It loads the 'flet.dev' website and includes basic event handlers for page loading and errors. The `expand=True` property ensures the WebView takes up available space.

```python
import flet as ft
import flet_webview as ftwv


def main(page: ft.Page):
    wv = ftwv.WebView(
        url="https://flet.dev",
        on_page_started=lambda _: print("Page started"),
        on_page_ended=lambda _: print("Page ended"),
        on_web_resource_error=lambda e: print("Page error:", e.data),
        expand=True,
    )
    page.add(wv)


ft.app(main)

```

--------------------------------

### Basic InteractiveViewer Example

Source: <https://flet.dev/docs/controls/interactiveviewer>

This example demonstrates how to use the InteractiveViewer control to display an image that can be panned and zoomed. It sets minimum and maximum scale values, boundary margins, and event handlers for interaction.

```python
import flet as ft  

def main(page: ft.Page):  
    page.add(  
        ft.InteractiveViewer(  
            min_scale=0.1,  
            max_scale=15,  
            boundary_margin=ft.margin.all(20),  
            on_interaction_start=lambda e: print(e),  
            on_interaction_end=lambda e: print(e),  
            on_interaction_update=lambda e: print(e),  
            content=ft.Image(  
                src="https://picsum.photos/500/500",  
            ),  
        )  
    )  

ft.app(main)  

```

--------------------------------

### Flet Board Resizing Logic

Source: <https://flet.dev/docs/tutorials/trello-clone>

This Python method, `resize`, is designed to adjust the layout of board lists based on the available screen width and the state of a navigation rail. It calculates the appropriate width for the board lists, considering whether the navigation rail is extended or collapsed, and updates the board's dimensions.

```python
def resize(self, nav_rail_extended, width, height):  
    self.board_lists.width = (width - 310) if nav_rail_extended else (width - 50)  
    self.height = height  
    self.update()  
```

--------------------------------

### Flet Row Expand Example - Integer Factor

Source: <https://flet.dev/docs/controls/row>

Demonstrates using integer expand factors to divide available space among multiple children in a Flet Row. The width of each child is proportional to its `expand` value relative to the sum of all expand factors.

```python
r = ft.Row([
  ft.Container(expand=1, content=ft.Text("A")),
  ft.Container(expand=3, content=ft.Text("B")),
  ft.Container(expand=1, content=ft.Text("C"))
])
```

--------------------------------

### Animate Scale with Flet

Source: <https://flet.dev/docs/cookbook/animations>

Illustrates animating the scale of a Flet container using `animate_scale`. The animation is set with a duration and a `BOUNCE_OUT` curve. Clicking the button scales the container up to twice its original size, animating the transition.

```python
import flet as ft

def main(page: ft.Page):

    c = ft.Container(
        width=100,
        height=100,
        bgcolor="blue",
        border_radius=5,
        scale=ft.transform.Scale(scale=1),
        animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
    )

    def animate(e):
        c.scale = 2
        page.update()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30
    page.add(
        c,
        ft.ElevatedButton("Animate!", on_click=animate),
    )

ft.app(main)
```

--------------------------------

### Displaying Large Lists with ListView (Efficient)

Source: <https://flet.dev/docs/cookbook/large-lists>

Shows how to use the Flet `ListView` control to efficiently display a large list of 5,000 text items. `ListView` renders items on demand, significantly improving scrolling performance compared to `Column` or `Row`. It requires a specified height or width to function correctly, often achieved using `expand=True`.

```python
import flet as ft  

def main(page: ft.Page):  
    lv = ft.ListView(expand=True, spacing=10)  
    for i in range(5000):  
        lv.controls.append(ft.Text(f"Line {i}"))  
    page.add(lv)  

ft.app(main, view=ft.AppView.WEB_BROWSER)  

```

--------------------------------

### Create Pie Chart with Interactive Titles using Flet

Source: <https://flet.dev/docs/controls/piechart>

This Python example showcases how to create a Flet PieChart with interactive titles. Each section has a title that changes in style and size when hovered over. It also adjusts the radius of the hovered section for a more pronounced visual effect. The chart features a center space, making it suitable for donut chart representations.

```python
import flet as ft

def main(page: ft.Page):
    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
        size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=22,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
    )

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                40,
                title="40%",
                title_style=normal_title_style,
                color=ft.Colors.BLUE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                30,
                title="30%",
                title_style=normal_title_style,
                color=ft.Colors.YELLOW,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.Colors.PURPLE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.Colors.GREEN,
                radius=normal_radius,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
        expand=True,
    )

    page.add(chart)

ft.app(main)
```

--------------------------------

### Expand Child Control to Fill Space in Flet Column

Source: <https://flet.dev/docs/controls/column>

Shows how to make a child control within a Flet Column expand to fill the available space. This can be done with a boolean `expand=True` or by using an integer 'expand factor' to proportionally divide space among multiple expanded children.

```python
r = ft.Column([
  ft.Container(expand=True, content=ft.Text("Here is search results")),
  ft.Text("Records found: 10")
])
```

```python
r = ft.Column([
  ft.Container(expand=1, content=ft.Text("Header")),
  ft.Container(expand=3, content=ft.Text("Body")),
  ft.Container(expand=1, content=ft.Text("Footer"))
])
```

--------------------------------

### Animate Control Offset with Flet

Source: <https://flet.dev/docs/cookbook/animations>

Enables implicit animation of the Control.offset property using animate_offset. This is useful for creating sliding effects. The offset property specifies horizontal and vertical translation of a control scaled to its size.

```python
import flet as ft

def main(page: ft.Page):

    c = ft.Container(
        width=150,
        height=150,
        bgcolor="blue",
        border_radius=10,
        offset=ft.transform.Offset(-2, 0),
        animate_offset=ft.animation.Animation(1000),
    )

    def animate(e):
        c.offset = ft.transform.Offset(0, 0)
        c.update()

    page.add(
        c,
        ft.ElevatedButton("Reveal!", on_click=animate),
    )

ft.app(main)

```

--------------------------------

### ResponsiveRow Basic Usage

Source: <https://flet.dev/docs/controls/responsiverow>

Demonstrates the basic usage of ResponsiveRow with two columns spanning 6 virtual columns each.

```APIDOC
## POST /api/responsive_row

### Description
This example shows how to create a ResponsiveRow with two child columns, each spanning 6 virtual columns.

### Method
POST

### Endpoint
/api/responsive_row

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **controls** (list) - Required - A list of controls to display inside the ResponsiveRow.
  - **col** (integer) - Required - The number of columns a control should span.
  - **controls** (list) - Required - A list of controls to display inside the Column.
  - **text** (string) - Required - The text content of the Text control.

### Request Example
```json
{
  "controls": [
    {
      "type": "Column",
      "col": 6,
      "controls": [
        {
          "type": "Text",
          "value": "Column 1"
        }
      ]
    },
    {
      "type": "Column",
      "col": 6,
      "controls": [
        {
          "type": "Text",
          "value": "Column 2"
        }
      ]
    }
  ]
}
```

### Response

#### Success Response (200)

- **message** (string) - Indicates successful creation of the ResponsiveRow.

#### Response Example

```json
{
  "message": "ResponsiveRow created successfully"
}
```

```

--------------------------------

### Basic ResponsiveRow Layout in Flet

Source: https://flet.dev/docs/controls/responsiverow

Demonstrates a basic ResponsiveRow layout with two columns, each spanning 6 virtual columns. This sets up a simple two-column structure that can be used as a foundation for more complex layouts.

```python
import flet as ft

ft.ResponsiveRow([
    ft.Column(col=6, controls=[ft.Text("Column 1")]),
    ft.Column(col=6, controls=[ft.Text("Column 2")])
])
```

--------------------------------

### Add Container with Styling (Flet)

Source: <https://flet.dev/docs/tutorials/python-calculator>

Demonstrates how to use the `Container` control in Flet to add a styled background with rounded corners and padding to the calculator. It wraps the calculator content in a `Column` to allow for decoration.

```python
page.add(
    ft.Container(
        width=350,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=ft.Column(
            controls= [] # Controls will the six rows with the text
                   # and the calculator buttons.
        )
    )
)
```

--------------------------------

### Set Page Padding to Zero in Python

Source: <https://flet.dev/docs/controls/page>

Illustrates how to remove any default padding around the page content by setting the `page.padding` property to 0. After modifying the padding, `page.update()` must be called to apply the changes to the user interface. This is useful for achieving a full-bleed layout.

```python
page.padding = 0
page.update()
```

--------------------------------

### Generate Base64 from Image File (Linux/macOS/WSL)

Source: <https://flet.dev/docs/controls/image>

This command-line instruction shows how to convert an image file into its Base64 string representation using the `base64` utility available on Linux, macOS, and Windows Subsystem for Linux (WSL). The output is saved to a specified text file, which can then be used with image display controls.

```bash
base64 -i <image.png> -o <image-base64.txt>
```

--------------------------------

### Expanding Children in Row

Source: <https://flet.dev/docs/controls/row>

Explains how to use the `expand` and `expand_loose` properties to control how child widgets fill available space within a Row.

```APIDOC
## Expanding children

When a child Control is placed into a Row you can "expand" it to fill the available space. Every Control has `expand` property that can have either a boolean value (`True` - expand control to fill all available space) or an integer - an "expand factor" specifying how to divide a free space with other expanded child controls. For example, this code creates a row with a TextField taking all available space and an ElevatedButton next to it:
```

r = ft.Row([
  ft.TextField(hint_text="Enter your name", expand=True),
  ft.ElevatedButton(text="Join chat")
])

```

The following example with numeric expand factors creates a Row with 3 containers in it and having widths of `20% (1/5)`, `60% (3/5)` and `20% (1/5)` respectively:
```

r = ft.Row([
  ft.Container(expand=1, content=ft.Text("A")),
  ft.Container(expand=3, content=ft.Text("B")),
  ft.Container(expand=1, content=ft.Text("C"))
])

```

In general, the resulting width of a child in percents is calculated as `expand / sum(all expands) * 100%`.
If you need to give the child Control of the Row the flexibility to expand to fill the available space horizontally but not require it to fill the available space, set its `expand_loose` property to `True`.
```

--------------------------------

### Display Image from Base64 String in Flet (Python)

Source: <https://flet.dev/docs/controls/image>

This Python code snippet demonstrates how to use the `flet` library to display an image directly from a Base64 encoded string. It utilizes the `ft.Image` control, setting the `src_base64` property to the encoded image data. The image will be rendered within the Flet application window. Ensure the Base64 string is valid and represents an image format supported by Flet.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Image(
            src_base64="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"
        )
    )

ft.app(target=main)

```

--------------------------------

### Flet Page Resize Handler

Source: <https://flet.dev/docs/tutorials/trello-clone>

This Python method, `page_resize`, is an event handler for page resizing in a Flet application. It checks if the active view is a `Board` and, if so, calls the `resize` method on the active view to adjust the layout. Finally, it updates the page to reflect any layout changes.

```python
def page_resize(self, e=None):  
    if type(self.active_view) is Board:  
        self.active_view.resize(self.sidebar.visible, self.page.width, self.page.height)  
    self.page.update()  
```

--------------------------------

### Flet Row: Enable Wrapping for Responsive Layouts

Source: <https://flet.dev/docs/controls/row>

Shows how to enable wrapping for Flet Row controls, allowing child items to move to the next line when the available horizontal space is insufficient. It uses a Slider to adjust the Row's width dynamically and demonstrates `wrap`, `spacing`, and `run_spacing` properties. This requires the 'flet' library.

```python
import flet as ft  

def main(page: ft.Page):  
    def items(count):  
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER,  
                    border_radius=ft.border_radius.all(5),  
                )  
            )  
        return items  

    def slider_change(e):  
        row.width = float(e.control.value)  
        row.update()  

    width_slider = ft.Slider(  
        min=0,  
        max=page.window.width,  
        divisions=20,  
        value=page.window.width,  
        label="{value}",  
        on_change=slider_change,  
    )  

    row = ft.Row(  
        wrap=True,  
        spacing=10,  
        run_spacing=10,  
        controls=items(30),  
        width=page.window.width,  
    )  

    page.add(  
        ft.Column(  
            [  
                ft.Text(  
                    "Change the row width to see how child items wrap onto multiple rows:"  
                ),  
                width_slider,  
            ]  
        ),  
        row,  
    )  


ft.app(main)  
```

--------------------------------

### Enable Flet Startup Screen (TOML)

Source: <https://flet.dev/docs/publish>

Configures the startup screen, shown after the boot screen while third-party packages are unpacked and the app initializes. Similar to the boot screen, it can be enabled globally or per platform, with customizable messages. This configuration corresponds to `[tool.flet.app.startup_screen]` and `[tool.flet.<platform>.app.startup_screen]` sections in `pyproject.toml`.

```toml
[tool.flet.app.startup_screen]
show = true
message = "Starting up the app…"

```

```toml
[tool.flet.android.app.startup_screen]
show = true

```

--------------------------------

### Enable Flet Boot Screen (TOML)

Source: <https://flet.dev/docs/publish>

Configures the boot screen, which is displayed while the app archive is unpacked. It can be enabled globally or for specific platforms, with an option to customize the displayed message. This configuration corresponds to `[tool.flet.app.boot_screen]` and `[tool.flet.<platform>.app.boot_screen]` sections in `pyproject.toml`.

```toml
[tool.flet.app.boot_screen]
show = true
message = "Preparing the app for its first launch…"

```

```toml
[tool.flet.android.app.boot_screen]
show = true

```

--------------------------------

### ResponsiveRow with Breakpoints

Source: <https://flet.dev/docs/controls/responsiverow>

Illustrates how to configure the `col` property for different breakpoints to achieve responsive design.

```APIDOC
## POST /api/responsive_row_breakpoints

### Description
This example demonstrates how to make a ResponsiveRow responsive by defining `col` properties for specific breakpoints (e.g., 'sm'). Content collapses to a single column on smaller screens and takes two columns on larger screens.

### Method
POST

### Endpoint
/api/responsive_row_breakpoints

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **controls** (list) - Required - A list of controls to display inside the ResponsiveRow.
  - **col** (object) - Required - An object defining column spans for different breakpoints.
    - **sm** (integer) - Optional - Number of columns to span on small screens (>= 576px).
  - **controls** (list) - Required - A list of controls to display inside the Column.
  - **text** (string) - Required - The text content of the Text control.

### Request Example
```json
{
  "controls": [
    {
      "type": "Column",
      "col": {"sm": 6},
      "controls": [
        {
          "type": "Text",
          "value": "Column 1"
        }
      ]
    },
    {
      "type": "Column",
      "col": {"sm": 6},
      "controls": [
        {
          "type": "Text",
          "value": "Column 2"
        }
      ]
    }
  ]
}
```

### Response

#### Success Response (200)

- **message** (string) - Indicates successful creation of the responsive ResponsiveRow.

#### Response Example

```json
{
  "message": "ResponsiveRow with breakpoints created successfully"
}
```

```

--------------------------------

### Expand Controls in Flet Rows and Columns

Source: https://flet.dev/docs/controls

Illustrates the use of the 'expand' property in Flet to make child controls fill available space within Row and Column layouts. Supports boolean and integer expand factors.

```python
import flet as ft

def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Card(
                            content=ft.Text("Card_1"),
                            color=ft.Colors.ORANGE_300,
                            expand=True,
                            height=page.height,
                            margin=0,
                        ),
                        ft.Card(
                            content=ft.Text("Card_2"),
                            color=ft.Colors.GREEN_100,
                            expand=True,
                            height=page.height,
                            margin=0,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        ),
    )

ft.app(main)
```

--------------------------------

### Flet Margin Usage Examples

Source: <https://flet.dev/docs/reference/types/margin>

Demonstrates various ways to apply margins to Flet containers using the Margin class's helper methods. This includes applying margins to all sides, symmetric margins, and margins to specific sides. The examples show how to instantiate Margin objects and assign them to a container's margin property.

```python
container_1.margin = margin.all(10)
container_2.margin = 20 # same as margin.all(20)
container_3.margin = margin.symmetric(vertical=10)
container_4.margin = margin.only(left=10)
```

--------------------------------

### Adapt UI Based on Platform in Flet

Source: <https://flet.dev/docs/controls/page>

Demonstrates how to conditionally render UI elements based on the operating system the Flet application is running on using the page.platform property. This allows for platform-specific UI adjustments.

```python
def main(page: ft.Page):
    if page.platform == ft.PagePlatform.MACOS:
        page.add(ft.CupertinoDialogAction("Cupertino Button"))
    else:
        page.add(ft.TextButton("Material Button"))
```

--------------------------------

### Python: Implement Horizontal Divider in Flet App

Source: <https://flet.dev/docs/controls/divider>

This Python code snippet demonstrates how to use the Flet Divider control to create horizontal visual separators within a UI layout. It showcases different Divider configurations, including default, custom height, color, thickness, and indents, within a Flet application. The Divider is used to visually segment various colored container widgets.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
  
    page.add(  
        ft.Column(  
            [  
                ft.Container(  
                    bgcolor=ft.Colors.AMBER,  
                    alignment=ft.alignment.center,  
                    expand=True,  
                ),  
                ft.Divider(),  
                ft.Container(  
                    bgcolor=ft.Colors.PINK, alignment=ft.alignment.center, expand=True  
                ),  
                ft.Divider(height=1, color="white"),  
                ft.Container(  
                    bgcolor=ft.Colors.BLUE_300,  
                    alignment=ft.alignment.center,  
                    expand=True,  
                ),  
                ft.Divider(height=9, thickness=3),  
                ft.Container(  
                    bgcolor=ft.Colors.DEEP_PURPLE_200,  
                    alignment=ft.alignment.center,  
                    expand=True,  
                ),  
            ],  
            spacing=0,  
            expand=True,  
        ),  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Flet Rectangle Drawing

Source: <https://flet.dev/docs/controls/canvas>

Draws a rectangle with specified width, height, and position. It supports rounded corners via the `border_radius` property and can be styled using a `Paint` object. The `x` and `y` coordinates define the top-left corner of the rectangle.

```python
ft.Rect(
    x=50,
    y=50,
    width=100,
    height=80,
    border_radius=ft.border_radius.all(10),
    paint=ft.Paint(color=ft.colors.RED)
)
```

--------------------------------

### Flet Column Spacing Example

Source: <https://flet.dev/docs/controls/column>

Demonstrates how to control the vertical spacing between child controls in a Flet Column. It uses a slider to dynamically adjust the spacing property, allowing for visual feedback.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    def items(count):
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER,  
                    border_radius=ft.border_radius.all(5),  
                )  
            )  
        return items  
  
    def spacing_slider_change(e):  
        col.spacing = int(e.control.value)  
        col.update()  
  
    gap_slider = ft.Slider(  
        min=0,  
        max=100,  
        divisions=10,  
        value=0,  
        label="{value}",  
        width=500,  
        on_change=spacing_slider_change,  
    )  
  
    col = ft.Column(spacing=0, controls=items(5))  
  
    page.add(ft.Column([ft.Text("Spacing between items"), gap_slider]), col)  
  
  
ft.app(main)  

```

--------------------------------

### Flet expand_loose Example in Rows

Source: <https://flet.dev/docs/controls>

Demonstrates the use of `expand_loose = True` within `ft.Row` controls in Flet. This property allows child controls to expand to fill available space without being strictly required to do so, affecting layout behavior when `expand` is also true.

```python
import flet as ft  


class Message(ft.Container):
    def __init__(self, author, body):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Text(author, weight=ft.FontWeight.BOLD),
                ft.Text(body),
            ],
        )
        self.border = ft.border.all(1, ft.Colors.BLACK)
        self.border_radius = ft.border_radius.all(10)
        self.bgcolor = ft.Colors.GREEN_200
        self.padding = 10
        self.expand = True
        self.expand_loose = True


def main(page: ft.Page):

    chat = ft.ListView(
        padding=10,
        spacing=10,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body="Hi, how are you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Hi I am good thanks, how about you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Thank you!",
                    ),
                ],
            ),
        ],
    )

    page.window.width = 393
    page.window.height = 600
    page.window.always_on_top = False

    page.add(chat)


ft.app(main)

```

--------------------------------

### Sync Event Handler in Flet

Source: <https://flet.dev/docs/getting-started/async-apps>

Demonstrates a synchronous event handler for a Flet page resize event. This type of handler is suitable when the event logic does not involve any asynchronous operations. It defines a simple function to print the new page dimensions and assigns it to the page's on_resize event.

```python
def page_resize(e):
    print("New page size:", page.window.width, page.window.height)

page.on_resize = page_resize
```

--------------------------------

### Page Show Semantics Debugger Property

Source: <https://flet.dev/docs/controls/page>

The `show_semantics_debugger` property, when set to `True`, activates an overlay that displays accessibility information provided by the Flet framework, aiding in debugging accessibility features.

```APIDOC
## Page Show Semantics Debugger Property

### Description
`True` turns on an overlay that shows the accessibility information reported by the framework.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
page.show_semantics_debugger = True
page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Displaying Large Lists with Column (Inefficient)

Source: https://flet.dev/docs/cookbook/large-lists

Demonstrates adding a large number of text controls (5000) to a Flet page using a Column layout. This approach is inefficient as it renders all items at once, leading to slow initial loading and laggy scrolling. It's suitable for smaller lists but ineffective for hundreds or thousands of items.

```python
import flet as ft  

def main(page: ft.Page):  
    for i in range(5000):  
        page.controls.append(ft.Text(f"Line {i}"))  
    page.scroll = "always"  
    page.update()  

ft.app(main, view=ft.AppView.WEB_BROWSER)  

```

--------------------------------

### Structure Flet app layout with Row and Column

Source: <https://flet.dev/docs/tutorials/python-todo>

Organizes Flet UI elements using `Row` and `Column` controls for horizontal and vertical layout management. This code snippet structures the To-Do app by placing a `TextField` and `FloatingActionButton` within a `Row`, and arranging this row along with a task display column within a main `Column`. It centers the main column horizontally on the page. Requires the 'flet' package.

```python
import flet as ft


def main(page: ft.Page):
    def add_clicked(e):
        tasks_view.controls.append(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        view.update()

    new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
    tasks_view = ft.Column()
    view=ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    new_task,
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
                ],
            ),
            tasks_view,
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)

ft.app(main)

```

--------------------------------

### Flet Row Expand Example - Boolean

Source: <https://flet.dev/docs/controls/row>

Shows how to make a child control in a Flet Row expand to fill all available horizontal space using `expand=True`. This is useful for creating layouts where one element should take precedence.

```python
r = ft.Row([
  ft.TextField(hint_text="Enter your name", expand=True),
  ft.ElevatedButton(text="Join chat")
])
```

--------------------------------

### Flet RoundedRectangleBorder Usage for FAB

Source: <https://flet.dev/docs/reference/types/outlinedborder>

This Python code snippet demonstrates how to use the RoundedRectangleBorder to style a Flet FloatingActionButton. It imports the flet library and defines a main function that sets up a page with a FAB. The FAB's shape is customized using RoundedRectangleBorder with a radius of 5.

```python
import flet as ft

def main(page: ft.Page):
    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD), ft.Text("Add")], alignment="center", spacing=5
        ),
        bgcolor=ft.Colors.AMBER_300,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
    )

    page.add(ft.Text("Just a text!"))

ft.app(main)

```

--------------------------------

### Flet Row with Wrap for Grid-like Layout

Source: <https://flet.dev/docs/cookbook/large-lists>

Illustrates creating a grid-like layout using Flet's `ft.Row` with the `wrap=True` property. This approach allows controls to wrap to the next line when the container width is insufficient. The example demonstrates adding 5000 items to a scrollable row and includes setting `FLET_WS_MAX_MESSAGE_SIZE` to handle the large data.

```python
import os
import flet as ft

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"

def main(page: ft.Page):
    r = ft.Row(wrap=True, scroll="always", expand=True)
    page.add(r)

    for i in range(5000):
        r.controls.append(
            ft.Container(
                ft.Text(f"Item {i}"),
                width=100,
                height=100,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.AMBER_100,
                border=ft.border.all(1, ft.Colors.AMBER_400),
                border_radius=ft.border_radius.all(5),
            )
        )
    page.update()

ft.app(main, view=ft.AppView.WEB_BROWSER)

```

--------------------------------

### Customize Scrollbar Theme with ScrollbarTheme

Source: <https://flet.dev/docs/reference/types/scrollbartheme>

This code snippet demonstrates how to customize the scrollbar's appearance by applying a ScrollbarTheme to the page's theme. It showcases setting various properties like track color, visibility, border color, thumb visibility, thumb color, thickness, radius, margins, and minimum thumb length.

```python
page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
        track_color={
            ft.MaterialState.HOVERED: ft.Colors.AMBER,
            ft.MaterialState.DEFAULT: ft.Colors.TRANSPARENT,
        },
        track_visibility=True,
        track_border_color=ft.Colors.BLUE,
        thumb_visibility=True,
        thumb_color={
            ft.MaterialState.HOVERED: ft.Colors.RED,
            ft.MaterialState.DEFAULT: ft.Colors.GREY_300,
        },
        thickness=30,
        radius=15,
        main_axis_margin=5,
        cross_axis_margin=10,
    )
)
```

--------------------------------

### ScrollbarTheme Customization

Source: <https://flet.dev/docs/reference/types/scrollbartheme>

This section details the properties available for the ScrollbarTheme class, which allows for customization of scrollbar colors, thickness, visibility, and more.

```APIDOC
## ScrollbarTheme Properties

This document outlines the properties available for customizing the `ScrollbarTheme` in Flet.

### `thumb_visibility`

- **Type**: boolean or dict[ft.ControlState, boolean]
- **Description**: Determines if the scrollbar thumb should always be visible. If `False`, it fades out when not in use. If `True`, it remains visible.

### `thickness`

- **Type**: float or dict[ft.ControlState, float]
- **Description**: Sets the thickness of the scrollbar along its cross axis.

### `track_visibility`

- **Type**: boolean or dict[ft.ControlState, boolean]
- **Description**: Controls the visibility of the scrollbar track. Defaults to `False`. If `None`, it falls back to the theme's `scrollbar_theme.track_visibility`.

### `radius`

- **Type**: float
- **Description**: Defines the radius for the rounded corners of the scrollbar thumb.

### `thumb_color`

- **Type**: string or dict[ft.ControlState, string]
- **Description**: Overrides the default color of the scrollbar thumb.

### `track_color`

- **Type**: string or dict[ft.ControlState, string]
- **Description**: Overrides the default color of the scrollbar track.

### `track_border_color`

- **Type**: string or dict[ft.ControlState, string]
- **Description**: Overrides the default color of the scrollbar track's border.

### `cross_axis_margin`

- **Type**: float
- **Description**: The distance from the scrollbar thumb to the nearest cross-axis edge in logical pixels. Defaults to 0.

### `main_axis_margin`

- **Type**: float
- **Description**: The distance from the scrollbar thumb's start and end to the viewport edge in logical pixels. Defaults to 0.

### `min_thumb_length`

- **Type**: float
- **Description**: The preferred minimum size of the scrollbar thumb.

### `interactive`

- **Type**: boolean
- **Description**: Whether the scrollbar is interactive (responds to dragging and tapping). Defaults to `True`, unless on Android where it defaults to `False` if `None`.

### Example Usage

```python
page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
        track_color={
            ft.MaterialState.HOVERED: ft.Colors.AMBER,
            ft.MaterialState.DEFAULT: ft.Colors.TRANSPARENT,
        },
        track_visibility=True,
        track_border_color=ft.Colors.BLUE,
        thumb_visibility=True,
        thumb_color={
            ft.MaterialState.HOVERED: ft.Colors.RED,
            ft.MaterialState.DEFAULT: ft.Colors.GREY_300,
        },
        thickness=30,
        radius=15,
        main_axis_margin=5,
        cross_axis_margin=10,
    )
)
```

```

--------------------------------

### Modify ft.app for Web Browser View

Source: https://flet.dev/docs/publish/web/dynamic-website/hosting/replit

This Python code snippet demonstrates how to modify the `ft.app()` call within your Flet application's `main.py` file. By adding the `view=ft.AppView.WEB_BROWSER` parameter, the Flet app will be configured to run and display directly in a web browser, which is essential for deployment on platforms like Replit.

```python
ft.app(main, view=ft.AppView.WEB_BROWSER)
```

--------------------------------

### Flet Column Wrapping Example

Source: <https://flet.dev/docs/controls/column>

Illustrates how to enable content wrapping within a Flet Column. When the column's height is constrained, child items will wrap to new lines.

```python
import flet as ft  
  
HEIGHT = 400  
  
  
def main(page: ft.Page):  
  
    def items(count):  
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=30,  
                    height=30,  
                    bgcolor=ft.Colors.AMBER,  
                    border_radius=ft.border_radius.all(5),  
                )  
            )  
        return items  
  
    def slider_change(e):  
        col.height = float(e.control.value)  
        col.update()  
  
    width_slider = ft.Slider(  
        min=0,  
        max=HEIGHT,  
        divisions=20,  
        value=HEIGHT,  
        label="{value}",  
        width=500,  
        on_change=slider_change,  
    )  
  
    col = ft.Column(  
        wrap=True,  
        spacing=10,  
        run_spacing=10,  
        controls=items(10),  
        height=HEIGHT,  
    )  
  
    page.add(  
        ft.Column(  
            [  
                ft.Text(  
                    "Change the column height to see how child items wrap onto multiple columns:"  
                ),  
                width_slider,  
            ]  
        ),  
        ft.Container(content=col, bgcolor=ft.Colors.TRANSPARENT),  
    )  
  
  
ft.app(main)  


```

--------------------------------

### Flet View Control Scroll to Method

Source: <https://flet.dev/docs/controls/view>

Details the `scroll_to()` method for the Flet View control, which allows programmatic scrolling to specific positions (absolute offset, relative delta, or by control key).

```python
# Example usage (assuming 'page' is a Flet page object)
# page.scroll_to(offset=100)
# page.scroll_to(delta=50)
# page.scroll_to(key="my_control_id")
```

--------------------------------

### Simple ExpansionPanelList Example in Python

Source: <https://flet.dev/docs/controls/expansionpanel>

Demonstrates how to create and manage a list of expandable panels using Flet's ExpansionPanelList and ExpansionPanel controls. It includes handling panel expansion/collapse events and deleting panels.

```python
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_change(e: ft.ControlEvent):
        print(f"change on panel with index {e.data}")

    def handle_delete(e: ft.ControlEvent):
        panel.controls.remove(e.control.data)
        page.update()

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        elevation=8,
        divider_color=ft.Colors.AMBER,
        on_change=handle_change,
        controls=[
            ft.ExpansionPanel(
                # has no header and content - placeholders will be used
                bgcolor=ft.Colors.BLUE_400,
                expanded=True,
            )
        ],
    )

    colors = [
        ft.Colors.GREEN_500,
        ft.Colors.BLUE_800,
        ft.Colors.RED_800,
    ]

    for i in range(3):
        bgcolor = colors[i % len(colors)]

        exp = ft.ExpansionPanel(
            bgcolor=bgcolor,
            header=ft.ListTile(title=ft.Text(f"Panel {i}"), bgcolor=bgcolor),
        )

        exp.content = ft.ListTile(
            title=ft.Text(f"This is in Panel {i}"),
            subtitle=ft.Text(f"Press the icon to delete panel {i}"),
            trailing=ft.IconButton(ft.Icons.DELETE, on_click=handle_delete, data=exp),
            bgcolor=bgcolor,
        )

        panel.controls.append(exp)

    page.add(panel)


ft.app(main)
```

--------------------------------

### Basic CupertinoAppBar Example in Python

Source: <https://flet.dev/docs/controls/cupertinoappbar>

Demonstrates how to create a basic iOS-styled application bar using Flet's CupertinoAppBar. This example shows setting the leading icon, background color, trailing icon, and a middle text element. It requires the Flet library. The output is a Flet application with the specified app bar and a simple text body.

```python
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        trailing=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED),
        middle=ft.Text("CupertinoAppBar Example"),
        brightness=ft.Brightness.LIGHT,
    )
    page.add(ft.Text("Body!"))

ft.app(main)
```

--------------------------------

### Create Flet Border with `border.all`

Source: <https://flet.dev/docs/reference/types/border>

Demonstrates how to set a uniform border on all four sides of a container using the `border.all` helper method. This method takes a width and a color as arguments.

```python
container_1.border = ft.border.all(10, ft.Colors.PINK_600)
```

--------------------------------

### Page Platform Brightness

Source: <https://flet.dev/docs/controls/page>

The `platform_brightness` property provides the current brightness mode of the host platform. This is a read-only property.

```APIDOC
## Page Platform Brightness

### Description
The current brightness mode of the host platform. Value is read-only and of type `Brightness`.

### Method
Read-only

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
N/A

### Response
#### Success Response (200)
N/A

#### Response Example
N/A
```

--------------------------------

### InteractiveViewerInteractionUpdateEvent Properties

Source: <https://flet.dev/docs/reference/types/interactiveviewerinteractionupdateevent>

This section describes the properties available on the InteractiveViewerInteractionUpdateEvent object, which are populated during user interaction with an InteractiveViewer.

```APIDOC
## InteractiveViewerInteractionUpdateEvent Properties

### Description
This event object provides details about user interactions such as panning, scaling, and rotation within an `InteractiveViewer` widget.

### Properties

#### `pointer_count`
- **Type**: `int`
- **Description**: The number of pointers (e.g., fingers) currently interacting with the widget. Note that trackpad gestures may count as two fingers regardless of actual usage due to platform limitations.

#### `global_focal_point`
- **Type**: `Offset`
- **Description**: The focal point of the interaction, represented in global screen coordinates.

#### `local_focal_point`
- **Type**: `Offset`
- **Description**: The focal point of the interaction, represented in the widget's local coordinate system.

#### `scale`
- **Type**: `float`
- **Description**: The scale factor implied by the average distance between all interacting pointers.

#### `horizontal_scale`
- **Type**: `float`
- **Description**: The scale factor implied by the average distance between pointers along the horizontal axis.

#### `vertical_scale`
- **Type**: `float`
- **Description**: The scale factor implied by the average distance between pointers along the vertical axis.

#### `rotation`
- **Type**: `float`
- **Description**: The rotation angle (in radians) implied by the first two pointers that initiated contact.
```

--------------------------------

### ExpansionPanelList and ExpansionPanel Overview

Source: <https://flet.dev/docs/controls/expansionpanel>

This section details the properties and events of ExpansionPanelList and its child ExpansionPanel controls, demonstrating how to create interactive, expandable panels.

```APIDOC
## ExpansionPanelList
A material expansion panel list that lays out its children and animates expansions.

### Properties

*   **controls** (list[ExpansionPanel]) - A list of `ExpansionPanel`s to display inside `ExpansionPanelList`.
*   **divider_color** (color) - The color of the divider when `ExpansionPanel.expanded` is `False`.
*   **elevation** (int) - Defines the elevation of the children controls (`ExpansionPanel`s), while it is expanded. Default value is `2`.
*   **expanded_header_padding** (Padding) - Defines the padding around the header when expanded. Default value is `padding.symmetric(vertical=16.0)`.
*   **expanded_icon_color** (color) - The color of the icon. Defaults to `colors.BLACK_54` in light theme mode and `colors.WHITE_60` in dark theme mode.
*   **spacing** (float) - The size of the gap between the `ExpansionPanel`s when expanded.

### Events

*   **on_change** (func) - Fires when an `ExpansionPanel` is expanded or collapsed. The event's data (`e.data`), contains the index of the `ExpansionPanel` which triggered this event.

## ExpansionPanel Properties

*   **bgcolor** (color) - The background color of the panel.
*   **content** (Control) - The control to be found in the body of the `ExpansionPanel`. It is displayed below the `header` when the panel is expanded. If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as content.
*   **can_tap_header** (bool) - If `True`, tapping on the panel's `header` will expand or collapse it. Defaults to `False`.
*   **expanded** (bool) - Whether expanded(`True`) or collapsed(`False`). Defaults to `False`.
*   **header** (Control) - The control to be found in the header of the `ExpansionPanel`. If `can_tap_header` is `True`, tapping on the header will expand or collapse the panel. If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as header.
```

--------------------------------

### Flet GridView Example for Large Data Sets

Source: <https://flet.dev/docs/cookbook/large-lists>

Demonstrates how to use Flet's GridView to efficiently arrange a large number of controls (5000 items) in a scrollable grid. It highlights the smooth scrolling and responsiveness achieved with GridView, especially when compared to using wrap=True with Row or Column. The example also includes setting `FLET_WS_MAX_MESSAGE_SIZE` to handle large data transmission.

```python
import os
import flet as ft

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"

def main(page: ft.Page):
    gv = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    page.add(gv)

    for i in range(5000):
        gv.controls.append(
            ft.Container(
                ft.Text(f"Item {i}"),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.AMBER_100,
                border=ft.border.all(1, ft.Colors.AMBER_400),
                border_radius=ft.border_radius.all(5),
            )
        )
    page.update()

ft.app(main, view=ft.AppView.WEB_BROWSER)

```

--------------------------------

### Programmatic Scrolling with `scroll_to()`

Source: <https://flet.dev/docs/controls/column>

Demonstrates how to programmatically scroll the content of a Column using the `scroll_to()` method with various parameters like offset, key, and delta.

```APIDOC
## Scrolling Column Programmatically

The `scroll_to()` method allows you to programmatically scroll the content of a Column. You can specify the scroll position using `offset`, scroll to a specific control by its `key`, or adjust the scroll position by a `delta` value. The scrolling can be animated using the `duration` parameter and customized with `curve`.

### Method
`scroll_to(offset=None, key=None, delta=None, duration=0, curve=None)`

### Parameters

#### `offset` (float)
- Scrolls to the specified offset from the top. `offset=0` scrolls to the top, `offset=-1` scrolls to the bottom.

#### `key` (str)
- Scrolls to the control with the specified key.

#### `delta` (float)
- Adjusts the scroll position by the specified delta value. Positive values scroll down, negative values scroll up.

#### `duration` (int)
- The duration of the scroll animation in milliseconds. If 0, the scroll is immediate.

#### `curve` (ft.AnimationCurve)
- The animation curve to use for the scroll animation. Examples: `ft.AnimationCurve.LINEAR`, `ft.AnimationCurve.EASE_IN_OUT`.

### Request Example
```python
# Scroll to an offset of 500 pixels with a 1000ms duration
cl.scroll_to(offset=500, duration=1000)

# Scroll to the control with key '20' with a 1000ms duration
cl.scroll_to(key="20", duration=1000)

# Scroll down by 100 pixels with a 200ms duration
cl.scroll_to(delta=100, duration=200)

# Scroll to the end with a 2000ms duration and EASE_IN_OUT curve
cl.scroll_to(offset=-1, duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT)
```

### Response

This method does not return a value, but modifies the scroll position of the Column.

```

--------------------------------

### Simple AppBar in Python

Source: https://flet.dev/docs/controls/appbar

Demonstrates the creation of a basic AppBar in Flet. This example shows how to set the title, leading icon, background color, and action buttons including a popup menu. It requires the flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "AppBar Example"

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )
    page.add(ft.Text("Body!"))


ft.app(target=main)

```

--------------------------------

### ResponsiveRow Live Example

Source: <https://flet.dev/docs/controls/responsiverow>

Provides a complete Python code example demonstrating a dynamic ResponsiveRow that updates on page resize.

```APIDOC
## GET /api/responsive_row_live_example

### Description
This endpoint provides a full Python code example for a live, interactive ResponsiveRow. It includes functionality to display the current page width and updates the layout based on window resizing.

### Method
GET

### Endpoint
/api/responsive_row_live_example

### Parameters
None

### Request Example
(No request body for GET request)

### Response
#### Success Response (200)
- **code** (string) - The Python code for the live ResponsiveRow example.

#### Response Example
```python
import flet as ft

def main(page: ft.Page):
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize

    pw = ft.Text(bottom=50, right=50, style=ft.TextTheme.display_small)
    page.overlay.append(pw)
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
            run_spacing={"xs": 10},
        ),
    )
    page_resize(None)

ft.app(main)
```

```

--------------------------------

### Python Pagelet Example with Appbar, BottomAppBar, and Drawer

Source: https://flet.dev/docs/controls/pagelet

This example demonstrates how to create a Flet Pagelet control. It includes a custom AppBar, a BottomAppBar with action buttons, and an end drawer that can be opened via a FloatingActionButton. The Pagelet itself is configured with specific dimensions and background colors.

```python
import flet as ft  

def main(page: ft.Page):  
    def open_pagelet_end_drawer(e):  
        pagelet.show_drawer(ed)  
  
    ed = ft.NavigationDrawer(  
        controls=[  
            ft.NavigationDrawerDestination(  
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"  
            ),  
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_COMMENT, label="Item 2"),  
        ],  
    )  
    pagelet = ft.Pagelet(  
        appbar=ft.AppBar(  
            title=ft.Text("Pagelet AppBar Title"), bgcolor=ft.Colors.AMBER_ACCENT  
        ),  
        content=ft.Container(ft.Text("Pagelet Body"), padding=ft.padding.all(16)),  
        bgcolor=ft.Colors.AMBER_100,  
        bottom_app_bar=ft.BottomAppBar(  
            bgcolor=ft.Colors.BLUE,  
            shape=ft.NotchShape.CIRCULAR,  
            content=ft.Row(  
                controls=[  
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),  
                    ft.Container(expand=True),  
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),  
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),  
                ]  
            ),  
        ),  
        end_drawer=ed,  
        floating_action_button=ft.FloatingActionButton(  
            "Open", on_click=open_pagelet_end_drawer, shape=ft.CircleBorder()  
        ),  
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,  
        width=400,  
        height=400,  
    )  

    page.add(pagelet)  


ft.app(main)  
```

--------------------------------

### CupertinoAlertDialog and Adaptive AlertDialog Example in Python

Source: <https://flet.dev/docs/controls/cupertinoalertdialog>

Demonstrates how to use CupertinoAlertDialog, AlertDialog, and adaptive dialogs in Flet. It shows how to configure actions for each dialog type and how to open them using page.open(). The adaptive dialog example showcases platform-specific action button rendering.

```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    def handle_action_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.text}"))
        # e.control is the clicked action button, e.control.parent is the corresponding parent dialog of the button
        page.close(e.control.parent)

    cupertino_actions = [
        ft.CupertinoDialogAction(
            "Yes",
            is_destructive_action=True,
            on_click=handle_action_click,
        ),
        ft.CupertinoDialogAction(
            text="No",
            is_default_action=False,
            on_click=handle_action_click,
        ),
    ]

    material_actions = [
        ft.TextButton(text="Yes", on_click=handle_action_click),
        ft.TextButton(text="No", on_click=handle_action_click),
    ]

    page.add(
        ft.FilledButton(
            text="Open Material Dialog",
            on_click=lambda e: page.open(
                ft.AlertDialog(
                    title=ft.Text("Material Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=material_actions,
                )
            ),
        ),
        ft.CupertinoFilledButton(
            text="Open Cupertino Dialog",
            on_click=lambda e: page.open(
                ft.CupertinoAlertDialog(
                    title=ft.Text("Cupertino Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=cupertino_actions,
                )
            ),
        ),
        ft.FilledButton(
            text="Open Adaptive Dialog",
            adaptive=True,
            bgcolor=ft.Colors.BLUE_ACCENT,
            on_click=lambda e: page.open(
                ft.AlertDialog(
                    adaptive=True,
                    title=ft.Text("Adaptive Alert Dialog"),
                    content=ft.Text("Do you want to delete this file?"),
                    actions=(
                        cupertino_actions
                        if page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.MACOS]
                        else material_actions
                    ),
                )
            ),
        ),
    )


ft.app(main)

```

--------------------------------

### Basic Example

Source: <https://flet.dev/docs/controls/cupertinodatepicker>

A basic example demonstrating how to open and use the CupertinoDatePicker.

```APIDOC
## POST /open_cupertino_date_picker

### Description
Opens a CupertinoDatePicker dialog within a bottom sheet.

### Method
POST

### Endpoint
/

### Request Body
```json
{
  "control": "CupertinoBottomSheet",
  "properties": {
    "content": {
      "control": "CupertinoDatePicker",
      "properties": {
        "date_picker_mode": "CupertinoDatePickerMode.DATE_AND_TIME",
        "on_change": "handle_date_change"
      }
    },
    "height": 216,
    "padding": {
      "control": "padding",
      "properties": {
        "only": {
          "top": 6
        }
      }
    }
  }
}
```

### Response

#### Success Response (200)

Indicates the dialog was opened successfully. The actual UI update is handled client-side.

#### Response Example

```json
{
  "status": "success",
  "message": "CupertinoDatePicker opened"
}
```

```

--------------------------------

### Page Platform

Source: https://flet.dev/docs/controls/page

The `platform` property indicates the operating system the application is running on. It can be used to create adaptive UIs tailored to specific platforms like macOS or others.

```APIDOC
## Page Platform

### Description
Operating system the application is running on. Value is of type `PagePlatform`. This property can be used to create adaptive UI with different controls depending on the operating system.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
def main(page: ft.Page):
    if page.platform == ft.PagePlatform.MACOS:
        page.add(ft.CupertinoDialogAction("Cupertino Button"))
    else:
        page.add(ft.TextButton("Material Button"))
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Display Images with Flet Image Control (Python)

Source: https://flet.dev/docs/controls/image

This Python code snippet demonstrates how to use the Flet Image control to display images. It shows how to load local assets and remote URLs, customize image appearance with properties like width, height, fit, and border_radius, and handle multiple images in a scrollable row. This example requires the flet library to be installed.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    images = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.app(main)

```

--------------------------------

### Open OAuth Authorization in New Tab (Flet)

Source: <https://flet.dev/docs/cookbook/authentication>

This Flet code snippet demonstrates how to make the OAuth provider's authorization page open in a new browser tab. By setting `web_window_name="_blank"` within the `page.launch_url()` call, the user is directed to the authorization URL in a separate tab, preventing disruption of their current session.

```python
page.login(
    provider,
    on_open_authorization_url=lambda url: page.launch_url(url, web_window_name="_blank")
)
```

--------------------------------

### Flet Text Drawing

Source: <https://flet.dev/docs/controls/canvas>

Renders text with specified styling, alignment, and layout constraints. The `text` property holds the content, `style` defines font properties, and `max_width` and `max_lines` control text wrapping and truncation. `alignment` determines the text's rotation and positioning anchor.

```python
ft.Text(
    "Hello, Flet!",
    x=20,
    y=20,
    width=200,
    max_lines=2,
    ellipsis="...",
    rotate=0.1,
    alignment=ft.alignment.center,
    style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
)
```

--------------------------------

### Page Query Property

Source: <https://flet.dev/docs/controls/page>

The `query` property provides access to the query string part of the application's URL (the part after '?'). It returns an instance of `QueryString`, offering helper methods to fetch query parameters.

```APIDOC
## Page Query Property

### Description
A part of app URL after `?`. The value is an instance of `QueryString` with helper methods for fetching query parameters.

### Method
Read-only

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
# Assuming the URL is /?user=john&id=123
user = page.query.get("user") # "john"
id = page.query.get_int("id") # 123
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Create BorderRadius with vertical corners

Source: https://flet.dev/docs/reference/types/borderradius

The `ft.border_radius.vertical(top, bottom)` method enables setting separate border radius values for the top and bottom vertical corners of a rectangle. Both `top` and `bottom` parameters default to 0, resulting in no vertical rounding if not specified.

```python
ft.border_radius.vertical(top=15, bottom=25)
```

--------------------------------

### Page Theme Mode Property

Source: <https://flet.dev/docs/controls/page>

The `theme_mode` property determines the page's theme mode. It can be set to `ThemeMode.SYSTEM`, `ThemeMode.LIGHT`, or `ThemeMode.DARK`, with `ThemeMode.SYSTEM` being the default.

```APIDOC
## Page Theme Mode Property

### Description
The page's theme mode. Value is of type `ThemeMode` and defaults to `ThemeMode.SYSTEM`.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    # Set theme to dark mode
    page.theme_mode = ft.ThemeMode.DARK
    page.add(ft.Text("Dark mode text"))
    page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### ExpansionTile Widget API

Source: https://flet.dev/docs/controls/expansiontile

Documentation for the ExpansionTile widget, detailing its properties and how to use it.

```APIDOC
## ExpansionTile Widget

A single-line ListTile with an expansion arrow icon that expands or collapses the tile to reveal or hide its children.

### Properties

- **affinity** (TileAffinity) - Optional - Typically used to force the expansion arrow icon to the tile's `leading` or `trailing` edge. Defaults to `TileAffinity.PLATFORM`.
- **bgcolor** (Color) - Optional - The color to display behind the sublist when expanded.
- **controls** (list[Control]) - Optional - The controls to be displayed when the tile expands. Typically a list of `ListTile` controls.
- **controls_padding** (Padding) - Optional - Defines the padding around the `controls`.
- **clip_behavior** (ClipBehavior) - Optional - The content will be clipped (or not) according to this option. Defaults to `ClipBehavior.NONE`.
- **collapsed_bgcolor** (Color) - Optional - Defines the background color of tile when the sublist is collapsed.
- **collapsed_icon_color** (Color) - Optional - The icon color of tile's expansion arrow icon when the sublist is collapsed.
- **collapsed_shape** (OutlinedBorder) - Optional - The tile's border shape when the sublist is collapsed.
- **collapsed_text_color** (Color) - Optional - The color of the tile's titles when the sublist is collapsed.
- **dense** (bool) - Optional - Whether this list tile is part of a vertically dense list. Dense list tiles default to a smaller height. Defaults to `False`.
- **enable_feedback** (bool) - Optional - Whether detected gestures should provide acoustic and/or haptic feedback. Defaults to `True`.
- **expanded_alignment** (Alignment) - Optional - Defines the alignment of children, which are arranged in a column when the tile is expanded.
- **expanded_cross_axis_alignment** (CrossAxisAlignment) - Optional - Defines the alignment of each child control within `controls` when the tile is expanded. Defaults to `CrossAxisAlignment.CENTER`.
- **icon_color** (Color) - Optional - The icon color of tile's expansion arrow icon when the sublist is expanded.
- **initially_expanded** (bool) - Optional - A boolean value which defines whether the tile is initially expanded or collapsed. Defaults to `False`.
- **leading** (Control) - Optional - A `Control` to display before the title.

### Example

```python
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.spacing = 0
    page.padding = 0

    def handle_expansion_tile_change(e):
        page.open(
            ft.SnackBar(
                ft.Text(
                    f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"
                ),
                duration=1000,
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    page.add(
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 1"),
            subtitle=ft.Text("Trailing expansion arrow icon"),
            bgcolor=ft.Colors.BLUE_GREY_200,
            collapsed_bgcolor=ft.Colors.BLUE_GREY_200,
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.Colors.RED,
            text_color=ft.Colors.RED,
            controls=[
                ft.ListTile(
                    title=ft.Text("This is sub-tile number 1"),
                    bgcolor=ft.Colors.BLUE_GREY_200,
                )
            ],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 2"),
            subtitle=ft.Text("Custom expansion arrow icon"),
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
            collapsed_text_color=ft.Colors.GREEN,
            text_color=ft.Colors.GREEN,
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 3"),
            subtitle=ft.Text("Leading expansion arrow icon"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=True,
            collapsed_text_color=ft.Colors.BLUE_800,
            text_color=ft.Colors.BLUE_200,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        ),
    )

ft.app(main)
```

```

--------------------------------

### NavigationDrawer from Left Edge (Python)

Source: https://flet.dev/docs/controls/navigationdrawer

Demonstrates creating and displaying a Flet NavigationDrawer that slides in from the left edge of the page. It includes handling dismissal and selection changes, and opens via a button click. Dependencies: flet.

```python
import flet as ft


def main(page: ft.Page):

    def handle_dismissal(e):
        print(f"Drawer dismissed!")

    def handle_change(e):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.close(drawer)

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.Icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.Icons.PHONE,
            ),
        ],
    )

    page.add(ft.ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer)))


ft.app(main)

```

--------------------------------

### PieChartSection Properties API

Source: <https://flet.dev/docs/reference/types/piechartsection>

This section details the properties of the PieChartSection class.

```APIDOC
## PieChartSection Properties

This section details the properties of the PieChartSection class.

### Properties

- **value** (float) - Determines how much the section should occupy. This depends on the sum of all sections; each section should occupy (`value` / sum of all values) * 360 degrees.
- **radius** (float) - External radius of the section.
- **color** (Color) - Background color of the section.
- **border_side** (BorderSide) - The border around the section shape. Value is of type `BorderSide`.
- **title** (str) - A title drawn at the center of the section. No title is drawn if `title` is empty.
- **title_style** (TextStyle) - The style to draw `title` with. The value is an instance of `TextStyle` class.
- **title_position** (float) - By default, the title is drawn in the middle of the section, but its position can be changed with `title_position` property, which value must be between 0.0 (near the center) and 1.0 (near the outside of the pie chart).
- **badge** (Control) - An optional `Control` drawn in the middle of a section.
- **badge_position** (float) - By default, the badge is drawn in the middle of the section, but its position can be changed with `badge_position` property, which value must be between 0.0 (near the center) and 1.0 (near the outside of the pie chart).
```

--------------------------------

### Configure PWA Manifest File

Source: <https://flet.dev/docs/publish/web/dynamic-website>

Customize PWA's name, description, and colors by editing the `manifest.json` file located in the root of the `assets` directory. This file controls how the PWA appears to users and its basic metadata. Key properties include `name`, `short_name`, `description`, `theme_color`, and `background_color`.

```json
{
  "name": "My Flet App",
  "short_name": "App",
  "description": "A cool Flet application.",
  "theme_color": "#ffffff",
  "background_color": "#ffffff"
}
```

--------------------------------

### Create BorderRadius with horizontal corners

Source: <https://flet.dev/docs/reference/types/borderradius>

The `ft.border_radius.horizontal(left, right)` method allows setting distinct border radius values for the left and right horizontal corners of a rectangle. The `left` and `right` parameters default to 0 if not provided, meaning no horizontal rounding.

```python
ft.border_radius.horizontal(left=10, right=20)
```

--------------------------------

### WebView Control Documentation

Source: <https://flet.dev/docs/controls/webview>

This section provides detailed information about the WebView control, including its properties, methods, and how to integrate it into your Flet application.

```APIDOC
## WebView Control

Easily load web pages while allowing user interaction within your Flet application.

### Installation

To use the WebView control, add `flet-webview` to your `pyproject.toml` dependencies:

```toml
[project]
...
dependencies = [
  "flet==0.27.6",
  "flet-webview==0.1.0",
]
```

### Example Usage

A simple implementation that loads the flet.dev website:

```python
import flet as ft
import flet_webview as ftwv

def main(page: ft.Page):
    wv = ftwv.WebView(
        url="https://flet.dev",
        on_page_started=lambda _: print("Page started"),
        on_page_ended=lambda _: print("Page ended"),
        on_web_resource_error=lambda e: print("Page error:", e.data),
        expand=True,
    )
    page.add(wv)

ft.app(main)
```

### Properties

- **`bgcolor`** (color) - Sets the background color of the WebView.
- **`enable_javascript`** (bool) - Enables or disables JavaScript execution. Disabling JavaScript may lead to unexpected behavior.
- **`prevent_link`** (str) - Specifies a prefix for links to prevent navigation or downloading.
- **`url`** (str) - The initial URL to load in the WebView.

*Note: `javascript_enabled` is deprecated and `enable_javascript` should be used instead.*

### Methods

- **`can_go_back()`** (bool) - Returns `True` if there is a back history item (Android, iOS, macOS only).
- **`can_go_forward()`** (bool) - Returns `True` if there is a forward history item (Android, iOS, macOS only).
- **`clear_cache()`** - Clears all caches used by the WebView (Android, iOS, macOS only).
- **`clear_local_storage()`** - Clears the local storage used by the WebView (Android, iOS, macOS only).
- **`disable_zoom()`** - Disables zooming controls and gestures (Android, iOS, macOS only).
- **`enable_zoom()`** - Enables zooming controls and gestures (Android, iOS, macOS only).
- **`get_current_url()`** (str | None) - Returns the current URL being displayed or `None` if no URL has been loaded (Android, iOS, macOS only).
- **`get_title()`** (str) - Returns the title of the currently loaded page (Android, iOS, macOS only).
- **`get_user_agent()`** (str) - Gets the value used for the HTTP `User-Agent:` request header (Android, iOS, macOS only).
- **`go_back()`** - Navigates back in the WebView history if `can_go_back()` returns `True` (Android, iOS, macOS only).
- **`go_forward()`** - Navigates forward in the WebView history if `can_go_forward()` returns `True` (Android, iOS, macOS only).
- **`load_file(absolute_path: str)`** - Loads a local file specified by its absolute path (Android, iOS, macOS only).
- **`load_html(html: str, base_url: str | None = None)`** - Loads an HTML string. `base_url` can be provided for resolving relative URLs (Android, iOS, macOS only).
- **`load_request(url: str, method: WebviewRequestMethod = WebviewRequestMethod.GET)`** - Makes an HTTP request and loads the response. `method` specifies the HTTP method (Android, iOS, macOS only).
- **`reload()`** - Reloads the current URL (Android, iOS, macOS only).
- **`run_javascript(value: str)`** - Executes the given JavaScript code in the context of the current page (Android, iOS, macOS only).
- **`scroll_by(x: int, y: int)`** - Scrolls the WebView by the specified number of pixels on the x and y axes (Android, iOS, macOS only).
- **`scroll_to(x: int, y: int)`** - Scrolls the WebView to the specified pixel coordinates (Android, iOS, macOS only).

### Events

- **`on_page_started`** (EventHandler) - Called when the page starts loading.
- **`on_page_ended`** (EventHandler) - Called when the page finishes loading.
- **`on_web_resource_error`** (EventHandler) - Called when a web resource error occurs.

```

--------------------------------

### Flet Column Vertical Alignment Example

Source: https://flet.dev/docs/controls/column

Demonstrates various vertical alignment options for child controls within a Flet Column. It showcases alignments like START, CENTER, END, SPACE_BETWEEN, SPACE_AROUND, and SPACE_EVENLY.

```python
import flet as ft  
  
  
def main(page: ft.Page):  
    def items(count):  
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER_500,  
                )  
            )  
        return items  
  
    def column_with_alignment(align: ft.MainAxisAlignment):  
        return ft.Column(  
            [  
                ft.Text(str(align), size=10),  
                ft.Container(  
                    content=ft.Column(items(3), alignment=align),  
                    bgcolor=ft.Colors.AMBER_100,  
                    height=400,  
                ),  
            ]  
        )  
  
    page.add(  
        ft.Row(  
            [  
                column_with_alignment(ft.MainAxisAlignment.START),  
                column_with_alignment(ft.MainAxisAlignment.CENTER),  
                column_with_alignment(ft.MainAxisAlignment.END),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),  
                column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),  
            ],  
            spacing=30,  
            alignment=ft.MainAxisAlignment.START,  
        )  
    )  
  
  
ft.app(target=main)  


```

--------------------------------

### NavigationDrawer from Right Edge (Python)

Source: <https://flet.dev/docs/controls/navigationdrawer>

Illustrates how to implement a Flet NavigationDrawer that slides in from the right edge of the page using the `position` property. It showcases event handling for dismissal and selection changes. Dependencies: flet.

```python
import flet as ft


def main(page: ft.Page):

    def handle_dismissal(e):
        print("End drawer dismissed")

    def handle_change(e):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.close(end_drawer)

    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT), label="Item 2"
            ),
        ],
    )

    page.add(
        ft.ElevatedButton("Show end drawer", on_click=lambda e: page.open(end_drawer))
    )


ft.app(main)

```

--------------------------------

### Canvas Properties and Events

Source: <https://flet.dev/docs/controls/canvas>

Details on how to configure and interact with the Canvas control, including resize behavior and shape management.

```APIDOC
## Canvas Properties

### `resize_interval`

Sampling interval in milliseconds for `on_resize` event. Defaults to `0` - call `on_resize` immediately on every change.

### `shapes`

The list of `Shape` objects (see below) to draw on the canvas.

## Canvas Events

### `on_resize`

Fires when the size of canvas has changed. Event object `e` is an instance of `CanvasResizeEvent`.
```

--------------------------------

### Open AlertDialog with page.open()

Source: <https://flet.dev/docs/controls/alertdialog>

Demonstrates how to open an AlertDialog by calling the page.open() helper-method. This is the standard way to present dialogs to the user in Flet.

```python
loading...

```

--------------------------------

### Theme Properties

Source: <https://flet.dev/docs/reference/types/theme>

This section details the properties available within the Flet Theme class, allowing for comprehensive customization of the application's appearance.

```APIDOC
## Theme Properties Documentation

### Description
This documentation lists the properties of the `Theme` class in Flet, which controls the visual styling of the application. Each property allows customization of specific UI elements or global theme settings.

### Properties

- **`appbar_theme`** (AppBarTheme) - Defines the theme for the application bar.
- **`badge_theme`** (BadgeTheme) - Defines the theme for badges.
- **`banner_theme`** (BannerTheme) - Defines the theme for banners.
- **`bottom_appbar_theme`** (BottomAppBarTheme) - Defines the theme for the bottom application bar.
- **`bottom_sheet_theme`** (BottomSheetTheme) - Defines the theme for bottom sheets.
- **`button_theme`** (ButtonTheme) - *Deprecated*. Use specific button themes instead.
- **`canvas_color`** (ColorValue) - The color of the canvas.
- **`card_color`** (ColorValue) - The color of cards.
- **`card_theme`** (CardTheme) - Defines the theme for cards.
- **`checkbox_theme`** (CheckboxTheme) - Defines the theme for checkboxes.
- **`chip_theme`** (ChipTheme) - Defines the theme for chips.
- **`color_scheme_seed`** (ColorValue) - A seed color to generate the color scheme.
- **`color_scheme`** (ColorScheme) - The color scheme for the theme.
- **`elevated_button_theme`** (ElevatedButtonTheme) - Defines the theme for elevated buttons.
- **`date_picker_theme`** (DatePickerTheme) - Defines the theme for the date picker.
- **`dialog_bgcolor`** (ColorValue) - The background color of dialogs.
- **`dialog_theme`** (DialogTheme) - Defines the theme for dialogs.
- **`disabled_color`** (ColorValue) - The color for disabled elements.
- **`divider_color`** (ColorValue) - The color of dividers.
- **`divider_theme`** (DividerTheme) - Defines the theme for dividers.
- **`expansion_tile_theme`** (ExpansionTileTheme) - Defines the theme for expansion tiles.
- **`filled_button_theme`** (FilledButtonTheme) - Defines the theme for filled buttons.
- **`focus_color`** (ColorValue) - The color when an element has focus.
- **`font_family`** (string) - The base font family for the UI.
- **`highlight_color`** (ColorValue) - The highlight color.
- **`hint_color`** (ColorValue) - The hint color for text fields etc.
- **`hover_color`** (ColorValue) - The color when hovering over an element.
- **`icon_button_theme`** (IconButtonTheme) - Defines the theme for icon buttons.
- **`indicator_color`** (ColorValue) - The color of the indicator.
- **`list_tile_theme`** (ListTileTheme) - Defines the theme for list tiles.
- **`navigation_bar_theme`** (NavigationBarTheme) - Defines the theme for navigation bars.
- **`navigation_drawer_theme`** (NavigationDrawerTheme) - Defines the theme for navigation drawers.
- **`navigation_rail_theme`** (NavigationRailTheme) - Defines the theme for navigation rails.
- **`outlined_button_theme`** (OutlinedButtonTheme) - Defines the theme for outlined buttons.
- **`page_transitions`** (PageTransitionsTheme) - Defines page transition animations.
- **`primary_text_theme`** (TextTheme) - Text theme for primary color contrast.
- **`popup_menu_theme`** (PopupMenuTheme) - Defines the theme for popup menus.
- **`primary_color`** (ColorValue) - The primary color of the theme.
- **`primary_color_dark`** (ColorValue) - A darker shade of the primary color.
- **`primary_color_light`** (ColorValue) - A lighter shade of the primary color.
- **`primary_swatch`** (ColorValue) - The primary color swatch.
- **`progress_indicator_theme`** (ProgressIndicatorTheme) - Defines the theme for progress indicators.
- **`radio_theme`** (RadioTheme) - Defines the theme for radio buttons.
- **`scaffold_bgcolor`** (ColorValue) - The background color of the scaffold.
- **`scrollbar_theme`** (ScrollbarTheme) - Defines the theme for scrollbars.
- **`search_bar_theme`** (SearchBarTheme) - Defines the theme for search bars.
- **`search_view_theme`** (SearchViewTheme) - Defines the theme for search views.
- **`secondary_header_color`** (ColorValue) - The secondary header color.
- **`segmented_button_theme`** (SegmentedButtonTheme) - Defines the theme for segmented buttons.
- **`shadow_color`** (ColorValue) - The color of shadows.
- **`slider_theme`** (SliderTheme) - Defines the theme for sliders.
- **`snackbar_theme`** (SnackBarTheme) - Defines the theme for snackbars.
- **`splash_color`** (ColorValue) - The splash color.
- **`system_overlay_style`** (SystemOverlayStyle) - Style for system overlays (e.g., status bar).
- **`switch_theme`** (SwitchTheme) - Defines the theme for switches.
- **`tabs_theme`** (TabsTheme) - Defines the theme for tabs.
- **`text_button_theme`** (TextButtonTheme) - Defines the theme for text buttons.
- **`text_theme`** (TextTheme) - Defines text styles contrasting with card/canvas colors.
- **`time_picker_theme`** (TimePickerTheme) - Defines the theme for the time picker.
- **`tooltip_theme`** (TooltipTheme) - Defines the theme for tooltips.
- **`unselected_control_color`** (ColorValue) - The color for unselected controls.
- **`use_material3`** (bool) - Whether to use Material 3 design. Defaults to `True`.
- **`visual_density`** (VisualDensity) - The visual density of the theme.
```

--------------------------------

### Flet VerticalDivider Example

Source: <https://flet.dev/docs/controls/verticaldivider>

Demonstrates how to use the VerticalDivider control in a Flet application to create visual separators within a Row. It showcases different configurations for width and color. This example requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.Container(
                    bgcolor=ft.Colors.ORANGE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    bgcolor=ft.Colors.BROWN_400,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(width=1, color="white"),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.VerticalDivider(width=9, thickness=3),
                ft.Container(
                    bgcolor=ft.Colors.GREEN_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )

ft.app(main)
```

--------------------------------

### TextStyle Properties

Source: <https://flet.dev/docs/reference/types/textstyle>

This section details the properties available for the TextStyle object, allowing for comprehensive text styling.

```APIDOC
## TextStyle Properties

### Description
Provides a comprehensive set of properties to define the visual style of text elements within the Flet framework.

### Properties

#### `baseline`
- **Type**: `TextBaseline`
- **Description**: The common baseline for aligning this text span with its parent or the line box.

#### `bgcolor`
- **Type**: `Color` (or any color type supported by Flet)
- **Description**: Sets the background color of the text.

#### `color`
- **Type**: `Color` (or any color type supported by Flet)
- **Description**: Sets the foreground color of the text.

#### `decoration`
- **Type**: `TextDecoration`
- **Description**: Specifies decorations to be painted near the text, such as underlines.

#### `decoration_color`
- **Type**: `Color` (or any color type supported by Flet)
- **Description**: Defines the color used for painting text decorations.

#### `decoration_style`
- **Type**: `TextDecorationStyle`
- **Default**: `TextDecorationStyle.SOLID`
- **Description**: Sets the style of the text decoration (e.g., dashed, dotted).

#### `decoration_thickness`
- **Type**: `float`
- **Description**: The thickness of the decoration stroke, relative to the font's default thickness.

#### `font_family`
- **Type**: `str`
- **Description**: The name of the font family to use for the text. See `Text.font_family` for more details.

#### `foreground`
- **Type**: `Paint`
- **Description**: A `Paint` object used for drawing the foreground of the text.

#### `height`
- **Type**: `float`
- **Description**: The height of the text span, expressed as a multiple of the font size. See detailed explanation for more information.

#### `italic`
- **Type**: `bool`
- **Description**: If `True`, uses an italic typeface.

#### `letter_spacing`
- **Type**: `float`
- **Description**: Adds space between each letter in logical pixels. Negative values bring letters closer.

#### `overflow`
- **Type**: `TextOverflow`
- **Description**: Specifies how to handle visual text overflow.

#### `shadow`
- **Type**: `BoxShadow` or `list[BoxShadow]`
- **Description**: A single `BoxShadow` instance or a list of `BoxShadow` instances to apply a shadow effect.

#### `size`
- **Type**: `float`
- **Default**: `14`
- **Description**: The font size in logical pixels.

#### `weight`
- **Type**: `FontWeight`
- **Default**: `FontWeight.NORMAL`
- **Description**: The weight (boldness) of the font.

#### `word_spacing`
- **Type**: `float`
- **Description**: Adds space between words in logical pixels. Negative values bring words closer.
```

--------------------------------

### Flet Container Animation Example

Source: <https://flet.dev/docs/reference/types/animationvalue>

Demonstrates how to use ft.Animation to animate a Flet container's properties like width, height, and bgcolor. The animation uses a specified duration and curve. The default animation is linear with 150ms duration if 'animate' is None.

```python
import flet as ft

def main(page: ft.Page):

    c = ft.Container(
        width=200,
        height=200,
        bgcolor="red",
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
    )

    def animate_container(e):
        c.width = 100 if c.width == 200 else 200
        c.height = 100 if c.height == 200 else 200
        c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.update()

    page.add(c, ft.ElevatedButton("Animate container", on_click=animate_container))

ft.app(main)

```

--------------------------------

### Page Properties

Source: <https://flet.dev/docs/controls/page>

Properties that define the appearance and behavior of the Flet page.

```APIDOC
## Page Properties

### `title`

A title of browser or native OS window.

**Example:**
```python
page.title = "My awesome app"
page.update()
```

### `url`

The complete web app's URL.

### `vertical_alignment`

How the child Controls should be placed vertically. Value is of type `MainAxisAlignment` and defaults to `MainAxisAlignment.START`.

### `views`

A list of `View` controls to build navigation history. The last view in the list is the one displayed on a page. The first view is a "root" view which cannot be popped.

### `web`

`True` if the application is running in the web browser.

### `width`

A width of a web page or content area of a native OS window containing Flet app. This property is read-only. It's usually being used inside `page.on_resized` handler.

### `window`

A class with properties/methods/events to control app's native OS window. Value is of type `Window`.

```

--------------------------------

### Flet Multiline TextFields Example

Source: https://flet.dev/docs/controls/textfield

Illustrates the use of multiline TextFields in Flet. This includes standard multiline fields, disabled ones with pre-filled content, and fields that automatically adjust height with a maximum line limit.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(label="standard", multiline=True),
        ft.TextField(
            label="disabled",
            multiline=True,
            disabled=True,
            value="line1\nline2\nline3\nline4\nline5",
        ),
        ft.TextField(
            label="Auto adjusted height with max lines",
            multiline=True,
            min_lines=1,
            max_lines=3,
        ),
    )

ft.app(main)

```

--------------------------------

### Create Static Font Instances from Variable Fonts (Command Line)

Source: <https://flet.dev/docs/cookbook/fonts>

Provides a command-line example using 'fonttools' to create static instances from variable fonts. This is a workaround to use variable fonts in Flet, which currently only supports static fonts. It specifies weight and width parameters for the font mutation.

```bash
fonttools varLib.mutator ./YourVariableFont-VF.ttf wght=140 wdth=85
```

--------------------------------

### Initialize FilePicker Control in Flet App

Source: <https://flet.dev/docs/cookbook/file-picker-and-uploads>

This Python snippet demonstrates how to initialize a FilePicker control and add it to the page's overlay. Adding it to the overlay ensures the control does not affect the app's layout, as it has zero dimensions.

```python
import flet as ft

file_picker = ft.FilePicker()
page.overlay.append(file_picker)
page.update()
```

--------------------------------

### InteractiveViewer Control

Source: <https://flet.dev/docs/controls/interactiveviewer>

Documentation for the InteractiveViewer control, covering its properties, methods, and events.

```APIDOC
## InteractiveViewer

Allows users to pan, zoom, and rotate the provided `content`.

### Properties

- **alignment** (Alignment) - Alignment of the `content` within.
- **bgcolor** (Color) - The background color.
- **boundary_margin** (Margin) - A margin for the visible boundaries of the `content`.
- **clip_behavior** (ClipBehavior) - How to clip the `content`. Defaults to `ClipBehavior.HARD_EDGE`.
- **constrained** (bool) - Whether the normal size constraints at this point in the widget tree are applied to the child.
- **content** (Control) - The `Control` to be transformed by the `InteractiveViewer`.
- **interaction_end_friction_coefficient** (float) - Changes the deceleration behavior after a gesture. Must be greater than `0`. Defaults to `0.0000135`.
- **interaction_update_interval** (int) - The interval (in milliseconds) at which the `on_interaction_update` event is fired. Defaults to `0`.
- **max_scale** (float) - The maximum allowed scale. Must be greater than or equal to `min_scale`. Defaults to `2.5`.
- **min_scale** (float) - The minimum allowed scale. Must be greater than `0` and less than or equal to `max_scale`. Defaults to `0.8`.
- **pan_enabled** (bool) - Whether panning is enabled. Defaults to `True`.
- **scale_enabled** (bool) - Whether scaling is enabled. Defaults to `True`.
- **scale_factor** (float) - The amount of scale to be performed per pointer scroll. Defaults to `200.0`.
- **trackpad_scroll_causes_scale** (bool) - Whether scrolling up/down on a trackpad should cause scaling instead of panning. Defaults to `False`.

### Methods

- **pan(dx, dy)**: Pans the `InteractiveViewer` by a specific amount.
  - `dx` (int): The number of pixels to pan on the x-axis.
  - `dy` (int): The number of pixels to pan on the y-axis.

- **reset(animation_duration=None)**: Resets the `InteractiveViewer` to its initial state.
  - `animation_duration` (DurationValue): Animates the reset with the given duration.

- **restore_state()**: Restores the state of the `InteractiveViewer` previously saved using `save_state`.

- **save_state()**: Saves the current state of the `InteractiveViewer`, which can be restored later using `restore_state`.

- **zoom(factor)**: Zooms in or out to a specific level.
  - `factor` (float): The zoom factor. Values below `1` will zoom out, values above `1` will zoom in.

### Events

- **on_interaction_end**: Fires when the user ends a pan or scale gesture. Event handler argument is of type `InteractiveViewerInteractionEndEvent`.
- **on_interaction_start**: Fires when the user begins a pan or scale gesture. Event handler argument is of type `InteractiveViewerInteractionStartEvent`.
- **on_interaction_update**: Fires when the user updates a pan or scale gesture. Event handler argument is of type `InteractiveViewerInteractionUpdateEvent`.

### Basic Example

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            on_interaction_start=lambda e: print(e),
            on_interaction_end=lambda e: print(e),
            on_interaction_update=lambda e: print(e),
            content=ft.Image(
                src="https://picsum.photos/500/500",
            ),
        )
    )

ft.app(main)
```

```

--------------------------------

### Page Scroll Property

Source: https://flet.dev/docs/controls/page

The `scroll` property enables vertical scrolling for the Page, preventing content overflow. It accepts values from the `ScrollMode` enum.

```APIDOC
## Page Scroll Property

### Description
Enables a vertical scrolling for the Page to prevent its content overflow. Value is of type `ScrollMode`.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    # Add controls that might cause overflow
    for i in range(50):
        page.add(ft.Text(f"Item {i}"))
    page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Flet SearchBar Basic Example

Source: https://flet.dev/docs/controls/searchbar

Demonstrates a basic Flet SearchBar implementation. It includes event handlers for changes, submissions, and taps, along with controls to open and close the search view. Dependencies include the flet library. It takes no explicit input but interacts with user input and page events.

```python
import flet as ft

def main(page):
  
    def close_anchor(e):
        text = f"Color {e.control.data}"
        print(f"closing view from {text}")
        anchor.close_view(text)
  
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")
  
    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")
  
    def handle_tap(e):
        print(f"handle_tap")
        anchor.open_view()
  
    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )
  
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    "Open Search View",
                    on_click=lambda _: anchor.open_view(),
                ),
            ],
        ),
        anchor,
    )

ft.app(main)
```

--------------------------------

### Flet Basic Date Picker Example

Source: <https://flet.dev/docs/controls/datepicker>

Demonstrates how to implement a basic DatePicker in Flet. It shows how to open the date picker dialog, handle date changes, and dismissals. This example utilizes Flet's `page.open()` method to display the dialog.

```python
import datetime  
import flet as ft  
  
  
def main(page: ft.Page):  
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
  
    def handle_change(e):  
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))  
  
    def handle_dismissal(e):  
        page.add(ft.Text(f"DatePicker dismissed"))  
  
    page.add(  
        ft.ElevatedButton(  
            "Pick date",  
            icon=ft.Icons.CALENDAR_MONTH,  
            on_click=lambda e: page.open(  
                ft.DatePicker(  
                    first_date=datetime.datetime(year=2000, month=10, day=1),  
                    last_date=datetime.datetime(year=2025, month=10, day=1),  
                    on_change=handle_change,  
                    on_dismiss=handle_dismissal,  
                )  
            ),  
        )  
    )  
  
  
ft.app(main)  

```

--------------------------------

### Page RTL Property

Source: <https://flet.dev/docs/controls/page>

The `rtl` property controls the text direction for the page. Setting it to `True` enables right-to-left text direction, defaulting to `False` for left-to-right.

```APIDOC
## Page RTL Property

### Description
`True` to set text direction to right-to-left. Defaults to `False`.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
# Enable right-to-left text direction
page.rtl = True
page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### PopupMenuButton API

Source: https://flet.dev/docs/controls/popupmenubutton

The PopupMenuButton is an icon button which displays a menu when clicked. It allows customization of its appearance, content, and behavior.

```APIDOC
## PopupMenuButton

An icon button which displays a menu when clicked.

### Properties

- **bgcolor** (Color) - The menu's background color.
- **clip_behavior** (ClipBehavior) - The `content` will be clipped (or not) according to this option. Defaults to `ClipBehavior.NONE`.
- **content** (Control) - A `Control` that will be displayed instead of "more" icon.
- **elevation** (int) - The menu's elevation when opened. Defaults to `8`.
- **enable_feedback** (bool) - Whether detected gestures should provide acoustic and/or haptic feedback. Defaults to `True`.
- **icon** (Icon) - If provided, an icon to draw on the button.
- **icon_color** (Color) - The `icon`'s color.
- **icon_size** (int) - The `icon`'s size.
- **items** (list[PopupMenuItem]) - A collection of `PopupMenuItem` controls to display in a dropdown menu.
- **menu_position** (PopupMenuPosition) - Defines position of the popup menu relative to the button. Defaults to `PopupMenuPosition.OVER`.
- **padding** (Padding) - Defaults to `padding.all(8.0)`.
- **shadow_color** (Color) - The color used to paint the shadow below the menu.
- **shape** (OutlinedBorder) - The menu's shape. Defaults to `CircleBorder(radius=10.0)`.
- **splash_radius** (int) - The splash radius.
- **surface_tint_color** (Color) - The color used as an overlay on color to indicate elevation.

### Events

- **on_cancel** (function) - Called when the user dismisses/cancels the popup menu without selecting an item.
- **on_open** (function) - Called when the popup menu is shown.

### Request Example

```python
import flet as ft

def main(page: ft.Page):
    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, text="Check power"),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                    ft.Text("Item with a custom content"),
                ]),
                on_click=lambda _: print("Button with custom content clicked!"),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                text="Checked item", checked=False, on_click=check_item_clicked
            ),
        ]
    )
    page.add(pb)

ft.app(main)
```

### Response Example

```json
{
  "message": "PopupMenuButton created successfully"
}
```

```

--------------------------------

### MenuButton Properties

Source: https://flet.dev/docs/controls/submenubutton

Details on the configurable properties of the MenuButton control.

```APIDOC
## MenuButton Properties

### `alignment_offset`

The offset of the menu relative to the alignment origin determined by `MenuStyle.alignment` on the `style` attribute.

### `clip_behavior`

Whether to clip the content of this control or not.
Value is of type `ClipBehavior` and defaults to `ClipBehavior.HARD_EDGE`.

### `content`

The child control to be displayed in the middle portion of this button.
Typically this is the button's label, using a `Text` control.

### `controls`

A list of controls that appear in the menu when it is opened.
Typically either `MenuItemButton` or `SubMenuButton` controls.
If this list is empty, then the button for this menu item will be disabled.

### `leading`

An optional control to display before the `content`.
Typically an `Icon` control.

### `menu_style`

Customizes this menu's appearance.
Value is of type `MenuStyle`.

### `style`

Customizes this button's appearance.
Value is of type `ButtonStyle`.

### `trailing`

An optional control to display after the `content`.
Typically an `Icon` control.
```

--------------------------------

### AppLayout Class for Flet App Layout

Source: <https://flet.dev/docs/tutorials/trello-clone>

Defines the `AppLayout` class, inheriting from `ft.Row`, to structure the application's main layout. It includes a toggle button for the navigation rail, a `Sidebar` component, and an `active_view` area.

```python
import flet as ft
from sidebar import Sidebar


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_LEFT,
            icon_color=ft.Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=ft.Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, page)
        self._active_view: Control = ft.Column(
            controls=[ft.Text("Active View")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view:
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page.update()
```

--------------------------------

### Simple BottomSheet Example in Python

Source: <https://flet.dev/docs/controls/bottomsheet>

This example demonstrates how to create and display a simple modal bottom sheet using Flet. It includes a button to open the bottom sheet and a dismiss button within the sheet. The `on_dismiss` event handler is also shown, which adds a text to the page when the sheet is dismissed. This requires the Flet library.

```python
import flet as ft

def main(page: ft.Page):
    page.title = "BottomSheet example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def bs_dismissed(e):
        page.add(ft.Text("Bottom sheet dismissed"))

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Here is a bottom sheet!"),
                    ft.ElevatedButton("Dismiss", on_click=lambda _: page.close(bs)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=50,
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)
    page.add(
        ft.ElevatedButton("Display bottom sheet", on_click=lambda e: page.open(bs))
    )


ft.app(target=main)

```

--------------------------------

### Instantiate and Add Reusable CalculatorApp Component to Page

Source: <https://flet.dev/docs/tutorials/python-calculator>

Demonstrates how to create multiple instances of a reusable `CalculatorApp` component and add them to the Flet page. This promotes composability and reusability in Flet applications.

```python
# create application instance  
calc1 = CalculatorApp()  
calc2 = CalculatorApp()  
  
# add application's root control to the page  
page.add(calc1, calc2)
```

--------------------------------

### Page PWA Property

Source: <https://flet.dev/docs/controls/page>

The `pwa` property is a boolean indicating whether the application is currently running as a Progressive Web App (PWA). This is a read-only property.

```APIDOC
## Page PWA Property

### Description
`True` if the application is running as Progressive Web App (PWA). Value is read-only.

### Method
Read-only

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
if page.pwa:
    print("Running as PWA")
else:
    print("Not running as PWA")
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Flet Adaptive App Example (Python)

Source: https://flet.dev/docs/getting-started/adaptive-apps

This Python code demonstrates a basic Flet application with adaptive capabilities. By setting `page.adaptive = True`, the app's UI elements, such as the AppBar and NavigationBar, will automatically adjust their appearance based on whether the app is running on iOS or Android. It includes examples of adaptive controls like Checkbox, TextField, Switch, and FilledButton.

```python
import flet as ft  
  
  
def main(page):
  
    page.adaptive = True  
  
    page.appbar = ft.AppBar(  
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),  
        title=ft.Text("Adaptive AppBar"),  
        actions=[
            ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))  
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),  
    )  
  
    page.navigation_bar = ft.NavigationBar(  
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),  
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),  
            ft.NavigationBarDestination(  
                icon=ft.Icons.BOOKMARK_BORDER,  
                selected_icon=ft.Icons.BOOKMARK,  
                label="Bookmark",  
            ),
        ],
        border=ft.Border(  
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)  
        ),  
    )  
  
    page.add(  
        ft.SafeArea(  
            ft.Column(  
                [
                    ft.Checkbox(value=False, label="Dark Mode"),  
                    ft.Text("First field:"),  
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),  
                    ft.Text("Second field:"),  
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),  
                    ft.Switch(label="A switch"),  
                    ft.FilledButton(content=ft.Text("Adaptive button")),  
                    ft.Text("Text line 1"),  
                    ft.Text("Text line 2"),  
                    ft.Text("Text line 3"),  
                ]  
            )  
        )  
    )  
  
  
ft.app(main)  
```

--------------------------------

### TooltipTheme Properties

Source: <https://flet.dev/docs/reference/types/tooltiptheme>

This section details the properties available for customizing the TooltipTheme.

```APIDOC
## TooltipTheme Properties

### Description
Customizes the appearance of `Tooltip` controls across the application.

### Method
N/A (Configuration Class)

### Endpoint
N/A

### Parameters
#### Class Properties
- **enable_feedback** (bool) - Overrides the default value of `Tooltip.enable_feedback`.
- **exclude_from_semantics** (bool) - Overrides the default value of `Tooltip.exclude_from_semantics`.
- **height** (int) - Overrides the default value of `Tooltip.height`.
- **text_style** (TextStyle) - Overrides the default value of `Tooltip.text_style`.
- **prefer_below** (bool) - Overrides the default value of `Tooltip.prefer_below`.
- **vertical_offset** (int) - Overrides the default value of `Tooltip.vertical_offset`.
- **padding** (EdgeInsetsGeometry) - Overrides the default value of `Tooltip.padding`.
- **wait_duration** (int) - Overrides the default value of `Tooltip.wait_duration`.
- **exit_duration** (int) - Overrides the default value of `Tooltip.exit_duration`.
- **show_duration** (int) - Overrides the default value of `Tooltip.show_duration`.
- **margin** (EdgeInsetsGeometry) - Overrides the default value of `Tooltip.margin`.
- **trigger_mode** (TooltipTriggerMode) - Overrides the default value of `Tooltip.trigger_mode`.
- **decoration** (Decoration) - Overrides the default value of `Tooltip.decoration`.

### Request Example
```json
{
  "enable_feedback": true,
  "height": 30,
  "text_style": {
    "color": "blue",
    "font_size": 14
  },
  "prefer_below": false,
  "vertical_offset": 20,
  "padding": {"left": 10, "top": 5, "right": 10, "bottom": 5},
  "wait_duration": 500,
  "exit_duration": 200,
  "show_duration": 1500,
  "margin": {"left": 5, "top": 5, "right": 5, "bottom": 5},
  "trigger_mode": "longpress",
  "decoration": {
    "color": "yellow"
  }
}
```

### Response

#### Success Response (200)

N/A (This is a configuration class, not an API endpoint with direct request/response)

#### Response Example

N/A

```

--------------------------------

### Flet ExpansionTile Control Example in Python

Source: https://flet.dev/docs/controls/expansiontile

This Python code demonstrates how to use the Flet ExpansionTile control to create expandable list items. It shows different configurations for titles, subtitles, background colors, and custom expansion icons. The example also includes an event handler for expansion state changes.

```python
import flet as ft  


def main(page: ft.Page):  
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.spacing = 0  
    page.padding = 0  

    def handle_expansion_tile_change(e):  
        page.open(  
            ft.SnackBar(  
                ft.Text(  
                    f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"  
                ),  
                duration=1000,  
            )  
        )  
        if e.control.trailing:  
            e.control.trailing.name = (  
                ft.Icons.ARROW_DROP_DOWN  
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE  
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE  
            )  
            page.update()  

    page.add(  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 1"),  
            subtitle=ft.Text("Trailing expansion arrow icon"),  
            bgcolor=ft.Colors.BLUE_GREY_200,  
            collapsed_bgcolor=ft.Colors.BLUE_GREY_200,  
            affinity=ft.TileAffinity.PLATFORM,  
            maintain_state=True,  
            collapsed_text_color=ft.Colors.RED,  
            text_color=ft.Colors.RED,  
            controls=[  
                ft.ListTile(  
                    title=ft.Text("This is sub-tile number 1"),  
                    bgcolor=ft.Colors.BLUE_GREY_200,  
                )  
            ],  
        ),  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 2"),  
            subtitle=ft.Text("Custom expansion arrow icon"),  
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),  
            collapsed_text_color=ft.Colors.GREEN,  
            text_color=ft.Colors.GREEN,  
            on_change=handle_expansion_tile_change,  
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],  
        ),  
        ft.ExpansionTile(  
            title=ft.Text("ExpansionTile 3"),  
            subtitle=ft.Text("Leading expansion arrow icon"),  
            affinity=ft.TileAffinity.LEADING,  
            initially_expanded=True,  
            collapsed_text_color=ft.Colors.BLUE_800,  
            text_color=ft.Colors.BLUE_200,  
            controls=[  
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),  
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),  
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),  
            ],  
        ),  
    )  


ft.app(main)  
```

--------------------------------

### Configure Version and Build Number in pyproject.toml

Source: <https://flet.dev/docs/publish>

Sets the application's version number and build number, which are crucial for app store submissions and user identification. The version is a user-facing string (e.g., '1.0.0'), while the build number is an internal integer identifier for releases.

```toml
[project]
name = "my_app"
version = "1.0.0"
description = "My Flet app"
authors = [
  {name = "John Smith", email = "john@email.com"}
]
dependencies = ["flet==0.25.0"]

[tool.flet]
build_number = 1

```

--------------------------------

### MenuItemButton Basic Example

Source: <https://flet.dev/docs/controls/menuitembutton>

A basic example demonstrating the usage of MenuItemButton within a MenuBar to change background colors.

```APIDOC
## Basic Example

### Description
This example shows how to use `MenuItemButton` within a `MenuBar` to allow users to select background colors for a container.

### Method
N/A (UI Component)

### Endpoint
N/A (UI Component)

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Blue"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Green"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Red"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Row([menubar]),
        ft.Container(
            ref=bg_container,
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Text(
                "Choose a bgcolor from the menu",
                style=ft.TextStyle(weight=ft.FontWeight.W_500),
            ),
            alignment=ft.alignment.center,
        ),
    )

ft.app(main)
```

### Response

#### Success Response (200)

N/A (UI Component)

#### Response Example

N/A (UI Component)

```

--------------------------------

### Flet PopupMenuButton Example

Source: https://flet.dev/docs/controls/popupmenubutton

Demonstrates how to create and use a PopupMenuButton in Flet. This example showcases adding different types of PopupMenuItems, including text-only items, items with icons, custom content, and checkable items. It also includes an event handler for click actions.

```python
import flet as ft  


def main(page: ft.Page):  
    def check_item_clicked(e):
        e.control.checked = not e.control.checked  
        page.update()  

    pb = ft.PopupMenuButton(  
        items=[
            ft.PopupMenuItem(text="Item 1"),  
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, text="Check power"),  
            ft.PopupMenuItem(  
                content=ft.Row(  
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),  
                        ft.Text("Item with a custom content"),  
                    ]
                ),  
                on_click=lambda _: print("Button with custom content clicked!"),  
            ),  
            ft.PopupMenuItem(),  # divider  
            ft.PopupMenuItem(  
                text="Checked item", checked=False, on_click=check_item_clicked  
            ),
        ]  
    )
    page.add(pb)


ft.app(main)
```

--------------------------------

### Check Flet Version

Source: <https://flet.dev/docs/getting-started>

Displays the currently installed version of the Flet package. This command is useful for verifying the installation and checking compatibility.

```bash
flet --version
```

--------------------------------

### Scroll to Control Key using Flet

Source: <https://flet.dev/docs/controls/column>

Illustrates scrolling to a specific control within a scrollable Flet container using its unique 'key' property. This requires the control to have a 'key' assigned and is useful for navigating to specific elements on a page. The method supports animation duration.

```python
import flet as ft

def main(page: ft.Page):
    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    def scroll_to_key(e):
        cl.scroll_to(key="20", duration=1000)

    page.add(
        ft.Container(cl, border=ft.border.all(1)),
        ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
    )

ft.app(main)
```

--------------------------------

### Configure Flet Splash Screen Settings (TOML)

Source: <https://flet.dev/docs/publish>

Defines splash screen colors and enables/disables splash screens for different platforms (web, iOS, Android) using `pyproject.toml`. These settings correspond to `--splash-color`, `--splash-dark-color`, `--no-web-splash`, `--no-ios-splash`, and `--no-android-splash` command-line options.

```toml
[tool.flet.splash]
color = "#FFFF00" # --splash-color
dark_color = "#8B8000" # --splash-dark-color
web = false # --no-web-splash
ios = false # --no-ios-splash
android = false # --no-android-splash

```

--------------------------------

### Apply Gaussian Blur to Flet Container

Source: <https://flet.dev/docs/controls/container>

This Python code snippet demonstrates how to apply a Gaussian blur effect to a Flet Container. It shows how to use the `blur` property with a single number for uniform blur, a tuple for distinct horizontal and vertical blur, and a `ft.Blur` object for advanced blur configurations. The example also includes interactive elements to change the background image, illustrating the blur's visual impact.

```python
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    i = 1

    img_container = ft.Container(
        image=ft.DecorationImage(src="https://picsum.photos/250/250"),
        width=250,
        height=250,
    )

    def change_img(e):
        nonlocal i
        print(f"button clicked {i}")
        img_container.image = ft.DecorationImage(
            src=f"https://picsum.photos/250/250?random={i}"
        )
        i += 1
        page.update()

    page.add(
        ft.Stack(
            [
                img_container,
                ft.Container(
                    width=100,
                    height=100,
                    blur=10,
                    bgcolor="#22CCCC00",
                ),
                ft.Container(
                    width=100,
                    height=100,
                    left=20,
                    top=120,
                    blur=(0, 10),
                ),
                ft.Container(
                    top=50,
                    right=10,
                    blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                    width=100,
                    height=100,
                    bgcolor="#44CCCCCC",
                    border_radius=10,
                    border=ft.border.all(2, ft.Colors.BLACK),
                ),
                ft.ElevatedButton(
                    text="Change Background",
                    bottom=5,
                    right=5,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=8)),
                    on_click=change_img,
                ),
            ]
        )
    )

ft.app(main)
```

--------------------------------

### Column Control Properties

Source: <https://flet.dev/docs/controls/column>

Overview of the properties available for the Column control, which define its layout, appearance, and scrolling behavior.

```APIDOC
## Column Control Properties

### `alignment`

How the child Controls should be placed vertically.
Value is of type `MainAxisAlignment`.

### `auto_scroll`

`True` if scrollbar should automatically move its position to the end when children updated. Must be `False` for `scroll_to()` method to work.

### `controls`

A list of Controls to display inside the Column.

### `horizontal_alignment`

How the child Controls should be placed horizontally.
Value is of type `CrossAxisAlignment` and defaults to `CrossAxisAlignment.START`.

### `on_scroll_interval`

Throttling in milliseconds for `on_scroll` event.
Defaults to `10`.

### `rtl`

`True` to set text direction to right-to-left.
Defaults to `False`.

### `run_alignment`

How the runs should be placed in the cross-axis when `wrap=True`.
Value is of type `MainAxisAlignment` and defaults to `MainAxisAlignment.START`.

### `run_spacing`

Spacing between runs when `wrap=True`.
Default value is 10.

### `scroll`

Enables a vertical scrolling for the Column to prevent its content overflow.
Value is of type `ScrollMode` and defaults to `ScrollMode.None`.

### `spacing`

Spacing between the `controls`. It is applied only when `alignment` is set to `MainAxisAlignment.START`, `MainAxisAlignment.END` or `MainAxisAlignment.CENTER`.
Default value is `10` virtual pixels.

### `tight`

Specifies how much space should be occupied vertically.
Defaults to `False` - allocate all space to children.

### `wrap`

When set to `True` the Column will put child controls into additional columns (runs) if they don't fit a single column.
```

--------------------------------

### Flet Padding Examples

Source: <https://flet.dev/docs/reference/types/padding>

Demonstrates various ways to apply padding to Flet containers using the `Padding` class and its helper methods. This includes applying uniform padding, symmetric padding, and padding to specific sides.

```python
container_1.padding = ft.padding.all(10)
container_2.padding = 20
container_3.padding = ft.padding.symmetric(horizontal=10)
container_4.padding=padding.only(left=10)
```

--------------------------------

### Page Theme Property

Source: <https://flet.dev/docs/controls/page>

The `theme` property allows for customization of the application's theme in light mode. Themes can be generated from a 'seed' color, influencing the overall visual appearance.

```APIDOC
## Page Theme Property

### Description
Customizes the theme of the application when in light theme mode. Currently, a theme can only be automatically generated from a "seed" color. For example, to generate light theme from a green color. Value is an instance of the `Theme()` class - more information in the theming guide.

### Method
Read/Write

### Endpoint
N/A

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
import flet as ft

def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN)
    page.add(ft.Text("Styled text", style=ft.TextThemeStyle.BODY_LARGE))
    page.update()
```

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

```

--------------------------------

### Flet SubmenuButton for Menu Interaction

Source: https://flet.dev/docs/controls/submenubutton

This Python script utilizes Flet's SubmenuButton and MenuItemButton to build a user interface with dropdown menus. It allows users to select background colors and text alignments for a central container. The script handles click and hover events to update the UI dynamically. Dependencies include the 'flet' library.

```python
import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_alignment_click(e):
        print("in handle alignment click method")
        print(
            f"bg_container.alignment: {bg_container.alignment}, bg_container.content: {bg_container.content}"
        )
        bg_container.current.alignment = e.control.data
        page.update()
        print(
            f"e.control.content.value: {e.control.content.value}, e.control.data: {e.control.data}"
        )

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    bg_container = ft.Container(
        expand=True,
        bgcolor=ft.Colors.SURFACE,
        content=ft.Text(
            "Choose a bgcolor from the menu",
            style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
        ),
        alignment=ft.alignment.center,
    )
    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Change Body"),
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("BG Color"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Blue"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Green"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Red"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                        ],
                    ),
                    ft.SubmenuButton(
                        content=ft.Text("Text alignment"),
                        leading=ft.Icon(ft.Icons.LOCATION_PIN),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("bottom_center"),
                                data=ft.alignment.bottom_center,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREY_100
                                    }
                                ),
                                on_click=handle_alignment_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("bottom_left"),
                                data=ft.alignment.bottom_left,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREY_100
                                    }
                                ),
                                on_click=handle_alignment_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("top_center"),
                                data=ft.alignment.top_center,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREY_100
                                    }
                                ),

```

--------------------------------

### Announce Tooltip with SemanticsService

Source: <https://flet.dev/docs/controls/semanticsservice>

Sends a semantic announcement for a tooltip, currently supported on Android. This feature allows screen readers like TalkBack to read the tooltip message to the user, improving usability for visually impaired users.

```python
import flet as ft

def main(page: ft.Page):
    # Example usage of announce_tooltip
    # page.semantics_service.announce_tooltip("This is a helpful tooltip.")
    pass

ft.app(target=main)
```

--------------------------------

### Set and Test Platform in Flet Application

Source: <https://flet.dev/docs/controls/page>

Shows how to programmatically set the Flet page's platform property for testing purposes. It includes functions to switch the platform to Android or iOS and print the current platform value.

```python
import flet as ft

def main(page):
    def set_android(e):
        page.platform = ft.PagePlatform.ANDROID
        page.update()
        print("New platform:", page.platform)

    def set_ios(e):
        page.platform = "ios"
        page.update()
        print("New platform:", page.platform)

    page.add(
        ft.Switch(label="Switch A", adaptive=True),
        ft.ElevatedButton("Set Android", on_click=set_android),
        ft.ElevatedButton("Set iOS", on_click=set_ios),
    )

    print("Default platform:", page.platform)

ft.app(main)
```

--------------------------------

### Flet PermissionHandler Basic Example

Source: <https://flet.dev/docs/controls/permissionhandler>

This Python code demonstrates the basic usage of the PermissionHandler control in Flet. It shows how to initialize the control, add it to the page overlay, and implement functions to check, request, and open app settings for microphone permissions. The example utilizes Flet's UI elements like OutlinedButton and Text to display the status and results of permission operations.

```python
import flet as ft

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("PermissionHandler Tests"))
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    def check_permission(e):
        o = ph.check_permission(e.control.data)
        page.add(ft.Text(f"Checked {e.control.data.name}: {o}"))

    def request_permission(e):
        o = ph.request_permission(e.control.data)
        page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))

    def open_app_settings(e):
        o = ph.open_app_settings()
        page.add(ft.Text(f"App Settings: {o}"))

    page.add(
        ft.OutlinedButton(
            "Check Microphone Permission",
            data=ft.PermissionType.MICROPHONE,
            on_click=check_permission,
        ),
        ft.OutlinedButton(
            "Request Microphone Permission",
            data=ft.PermissionType.MICROPHONE,
            on_click=request_permission,
        ),
        ft.OutlinedButton(
            "Open App Settings",
            on_click=open_app_settings,
        ),
    )

ft.app(main)

```

--------------------------------

### Flet Row: Demonstrate Horizontal Alignment Options

Source: <https://flet.dev/docs/controls/row>

Illustrates various horizontal alignment options for Flet Row controls, including START, CENTER, END, SPACE_BETWEEN, SPACE_AROUND, and SPACE_EVENLY. Each alignment is demonstrated within a container showing the effect on child items. This requires the 'flet' library.

```python
import flet as ft  

def main(page: ft.Page):  
    page.scroll = ft.ScrollMode.AUTO  

    def items(count):  
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER_500,  
                )  
            )  
        return items  

    def row_with_alignment(align: ft.MainAxisAlignment):  
        return ft.Column(  
            [  
                ft.Text(str(align), size=16),  
                ft.Container(  
                    content=ft.Row(items(3), alignment=align),  
                    bgcolor=ft.Colors.AMBER_100,  
                ),  
            ],  
        )  

    page.add(  
        ft.Column(  
            [  
                row_with_alignment(ft.MainAxisAlignment.START),  
                row_with_alignment(ft.MainAxisAlignment.CENTER),  
                row_with_alignment(ft.MainAxisAlignment.END),  
                row_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),  
                row_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),  
                row_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),  
            ],  
            scroll=ft.ScrollMode.AUTO,  
        )  
    )  


ft.app(main)  
```

--------------------------------

### Configure Manifest Application Element Properties in pyproject.toml

Source: <https://flet.dev/docs/publish/android>

Adds custom properties to the `<application>` element in `AndroidManifest.xml` for Flet Android builds. These are configured in `pyproject.toml` under `[tool.flet.android.manifest_application]`.

```toml
[tool.flet.android.manifest_application]
usesCleartextTraffic = "true"
requestLegacyExternalStorage = "true"

```

--------------------------------

### Set Clipboard Content

Source: <https://flet.dev/docs/controls/page>

Sets the text content of the client's clipboard (web browser or desktop). This allows the Flet application to copy data to the user's clipboard.

```python
page.set_clipboard("This value comes from Flet app")
```

--------------------------------

### Flet Row: Control Spacing Between Items

Source: <https://flet.dev/docs/controls/row>

Demonstrates how to control the spacing between child controls within a Flet Row. It uses a Slider to dynamically adjust the `spacing` property of the Row, affecting the horizontal gap between items. This requires the 'flet' library.

```python
import flet as ft  

def main(page: ft.Page):  
    def items(count):
        items = []  
        for i in range(1, count + 1):  
            items.append(  
                ft.Container(  
                    content=ft.Text(value=str(i)),  
                    alignment=ft.alignment.center,  
                    width=50,  
                    height=50,  
                    bgcolor=ft.Colors.AMBER,  
                    border_radius=ft.border_radius.all(5),  
                )  
            )  
        return items  

    def gap_slider_change(e):  
        row.spacing = int(e.control.value)  
        row.update()  

    gap_slider = ft.Slider(  
        min=0,  
        max=50,  
        divisions=50,  
        value=0,  
        label="{value}",  
        on_change=gap_slider_change,  
    )  

    row = ft.Row(spacing=0, controls=items(10), scroll=ft.ScrollMode.AUTO)  

    page.add(ft.Column([ft.Text("Spacing between items"), gap_slider]), row)  


ft.app(main)  
```

--------------------------------

### Implement Adaptive Navigation Bar with Custom Destinations (Python)

Source: <https://flet.dev/docs/getting-started/adaptive-apps>

Demonstrates how to use the custom `AdaptiveNavigationBarDestination` control within a Flet `NavigationBar`. The `main` function sets up the page's `adaptive` property to `True` and configures the `NavigationBar` with multiple destinations, each using the custom control with platform-specific icons. This results in a UI that adapts icons based on the operating system.

```python
import flet as ft
from adaptive_navigation_destination import AdaptiveNavigationBarDestination

def main(page):

    page.adaptive = True

    page.navigation_bar = ft.NavigationBar(
        selected_index=2,
        destinations=[
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.PERSON_3_FILL,
                android_icon=ft.Icons.PERSON,
                label="Contacts",
            ),
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.CHAT_BUBBLE_2,
                android_icon=ft.Icons.CHAT,
                label="Chats",
            ),
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.SETTINGS,
                android_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
    )

    page.update()


ft.app(main)

```
