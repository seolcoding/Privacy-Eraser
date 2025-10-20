### PySide6 Application Entry Point (`main.py`)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/systray/README.md

Describes the initialization process of the PySide6 application, including QApplication setup, system tray availability checks, crucial application settings like `setQuitOnLastWindowClosed(False)`, and starting the event loop.

```APIDOC
main.py:
  - Initializes QApplication.
  - Checks for System Tray Availability:
    - Uses QSystemTrayIcon.isSystemTrayAvailable().
    - If not available, shows critical message and exits.
  - Crucial Application Setting:
    - Calls QApplication.setQuitOnLastWindowClosed(False) to prevent termination when the main window is closed, allowing it to continue running with only the system tray icon visible.
  - Creates an instance of the Window class, shows it, and starts the event loop.
```

--------------------------------

### Run PySide6 Basic Layouts Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/basiclayouts/README.md

Instructions to execute the PySide6 application demonstrating various layout managers. Ensure PySide6 is installed and navigate to the example directory before running the script.

```Bash
python basiclayouts.py
```

--------------------------------

### PySide6 Main Application Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Describes the setup in `main.py`, including enabling Qt Speech debug logging, initializing `QApplication`, and showing the `MainWindow`.

```APIDOC
main.py:
  - QLoggingCategory.setFilterRules("qt.speech.tts=true\nqt.speech.tts.*=true")
    - Enables detailed debug output from the Qt Speech module
  - Initializes QApplication
  - Creates and shows the MainWindow instance
```

--------------------------------

### Execute PySide6 Anchor Layout Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/anchorlayout/README.md

Instructions to run the PySide6 anchor layout example script from the command line, assuming PySide6 is installed and the current directory is `examples/widgets/graphicsview/anchorlayout`.

```Bash
python anchorlayout.py
```

--------------------------------

### Execute PySide6 Drag and Drop Example Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/draganddrop/dropsite/README.md

Command-line instructions to run the provided PySide6 drag and drop example application. Ensure PySide6 is installed and navigate to the specified directory before execution.

```Bash
python main.py
```

--------------------------------

### Main Application Initialization (Python)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Describes the entry point of the application, detailing the setup of the QApplication and the main Camera window, initiating the application's event loop.

```APIDOC
main.py:
  - Initializes QApplication.
  - Creates an instance of the Camera main window.
  - Shows the window and starts the event loop.
```

--------------------------------

### Run PySide6 Text Editor Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/richtext/textedit/README.md

Instructions to execute the PySide6 rich text editor example from the command line. Ensure PySide6 and its `QtPrintSupport` module are installed. The example can be run without arguments to load a default HTML file, or with a file path to open a specific document.

```bash
python textedit.py
```

```bash
python textedit.py your_document.html
```

--------------------------------

### Run PySide6 QML Extension Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/extended/README.md

Instructions to execute the PySide6 QML extension example. This involves ensuring PySide6 is installed, navigating to the specific example directory, and running the main Python script from the command line.

```Bash
python main.py
```

--------------------------------

### Execute PySide6 Fetch More Example Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/fetchmore/README.md

This command initiates the PySide6 'Fetch More' example application. Ensure PySide6 is installed and you are in the correct directory before execution. The script will open a window demonstrating incremental data loading.

```Bash
python fetchmore.py
```

--------------------------------

### PySide6 MainWindow Initialization with QTextToSpeech

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Describes the initialization process of the `MainWindow` class, including UI setup, creation of the `QTextToSpeech` instance, population of available engines, and connection of UI signals to slots.

```APIDOC
MainWindow:
  __init__():
    - UI setup from ui_mainwindow.py
    - self._speech = QTextToSpeech() (initial instance, defaults to system engine)
    - Populate _ui.engine QComboBox:
      - Add "Default"
      - Add all QTextToSpeech.availableEngines()
      - Select first engine (triggers engine_selected slot)
    - Connect UI controls:
      - Sliders (rate, pitch, volume) to respective set_X slots
      - ComboBox currentIndexChanged signals
      - Button clicked signals
```

--------------------------------

### Main Application Logic API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/contextinfo/README.md

Outlines the entry point and setup for the PySide6 OpenGL application, including command-line argument parsing for OpenGL implementation and the application lifecycle.

```APIDOC
Main Application Logic (if __name__ == "__main__"):
  - Description: Initializes and runs the PySide6 application.
  - Details: Uses ArgumentParser to allow specifying OpenGL implementation (GLES, Software, Desktop) via command-line flags. These are set using QCoreApplication.setAttribute(). Creates QApplication. Creates and shows an instance of MainWindow. Calls main_window.update_description() to populate the info text edit *after* the window (and thus the OpenGL context) is likely initialized and shown. Starts the event loop.
```

--------------------------------

### Run PySide6 Diagramscene Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/diagramscene/README.md

Instructions on how to execute the PySide6 diagramscene example application from the command line. Ensure PySide6 is installed and navigate to the specified directory before running the script.

```Bash
python diagramscene.py
```

--------------------------------

### Camera Class Initialization (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Details the initial setup of the Camera window, including UI loading, handling camera and microphone permission requests for specific operating systems, creating audio input, and populating available video input devices.

```APIDOC
Camera Class Methods:
  __init__ / initialize:
    - Loads UI from .ui file.
    - Handles camera and microphone permission requests (Android/macOS).
    - Creates QAudioInput (m_audioInput).
    - Populates menu with available video input devices (QMediaDevices.videoInputs()) using QActionGroup.
    - Calls setCamera() with default video input.
```

--------------------------------

### PySide6 Python Modules for Application Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/intro/README.md

This section lists the key PySide6 modules and classes used in the `main.py` file. These components are essential for initializing the GUI application, configuring the OpenGL surface format for 3D rendering, and loading the QML engine.

```APIDOC
PySide6.QtGui.QGuiApplication
PySide6.QtGui.QSurfaceFormat (Used to set default surface format properties like multisampling)
PySide6.QtQml.QQmlApplicationEngine
PySide6.QtQuick3D.QQuick3D (Used for idealSurfaceFormat())
```

--------------------------------

### Run PySide6 Dock Widgets Example Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/mainwindows/dockwidgets/README.md

This command executes the `dockwidgets.py` script, launching the PySide6 application that demonstrates `QDockWidget` functionality. Before running, ensure PySide6 (including `PySide6.QtPrintSupport`) is installed and you are in the `examples/widgets/mainwindows/dockwidgets` directory.

```bash
python dockwidgets.py
```

--------------------------------

### Running the PySide6 QML Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter2-methods/README.md

Instructions to navigate to the example directory and execute the Python script to run the PySide6 QML application. This command starts the application demonstrating QML-Python interaction.

```Bash
python methods.py
```

--------------------------------

### Build and Install PySide/Shiboken Example with CMake (MSBuild)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/doc/samplebinding.rst

Command to build and install the PySide/Shiboken example using CMake's build command, targeting the 'install' target with the 'Release' configuration. This method is suitable when a Visual Studio generator has been configured, providing an alternative to Ninja.

```bash
cmake --build . --target install --config Release
```

--------------------------------

### APIDOC: Python Application Runner (main.py)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Documentation for the `main.py` script, which serves as the entry point for the PySide6 application. It outlines the standard setup for initializing the QML engine and loading the main QML component.

```APIDOC
main.py (Python Script)
  Purpose: Application Entry Point

  Steps:
    1. Initialize QApplication.
    2. Initialize QQmlApplicationEngine.
    3. Add import path for Python modules (e.g., for "Finance" module).
    4. Load Finance/Main.qml from the "Finance" QML module (defined in Finance/qmldir).
    5. Start the QApplication event loop.
```

--------------------------------

### Run PySide6 Dir View Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/dirview/README.md

Execute the Python script to open the file system viewer, starting from the default directory (usually home or root).

```Bash
python dirview.py
```

--------------------------------

### Python Application Runner (main.py) - Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quickcontrols/filesystemexplorer/README.md

Describes the setup process for the PySide6/QML application, including initialization of the application engine, setting metadata, and configuring QML module paths.

```APIDOC
main.py (Application Runner):
  1. Initializes QGuiApplication and QQmlApplicationEngine.
  2. Sets application metadata (name, version, icon).
  3. QML Module Path Configuration:
     - engine.addImportPath(sys.path[0]): Adds the current directory to QML import paths, allowing QML to find 'FileSystemModule' and registered Python types.
  4. Loading Main QML:
     - engine.loadFromModule("FileSystemModule", "Main"): Loads the root QML file 'Main.qml' from the 'FileSystemModule'.
  5. Command-Line Argument Handling:
     - Optionally takes a path as a command-line argument to set the initial directory for the 'FileSystemModel' singleton after QML engine loads.
```

--------------------------------

### FastAPI Backend Server Startup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Initializes the database and starts the FastAPI application server using Uvicorn. The server typically listens on `http://127.0.0.1:8000`, making the API accessible to clients.

```Python
# In Backend/main.py
from .database import initialize_database
import uvicorn

if __name__ == "__main__":
    initialize_database()
    uvicorn.run("rest_api:app", host="127.0.0.1", port=8000, reload=True)
```

--------------------------------

### Start QStateMachine and Main Application Loop (PySide6)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/animation/states/README.md

Describes the final steps for initiating the QStateMachine and the overall application flow. It covers starting the machine, the immediate application of initial state properties, and how animations execute during transitions. It also outlines the standard PySide6 application setup, including QApplication, QGraphicsView, and the event loop.

```APIDOC
Starting the State Machine and Main Application:
  - machine.start():
    - Machine enters state1.
    - Properties assigned by state1 are applied (initial conditions, no animation occurs *into* the very first state).
  - On button click (e.g., t1 fires):
    - state2 becomes target.
    - Animations added to t1 run, interpolating properties from state1 values to state2 values.
  - Main Application Flow:
    - Create QApplication instance.
    - Set up QGraphicsScene with all items and proxies.
    - Create and configure QStateMachine.
    - Create QGraphicsView, set the scene, and show the view.
    - Start the event loop (app.exec()).
```

--------------------------------

### Build PySide/Shiboken Example with Ninja

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/doc/samplebinding.rst

Commands to build and install the configured PySide/Shiboken example using the Ninja build system after CMake configuration.

```bash
ninja
ninja install
cd ..
```

--------------------------------

### Python Application Entry Point: main.py

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webenginewidgets/simplebrowser/README.md

Describes the initialization and setup process of the PySide6 browser application, including QApplication setup, default QWebEngineSettings, and initial window creation.

```APIDOC
main.py (Application Entry Point):
  - Initializes QApplication.
  - Sets default QWebEngineSettings on QWebEngineProfile.defaultProfile() (e.g., enabling plugins, DNS prefetch, screen capture).
  - Creates an instance of Browser (the application-level manager).
  - Calls browser.create_hidden_window() to get the first BrowserWindow.
  - Loads an initial URL (from command-line argument or a default like "chrome://qt") into the first tab of this window.
  - Shows the window.
```

--------------------------------

### Run PySide6 Dir View Example with Custom Path and Options

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/dirview/README.md

Execute the Python script, specifying a starting directory and optional flags to disable custom icons and file system change watching.

```Bash
python dirview.py /path/to/your/directory

# Start in the current directory, disable custom icons, and disable watching for changes
python dirview.py . -c -w
```

--------------------------------

### Run PySide6 Example Application via Command Line

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/mainwindows/application/README.md

Instructions for executing the PySide6 example application from the terminal. This includes the basic command to launch the application and an option to open a specified file upon startup.

```bash
python application.py
```

```bash
python application.py yourfile.txt
```

--------------------------------

### Execute PySide6 Lighting Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/effects/lighting/README.md

This command runs the `lighting.py` script, which launches a PySide6 application demonstrating dynamic 2D lighting and shadow effects. Ensure PySide6 is installed and you are in the correct directory.

```bash
python lighting.py
```

--------------------------------

### Run PySide6 QML List Property Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter5-listproperties/README.md

This command executes the Python script `listproperties.py`, which initializes the QML application demonstrating the `ListProperty` functionality. Ensure PySide6 is installed and the current directory is `examples/qml/tutorials/extending-qml/chapter5-listproperties`.

```Bash
python listproperties.py
```

--------------------------------

### Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointconfiguration/doc/pointconfiguration.rst

The main entry point for the application. It initializes the `QApplication`, creates an instance of `ChartWindow`, sets its size, makes it visible, and starts the Qt event loop.

```python
import sys
from PySide6.QtWidgets import QApplication
from chartwindow import ChartWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
```

--------------------------------

### Run PySide6 String List Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick/models/stringlistmodel/README.md

Instructions to navigate to the example directory and execute the Python script to run the application.

```Bash
python stringlistmodel.py
```

--------------------------------

### PySide6 Main Application Execution Flow

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/spatialaudio/audiopanning/README.md

API documentation for the main entry point of the PySide6 application, detailing the standard setup procedures including QApplication initialization, metadata configuration, command-line argument parsing for initial file loading, and the start of the Qt event loop.

```APIDOC
if __name__ == '__main__':
  - QApplication: Initializes the Qt application instance
  - Application Metadata: Sets name and version
  - Command-line Arguments: Parses for initial audio file path
  - AudioWidget: Creates and displays an instance
  - Initial File Setting: If provided via command line, sets it on AudioWidget
  - Qt Event Loop: Starts the application's event loop (app.exec())
```

--------------------------------

### Run PySide6 Address Book Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/address_book/README.md

Instructions to execute the main Python script for the PySide6 Address Book application from the command line. Ensure PySide6 is installed and navigate to the correct directory before running the command.

```Bash
python address_book.py
```

--------------------------------

### Execute PySide6 Basic Sort/Filter Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/basicfiltermodel/README.md

This command executes the `basicsortfiltermodel.py` script, launching the PySide6 example application. It requires PySide6 to be installed and the current directory to be `examples/widgets/itemviews/basicfiltermodel` for successful execution.

```Bash
python basicsortfiltermodel.py
```

--------------------------------

### Run PySide6 JSON Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/jsonmodel/README.md

Instructions to execute the PySide6 JSON model application from the command line. Ensure PySide6 is installed and navigate to the correct directory before running.

```Bash
python jsonmodel.py
```

--------------------------------

### Run PySide6 Widget Gallery Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgetsgallery/README.md

Executes the `main.py` script to launch the PySide6 Widget Gallery application, demonstrating various Qt widgets and their interactive features.

```bash
python main.py
```

--------------------------------

### Execute PySide6 Concentric Circles Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/painting/concentriccircles/README.md

This command runs the Python script for the concentric circles example. Before execution, ensure PySide6 is installed and the current working directory is 'examples/widgets/painting/concentriccircles'.

```Bash
python concentriccircles.py
```

--------------------------------

### Building Scriptable Application with QMake

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/scriptableapplication/doc/scriptableapplication.rst

Commands to build the scriptable application example using QMake. This involves creating a build directory, running qmake to generate Makefiles, and then compiling the project using make (or nmake/jom on Windows).

```bash
mkdir build
cd build
qmake ..
make # or nmake / jom for Windows
```

--------------------------------

### Main Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/player/README.md

Illustrates the standard PySide6 application setup, including QApplication initialization, MainWindow instantiation, and entering the event loop.

```Python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QSlider, QFileDialog
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaFormat
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QIcon, QKeySequence

# Assuming MainWindow class definition is available (e.g., in this file or imported)
# class MainWindow(QMainWindow):
#   ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(800, 600) # Example size
    main_window.show()
    sys.exit(app.exec())
```

--------------------------------

### Execute PySide6 Thread Signals Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/thread_signals/README.md

Instructions to run the PySide6 `thread_signals.py` example script from the command line. This command starts the application, which demonstrates background processing with thread signals.

```Bash
python thread_signals.py
```

--------------------------------

### Running PySide6 QML Method Example and Output

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/methods/README.md

Provides instructions on how to execute the PySide6 QML example from the command line and shows the expected console output, demonstrating the successful invocation of the Python `invite` method from QML and its effect on the guest list.

```bash
python main.py
```

```plaintext
Bob Jones is having a birthday!
They are inviting:
    Leo Hodges
    Jack Smith
    Anne Brown
    William Green
```

--------------------------------

### PySide6 Main Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/draganddrop/dropsite/README.md

Documentation for the `main.py` script, which serves as the entry point for the PySide6 application. It initializes the `QApplication` and displays the `DropSiteWindow`.

```APIDOC
Script: main.py
  Purpose: Initializes the QApplication and displays the main application window.

  Actions:
    - Initializes QApplication.
    - Creates an instance of DropSiteWindow.
    - Shows the DropSiteWindow.
    - Starts the application event loop.
```

--------------------------------

### Run PySide6 Regular Expression Example Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/tools/regularexpression/README.md

Execute the main Python script to launch the PySide6 regular expression example application from the command line. Ensure PySide6 is installed and you are in the correct directory.

```Bash
python regularexpression.py
```

--------------------------------

### Python Application Runner Setup (main.py)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/proceduraltexture/README.md

Describes the setup process for the PySide6 application, including initialization of the Qt application and QML engine, adding import paths, and loading the main QML file from a module.

```APIDOC
main.py (Application Runner):
  1. Initializes QGuiApplication.
  2. Initializes QQmlApplicationEngine.
  3. Adds application directory to QML import path:
     engine.addImportPath(os.fspath(app_dir))
  4. Loads main QML file from QML module:
     engine.loadFromModule("ProceduralTextureModule", "Main")
```

--------------------------------

### Run PySide6 QML-Python Signal Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/signals/qmltopy3/README.md

Execute the main Python script from the command line to launch the application. This command starts the PySide6 application, demonstrating the QML-to-Python signal handling in action.

```Bash
python main.py
```

--------------------------------

### Run PySide6 Character Map Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgets/charactermap/README.md

Instructions to navigate to the example directory and execute the main Python script to launch the PySide6 Character Map application.

```Bash
python main.py
```

--------------------------------

### Run PySide6 PDF Viewer Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/pdfwidgets/pdfviewer/README.md

This command executes the PySide6 PDF viewer application. Optionally, a path to a PDF file can be provided as a command-line argument to open it directly on startup. If no path is provided, the application will start with a blank view, allowing users to open a file via the 'Open' action.

```bash
python main.py [path_to_pdf_file.pdf]
```

--------------------------------

### APIDOC: PySide6 QTableView Main Application Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/spinboxdelegate/README.md

Documentation for setting up the main application, including model and view creation, and assigning the custom SpinBoxDelegate to the QTableView.

```APIDOC
Main Application Setup:
  Model: QStandardItemModel (4 rows, 2 columns)
    Populated with sample integer values.
  View: QTableView
    Model set: tableView.setModel(QStandardItemModel)
  Delegate Assignment:
    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)
```

--------------------------------

### Run PySide6 Elastic Nodes Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/elasticnodes/README.md

Instructions on how to execute the PySide6 elastic nodes example from the command line. This requires PySide6 to be installed and navigating to the correct directory where the 'elasticnodes.py' script resides.

```Bash
python elasticnodes.py
```

--------------------------------

### Run PySide6 QML Default Property Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced3-Default-properties/README.md

This command demonstrates how to execute the Python script to run the PySide6 QML example. It assumes PySide6 is installed and the current directory is `examples/qml/tutorials/extending-qml-advanced/advanced3-Default-properties`.

```bash
python main.py
```

--------------------------------

### Build and Install WigglyWidget C++ Binding with Ninja

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgetbinding/doc/widgetbinding.md

Commands to compile the C++ binding project using the Ninja build system and then install the generated shared libraries, making them accessible for the Python application to import.

```bash
ninja
ninja install
cd ..
```

--------------------------------

### Run PySide6 Star Delegate Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/stardelegate/README.md

Instructions on how to execute the PySide6 star delegate example script from the command line.

```Bash
python stardelegate.py
```

--------------------------------

### Main Application Execution Flow

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/network/blockingfortuneclient/README.md

Describes the entry point of the application, initializing the QApplication, creating the BlockingClient instance, showing the window, and starting the Qt event loop.

```APIDOC
Main Application Execution (if __name__ == "__main__"):
  - Creates QApplication.
  - Creates an instance of BlockingClient.
  - Shows the client window.
  - Starts the Qt event loop.
```

--------------------------------

### Python Backend Initialization with QWebChannel and WebSockets

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webchannel/standalone/README.md

Demonstrates the core setup of the Python backend using PySide6, including QApplication, QWebSocketServer, WebSocketClientWrapper, and QWebChannel to expose a Core object to JavaScript clients. It shows how the server is started, connections are managed, and the Core object is registered.

```Python
# main.py setup
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtNetwork import QHostAddress
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QDesktopServices
# Assuming WebSocketClientWrapper and Core are defined elsewhere

app = QApplication([])
server = QWebSocketServer("MyWebSocketServer", QWebSocketServer.NonSecureMode)
server.listen(QHostAddress.LocalHost, 12345)

client_wrapper = WebSocketClientWrapper(server)
channel = QWebChannel()

# Connect new client connections to the QWebChannel
client_wrapper.client_connected.connect(channel.connectTo)

# Create and register the Core object
core = Core(dialog) # 'dialog' would be an instance of your GUI
channel.registerObject("core", core)

# Launch the HTML frontend
QDesktopServices.openUrl("file:///path/to/index.html")

app.exec()
```

--------------------------------

### PySide6: Main Application Flow for JSON Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/jsonmodel/README.md

This section outlines the main application setup, demonstrating how to initialize the QApplication and QTreeView, instantiate and integrate the custom JsonModel, load JSON data, and customize the view's appearance.

```APIDOC
Main Application Flow (jsonmodel.py's if __name__ == "__main__":):
  Steps:
    1. Create QApplication instance.
    2. Create QTreeView instance.
    3. Instantiate JsonModel.
    4. Set JsonModel on QTreeView using setModel().
    5. Load JSON data from 'example.json' using Python's standard json module (json.load()).
    6. Pass the loaded Python dictionary/list to model.load().
    7. Customize QTreeView appearance (e.g., setHeaderData, setAlternatingRowColors).
    8. Show the QTreeView.
    9. Start the QApplication event loop.
```

--------------------------------

### Run PySide6 QML Binding Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter3-bindings/README.md

This command executes the Python script that launches the PySide6 QML application demonstrating property bindings. Ensure PySide6 is installed and you are in the correct directory before running.

```Bash
python bindings.py
```

--------------------------------

### PySide6 Main Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/dialogs/licensewizard/README.md

Describes the main application setup, including QApplication instantiation, wizard creation, display, and event loop initiation, which launches the PySide6 wizard.

```APIDOC
Main Application (main.py):
  - Creates QApplication instance.
  - Creates an instance of LicenseWizard.
  - Shows the wizard using wizard.show().
  - Starts the event loop.
```

--------------------------------

### PySide6 Server Class Initialization and UI Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/network/fortuneserver/README.md

Details the `Server` class constructor, including UI element setup, fortune string storage, `QTcpServer` initialization, listening on an available port, and connecting the `newConnection` signal.

```APIDOC
Server class (subclass of QDialog):
  __init__():
    Purpose: Initializes the server application, sets up the UI, stores fortunes, and starts the TCP server.
    UI Setup:
      - status_label (QLabel): Displays IP address(es) and port.
      - Quit QPushButton: Closes the application.
      - Layouts: Basic Qt layouts.
    Fortune Storage:
      - self.fortunes (tuple): Predefined fortune strings.
    Server Initialization:
      - self._tcp_server (QTcpServer): Instance for handling TCP connections.
      - Start Listening:
        - Method: self._tcp_server.listen() (listens on QHostAddress.Any, OS picks port).
        - Error Handling: QMessageBox.critical on failure.
        - Port Retrieval: self._tcp_server.serverPort().
        - Status Update: status_label updated with IP/port.
      - Signal Connection:
        - Signal: self._tcp_server.newConnection
        - Slot: self.send_fortune
```

--------------------------------

### PySide6 QTreeView Basic Setup and Data Population

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/tutorials/modelview/README.md

This snippet shows basic operations for populating a QStandardItemModel and setting it on a QTreeView, followed by expanding all nodes. It demonstrates initial data setup for a tree view.

```Python
# america_item.appendRow(QStandardItem("Canada"))
#
# self._tree_view.setModel(self._standard_model)
# self._tree_view.expandAll()
```

--------------------------------

### PySide6 Application Initialization

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/part1/README.md

Standard PySide6 application setup in `main.py`, initializing `QApplication` and `QQmlApplicationEngine`, adding import paths, and loading the main QML file.

```Python
import sys
from pathlib import Path
from PySide6.QtGui import QApplication
from PySide6.QtQml import QQmlApplicationEngine

# Ensure the Python module is discoverable by QML
# This is crucial for @QmlElement decorated classes
# sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Add the current directory to the QML import path
    # This allows QML to find the 'Finance' module defined by qmldir
    engine.addImportPath(str(Path(__file__).parent))

    # Load the main QML file from the 'Finance' module
    engine.loadFromModule("Finance", "Main")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
```

--------------------------------

### Main Application Setup with QTableWidget and StarDelegate

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/stardelegate/README.md

Demonstrates how to set up a QTableWidget, apply the StarDelegate, populate it with sample data, and configure edit triggers for the custom delegate.

```APIDOC
Main Application Setup (in stardelegate.py's if __name__ == '__main__':):
  1. Initialize QApplication.
  2. Create QTableWidget instance.
  3. Create StarDelegate instance.
  4. Set StarDelegate on QTableWidget: table_widget.setItemDelegate(delegate).
  5. Populate table with sample data, storing integer ratings using QTableWidgetItem.setData(0, integer_rating).
  6. Configure edit triggers (e.g., DoubleClicked, SelectedClicked).
  7. Show the table widget and start the application event loop.
```

--------------------------------

### Execute PySide6 Text Object Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/richtext/textobject/README.md

This command runs the provided PySide6 example script, which demonstrates embedding custom SVG objects into a rich text editor. Ensure all PySide6 dependencies, including QtSvg, are installed before execution.

```Bash
python textobject.py
```

--------------------------------

### PySide6 MainWindow Menu Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/xml/dombookmarks/README.md

The `MainWindow` sets up standard 'File' and 'Help' menus. The 'File' menu includes 'Open...' and 'Save As...' actions, which are connected to the respective file operation methods.

```APIDOC
MainWindow.create_actions()
  Defines QAction objects for 'Open', 'Save As', 'Exit', 'About', 'About Qt'.
  Connects actions to corresponding slots (e.g., open(), save_as(), close()).

MainWindow.create_menus()
  Creates a 'File' menu and adds 'Open', 'Save As', and 'Exit' actions.
  Creates a 'Help' menu and adds 'About' and 'About Qt' actions.
```

--------------------------------

### Camera Class: Camera Start/Stop Control (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Explains the actions available for manually controlling the camera's state. These actions directly call the `start()` and `stop()` methods of the `QCamera` object.

```APIDOC
Camera Class UI Interaction:
  Camera Control:
    - "Start Camera" action: Calls m_camera.start().
    - "Stop Camera" action: Calls m_camera.stop().
```

--------------------------------

### Run Blur Picker Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/effects/blurpicker/README.md

Instructions to execute the PySide6 Blur Picker application from the command line after navigating to the example directory.

```Bash
python main.py
```

--------------------------------

### PySide6 Application Main Entry Point APIDOC

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/audiooutput/README.md

Documentation for the main application entry point, responsible for initializing the Qt application, checking for available audio output devices, and starting the main window.

```APIDOC
Application Main Entry Point:
  if __name__ == "__main__":
    - Initializes QApplication.
    - Checks for available audio output devices; exits if none are found.
    - Creates and shows the AudioTest main window.
    - Enters the Qt event loop.
```

--------------------------------

### SQLAlchemy Database Setup in Python

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

This conceptual Python snippet illustrates the core components for setting up a SQLAlchemy ORM database. It defines the `Base` for declarative models, a `Finance` ORM class mapped to the 'finances' table, an `engine` for database connection, and a `Session` factory for database interactions.

```Python
# From database.py (conceptual)
Base = declarative_base()
class Finance(Base):
    __tablename__ = 'finances'
    # ... column definitions ...
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
```

--------------------------------

### PySide6.QtWidgets Module API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Documentation for key classes within the PySide6.QtWidgets module, detailing UI components used in the text-to-speech example.

```APIDOC
PySide6.QtWidgets:
  QApplication: Manages the application event loop.
  QMainWindow (custom MainWindow class): The main application window.
  QTextEdit (named plainTextEdit in UI): For users to input the text to be spoken.
  QPushButton (named speakButton, pauseButton, resumeButton, stopButton): For controlling speech playback.
  QComboBox (named engine, language, voice): For selecting the speech engine, locale, and voice.
  QSlider (named pitch, rate, volume): For adjusting speech parameters.
  QStatusBar: To display status messages from the speech engine.
  UI loading: Uses a compiled UI file (ui_mainwindow.py from mainwindow.ui).
```

--------------------------------

### PySide6 Modules and Classes for OpenGL Context Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/contextinfo/README.md

Overview of key PySide6 modules, classes, and external dependencies used in the OpenGL context information example, detailing their roles in managing the application UI, OpenGL rendering, and data handling.

```APIDOC
QtWidgets:
  QApplication: Manages the application event loop.
  QWidget (custom MainWindow class): The main UI window that hosts the OpenGL view and the text display.
  QPlainTextEdit: For displaying the context information.
  QHBoxLayout: For arranging the OpenGL view and text display side-by-side.
  QMessageBox: To warn if PyOpenGL is not installed.
QtGui:
  QWindow (subclassed as RenderWindow): The window that directly manages the OpenGL surface and context.
  QOpenGLContext: Represents an OpenGL context.
  QSurfaceFormat: For requesting specific OpenGL context properties (version, profile, depth/stencil buffer).
  QMatrix4x4: Used for the transformation matrix in shaders.
  QPlatformSurfaceEvent: Handled in RenderWindow (though not explicitly shown in the provided snippet, it's a common pattern for QWindow subclasses managing graphics).
QtOpenGL (PySide6 module for OpenGL integration utilities):
  QOpenGLBuffer: For creating Vertex Buffer Objects (VBOs).
  QOpenGLShader, QOpenGLShaderProgram: For compiling and linking GLSL shaders.
  QOpenGLVertexArrayObject: For managing Vertex Array Objects (VAOs).
QtCore:
  QCoreApplication (for setting OpenGL attributes).
  QLibraryInfo: To get Qt build information.
  QTimer: To drive the animation of the rotating triangle.
  Slot: Decorator for the timer's timeout handler.
  QFile, QIODevice: (Not directly used for shaders in this Python version as they are string literals, but often used for loading from files).
  Qt: For enums.
External Dependencies:
  PyOpenGL: Used for issuing most OpenGL drawing commands (e.g., GL.glEnable, GL.glClearColor, GL.glDrawArrays).
  numpy: Used to define vertex and color data for the triangle.
```

--------------------------------

### Running the PySide6 Custom Property Types Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter4-customPropertyTypes/README.md

This command line snippet provides instructions on how to execute the Python script for the custom property types example. It assumes PySide6 is installed and the user is in the correct directory.

```Bash
python customPropertyTypes.py
```

--------------------------------

### PySide6 MainWindow Class Definition and UI Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/xml/dombookmarks/README.md

The `MainWindow` class, a subclass of `QMainWindow`, sets up the main application window. It instantiates an `XbelTree` and sets it as its central widget, providing the primary user interface for interacting with XBEL files.

```APIDOC
class MainWindow(QMainWindow):
  __init__(parent: QWidget = None)
    Inherits from QMainWindow.
    Initializes:
      _xbel_tree: XbelTree - An instance of the XbelTree widget.
    Sets _xbel_tree as the central widget.
    Calls create_actions() and create_menus() to set up UI.
```

--------------------------------

### QML Main User Interface (main.qml) API

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/editingmodel/README.md

Outlines the structure of `main.qml`, including the `Window`, `ListView` instantiation with the Python model, delegate setup, and control buttons for model interaction.

```APIDOC
Window { # Root item
  ListView { # id: lv
    orientation: ListView.Horizontal
    model: BaseModel {} # Instantiates and assigns the Python model
    delegate: DropArea { # Delegate for each item
      onEntered: lv.model.move(drag.source.modelIndex, index) # Handles drag-and-drop reordering
    }
  }

  // Control Buttons
  Button {
    text: "Reset view"
    onClicked: lv.model.reset() # Calls Python model's reset method
  }
  Button {
    text: "Add element"
    onClicked: lv.model.append() # Calls Python model's append method
  }

  Rectangle { # Background for ListView
    // Visual clarity
  }

  Component.onCompleted: lv.model.reset() # Initial population of the view
}
```

--------------------------------

### Project Dependencies

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/contextinfo/README.md

Lists the external libraries required for the PySide6 OpenGL example application to function correctly.

```APIDOC
Dependencies:
  - PySide6
  - PyOpenGL (for OpenGL.GL calls)
  - NumPy (for vertex data definition)
  - Note: These are typically listed in a requirements.txt file. The application checks for PyOpenGL at runtime and shows a message box if it's missing.
```

--------------------------------

### Run PySide6 Drag and Drop Robot Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/dragdroprobot/README.md

This command executes the main Python script for the PySide6 drag and drop robot example. Ensure PySide6 is installed and you are in the correct directory (`examples/widgets/graphicsview/dragdroprobot`) before running.

```Bash
python dragdrobrobot.py
```

--------------------------------

### Run PySide6 PDF Viewer Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/pdf/quickpdfviewer/README.md

Command to execute the PySide6 PDF viewer application from the command line. An optional path to a PDF file can be provided, which the application will attempt to open on startup. If no path is given, it defaults to loading `test.pdf` from the `resources` subdirectory.

```Bash
python main.py [path_to_pdf_file.pdf]
```

--------------------------------

### PySide6 Application Setup: Colliding Mice Simulation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/collidingmice/README.md

API documentation for the main application setup in 'collidingmice.py', detailing the configuration of QGraphicsScene and QGraphicsView, scene population with Mouse objects, and the animation loop using QTimer.

```APIDOC
Main Application Setup (collidingmice.py - if __name__ == '__main__':):
  - Scene Initialization:
      Object: QGraphicsScene
      Configuration: Created with a defined scene rectangle. scene.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex) is set.
  - Populating the Scene:
      Action: Instantiates a specified number of Mouse objects (MOUSE_COUNT).
      Placement: Gives initial positions in a circular arrangement.
      Addition: Adds Mouse objects to the scene.
  - View Configuration:
      Object: QGraphicsView
      Display: Created to display the scene.
      Background: Set to 'cheese.jpg' loaded from Qt resource system (mice_rc.py).
      Rendering/Performance Hints:
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
      Interaction: view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) allows panning.
  - Animation Loop:
      Mechanism: QTimer
      Frequency: Configured to call scene.advance() periodically (approx. 30 times per second).
      Effect: Drives the advance(1) method on every Mouse item in the scene, controlling their movement and logic.
```

--------------------------------

### Install Project Dependencies

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/part3/README.md

Instructions to install necessary Python packages for both the backend and frontend components of the application. This includes backend requirements from 'requirements.txt' and the 'requests' library for the frontend.

```bash
pip install -r requirements.txt
```

```bash
pip install requests
```

--------------------------------

### Run PySide6 Plot Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/painting/plot/README.md

Instructions to execute the PySide6 animated plot example from the command line.

```Bash
python plot.py
```

--------------------------------

### PySide6 InputTest Class API (Main UI and Logic)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/audiosource/README.md

The central application widget that manages UI setup, audio input device selection, volume control, and real-time audio level processing and display.

```APIDOC
class InputTest(QWidget):
  __init__(self, parent=None)
    Description: Constructor for the main application widget.
    Parameters:
      parent (QWidget, optional): The parent widget.
    Actions: Calls initialize(), initialize_window(), and initialize_audio().

  initialize(self)
    Description: Performs initial setup, including microphone permission checks on relevant platforms.

  initialize_window(self)
    Description: Sets up the user interface components.
    Components:
      m_canvas (RenderArea): For level display.
      m_device_box (QComboBox): Populated with available audio input devices.
      m_volume_slider (QSlider): Controls QAudioSource input volume.
      m_mode_button (QPushButton): Toggles audio capture mode (currently only one implemented).
      m_suspend_resume_button (QPushButton): Toggles audio capture suspend/resume.
    Layout: Arranges elements using QVBoxLayout.

  initialize_audio(self, device_info: QAudioDevice)
    Description: Configures and starts audio input using the specified device.
    Parameters:
      device_info (QAudioDevice): The selected audio input device.
    Actions:
      1. Defines QAudioFormat (8000 Hz, 1 channel, Int16).
      2. Checks and uses nearest supported format if necessary.
      3. Creates AudioInfo instance.
      4. Creates self.m_audio_input = QAudioSource(device_info, format).
      5. Sets volume slider based on initial QAudioSource volume.
      6. Calls toggle_mode() to start capture.

  device_changed(self, index: int)
    Description: Slot triggered when a new audio device is selected in the QComboBox.
    Parameters:
      index (int): The index of the selected device.
    Actions: Stops current QAudioSource, disconnects signals, and re-initializes audio with the new device.

  slider_changed(self, value: int)
    Description: Slot triggered when the volume slider changes.
    Parameters:
      value (int): The slider's integer value (0-100).
    Actions: Converts value to a linear scale (0.0-1.0) and sets it on self.m_audio_input.setVolume().

  toggle_mode(self)
    Description: Toggles the audio capture mode (currently starts a readyRead-based "push" mode).
    Actions:
      1. Stops current QAudioSource.
      2. Calls toggle_suspend() to reset button state.
      3. Starts QAudioSource: io_device = self.m_audio_input.start().
      4. Connects io_device.readyRead signal to push_mode_slot.

  push_mode_slot(self, io_device: QIODevice) (Lambda, nested within toggle_mode)
    Description: Reads available audio data, calculates the level, and updates the display.
    Parameters:
      io_device (QIODevice): The I/O device associated with the QAudioSource.
    Actions:
      1. Reads available data: buffer = io.read(len).
      2. Calculates audio level using self.m_audio_info.calculate_level().
      3. Updates visual level display: self.m_canvas.set_level(level).

  toggle_suspend(self)
    Description: Toggles the suspend/resume state of the audio input.
    Actions:
      1. Checks self.m_audio_input.state().
      2. Calls self.m_audio_input.resume() if suspended/stopped, or self.m_audio_input.suspend() if active.
      3. Updates the button text ("Suspend recording" / "Resume recording").
```

--------------------------------

### Execute PySide6 Order Form Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/richtext/orderform/README.md

Instructions to run the PySide6 rich text order form example. Ensure PySide6 and its QtPrintSupport module are installed. Navigate to the specified directory and execute the Python script from the command line. The application will launch, allowing users to generate and print formatted letters.

```bash
python orderform.py
```

--------------------------------

### Execute PySide6 Flow Layout Example Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/flowlayout/README.md

This command executes the `flowlayout.py` script, which demonstrates a custom flow layout in PySide6. Ensure PySide6 is installed and you are in the correct directory (`examples/widgets/layouts/flowlayout`) before running. After execution, a window titled "Flow Layout" will appear, showcasing buttons that adapt their arrangement dynamically as the window is resized.

```bash
python flowlayout.py
```

--------------------------------

### Accessing Screen Objects (QScreen)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/screenshot/README.md

Methods provided by Qt to retrieve `QScreen` objects, which represent physical screens connected to the system. `primaryScreen()` gets the main screen, while `screen()` gets the screen a specific widget is on.

```APIDOC
QGuiApplication.primaryScreen() -> QScreen
  Returns the primary screen of the application.

QWidget.screen() -> QScreen
  Returns the QScreen object that the widget is currently displayed on.
```

--------------------------------

### PySide6 Main Application Execution

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/statemachine/trafficlight/README.md

Standard Python entry point for a PySide6 application. It initializes QApplication, creates and displays the main TrafficLight widget, and starts the event loop.

```APIDOC
Main Application Execution (if __name__ == '__main__':):
  - Creates QApplication.
  - Creates an instance of the main TrafficLight widget.
  - Resizes, shows the widget, and starts the event loop.
```

--------------------------------

### Run PySide6 SpinBox Delegate Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/spinboxdelegate/README.md

Command to execute the Python script for the Spin Box Delegate example, demonstrating how to launch the application from the command line.

```Bash
python spinboxdelegate.py
```

--------------------------------

### Camera Class: setCamera Method (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Explains the critical `setCamera` method, which is invoked on startup or camera selection. This method configures and starts the camera, initializes media capture components, and connects various signals for UI updates and error handling.

```APIDOC
Camera Class Methods:
  setCamera(cameraDevice: QCameraDevice):
    - Creates new QCamera instance for cameraDevice.
    - Initializes m_mediaRecorder = QMediaRecorder() (if not done).
    - Initializes m_imageCapture = QImageCapture() (if not done).
    - Creates/Updates m_captureSession = QMediaCaptureSession():
      - setAudioInput(m_audioInput)
      - setCamera(m_camera)
      - setImageCapture(m_imageCapture)
      - setRecorder(m_mediaRecorder)
      - setVideoOutput(self._ui.viewfinder)
    - Connects signals from m_camera, m_imageCapture, m_mediaRecorder to appropriate slots.
    - Starts the camera: m_camera.start().
    - Updates UI element states (buttons, etc.).
```

--------------------------------

### PySide6 Main Application Setup for Analog Clock

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/gui/analogclock/README.md

Demonstrates the minimal setup required to run the `AnalogClockWindow` application, including `QGuiApplication` initialization and event loop execution.

```Python
import sys
from PySide6.QtGui import QGuiApplication
# from your_module import AnalogClockWindow # Uncomment and adjust if AnalogClockWindow is in another file

# Assuming AnalogClockWindow class is defined or imported here

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    clock_window = AnalogClockWindow()
    clock_window.show()
    sys.exit(app.exec())
```

--------------------------------

### Run QML Plugin Example with pyside6-qml

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter6-plugins/doc/chapter6-plugins.rst

This command executes the QML application, `app.qml`, located in the `chapter6-plugins` directory. The `-I` flag specifies an include path for the `Charts` module, which is part of the plugin example.

```shell
pyside6-qml examples/qml/tutorials/extending-qml/chapter6-plugins/app.qml -I examples/qml/tutorials/extending-qml/chapter6-plugins/Charts
```

--------------------------------

### Execute PySide6 Dynamic Layouts Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/dynamiclayouts/README.md

This command runs the `dynamiclayouts.py` script, launching a PySide6 application that demonstrates dynamic UI layouts. Ensure you are in the `examples/widgets/layouts/dynamiclayouts` directory before execution.

```bash
python dynamiclayouts.py
```

--------------------------------

### Run PyInstaller for PySide6 Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/installer_test/README.md

Command to execute PyInstaller using the provided spec file to package the PySide6 application. This will create 'build' and 'dist' directories, with the packaged application located in 'dist/hello_app'.

```Bash
pyinstaller hello_app.spec
```

--------------------------------

### PySide6 Application Entry Point (main.py) API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/threadedqopenglwidget/README.md

API documentation for the `main.py` script, which serves as the application's entry point, initializing `QApplication` and allowing for single-threaded mode via command-line arguments.

```APIDOC
main.py (Application Entry Point):
  - Initializes QApplication.
  - Allows command-line argument --single to run in single-threaded mode.
```

--------------------------------

### Manually Start D-Bus Session Bus

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/dbus/listnames/README.md

Provides a shell command to manually start a D-Bus session bus. This step is often necessary in minimal environments or remote sessions where the D-Bus session bus is not automatically active.

```Shell
eval $(dbus-launch --auto-syntax)
```

--------------------------------

### PySide6 Main Application Script Initialization

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/mimetypesbrowser/README.md

This section describes the main entry point of the PySide6 application. It handles the initialization of the Qt application, creates and displays the main window, and starts the event loop to manage user interactions.

```APIDOC
mimetypesbrowser.py (Main Script):
  Initializes the QApplication.
  Creates an instance of MainWindow.
  Sets the main window's initial size and shows it.
  Starts the application event loop.
```

--------------------------------

### Building Scriptable Application with CMake on macOS/Linux

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/scriptableapplication/doc/scriptableapplication.rst

Commands to build the scriptable application example using CMake on macOS and Linux systems. This involves navigating to the example directory, creating a build directory, configuring CMake with the Ninja generator, and compiling the project.

```bash
cd ~/pyside-setup/examples/scriptableapplication
mkdir build
cd build
cmake .. -B. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja
./scriptableapplication
```

--------------------------------

### PySide6 Core Modules and Classes for QSettings Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/settingseditor/README.md

Overview of key PySide6 modules and classes utilized in the QSettings editor example, detailing their roles and functionalities for settings management, UI display, and input validation.

```APIDOC
QtCore:
  QSettings: The core class for saving and restoring application settings.
  QVariant: Implicitly used for handling various data types with QSettings.
  Qt: For enums (flags, roles, orientations, etc.).
  QDir: For path manipulation.
  QTimer: For auto-refresh functionality.
  QRegularExpression, QRegularExpressionValidator: Used by TypeChecker and VariantDelegate for input validation.
  QByteArray, QDate, QDateTime, QPoint, QRect, QSize, QTime.
QtWidgets:
  QApplication: Manages the application's event loop.
  QMainWindow (custom MainWindow class): The main application window.
  QTreeWidget, QTreeWidgetItem: Used to display the settings in a hierarchical tree structure (Setting, Type, Value).
  QItemDelegate (custom VariantDelegate class): Provides custom editors for different data types within the QTreeWidget.
  QDialog (custom LocationDialog class): A dialog to let the user specify parameters (format, scope, organization, application) for opening QSettings.
  QAction, QMenu: For menu bar actions.
  QFileDialog: For opening INI and Property List files.
  QInputDialog: For opening a Windows Registry path.
  QMessageBox: For displaying messages (e.g., "About").
  QCheckBox, QComboBox, QLineEdit, QSpinBox, QTableWidget: Used within LocationDialog and as editors by VariantDelegate.
QtGui:
  QColor: One of the data types supported for editing.
  QIcon: For icons in the SettingsTree.
  QIntValidator, QDoubleValidator: Used by VariantDelegate.
```

--------------------------------

### Building Scriptable Application with CMake on Windows

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/scriptableapplication/doc/scriptableapplication.rst

Commands to build the scriptable application example using CMake on Windows. This includes navigating to the example directory, creating a build directory, configuring CMake with the Ninja generator, explicitly specifying the C compiler for MSVC, and running the compiled executable.

```bash
cd C:\pyside-setup\examples\scriptableapplication
mkdir build
cd build
cmake .. -B. -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=cl.exe
ninja
.\scriptableapplication.exe
```

--------------------------------

### PySide6 Application Entry Point (`main.py`)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/serialport/terminal/README.md

Describes the role of `main.py` as the application's starting point, responsible for initializing the QApplication, creating the MainWindow, displaying it, and starting the event loop.

```APIDOC
main.py:
  Initializes QApplication.
  Creates an instance of MainWindow.
  Shows the MainWindow and starts the event loop.
```

--------------------------------

### Run PySide6 Tetrix Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgets/tetrix/README.md

Instructions to execute the PySide6 Tetrix game from the command line after navigating to the example directory.

```Bash
python tetrix.py
```

--------------------------------

### Run PySide6 QML to Python Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/signals/qmltopy1/README.md

Command to execute the PySide6 QML to Python signal/slot example from the command line.

```Bash
python main.py
```

--------------------------------

### JavaScript WebSocket and QWebChannel Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webchannel/standalone/index.html

This JavaScript code initializes a WebSocket connection to a specified server, then sets up a QWebChannel to facilitate communication with a backend PySide6 application. It includes functions to display messages, handle connection events (open, close, error), and manage sending user input and receiving messages from the backend.

```JavaScript
function output(message) {
  var output = document.getElementById("output");
  output.innerHTML = output.innerHTML + message + "\\n";
}
window.onload = function() {
  if (location.search != "")
    var baseUrl = (/[?&]webChannelBaseUrl=([A-Za-z0-9\\-:/\\.]+)/.exec(location.search)[1]);
  else
    var baseUrl = "ws://localhost:12345";
  output("Connecting to WebSocket server at " + baseUrl + ".");
  var socket = new WebSocket(baseUrl);
  socket.onclose = function() {
    console.error("web channel closed");
  };
  socket.onerror = function(error) {
    console.error("web channel error: " + error);
  };
  socket.onopen = function() {
    output("WebSocket connected, setting up QWebChannel.");
    new QWebChannel(socket, function(channel) {
      // make core object accessible globally
      window.core = channel.objects.core;
      document.getElementById("send").onclick = function() {
        var input = document.getElementById("input");
        var text = input.value;
        if (!text) {
          return;
        }
        output("Sent message: " + text);
        input.value = "";
        core.receiveText(text);
      }
      core.sendText.connect(function(message) {
        output("Received message: " + message);
      });
      core.receiveText("Client connected, ready to send/receive messages!");
      output("Connected to WebChannel, ready to send/receive messages!");
    });
  }
}
```

--------------------------------

### Python QWebChannel Setup in MainWindow

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webenginewidgets/markdowneditor/README.md

Python code demonstrating how the `MainWindow` class initializes a `QWebChannel`, registers the `Document` instance (exposed as "content") with the channel, and associates the channel with the `PreviewPage` for inter-process communication.

```Python
self._channel = QWebChannel(self)
self._channel.registerObject("content", self.m_content) # Expose Document as "content"
self._page.setWebChannel(self._channel)
```

--------------------------------

### Execute PySide6 DOM Bookmarks Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/xml/dombookmarks/README.md

Instructions to run the PySide6 DOM bookmarks example application from the command line. This script demonstrates XML DOM parsing and manipulation with a graphical user interface.

```Bash
python dombookmarks.py
```

--------------------------------

### Python: `main.py` Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/demos/documentviewer/README.md

The `main.py` script serves as the application's entry point. It initializes the QApplication, configures application settings, parses command-line arguments for file opening, creates and displays the MainWindow, and handles initial file loading if provided.

```APIDOC
main.py:
  - Initializes QApplication.
  - Sets QSettings organization and application names.
  - Parses command-line arguments (e.g., file path).
  - Creates and shows MainWindow.
  - Attempts to open a file if passed as an argument.
```

--------------------------------

### PySide6 QRhiWidget Class API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/rhi/simplerhiwidget/README.md

Documents the core methods of the `QRhiWidget` class, which serves as the base for integrating RHI rendering into a QWidget. It covers methods for one-time RHI setup, per-frame rendering, resource cleanup, and access to RHI instances and render targets.

```APIDOC
QRhiWidget:
  initialize(cb): For one-time RHI setup specific to the widget.
  render(cb): For per-frame rendering commands.
  releaseResources(): For cleaning up RHI resources.
  rhi(): Provides access to the QRhi instance.
  renderTarget(): Provides access to the QRhiRenderTarget for this widget.
```

--------------------------------

### Camera Class: Video Recording Control (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Outlines the slots responsible for controlling video recording. These slots directly interact with the `QMediaRecorder` object to start, pause, and stop the recording process.

```APIDOC
Camera Class UI Interaction:
  Video Recording:
    - record() slot: Controls m_mediaRecorder.record().
    - pause() slot: Controls m_mediaRecorder.pause().
    - stop() slot: Controls m_mediaRecorder.stop().
```

--------------------------------

### PySide6 Nano Browser MainWindow Class Implementation Details

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webenginewidgets/widgetsnanobrowser/README.md

Detailed breakdown of the `MainWindow` class, a subclass of `QMainWindow`, outlining its initialization, UI setup (toolbar, navigation, address bar), web view integration, and signal-slot connections for browser functionality.

```APIDOC
MainWindow (subclass of QMainWindow):
  __init__():
    Purpose: Initializes the main window, sets up UI components, and connects signals.
    Details:
      - Sets the initial window title.
      - Toolbar Setup:
        - A QToolBar (self.toolBar) is created and added to the QMainWindow.
        - Navigation Buttons:
          - A "Back" QPushButton (self.backButton) is created, an icon is set, and its clicked signal is connected to the self.back slot.
          - A "Forward" QPushButton (self.forwardButton) is created similarly and connected to the self.forward slot.
          - These buttons are added to the toolbar.
        - Address Bar: A QLineEdit (self.addressLineEdit) is created. Its returnPressed signal is connected to the self.load slot. This line edit is added to the toolbar.
      - Web View Setup:
        - A QWebEngineView instance (self.webEngineView) is created and set as the central widget of the QMainWindow.
      - Initial Page Load:
        - An initial URL (e.g., "http://qt.io") is set in self.addressLineEdit.
        - self.webEngineView.load(QUrl(initialUrl)) is called to load this page.
      - Signal Connections:
        - self.webEngineView.page().titleChanged.connect(self.setWindowTitle): The main window's title is automatically updated whenever the web page's title changes.
        - self.webEngineView.page().urlChanged.connect(self.urlChanged): The self.urlChanged slot is called when the URL of the web page changes.
  load():
    Purpose: Slot triggered when Enter is pressed in self.addressLineEdit.
    Details:
      - Retrieves the text from the address bar.
      - Uses QUrl.fromUserInput() to intelligently parse the text into a QUrl.
      - If the URL is valid, it calls self.webEngineView.load(url) to navigate to the new page.
  back():
    Purpose: Slot to navigate to the previous page in history.
    Details: Calls self.webEngineView.page().triggerAction(QWebEnginePage.WebAction.Back).
  forward():
    Purpose: Slot to navigate to the next page in history.
    Details: Calls self.webEngineView.page().triggerAction(QWebEnginePage.WebAction.Forward).
  urlChanged(url: QUrl):
    Purpose: Slot to update the address bar with the current URL.
    Details: Updates the text of self.addressLineEdit to display the current URL (url.toString()).

Main Application Script (if __name__ == '__main__':):
  - Creates QApplication.
  - Creates an instance of MainWindow.
  - Resizes the window to a fraction of the available screen geometry.
  - Shows the MainWindow and starts the Qt event loop (app.exec()).
```

--------------------------------

### Executing the PySide6 QML Extension Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml/chapter1-basics/README.md

This bash command shows how to run the Python script that initializes the PySide6 application and loads the QML file, demonstrating the custom QML type in action.

```Bash
python basics.py
```

--------------------------------

### Run PySide6 Syntax Highlighter Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/richtext/syntaxhighlighter/README.md

Execute the Python script to launch the PySide6 syntax highlighter application. This command runs the `syntaxhighlighter.py` file, which then displays its own source code with applied syntax highlighting rules.

```Bash
python syntaxhighlighter.py
```

--------------------------------

### Run PySide6 Basic Drawing Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/painting/basicdrawing/README.md

Instructions to execute the PySide6 basic drawing example script from the command line.

```Bash
python basicdrawing.py
```

--------------------------------

### PySide6 State Machine Ping-Pong API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/statemachine/ping_pong/README.md

API documentation for the `ping_pong.py` module, detailing custom event classes, state classes, transition classes, and the main state machine setup and execution flow.

```APIDOC
Module: ping_pong.py

Custom Event Classes:
  PingEvent(QEvent):
    Description: Custom event signaling a 'ping' action.
    Type: QEvent.User + 2
  PongEvent(QEvent):
    Description: Custom event signaling a 'pong' action.
    Type: QEvent.User + 3

Class: Pinger(QState)
  Description: Represents the state responsible for initiating a 'ping'.
  Methods:
    onEntry(self, event: QEvent):
      Description: Called when the Pinger state is entered.
      Parameters:
        event: QEvent - The event that triggered entry (typically not used for initial entry).
      Actions:
        - Posts a PingEvent to the state machine (self.machine().postEvent(PingEvent())).
        - Prints "ping?" to the console.

Class: PingTransition(QAbstractTransition)
  Description: Custom transition triggered by a PingEvent.
  Methods:
    eventTest(self, event: QEvent) -> bool:
      Description: Tests if the received event is a PingEvent.
      Parameters:
        event: QEvent - The event to test.
      Returns: True if event.type() == QEvent.User + 2, False otherwise.
    onTransition(self, event: QEvent):
      Description: Called when this transition executes after a successful eventTest.
      Parameters:
        event: QEvent - The PingEvent that triggered the transition.
      Actions:
        - Prints "pong!" to the console.
        - Posts a PongEvent to the state machine with a 500ms delay (machine.postDelayedEvent(PongEvent(), 500)).

Class: PongTransition(QAbstractTransition)
  Description: Custom transition triggered by a PongEvent.
  Methods:
    eventTest(self, event: QEvent) -> bool:
      Description: Tests if the received event is a PongEvent.
      Parameters:
        event: QEvent - The event to test.
      Returns: True if event.type() == QEvent.User + 3, False otherwise.
    onTransition(self, event: QEvent):
      Description: Called when this transition executes after a successful eventTest.
      Parameters:
        event: QEvent - The PongEvent that triggered the transition.
      Actions:
        - Prints "ping?" to the console.
        - Posts a PingEvent to the state machine with a 500ms delay (machine.postDelayedEvent(PingEvent(), 500)).

State Machine Setup (in `if __name__ == '__main__':` block):
  Description: Initializes and configures the PySide6 state machine for the ping-pong interaction.
  Components:
    - QCoreApplication instance created.
    - QStateMachine instance (`machine`) created.
    - Parallel State Group (`group = QState(QState.ParallelStates)`) created.
    - Child States:
      - `pinger = Pinger(group)`: An instance of the custom `Pinger` state.
      - `ponger = QState(group)`: A standard `QState` instance.
    - Transitions Added:
      - `pinger.addTransition(PongTransition())`: Adds a `PongTransition` to the `pinger` state.
      - `ponger.addTransition(PingTransition())`: Adds a `PingTransition` to the `ponger` state.
    - Machine Initialization:
      - `machine.addState(group)`: Adds the parallel group as a top-level state.
      - `machine.setInitialState(group)`: Sets the group as the initial state.
      - `machine.start()`: Starts the state machine execution.

Execution Flow:
  1. The state machine starts, and the `group` (parallel state) is entered.
  2. Both child states, `pinger` and `ponger`, are entered simultaneously.
  3. `pinger.onEntry()` executes:
     - Prints "ping?".
     - Posts an immediate `PingEvent`.
  4. The state machine processes the `PingEvent`.
  5. The `PingTransition` added to `ponger` (which is active) evaluates this `PingEvent`. Its `eventTest()` returns `True`.
  6. The `PingTransition`'s `onTransition()` method executes:
     - Prints "pong!".
     - Posts a `PongEvent` with a 500ms delay.
  7. After 500ms, the `PongEvent` is processed by the state machine.
  8. The `PongTransition` added to `pinger` (which is active) evaluates this `PongEvent`. Its `eventTest()` returns `True`.
  9. The `PongTransition`'s `onTransition()` method executes:
     - Prints "ping?".
     - Posts a `PingEvent` with a 500ms delay.
  10. The cycle repeats from step 4, creating the alternating "ping?" and "pong!" messages with delays.
```

--------------------------------

### Create QChart, QChartView, and Control Widget Layout

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointselectionandmarkers/doc/pointselectionandmarkers.rst

This snippet demonstrates the creation of the core chart components: a QChart instance, a QChartView to display it, and a control widget. It also sets up a horizontal layout to arrange the chart view and the customization control widget, emphasizing the initial setup of the chart and its display.

```python
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QHBoxLayout

# ... (assuming 'series' is already defined)
chart = QChart() # Emphasized
chart.addSeries(series)
chart.createDefaultAxes()
chart.setTitle("Light Markers and Point Selection Example")

chart_view = QChartView(chart) # Emphasized
chart_view.setRenderHint(QPainter.Antialiasing)

control_widget = QWidget()
main_layout = QHBoxLayout(self) # Emphasized (assuming 'self' is the main window/widget)
main_layout.addWidget(chart_view)
main_layout.addWidget(control_widget)
```

--------------------------------

### Initialize PySide6 QML 3D Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/intro/README.md

Initializes a PySide6 `QGuiApplication`, sets an ideal `QSurfaceFormat` for multisampling to enhance 3D rendering quality, and loads the main QML scene using `QQmlApplicationEngine`.

```Python
from PySide6.QtGui import QGuiApplication, QSurfaceFormat
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick3D import QQuick3D
import sys

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Set ideal surface format for 3D rendering with multisampling
    format = QQuick3D.idealSurfaceFormat(4)
    QSurfaceFormat.setDefaultFormat(format)

    engine = QQmlApplicationEngine()
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
```

--------------------------------

### Execute PySide6 MDI Application from Command Line

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/mainwindows/mdi/README.md

These commands illustrate how to run the PySide6 MDI example application. Users can launch the application directly or specify one or more text files to be opened automatically upon startup, demonstrating file association capabilities.

```Bash
python mdi.py
python mdi.py file1.txt file2.txt
```

--------------------------------

### PySide6.QtCore Module API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Documentation for key classes within the PySide6.QtCore module, covering core Qt functionalities like signals, slots, locales, and logging.

```APIDOC
PySide6.QtCore:
  Slot: For defining slots connected to signals.
  Signal: Although not explicitly defined for custom signals in this example, used implicitly by Qt's property system and QTextToSpeech.
  QLocale: Used for handling locale information.
  QLoggingCategory: Used in main.py to enable debug output for Qt Speech.
  QSignalBlocker: Used to temporarily block signals from QComboBoxes while they are being repopulated.
```

--------------------------------

### PySide6 Key Modules and Classes API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/httpserver/simplehttpserver/README.md

Reference for core PySide6 modules and classes used in the HTTP server example, detailing their purpose and role in building the server.

```APIDOC
Module: QtCore
  Class: QCoreApplication
    Description: Provides the event loop for this console-based application.

Module: QtNetwork
  Class: QTcpServer
    Description: Although QHttpServer handles HTTP logic, a QTcpServer instance is used underneath to listen for incoming TCP connections on a specific port. The QHttpServer is then bound to this QTcpServer.

Module: QtHttpServer
  Class: QHttpServer
    Description: The main class for creating the HTTP server. It handles parsing HTTP requests and routing them to appropriate handlers.
  Class: QHttpHeaders
    Description: Used to manipulate HTTP headers in responses.
  Implicitly Used:
    Class: QHttpRequest
      Description: Object representing an incoming HTTP request, passed as an argument to route and after-request handlers.
    Class: QHttpResponse
      Description: Object representing an outgoing HTTP response, passed as an argument to after-request handlers for modification.
```

--------------------------------

### PySide6 Utility API Highlights

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/dirview/README.md

Key utility classes and methods used in the PySide6 Dir View example, including icon providers, scrollers for touch gestures, and path normalization.

```APIDOC
QFileIconProvider: Provides native-looking icons for files and directories.
QScroller:
  - grabGesture(widget: QWidget, gesture_type: QScroller.ScrollerGestureType): Enables kinetic scrolling gestures on a widget.
    - ScrollerGestureType: TouchGesture (for touch-sensitive screens)
QDir:
  - cleanPath(path: str): Normalizes a directory path.
```

--------------------------------

### Configure PySide/Shiboken Example with CMake

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/doc/samplebinding.rst

Commands to navigate to the example directory, create a build directory, and run CMake to configure the project for a Release build using the Ninja generator. Includes specific commands for macOS/Linux and Windows, addressing compiler specification on Windows.

```bash
cd ~/pyside-setup/examples/samplebinding
mkdir build
cd build
cmake .. -B. -G Ninja -DCMAKE_BUILD_TYPE=Release
```

```bash
cd C:\pyside-setup\examples\samplebinding
mkdir build
cd build
cmake .. -B. -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=cl.exe
```

--------------------------------

### Run PySide6 QML to Python Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/signals/qmltopy2/README.md

Command to execute the PySide6 application demonstrating QML-to-Python communication with return values. Navigate to the specified directory and run the main Python script.

```bash
python main.py
```

--------------------------------

### PySide6 Main Application Execution

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/audiosource/README.md

The entry point for the PySide6 audio level application, handling QApplication initialization, device checks, and main window display.

```APIDOC
Main Application Execution:
  if __name__ == "__main__":
    QApplication_initialization()
      Description: Initializes the QApplication instance.

    Audio_device_check()
      Description: Checks for available audio input devices; displays QMessageBox and exits if none are found.

    InputTest_instance_creation_and_display()
      Description: Creates and shows an instance of the InputTest main window.

    Qt_event_loop_entry()
      Description: Enters the Qt event loop, starting the application's execution.
```

--------------------------------

### Running the PySide6 QML to Python Signal Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/signals/qmltopy4/README.md

Command to execute the PySide6 example demonstrating QML signal connection from a specific QML object to Python. Run this in the specified example directory.

```Bash
python main.py
```

--------------------------------

### PySide6 and External Module API Reference for OpenGL Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/hellogl2/README.md

Detailed API reference for PySide6 modules and external libraries used in the 'Hello GL2' OpenGL example, outlining classes, their purpose, and key functionalities.

```APIDOC
PySide6 QtOpenGLWidgets:
  QOpenGLWidget (subclassed as GLWidget): The core widget for rendering OpenGL content.
PySide6 QtGui:
  QOpenGLFunctions (implicitly used as a base for GLWidget or obtained from context): Provides access to OpenGL functions.
  QMatrix4x4: For handling transformation matrices (projection, model-view, world).
  QVector3D: For representing 3D vertices, normals, and light positions.
  QOpenGLContext: Represents the OpenGL context.
  QSurfaceFormat: For requesting specific OpenGL context properties (version, profile, depth buffer, samples).
  QMouseEvent: For handling mouse input for rotation.
PySide6 QtOpenGL:
  QOpenGLShaderProgram: For creating, compiling, and linking GLSL shader programs.
  QOpenGLShader: Represents individual vertex or fragment shaders.
  QOpenGLBuffer: For creating Vertex Buffer Objects (VBOs) to store geometry data on the GPU.
  QOpenGLVertexArrayObject: For managing Vertex Array Objects (VAOs) that encapsulate vertex attribute state.
PySide6 QtWidgets:
  QApplication: Manages the application event loop.
  QMainWindow (custom MainWindow class): The main application window.
  QWidget (custom Window class): A container widget that holds the GLWidget and rotation sliders.
  QSlider: Used to control the X, Y, and Z rotation of the 3D object.
  QVBoxLayout, QHBoxLayout: For arranging UI elements.
  QPushButton: For the "Dock/Undock" functionality.
  QMessageBox: For error messages (e.g., if PyOpenGL is missing).
PySide6 QtCore:
  Signal, Slot: For communication between GLWidget and Window (sliders).
  Qt: Namespace for various enums (e.g., Qt.MouseButton).
  QPointF, QSize.
OpenGL.GL (PyOpenGL) (External Dependency):
  Used for some OpenGL constants (e.g., GL.GL_FLOAT, GL.GL_TRIANGLES) and a few direct OpenGL API calls (e.g., glEnableVertexAttribArray, glVertexAttribPointer, glDrawArrays, glClear, glEnable) within GLWidget. These calls are made against the current context established by QOpenGLWidget.
Custom Classes:
  Logo (in logo.py): A helper class that programmatically generates vertex and normal data for the parts of the 3D "Qt" logo. The data is stored as a list of QVector3D objects (interleaved vertex, normal).
  GLWidget (in glwidget.py): The core QOpenGLWidget subclass where all OpenGL rendering occurs.
  Window (in window.py): A QWidget that groups an instance of GLWidget with three QSliders for controlling its rotation. Implements dock/undock functionality.
  MainWindow (in mainwindow.py): The main application window, which can host Window instances.
```

--------------------------------

### PySide6 Server: Main Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/network/fortuneserver/README.md

Describes the standard Python entry point for the application, including `QApplication` initialization, `Server` dialog creation, random module seeding, and starting the Qt event loop.

```APIDOC
Main Application Execution (if __name__ == "__main__"):
  1. QApplication Initialization.
  2. Server Dialog Creation: server = Server().
  3. Random Seed Initialization: Python random module.
  4. Start Qt Event Loop: server.exec().
```

--------------------------------

### Run PySide6 WigglyWidget Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgetbinding/doc/widgetbinding.md

Command to execute the `main.py` script, which launches the application demonstrating both the Python-translated and C++-bound versions of the custom WigglyWidget.

```bash
python main.py
```

--------------------------------

### APIDOC: Capture System Components

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/screencapture/README.md

Details the core PySide6 classes used for screen and window capture, and their integration via QMediaCaptureSession. This includes setting outputs and associating capture inputs.

```APIDOC
QScreenCapture:
  # Instance for capturing screen content.

  setScreen(screen: QScreen):
    # Sets the specific QScreen object to be captured.

  setActive(active: bool):
    # Activates or deactivates screen capture.

QWindowCapture:
  # Instance for capturing individual window content.

  setWindow(window: QCapturableWindow):
    # Sets the specific QCapturableWindow object to be captured.

  setActive(active: bool):
    # Activates or deactivates window capture.

QMediaCaptureSession:
  # The central manager for media capture operations.

  setVideoOutput(video_widget: QVideoWidget):
    # Sets the QVideoWidget instance where the captured video stream will be displayed.

  setScreenCapture(screen_capture: QScreenCapture):
    # Associates a QScreenCapture instance with the session as an input source.

  setWindowCapture(window_capture: QWindowCapture):
    # Associates a QWindowCapture instance with the session as an input source.

  # Error Handling:
  # Error signals from QScreenCapture and QWindowCapture are connected to slots
  # to display error messages to the user.
```

--------------------------------

### Create and Initialize QLineSeries

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointconfiguration/doc/pointconfiguration.rst

Instantiates a `QLineSeries` to hold the data points for the chart. It sets a name for the series and makes the individual points visible, then adds some example data.

```python
self.series = QLineSeries()
self.series.setName("My Line Series")
self.series.setPointsVisible(True)
# Add some dummy points
for i in range(10):
    self.series.append(i, i * 2)
```

--------------------------------

### main.py Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/serialbus/can/README.md

Initializes the PySide6 application, optionally sets Qt logging rules for CAN bus debugging, and creates/shows the main window.

```APIDOC
main.py:
  Initializes QApplication
  Optionally sets Qt logging rules for CAN bus debugging (QLoggingCategory.setFilterRules("qt.canbus* = true"))
  Creates and shows an instance of MainWindow
```

--------------------------------

### Run PySide6 QML Binding Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/binding/README.md

This bash command executes the main Python script for the PySide6 QML example. It initiates the application, which then demonstrates dynamic property binding and console output based on the QML and Python interaction.

```bash
python main.py
```

--------------------------------

### Execute PySide6 QML Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced6-Property-value-source/README.md

This snippet provides the command to run the PySide6 QML example from the specified directory. It initiates the application demonstrating dynamic property updates.

```bash
python main.py
```

--------------------------------

### APIDOC: QML Main Window (Main.qml)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Documentation for the main application window defined in `Main.qml`. It describes the layout, navigation, and instantiation of the Python backend model.

```APIDOC
Main.qml (QML Component)
  Base Component: ApplicationWindow (Material Design)

  Features:
    TabBar: Switches between "Expenses" (FinanceView.qml) and "Charts" (FinancePieChart.qml).
    StackLayout: Manages the views displayed by the TabBar.
    FinanceModel:
      id: finance_model
      Description: Instantiates the Python backend model for data management.
    ToolButton:
      Action: Opens AddDialog.qml for adding new finance entries.
      Signal Handling: On acceptance of AddDialog, calls finance_model.append() with entered data.
```

--------------------------------

### Run PySide6 QML Extension Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/adding/README.md

Instructions on how to execute the Python script to run the QML extension example. The script's output confirms that the QML module was loaded, the component instantiated, and its properties accessed correctly from Python.

```Bash
python main.py
```

--------------------------------

### PySide6 QModbusDataUnit Class

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/serialbus/modbus/modbusclient/README.md

QModbusDataUnit encapsulates the data for Modbus requests and responses. It specifies the register type (e.g., Coils, Holding Registers), start address, and the number of values, and holds the actual data.

```APIDOC
QModbusDataUnit:
  __init__(type: QModbusDataUnit.RegisterType, address: int, size: int)
    type: The type of Modbus registers (e.g., Coils, HoldingRegisters).
    address: The starting address of the registers.
    size: The number of registers.
  values() -> list[int] | QBitArray
    Returns the list of values in the data unit.
  setValues(values: list[int] | QBitArray)
    Sets the values for the data unit.
```

--------------------------------

### Frontend FinanceModel: Fetch All Data from Backend

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

The `fetchAllData()` method in the frontend's `FinanceModel` makes an HTTP GET request to the backend API to retrieve all finance entries. It parses the JSON response and populates the internal model data.

```Python
# In Frontend/financemodel.py
import requests

class FinanceModel:
    # ... other __init__ setup ...
    def fetchAllData(self):
        try:
            response = requests.get("http://127.0.0.1:8000/finances/")
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            # Assuming data is {'total': ..., 'items': [...]}
            self.m_finances = data.get('items', []) # Populate internal list
            # Emit signals for QML update if necessary
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        # ...
```

--------------------------------

### PySide6 Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/dialogs/extension/README.md

Standard Python entry point for a PySide6 application, demonstrating how to initialize QApplication, create and show a QDialog modally, and start the main event loop for the application.

```Python
import sys
from PySide6.QtWidgets import QApplication

# Assuming FindDialog class is defined elsewhere

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FindDialog()
    dialog.exec()
    sys.exit(app.exec())
```

--------------------------------

### PySide6 QFileSystemModel API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/dirview/README.md

Detailed API reference for PySide6's QFileSystemModel, covering its initialization, icon provisioning, root path settings, and options for behavior control.

```APIDOC
QFileSystemModel:
  - Initialization: QFileSystemModel()
  - setIconProvider(provider: QFileIconProvider): Sets the icon provider for the model.
  - setRootPath(path: str): Sets the root directory for the model. An empty string sets the context to the entire accessible file system.
  - setOption(option: QFileSystemModel.Option, on: bool = True): Sets or unsets a model option.
    - Options:
      - QFileSystemModel.DontUseCustomDirectoryIcons: Uses default icons for directories.
      - QFileSystemModel.DontWatchForChanges: Disables automatic updates on file system changes.
  - index(path: str): Returns the QModelIndex corresponding to the given file system path.
```

--------------------------------

### PySide6 QtGui and QtCore Modules API (Relevant Classes)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/axcontainer/axviewer/README.md

Details relevant classes from the `QtGui` and `QtCore` modules used in the ActiveX viewer example, specifically `QAction` for UI actions and `qApp` for application instance access.

```APIDOC
QtGui:
  QAction:
    Purpose: An abstract user interface action that can be inserted into menus, toolbars, or other widgets.
QtCore:
  qApp (QApplication.instance()):
    Purpose: A global pointer to the unique QApplication instance.
```

--------------------------------

### Python Application Initialization with PySide6 QML Engine

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/demos/colorpaletteclient/README.md

Details the initial setup of the PySide6 application, including the creation of the QGuiApplication and QQmlApplicationEngine, setting up QML import paths for Python classes, and loading the root QML component.

```APIDOC
main.py Initialization Flow:
  1. Create QGuiApplication instance.
  2. Set application's icon theme name.
  3. Initialize QQmlApplicationEngine.
  4. Add directory containing @QmlElement Python classes to QML import path.
  5. Load 'ColorPalette/Main.qml' as the root QML component.
```

--------------------------------

### RenderWindow Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/contextinfo/README.md

Details the `RenderWindow` class, a `QWindow` subclass responsible for setting up and managing an OpenGL context, initializing OpenGL resources (shaders, VBO, VAO), performing rendering operations, handling animation, and providing OpenGL information.

```APIDOC
RenderWindow (subclass of QWindow):
  - __init__():
    - Description: Initializes the OpenGL context and surface.
    - Details: Sets its surface type to QWindow.SurfaceType.OpenGLSurface. Sets a QSurfaceFormat (can be default or specified). Creates a QOpenGLContext and associates it with itself. Calls context.create().
  - init_gl():
    - Description: Initializes OpenGL resources (shaders, buffers).
    - Details: Called once rendering starts. Creates QOpenGLShaderProgram, QOpenGLVertexArrayObject (VAO), and QOpenGLBuffer (VBO). Selects appropriate GLSL shader source code (version 110 for compatibility profiles or older OpenGL, version 150 for core profiles) defined as string literals. Compiles and links vertex and fragment shaders using program.addShaderFromSourceCode() and program.link(). Retrieves attribute and uniform locations from the shader program. Creates the VBO, binds it, and allocates memory for vertex positions and colors (defined as NumPy arrays). The data is uploaded to the VBO. Sets up vertex attributes within a VAO (if supported) or directly, specifying how the shader program should interpret the data in the VBO using program.setAttributeBuffer() and program.enableAttributeArray().
  - render():
    - Description: Performs the OpenGL drawing operations.
    - Details: Called by exposeEvent and QTimer. Makes the OpenGL context current using self.context.makeCurrent(self). Obtains QOpenGLFunctions via self.context.functions() (though drawing commands use OpenGL.GL). If self.program is not yet initialized (first render), calls self.init_gl() and enables depth testing, sets clear color. Sets the OpenGL viewport. Clears color and depth buffers (GL.glClear()). Binds the shader program (self.program.bind()). Creates a transformation matrix (QMatrix4x4) for perspective, translation, and rotation (angle updated by a timer). Sets this matrix as a uniform value for the shader program. Binds the VAO (if used). Issues the draw call: GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3). Releases VAO and program. Swaps buffers: self.context.swapBuffers(self). Makes context not current: self.context.doneCurrent().
  - slot_timer():
    - Description: Animates the rendered object.
    - Details: A QTimer periodically calls self.render() and increments a rotation angle (self.angle) to animate the triangle.
  - glInfo():
    - Description: Retrieves and formats OpenGL context information.
    - Details: Makes the context current. Uses functions.glGetString() (where functions = self.context.functions()) to retrieve GL_VENDOR, GL_RENDERER, GL_VERSION, and GL_SHADING_LANGUAGE_VERSION. Formats this information along with QSurfaceFormat details of the context and the window.
  - Event Handling:
    - exposeEvent():
      - Description: Manages rendering and animation based on window exposure.
      - Details: Starts rendering (and the timer for animation) when the window is exposed. Stops timer if not exposed.
```

--------------------------------

### PySide6 3D Surface Application Architecture (APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/datavisualization/surface_model_numpy/README.md

This documentation outlines the core classes and their interactions within a PySide6 application demonstrating 3D surface visualization. It details the UI setup, data handling via custom models and proxies, and dynamic graph customization.

```APIDOC
Window(QWidget) in main.py:
  Description: Sets up the main user interface, including a Q3DSurface graph display area and a panel of controls.
  Methods/Interactions:
    - createWindowContainer(): Embeds Q3DSurface into the widget layout.
    - Instantiation: Creates UI controls (RadioButtons, Sliders, ComboBox, PushButtons).
    - Controller Integration: Instantiates SurfaceGraph, passing the Q3DSurface graph.
    - Signal Connections: Connects UI control signals to SurfaceGraph slots for user interactions.

SurfaceGraph(QObject) in surfacegraph.py:
  Description: Acts as the controller that manages the data models and applies customizations to the Q3DSurface graph.
  Initialization:
    - Parameters: Takes a Q3DSurface instance.
    - Axes Setup: Sets up three QValue3DAxis instances for X, Y, Z axes.
    - Series Initialization:
      - m_sqrtSinSeries: Uses QItemModelSurfaceDataProxy with SqrtSinModel.
      - m_heightMapSeries: Uses QHeightMapSurfaceDataProxy initialized with QImage from "mountain.png".
        - setValueRanges(): Maps image dimensions to X, Y, Z coordinate ranges.

  SqrtSinModel(QAbstractTableModel) defined within surfacegraph.py:
    Description: Custom model designed to provide data for the "SqrtSin" mathematical surface.
    Constructor:
      - Data Generation: Creates 1D NumPy arrays for X and Z coordinates (_x, _z).
      - Y-Value Calculation: Calculates Y (height) values using the formula y = (sin(R) / R + 0.24) * 1.61 (where R = sqrt(z*z + x*x)) and stores them in a 2D NumPy array (_data).
    Methods:
      - rowCount(): Returns the number of rows.
      - columnCount(): Returns the number of columns.
      - data(index, role): Returns values for custom roles (X_ROLE, Y_ROLE, Z_ROLE) mapped by QItemModelSurfaceDataProxy.
      - roleNames(): Exposes custom roles.

  QItemModelSurfaceDataProxy Setup:
    - m_sqrtSinProxy = QItemModelSurfaceDataProxy(self.m_sqrtSinModel, self)
    - setXPosRole("x"): Links proxy to custom 'x' role.
    - setYPosRole("y"): Links proxy to custom 'y' role.
    - setZPosRole("z"): Links proxy to custom 'z' role.

  Model Switching Slots:
    - enable_sqrt_sin_model():
      - Action: Removes current series, adds SqrtSin series.
      - Configuration: Reconfigures graph axes (titles, ranges, label formats).
      - UI Update: Updates UI sliders for axis range control.
    - enable_height_map_model():
      - Action: Removes current series, adds HeightMap series.
      - Configuration: Reconfigures graph axes (titles, ranges, label formats).
      - UI Update: Updates UI sliders for axis range control.

  UI Control Slots:
    - adjust_xmin(value), adjust_xmax(value), etc.: Updates axis ranges based on slider input.
    - change_theme(theme_index): Applies a selected Q3DTheme.
    - set_black_to_yellow_gradient(): Applies a predefined QLinearGradient.
    - set_green_to_red_gradient(): Applies a predefined QLinearGradient.
    - toggle_mode_none(), toggle_mode_item(), etc.: Changes the selectionMode of the graph.
```

--------------------------------

### PySide6 TrafficLightWidget Class UI Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/statemachine/trafficlight/README.md

Defines a QWidget subclass responsible for composing the UI of the traffic light. It instantiates three LightWidget instances (red, yellow, green) and arranges them vertically within a QVBoxLayout, setting a black background.

```APIDOC
TrafficLightWidget Class (subclass of QWidget):
  UI Setup:
    - Creates three instances of LightWidget: self._red_light, self._yellow_light, self._green_light, each initialized with its corresponding Qt.GlobalColor.
    - Arranges these LightWidgets vertically using a QVBoxLayout.
    - Sets a black background color for itself using QPalette.
```

--------------------------------

### Get Text Input with QInputDialog in PySide6

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/PySide6modern.md

Demonstrates how to use QInputDialog.getText to prompt the user for a single line of text input. This method is suitable for simple text entry scenarios, often used in 'Find' features.

```Python
QInputDialog.getText(parent, title, label)
```

--------------------------------

### Execute PySide6 RHI Example Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/rhi/simplerhiwidget/README.md

This bash command executes the `main.py` script located in the `examples/widgets/rhi/simplerhiwidget` directory, launching a PySide6 application that demonstrates RHI initialization and rendering of a rotating triangle.

```bash
python main.py
```

--------------------------------

### main.py Script API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/effects/blurpicker/README.md

API documentation for the `main.py` script, which serves as the entry point for the Blur Picker application, initializing the Qt application and displaying the `BlurPicker` window.

```APIDOC
main.py:
  Initializes QApplication.
  Creates BlurPicker instance.
  Sets window title and fixed size.
  Displays the BlurPicker window.
```

--------------------------------

### Execute PySide6 BorderLayout Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/borderlayout/README.md

This command executes the `borderlayout.py` script, launching the PySide6 application that demonstrates a custom BorderLayout. Ensure you are in the correct directory (`examples/widgets/layouts/borderlayout`) before running.

```bash
python borderlayout.py
```

--------------------------------

### PySide6 QtMultimedia API Reference for Screen Capture

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/screencapture/README.md

This section outlines the key PySide6 modules and classes used in the screen and window live capture example. It details their purpose and role in the application's functionality, covering multimedia capture, UI elements, and core application components.

```APIDOC
QtMultimedia:
  QScreenCapture: Captures the content of a QScreen as a video stream.
  QWindowCapture: Captures the content of a QWindow (via QCapturableWindow) as a video stream.
  QCapturableWindow: Represents a window that can be captured.
  QMediaCaptureSession: Manages the capture process, linking a capture source (like QScreenCapture or QWindowCapture) to outputs (like QVideoWidget).
  QMediaDevices: (used by ScreenListModel indirectly via QGuiApplication.screens()).
QtMultimediaWidgets:
  QVideoWidget: A widget used to display video content from QMediaCaptureSession.
QtWidgets:
  QApplication: Manages the application event loop.
  QWidget: (custom main class ScreenCapturePreview): The main application window.
  QListView: Used to display lists of available screens and windows.
  QLabel: For UI text labels.
  QPushButton: For starting and stopping the capture.
  QMessageBox: For displaying error messages related to window validity.
  Layout classes: (QGridLayout).
QtGui:
  QGuiApplication: Used for accessing screen and window lists.
  QScreen: Represents a system screen.
QtCore:
  QAbstractListModel: Base class for ScreenListModel and WindowListModel.
  QItemSelection, QModelIndex: For handling selections in QListView.
  Slot, Qt.
```

--------------------------------

### PySide6 Window Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/fetchmore/README.md

Documentation for the `Window` class, a subclass of `QWidget`, which serves as the main application window, displaying the file list and log viewer.

```APIDOC
Window (subclass of QWidget):
  Purpose: Main application window displaying the file list and log.
  UI:
    - _view: QListView to display FileListModel contents.
    - _log_viewer: QPlainTextEdit for fetching activity messages.
  Initialization:
    - Sets initial path (e.g., QDir.rootPath()) for FileListModel.
  Interaction:
    - activated (QListView signal): Connected to activated slot in Window.
    - activated (slot):
      - If item is a directory, calls _model.set_dir_path() to load new directory.
      - Clears log and resets fetch process.
  Logging:
    - update_log (slot): Receives info from model's number_populated signal and appends to log viewer.
```

--------------------------------

### Run PySide6 Digital Clock Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgets/digitalclock/README.md

Instructions to execute the PySide6 digital clock script from the command line.

```Bash
python digitalclock.py
```

--------------------------------

### Run PySide6 Spreadsheet Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/spreadsheet/README.md

Instructions on how to execute the PySide6 spreadsheet application from the command line after navigating to the correct directory.

```Bash
python main.py
```

--------------------------------

### Run PySide6 Interactive Gaussian Plot Script

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/external/matplotlib/widget_gaussian/README.md

This command executes the main Python script for the interactive Gaussian plot application. Ensure Matplotlib, NumPy, and SciPy are installed in your Python environment before running.

```Bash
python widget_gaussian.py
```

--------------------------------

### PySide6 QtCharts Bar Chart API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/barchart/README.md

Detailed API usage for creating a grouped bar chart using PySide6's QtCharts module, covering key classes, setup, data handling, axis configuration, and legend management.

```APIDOC
Key PySide6 Modules and Classes:
  QtCharts:
    QChartView: The widget used for displaying the chart.
    QChart: The core class representing the chart object.
    QBarSeries: The series type used for creating bar charts. It holds one or more QBarSet objects.
    QBarSet: Represents a single set of bars within a QBarSeries. In a grouped bar chart, each category will have one bar from each QBarSet.
    QBarCategoryAxis: Used for the X-axis to display category names (e.g., months).
    QValueAxis: Used for the Y-axis to display numerical values.
  QtWidgets:
    QApplication: Manages the application's event loop and overall execution.
    QMainWindow: Serves as the main window for displaying the chart view.
  QtGui:
    QPainter: Its RenderHint.Antialiasing enum value is used to enable anti-aliasing for smoother chart rendering.
  QtCore:
    Qt: Namespace for various enums, such as alignment flags (Qt.AlignBottom, Qt.AlignLeft) used for axes and legend positioning.

Chart Creation and Customization:
  Basic Setup:
    QChart(): Instantiates a QChart object.
    QChartView(chart): Creates a QChartView, passing the QChart object.
    chart.setTitle("Simple barchart example"): Sets the chart's title.
    chart.setAnimationOptions(QChart.SeriesAnimations): Enables series animations for visual feedback.
    chart_view.setRenderHint(QPainter.RenderHint.Antialiasing): Enables antialiasing on the QChartView.
  Data - Bar Sets (QBarSet):
    QBarSet("Label"): Creates multiple QBarSet instances, each representing a distinct data series and labeled.
    set_x.append([val1, val2, ...]): Appends numerical data to each QBarSet.
  Series (QBarSeries):
    QBarSeries(): Creates a QBarSeries object.
    series.append(set_x): Appends previously created QBarSet objects to the QBarSeries.
  Adding Series to Chart:
    chart.addSeries(series): Adds the QBarSeries (containing all bar sets) to the QChart object.
  Axes:
    Category Axis (X-axis):
      QBarCategoryAxis(): Instantiates a QBarCategoryAxis.
      axis_x.append(categories): Appends category names (e.g., ["Jan", "Feb", ...]) to the axis.
      chart.addAxis(axis_x, Qt.AlignBottom): Adds the category axis to the chart, aligned to the bottom.
      series.attachAxis(axis_x): Attaches the bar series to this X-axis.
    Value Axis (Y-axis):
      QValueAxis(): Instantiates a QValueAxis.
      axis_y.setRange(0, 15): Explicitly sets the numerical range for the Y-axis.
      chart.addAxis(axis_y, Qt.AlignLeft): Adds the value axis to the chart, aligned to the left.
      series.attachAxis(axis_y): Attaches the bar series to this Y-axis.
  Legend:
    chart.legend().setVisible(True): Makes the chart's legend visible.
    chart.legend().setAlignment(Qt.AlignBottom): Aligns the legend to the bottom of the chart.
  Bar Appearance:
    Relies on the default coloring scheme provided by QtCharts. Individual colors for bar sets are not explicitly set in this example.
```

--------------------------------

### Essential QML QtQuick3D Types for 3D Scene Construction

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/intro/README.md

This outlines the primary Qt Quick 3D QML types used to build and display the 3D scene. It includes components for the 3D view, environment settings, camera, lighting, 3D models, and their materials.

```APIDOC
View3D: The root item for displaying a 3D scene.
SceneEnvironment: Configures global scene properties like background color and rendering effects.
PerspectiveCamera: Defines the viewpoint and projection for the 3D scene.
DirectionalLight: A light source that casts parallel rays, illuminating the scene.
Model: Represents a 3D object to be rendered.
  source: Can refer to built-in primitive meshes (like "#Cylinder", "#Sphere") or external 3D model files.
DefaultMaterial: A simple material with basic properties like diffuseColor.
```

--------------------------------

### Execute PySide6 QML Attached Properties Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced5-Attached-properties/README.md

Provides the necessary steps to run the PySide6 example demonstrating attached properties, including navigating to the correct directory and executing the main Python script.

```Bash
python main.py
```

--------------------------------

### Run PySide6 Colliding Mice Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/collidingmice/README.md

Instructions to execute the PySide6 'Colliding Mice' simulation script from the command line after navigating to the example directory.

```bash
python collidingmice.py
```

--------------------------------

### PySide6 QGraphicsScene and QGraphicsView Setup

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/animation/appchooser/README.md

Details the setup of the `QGraphicsScene` and `QGraphicsView` for displaying interactive icons, including background color, scrollbar settings, and the initial placement of `Pixmap` instances.

```APIDOC
Scene Setup:
  - A QGraphicsScene is created with a white background.
  - A QGraphicsView displays this scene. Scrollbars are turned off, and frame style is minimal.
  - Four instances of Pixmap (p1, p2, p3, p4) are created using different icon images loaded from resources.
  - They are given initial geometries (positions and 64x64 size) and added to the scene.
```

--------------------------------

### Run PySide6 Painter Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/painting/painter/README.md

Execute the Python script for the PySide6 painter example from the command line after navigating to the correct directory. This command launches the GUI application.

```Bash
python painter.py
```

--------------------------------

### PySide6 Modules and Classes for QtCharts Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointselectionandmarkers/README.md

Overview of key PySide6 modules and classes used in the Point Selection and Custom Markers example, detailing their roles in chart display, UI interaction, graphics rendering, and core application management.

```APIDOC
QtCharts:
  QChartView: The widget used for displaying the chart.
  QChart: The core class representing the chart object.
  QSplineSeries: The series type used, which supports setLightMarker and setSelectedLightMarker properties for custom image markers.
  (Implicitly QValueAxis via QChart.createDefaultAxes()).
QtWidgets:
  QApplication: Manages the application's event loop.
  QMainWindow: Serves as the main window.
  QWidget: Used as a container for UI controls.
  QComboBox: For selecting different marker styles and line colors.
  QCheckBox: For toggling the visibility of unselected point markers.
  QLabel: For descriptive text in the UI.
  QGridLayout, QHBoxLayout: For arranging UI elements.
QtGui:
  QPainter: Its RenderHint.Antialiasing is used for smoother chart rendering. It's also used in utilities.py to draw custom marker images.
  QImage: Used to create or load custom markers that are then applied to the series.
  QColor: For specifying colors for programmatically generated markers and series lines.
QtCore:
  Slot: Decorator for methods connected to UI element signals and series events.
  QPointF: Represents data points (x, y coordinates) for the QSplineSeries.
  Qt: Namespace for enums like Qt.CheckState.
  (The Qt Resource System is used for loading some marker images).
```

--------------------------------

### FastAPI Endpoint: Retrieve All Finance Entries

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Implements a GET endpoint to retrieve all finance entries from the database. Supports optional pagination parameters `skip` and `limit` to control the number of results. Returns a JSON object containing the total count and a list of finance items.

```APIDOC
GET /finances/
  Parameters:
    skip: integer (optional, default: 0)
      Description: Number of items to skip
    limit: integer (optional, default: 100)
      Description: Maximum number of items to return
  Responses:
    200 OK:
      Content-Type: application/json
      Schema:
        total: integer
        items: array of FinanceRead
          - id: integer
            amount: float
            description: string
            date: string
    500 Internal Server Error:
      Description: Database or server error
```

--------------------------------

### PySide6 QtSql and QtWidgets API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/sql/relationaltablemodel/README.md

Reference for key PySide6 modules and classes used in the QSqlRelationalTableModel example, including their purpose and typical usage.

```APIDOC
PySide6.QtSql:
  QSqlDatabase: For establishing the in-memory SQLite database connection.
  QSqlRelationalTableModel: The core model for handling and displaying tables with foreign keys.
  QSqlRelation: Defines a relationship between a foreign key in one table and the primary key/display column of another table.
  QSqlRelationalDelegate: An item delegate that provides appropriate editors (e.g., QComboBox) for fields that are foreign keys managed by QSqlRelationalTableModel.
  QSqlQuery: Used for database schema creation (creating tables) and initial data population (inserting rows).

PySide6.QtWidgets:
  QApplication: Manages the application event loop.
  QTableView: Used to display the data from the QSqlRelationalTableModel.

PySide6.QtCore:
  Qt: (for enums like Qt.Orientation).
  QObject: (used for tr() in header data, though not strictly necessary for this example's string literals).
```

--------------------------------

### PySide6 Main Application Runner API

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/editingmodel/README.md

Describes the `main.py` script, which initializes the PySide6 application, registers the `BaseModel` with QML, and loads the main QML UI.

```APIDOC
# Application Setup
QGuiApplication # Initializes the GUI application
QQmlApplicationEngine # Manages QML components

# Model Registration
@QmlElement # Decorator on BaseModel for automatic QML registration
engine.addImportPath(Path(__file__).parent) # Ensures QML engine finds Python module

# QML Loading
engine.load("main.qml") # Loads the main QML user interface
```

--------------------------------

### PySide6.QtTextToSpeech Module API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Documentation for key classes within the PySide6.QtTextToSpeech module, including QTextToSpeech for speech synthesis and QVoice for voice representation.

```APIDOC
PySide6.QtTextToSpeech:
  QTextToSpeech: The main class for interacting with text-to-speech engines, synthesizing speech, and controlling playback.
  QVoice: Represents a specific voice available for synthesis, characterized by name, gender, and age.
```

--------------------------------

### Running the PySide6 QML Inheritance Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced2-Inheritance-and-coercion/README.md

This command provides instructions on how to execute the PySide6 example demonstrating QML inheritance and type coercion. Users should navigate to the specified directory and run the main Python script to observe the behavior.

```Bash
python main.py
```

--------------------------------

### Main Application Entry Point API Reference (PySide6)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/statemachine/rogue/README.md

Describes the standard Python entry point for the PySide6 application, including `QApplication` instantiation, `MainWindow` creation, and event loop execution.

```APIDOC
if __name__ == '__main__':
  - Creates QApplication instance.
  - Creates and shows an instance of MainWindow.
  - Starts the event loop (app.exec()).
```

--------------------------------

### PySide6 QtCharts Key Modules and Classes API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointconfiguration/README.md

This section provides an overview of the essential PySide6 modules and classes utilized in the per-point configuration example, detailing their purpose and role within the application's architecture. It covers components from QtCharts, QtWidgets, QtGui, and QtCore.

```APIDOC
QtCharts:
  QChartView: The widget used for displaying the chart.
  QChart: The core class representing the chart object.
  QLineSeries: The series type used, whose individual points are configured.
  QXYSeries.PointConfiguration: An enum used as a key to specify which visual property of a point (e.g., Color, Size, LabelVisibility, LabelFormat) is being set.
  (Implicitly QValueAxis via QChart.createDefaultAxes()).
QtWidgets:
  QApplication: Manages the application's event loop.
  QMainWindow: The main application window class (ChartWindow).
  QWidget: Used as a container for UI controls and for the main layout.
  QComboBox: Used for selecting predefined colors and sizes for a point.
  QCheckBox: Used for toggling the visibility of a point's label.
  QLineEdit: Used to display the coordinates of the selected point and to input a custom label for it.
  QLabel: For descriptive text in the UI.
  QGridLayout, QHBoxLayout: For arranging UI elements.
QtGui:
  QPainter: Its RenderHint.Antialiasing is used for smoother chart rendering.
  QColor: Used in conjunction with the color selection QComboBox.
  QIcon: Used with QComboBox items (though no actual icons are loaded in this example, it's part of the addItem signature used).
QtCore:
  Slot: Decorator for methods connected to UI element signals or chart signals.
  QPointF: Represents data points (x, y coordinates) for the QLineSeries.
```

--------------------------------

### PySide6 QtWidgets Module API (Relevant Classes)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/axcontainer/axviewer/README.md

Provides an overview of key classes from the `QtWidgets` module utilized in the ActiveX viewer example, including `QApplication`, `QMainWindow`, `QToolBar`, `QMessageBox`, and `QDialog`.

```APIDOC
QtWidgets:
  QApplication:
    Purpose: Manages the application's lifecycle and event loop.
  QMainWindow:
    Purpose: Serves as the main application window, providing a framework for building application user interfaces.
  QToolBar:
    Purpose: Provides a movable panel that contains a set of tool buttons.
  QMessageBox:
    Purpose: Provides a modal dialog box for informing the user or asking the user a question.
  QDialog:
    Purpose: The base class of dialog windows.
```

--------------------------------

### PySide6 Core Component Usage

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/painting/painter/README.md

Summarizes the key PySide6 and Qt components demonstrated in the Painter example, highlighting their roles in implementing custom drawing, event handling, and UI construction.

```APIDOC
Core Components:
  QPainter:
    - Used for all drawing operations on QWidget and QPixmap.
    - Methods: drawLine(), setPen(), setRenderHints().
  QWidget.paintEvent():
    - Standard method for custom painting on a widget.
  Mouse Event Handling:
    - mousePressEvent(event: QMouseEvent)
    - mouseMoveEvent(event: QMouseEvent)
    - mouseReleaseEvent(event: QMouseEvent)
    - Overridden for interactive drawing.
  QPixmap:
    - Used as an off-screen drawing buffer (canvas).
  QPen:
    - Configures line properties: width, color, cap style (Qt.PenCapStyle.RoundCap), join style (Qt.PenJoinStyle.RoundJoin).
  QMainWindow:
    - Main application window container.
  QToolBar:
    - Provides actions for UI controls (Save, Open, Clear, Color).
  QAction:
    - Represents an action in menus or toolbars.
  QFileDialog:
    - Standard dialog for file open/save operations.
  QColorDialog:
    - Standard dialog for color selection.
  QStandardPaths:
    - Used to get sensible default directories (e.g., PicturesLocation).
```

--------------------------------

### PySide6 SQL Books Database API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/sql/books/README.md

Overview of key PySide6 modules and classes used in the SQL 'Books' database example, detailing their roles in database interaction, UI display, and custom delegation.

```APIDOC
PySide6.QtSql:
  QSqlDatabase: For establishing and managing the SQLite database connection.
  QSqlRelationalTableModel: An editable SQL model that supports foreign key relationships.
  QSqlRelation: Defines a relationship between a foreign key in one table and a primary key in another, allowing display of human-readable values.
  QSqlRelationalDelegate: Provides views (like QTableView) with default editors (typically QComboBox) for fields that are foreign keys.
  QSqlTableModel: (base for QSqlRelationalTableModel, providing edit strategies like OnManualSubmit).
  QSqlQuery: Used in createdb.py for executing DDL (table creation) and DML (data insertion) statements.

PySide6.QtWidgets:
  QApplication: Manages the application event loop.
  QMainWindow (custom BookWindow class): The main application window.
  QTableView: To display and edit the book data.
  QStyledItemDelegate: (base for QSqlRelationalDelegate).
  QDataWidgetMapper: To map data from the model to individual editor widgets.
  QDialogButtonBox:
  QMessageBox: (for "About" dialog).
  Editor Widgets used by QDataWidgetMapper:
    QLineEdit: (for title).
    QSpinBox: (for year).
    QComboBox: (for author and genre, populated by the relational model).
  QSpinBox: (also used directly by BookDelegate for editing year in table).

PySide6.QtGui: (Primarily for BookDelegate)
  QPainter: For custom drawing of stars.
  QPixmap: To load star images from resources.
  QKeySequence: For "About" action shortcut.

PySide6.QtCore:
  Slot:
  Qt: (for enums like Orientation, ItemDataRole, State).
  QModelIndex:

Resource System (books.qrc): For embedding star images (star.svg, star-filled.svg).
```

--------------------------------

### MainWindow Class: Main Application Window

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/settingseditor/README.md

Defines the primary application window, managing menus, settings objects, and central widget display.

```APIDOC
MainWindow(QMainWindow):
  Description:
    - The main application window.
    - Manages the current QSettings object and passes it to the SettingsTree.

  Components:
    - SettingsTree instance (central widget)

  Functionality:
    - Sets up menus with actions:
      - "Open Application Settings..."
      - "Open INI File..."
      - "Open macOS Property List..."
      - "Open Windows Registry Path..."
      - Refresh
      - Toggle options
      - Exit
    - Provides slots to handle menu actions, including creating a LocationDialog to get parameters for application-specific settings.
```

--------------------------------

### MainWindow Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/contextinfo/README.md

Describes the `MainWindow` class, a `QWidget` subclass that serves as the main UI, integrating the `RenderWindow` and displaying application and OpenGL context information.

```APIDOC
MainWindow (subclass of QWidget - Main UI):
  - __init__():
    - Description: Constructs the main application UI.
    - Details: Creates a QPlainTextEdit (read-only) for displaying context information. Creates an instance of RenderWindow with a default QSurfaceFormat. Embeds the RenderWindow (which is a QWindow) into the QWidget-based layout using container = QWidget.createWindowContainer(self._render_window). Arranges the QPlainTextEdit and the container in an QHBoxLayout.
  - update_description():
    - Description: Populates the info display with system and OpenGL details.
    - Details: Called after MainWindow is shown. Retrieves Qt build info (QLibraryInfo.build()), Python version, and the OpenGL context information from self._render_window.glInfo(). Sets the combined information as plain text in the QPlainTextEdit.
```

--------------------------------

### PySide6 Key Modules and Classes API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/network/blockingfortuneclient/README.md

Detailed breakdown of PySide6 modules and classes used in the Blocking Fortune Client example, including their primary functions and relationships.

```APIDOC
QtWidgets:
  QApplication: Manages the application event loop.
  QWidget (custom main class BlockingClient): The main UI window.
  QLabel: For status messages and displaying the received fortune.
  QLineEdit: For host and port input by the user.
  QPushButton: For "Get Fortune" and "Quit" actions.
  QDialogButtonBox: Manages the action buttons.
  QGridLayout: For arranging UI elements.
  QMessageBox: For displaying error messages.
QtNetwork:
  QTcpSocket: Used for TCP client communication.
  QHostAddress: For resolving hostnames and network interface information.
  QNetworkInterface: Used to suggest a default local IP address in the host input field.
  QAbstractSocket.SocketError: Enum for socket error codes.
QtCore:
  QThread: Subclassed as FortuneThread to handle network operations off the main UI thread.
  Signal: For communication from FortuneThread back to BlockingClient (e.g., new_fortune, error).
  Slot: Decorator for methods connected to signals or UI events.
  QDataStream: For reading structured binary data (size-prefixed string) from the QTcpSocket.
  QMutex: Used within FortuneThread to manage its execution flow and access to shared parameters.
  QMutexLocker: Used within FortuneThread to manage its execution flow and access to shared parameters.
  QWaitCondition: Used within FortuneThread to manage its execution flow and access to shared parameters.
QtGui:
  QIntValidator: Used to validate port number input in the QLineEdit.
```

--------------------------------

### PySide6 QWizard: Adding Pages Sequentially

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/dialogs/trivialwizard/README.md

Demonstrates how to add pre-configured QWizardPage instances to a QWizard object, defining the sequential navigation order for a multi-step wizard.

```python
wizard.addPage(create_intro_page())
wizard.addPage(create_registration_page())
wizard.addPage(create_conclusion_page())
```

--------------------------------

### Run PySide/Shiboken Example Python Module

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/doc/samplebinding.rst

Command to execute the main Python script of the PySide/Shiboken example, demonstrating the usage of derived Icecream types and a delivery truck simulation after successful compilation.

```bash
python main.py
```

--------------------------------

### APIDOC: MainWindow Class (QMainWindow UI Setup)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/editabletreemodel/README.md

Documents the `MainWindow` class, a `QMainWindow` responsible for setting up the application's user interface. It describes the integration of `QTreeView`, menu actions, status bar, and an optional model tester.

```APIDOC
MainWindow Class (mainwindow.py)
  Inherits: QMainWindow
  Description: Sets up the application's user interface.
  UI Components:
    QTreeView:
      Central widget, configured to display the TreeModel.
      Features: alternating row colors, item selection behavior, scroll modes.
      Initial State: view.expandAll() called to display full tree.
      Post-Model Setup: Columns resized to their contents.
  Menus and Actions:
    File Menu:
      Exit Action: Connected to application exit.
    Actions Menu:
      Insert Row Action
      Insert Column Action
      Remove Row Action
      Remove Column Action
      Insert Child Action
      Connection: Actions are connected to slots in MainWindow that call corresponding methods on the TreeModel or interact with QTreeView's selection model to determine operation context.
  Status Bar:
    Displays information about the currently selected item's position.
  Development Tools:
    QAbstractItemModelTester:
      Optional (if "-t" command-line argument is passed).
      Helps validate the custom model's implementation during development.
```

--------------------------------

### Execute PySide6 Editable Tree Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/editabletreemodel/README.md

Instructions for running the provided PySide6 editable tree model example. This involves navigating to the project directory and executing the main Python script, with an optional flag to enable a model tester for debugging.

```Bash
python main.py
python main.py -t
```

--------------------------------

### Executing the PySide6 WigglyWidget Example Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgetbinding/README.md

This command runs the main PySide6 application script, which initializes the UI and displays both the C++-backed and pure Python WigglyWidgets in action.

```Shell
python main.py
```

--------------------------------

### Python: Running the Generated Binding Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/README.md

This command executes the main Python script after the build process. It assumes the compiled `Universe` Python module and `libuniverse` shared library are placed in the example's root directory, allowing the script to import and use the C++ bindings.

```python
python main.py
```

--------------------------------

### PySide6 Resource System API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/systray/README.md

Details on embedding resources like icons using Qt's Resource System for PySide6 applications.

```APIDOC
systray.qrc:
  - Resource collection file.
  - Embeds icon images (bad.png, heart.png, trash.png) used for the tray icon.
rc_systray.py (generated):
  - Python module for accessing embedded resources.
```

--------------------------------

### Camera Class: Settings Dialogs (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Explains the slots responsible for opening various configuration dialogs. These include general capture settings, as well as specific dialogs for image and video capture parameters.

```APIDOC
Camera Class UI Interaction:
  Settings:
    - configureCaptureSettings() slot: Opens capture settings dialog.
    - configureImageSettings() slot: Opens ImageSettings dialog.
    - configureVideoSettings() slot: Opens VideoSettings dialog.
```

--------------------------------

### PySide6 Modules and Classes for Draggable Text Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/draganddrop/draggabletext/README.md

Overview of key PySide6 modules and classes used in the draggable text example, detailing their roles in managing application events, UI elements, drag-and-drop operations, and resource handling.

```APIDOC
*   PySide6.QtWidgets:
    *   QApplication: Manages the application event loop.
    *   QWidget (custom main class DragWidget): The container for draggable labels and the drop target.
    *   QLabel (subclassed as DragLabel): Used for the individual draggable words.
    *   QFrame (used by DragLabel for styling).

*   PySide6.QtGui:
    *   QDrag: The core class for managing drag-and-drop operations.
    *   QMimeData: Container for the dragged text and hotspot data.
    *   QMouseEvent, QDragEnterEvent, QDropEvent: For event handling related to mouse interaction and drag-and-drop.
    *   QPixmap: For creating the drag cursor image (a render of the label).
    *   QPalette: For styling the DragWidget background.

*   PySide6.QtCore:
    *   Qt (for MouseButton, DropAction enums, AlignmentFlag).
    *   QPoint: For handling positions and hotspots.
    *   QByteArray, QIODevice (implicitly by QMimeData and QDataStream, though QDataStream is not explicitly used here for setText).
    *   QFile, QTextStream: For reading words from the text file resource.

*   Resource System:
    *   draggabletext.qrc: Embeds words.txt.
    *   draggabletext_rc.py (generated): Python module for accessing the resource.
```

--------------------------------

### Install Libraries and Bindings Module (CMake)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgetbinding/CMakeLists.txt

This section handles the installation of the compiled libraries and the Python bindings module. It installs the target libraries and any collected Shiboken shared libraries directly into the source directory, ensuring that the Python interpreter can successfully import the modules without requiring manual PATH configuration.

```CMake
install(TARGETS ${bindings_library} ${wiggly_library}
        LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        )
install(FILES ${windows_shiboken_shared_libraries} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
```

--------------------------------

### PySide6 QtMultimedia Key Concepts

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

This section outlines fundamental concepts for building camera applications with QtMultimedia. It covers the central role of QMediaCaptureSession, methods for device enumeration and dynamic configuration, the asynchronous nature of capture operations, UI integration strategies, platform-specific considerations for permissions, and metadata handling.

```APIDOC
QMediaCaptureSession:
  Role: Central class coordinating camera device, audio input, viewfinder, image capture, and video recording.
  Importance: Key to understanding the example's architecture.

Device Enumeration and Selection:
  Method: Using QMediaDevices to find available cameras.
  Purpose: Populating UI choices for camera selection.

Dynamic Configuration:
  Process: Querying hardware for supported formats, resolutions, codecs.
  Application: Dynamically populating settings dialogs.
  Target: Settings applied to QCamera, QImageCapture, and QMediaRecorder.

Asynchronous Operations:
  Nature: Image capture and video recording are asynchronous.
  Management: Signals used to manage state and provide feedback.
  Examples of Signals: imageCaptured, imageSaved, recorderStateChanged, durationChanged, error signals.

UI Integration:
  Method: Using .ui files (loaded by generated Python files) for UI layout.
  Logic: Connecting UI elements to Python slots for application logic.

Platform Considerations:
  Scope: Includes checks for Android/macOS.
  Purpose: Handling permissions for camera and microphone.

Metadata:
  Demonstration: Setting various metadata fields for video recordings.
```

--------------------------------

### PySide6 Core UI Components and Features

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/mainwindows/application/README.md

This section outlines the primary PySide6 classes and concepts utilized in the example application. It covers fundamental UI elements, file handling, settings management, and the signal-slot mechanism for event handling.

```APIDOC
QMainWindow: The base class for creating applications with menus, toolbars, and a status bar.
QTextEdit: The central widget for text editing.
QAction: For defining user-invokable commands that can be added to menus and toolbars.
QMenu, QMenuBar, QToolBar, QStatusBar: Standard components for building the main window structure.
QFileDialog: For native open and save file dialogs.
QFile, QSaveFile, QTextStream: For file input/output operations.
QMessageBox: For displaying standard dialogs like warnings or information messages.
QSettings: For persisting application settings (like window geometry).
QIcon.fromTheme: For using system theme icons with fallbacks to bundled resources.
Qt Resource System (.qrc): Used to embed image files for icons directly into the application.
Signals and Slots: Extensively used for connecting UI elements to application logic.
```

--------------------------------

### PySide6 Core Modules and Classes for Web Browser

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/webenginewidgets/widgetsnanobrowser/README.md

Overview of essential PySide6 modules and classes used in the Nano Browser example, detailing their roles in web rendering, UI management, and data handling.

```APIDOC
PySide6.QtWebEngineWidgets:
  QWebEngineView: The core widget for rendering web content.
PySide6.QtWebEngineCore:
  QWebEnginePage: Represents a web page within the view. Accessed via QWebEngineView.page(). Used here to trigger navigation actions (Back, Forward) and connect to signals like titleChanged and urlChanged.
PySide6.QtWidgets:
  QApplication: Manages the application event loop.
  QMainWindow (custom MainWindow class): Provides the main application window structure.
  QLineEdit: Used as the address bar for URL input and display.
  QToolBar: Hosts the navigation buttons and address bar.
  QPushButton: Used for the Back and Forward navigation buttons.
PySide6.QtGui:
  QIcon: Used to set icons for the navigation buttons (from Qt's standard themes).
PySide6.QtCore:
  QUrl: For handling and parsing URLs.
  Slot: For defining slot methods.
```

--------------------------------

### PySide6.QtGui API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/systray/README.md

Classes from PySide6.QtGui for handling graphical elements, icons, and window events.

```APIDOC
QIcon:
  - Used for setting the tray icon image and icons for actions or balloon messages.
QCloseEvent:
  - Handled in Window.closeEvent() for "minimize to tray" functionality.
```

--------------------------------

### APIDOC: QML Finance Pie Chart (FinancePieChart.qml)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Documentation for the QML component that visualizes finance data as a pie chart.

```APIDOC
FinancePieChart.qml (QML Component)
  Visualization: Pie Chart

  Data Source: finance_model.getCategoryData() (Python FinanceModel method)
  Description: Displays a pie chart based on summarized costs per category.
```

--------------------------------

### Main Application Entry Point (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/dialogs/classwizard/README.md

Documents the standard Python entry point for the `ClassWizard` application, demonstrating how the `QApplication` and `ClassWizard` instances are created to launch the wizard.

```APIDOC
Main Application (`classwizard.py`):
  if __name__ == "__main__":
    - Creates QApplication instance.
    - Creates an instance of ClassWizard.
```

--------------------------------

### Install SQLAlchemy for PySide6 Finance Manager

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/part2/README.md

Install the SQLAlchemy library, a crucial dependency for the PySide6 finance manager application's database integration. This step ensures the application can interact with the SQLite database for persistent storage. Users can choose to install directly or via a requirements file.

```bash
pip install sqlalchemy
# or pip install -r requirements.txt
```

--------------------------------

### Execute PySide6 QML Data Exposure Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/properties/README.md

This bash command runs the main Python script (`main.py`) which initializes the PySide6 application, loads the QML component, and demonstrates accessing structured data defined in Python from QML and then back in Python.

```bash
python main.py
```

--------------------------------

### VideoSettingsDialog Class (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

A `QDialog` designed for configuring video recording settings. It allows users to adjust parameters related to video capture.

```APIDOC
VideoSettingsDialog Class (QDialog):
  - Located in videosettings.py.
  - UI from videosettings.ui or videosettings_mobile.ui.
  - Purpose: Configuration of video recording settings.
```

--------------------------------

### PySide6.QtCore API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/systray/README.md

Core classes and decorators from PySide6.QtCore for signal/slot mechanisms and fundamental Qt types.

```APIDOC
Slot:
  - Decorator for defining slot methods.
Qt:
  - Provides various enums (e.g., Qt.WindowFlags, though not explicitly used for flags in this example).
```

--------------------------------

### PySide6 MainWindow Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/threadedqopenglwidget/README.md

API documentation for the `MainWindow` class, a `QWidget` subclass that demonstrates the integration of multiple `GLWidget` instances, each with its own threaded renderer.

```APIDOC
MainWindow Class (subclass of QWidget in mainwindow.py):
  - Creates a layout and adds two instances of GLWidget side-by-side.
  - Demonstrates multiple QOpenGLWidget's with their own threaded renderers.
```

--------------------------------

### CMake Configuration for Shiboken Python Bindings

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/README.md

Outlines the CMake setup for building the C++ library (`libuniverse`) and the Python extension module (`Universe`) using Shiboken. It details project setup, C++ compilation, manual Shiboken invocation, and linking steps.

```APIDOC
Project Setup: Defines project name "SampleBinding", C++ standard.

C++ Library Target (libuniverse):
  Compiles icecream.cpp and truck.cpp into a shared library named libuniverse.
  target_compile_definitions(${sample_library} PRIVATE BINDINGS_BUILD) is used with macros.h for symbol export.

Shiboken Invocation (Manual Setup):
  The CMake script manually locates a Python interpreter and uses a utility script (../utils/pyside_config.py) to find Shiboken paths, include directories, and necessary linker flags.
  An add_custom_command is used to execute shiboken6 (the Shiboken generator executable).
    Inputs: bindings.h (the wrapped header) and bindings.xml (the typesystem file).
    Output: Generated C++ wrapper files (e.g., universe_module_wrapper.cpp, icecream_wrapper.cpp, truck_wrapper.cpp) in the build directory.

Python Extension Module Target (Universe):
  An add_library(... MODULE ...) command compiles the Shiboken-generated C++ wrapper files into a Python extension module.
  This target is linked against the libuniverse C++ library and necessary Python and Shiboken libraries.
```

--------------------------------

### QML Root UI Setup and Python Service Integration

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/demos/colorpaletteclient/README.md

Describes how the main QML file initializes and integrates Python backend services like RestService and its associated resource objects, managing the initial view flow between server selection and color display.

```APIDOC
ColorPalette/Main.qml Setup:
  - Instantiates Python RestService.
  - Declares PaginatedColorUsersResource, PaginatedColorsResource, and BasicLogin Python objects as children of RestService (linking them to access manager and API factory).
  - Initially displays ServerSelection.qml for base URL configuration.
  - Upon server selection, transitions to ColorView.qml, passing references to Python resource objects (e.g., colors, users, colorLogin).
```

--------------------------------

### PySide6 Key Modules and Classes for Standard Dialogs

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/dialogs/standarddialogs/README.md

Overview of essential PySide6 modules and classes used in the standard dialogs example, detailing their purpose and specific standard dialog classes for UI interaction.

```APIDOC
PySide6.QtWidgets:
  QApplication: Manages the application event loop.
  QDialog: The main container for the example.
  QToolBox: To organize different categories of standard dialog demonstrations.
  QPushButton: To launch each standard dialog.
  QLabel: To display the results or chosen values from the dialogs.
  QGroupBox: For grouping dialog-specific option checkboxes.
  QCheckBox: For toggling dialog options.
  Standard Dialog Classes:
    QErrorMessage: For displaying error messages that the user can choose not to see again.
    QFileDialog: For selecting files (open single, open multiple, save) or directories (getExistingDirectory).
    QFontDialog: For selecting a font and its attributes.
    QColorDialog: For selecting a color.
    QInputDialog: For getting simple user input (text, integer, double, item from a list).
    QMessageBox: For displaying informational, warning, critical messages, or asking questions with standard/custom buttons.
PySide6.QtCore:
  Slot: For defining slot methods.
  Qt: For various enums (e.g., Qt.AlignmentFlag).
  QDir: Used with QFileDialog for default paths.
  QStandardPaths: Used by QFileDialog in the example to get default pictures location.
PySide6.QtGui:
  QFont, QPalette, QColor, QBrush: Used implicitly or explicitly by dialogs and for UI styling.
  QImageWriter: Used by QFileDialog to list supported mime types for saving.
```

--------------------------------

### PySide6 QtCharts Module and Class Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/areachart/README.md

Reference for key PySide6 modules and classes used in QtCharts examples, detailing their purpose and relevant sub-classes or enums.

```APIDOC
QtCharts:
  QChartView: The widget responsible for displaying the chart.
  QChart: The core class representing the chart object itself.
  QAreaSeries: The series type used to create area charts.
  QLineSeries: Used to define the boundary lines for the `QAreaSeries`.
  QValueAxis: (Used implicitly via `QChart.createDefaultAxes()`).

QtWidgets:
  QApplication: Manages the application's event loop and overall execution.
  QMainWindow: Serves as the main window for displaying the chart view.

QtGui:
  QPainter: Its `RenderHint.Antialiasing` enum value is used to enable anti-aliasing for smoother chart rendering.
  QPen: Used to define the style (color, width) of the lines and borders in the chart.
  QLinearGradient: A type of `QBrush` used to fill the area of the `QAreaSeries` with a color gradient.
  QGradient: The base class for gradients; `QGradient.ObjectBoundingMode` is used to define the gradient's coordinate system.
  QColor: Used implicitly when defining colors for pens and gradients.

QtCore:
  QPointF: Represents a point with floating-point precision, used to define data points for the `QLineSeries`.
  Qt: Namespace for various enums, including `Qt.Orientation` used to access default axes.
```

--------------------------------

### main.py Application Entry Point

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/network/googlesuggest/README.md

Documentation for the main application runner script, responsible for initializing the PySide6 application, creating the `SearchBox` UI, and starting the event loop.

```APIDOC
main.py (Application Runner)
  Description: The entry point for the PySide6 application.

  Execution Flow:
    1. Initializes QApplication.
    2. Creates an instance of SearchBox.
    3. Shows the SearchBox window.
    4. Starts the Qt event loop.
```

--------------------------------

### Console Output from PySide6 QML Grouped Properties Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced4-Grouped-properties/README.md

This is an example of the console output produced by running the PySide6 QML grouped properties example. It demonstrates the successful retrieval and processing of nested QML properties within the Python script, including identifying specific guest details.

```text
Bob Jones is having a birthday!
He is inviting:
    Leo Hodges
    Jack Smith
    Anne Brown
Anne Brown is wearing the best shoes!
```

--------------------------------

### PySide6 FileListModel API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/fetchmore/README.md

Documentation for the `FileListModel` class, a subclass of `QAbstractListModel`, responsible for managing and incrementally loading file system data for display.

```APIDOC
FileListModel (subclass of QAbstractListModel):
  Purpose: Manages and incrementally loads file system data for display in a QListView.
  Data Handling:
    set_dir_path(path: str):
      - Uses QDir.entryInfoList() to get a complete list of files/subdirectories.
      - Stores full list internally (self._file_list).
      - Initially exposes only a portion; self._file_count tracks visible items.
      - Emits beginResetModel() / endResetModel() to signal full model change.
  rowCount(parent: QModelIndex) -> int:
    - Returns self._file_count (number of items currently exposed to the view).
  data(index: QModelIndex, role: int) -> Any:
    - Provides display name, icon, background color for items up to self._file_count.
    - Background color alternates for different fetched batches.
  canFetchMore(parent_index: QModelIndex) -> bool:
    - Returns True if self._file_count < len(self._file_list), indicating more data is available.
  fetchMore(parent_index: QModelIndex):
    - Called by view when more items are needed (e.g., scrolling to end).
    - Calculates batch size (e.g., BATCH_SIZE = 100).
    - Calls beginInsertRows() to signal new rows.
    - Increments self._file_count by batch size.
    - Calls endInsertRows() to finalize operation.
    - Emits custom signal number_populated for logging.
  Icons:
    - Uses QFileIconProvider for system icons.
```

--------------------------------

### PySide6 Core API Usage Highlights

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgets/charactermap/README.md

Key PySide6 classes and methods demonstrated in the Character Map example, covering custom drawing, font management, event handling, and UI interactions.

```APIDOC
PySide6 API Components:
- QWidget.paintEvent: Custom drawing event handler for widgets.
- QPainter: Provides high-level painting on widgets and other paint devices.
- QFont: Manages font properties like family, size, and style.
- QFontMetrics: Provides font metric information for a given font, useful for layout calculations.
  - height(): Returns the height of the font.
  - horizontalAdvance(text: str): Returns the horizontal advance of the given text.
- QFontDatabase: Provides information about the fonts available in the system.
- QFontComboBox: A combo box that allows the user to select a font family.
- QScrollArea: Provides a scrollable view to another widget.
- Event Handling:
  - mouseMoveEvent: Triggered when the mouse cursor moves over the widget. Used for tooltips.
  - mousePressEvent: Triggered when a mouse button is pressed over the widget. Used for character selection.
- QToolTip: Provides a small pop-up window that displays a short description of a widget's purpose.
- QClipboard: Provides access to the window system's clipboard.
```

--------------------------------

### PySide6 Digital Clock API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgets/digitalclock/README.md

Detailed reference for PySide6 classes and methods used in the digital clock example, including QLCDNumber, QTimer, and QTime.

```APIDOC
PySide6 API Reference:
  Classes:
    DigitalClock (subclass of QLCDNumber):
      Description: Custom widget for displaying a digital clock.
      Methods:
        __init__():
          Description: Constructor. Sets segment style, digit count, initializes QTimer, and connects timeout signal.
          Calls:
            setSegmentStyle(QLCDNumber.SegmentStyle.Filled): Sets LCD segment style.
            setDigitCount(8): Configures display for 8 characters (hh:mm:ss).
            QTimer(): Initializes an internal QTimer.
            timer.timeout.connect(self.show_time): Connects timer's timeout signal to show_time slot.
            timer.start(1000): Starts the timer to emit timeout every 1000ms (1 second).
        show_time():
          Description: Slot executed every second by QTimer. Updates the LCD display with current time and implements blinking colon effect.
          Calls:
            QTime.currentTime(): Retrieves current system time.
            time.toString("hh:mm:ss"): Formats time into "hh:mm:ss" string.
            self.display(text): Updates the QLCDNumber display.
          Logic:
            Blinking Colon Effect: Replaces colons with spaces if current second is even.

    QLCDNumber:
      Description: Widget for displaying numbers or alphanumeric characters with an LCD-like appearance.
      Methods:
        setSegmentStyle(style: QLCDNumber.SegmentStyle):
          Description: Customizes the visual look of the LCD segments.
          Parameters:
            style: QLCDNumber.SegmentStyle - e.g., Filled, Flat, Outline.
        setDigitCount(count: int):
          Description: Sets the number of digits/characters the display can show.
          Parameters:
            count: int - The number of characters.
        display(value: Union[str, int]):
          Description: Updates the content shown on the LCD.
          Parameters:
            value: Union[str, int] - The string or integer to display.

    QTimer:
      Description: Used for generating regular, periodic events.
      Signals:
        timeout: Emitted when the timer expires.
      Methods:
        start(milliseconds: int):
          Description: Starts or restarts the timer with the given timeout interval.
          Parameters:
            milliseconds: int - The interval in milliseconds.
      Usage:
        timer.timeout.connect(slot): Connects the timer's timeout signal to a slot.

    QTime:
      Description: Provides functions for getting and manipulating time.
      Static Methods:
        currentTime():
          Description: Returns the current system time.
          Returns: QTime - The current time.
      Methods:
        toString(format: str):
          Description: Returns the time as a string formatted according to the given format string.
          Parameters:
            format: str - The format string (e.g., "hh:mm:ss").
          Returns: str - The formatted time string.

  Concepts:
    Slots:
      Description: Methods in Qt objects that can be connected to signals. Can be decorated with @Slot() for clarity and meta-object system exposure.
```

--------------------------------

### Run FastAPI Backend Server

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/part3/README.md

Command to start the Uvicorn server for the FastAPI backend. This server typically listens on 'http://127.0.0.1:8000' and initializes the database upon its first run.

```bash
python main.py
```

--------------------------------

### Applying GNU GPL: Interactive Program Startup Notice

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/LICENSES/GPL-3.0-only.txt

Template for a short notice to be output by a program when it starts in an interactive mode, informing users about the warranty status and redistribution conditions under the GNU General Public License.

```Text
<program>  Copyright (C) <year>  <name of author>
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
```

--------------------------------

### ImageSettingsDialog Class (PySide6 APIDOC)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

A `QDialog` that enables configuration of still image capture settings. It queries the `QImageCapture` object for supported formats and resolutions, populates UI elements, and applies selected settings.

```APIDOC
ImageSettingsDialog Class (QDialog):
  - Located in imagesettings.py.
  - UI from imagesettings.ui.
  - Constructor:
    - Queries the passed QImageCapture object and associated camera for supported image formats, resolutions, and quality settings.
    - Populates QComboBoxes (for format, resolution) and a QSlider (for quality) with supported values.
    - Displays current settings from the QImageCapture object.
  apply_image_settings():
    - When the dialog is accepted, applies selected settings back to the QImageCapture object (e.g., setImageFormat(), setResolution(), setQuality()).
```

--------------------------------

### Main QML Application Window Structure

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/part1/README.md

The primary QML file (`Main.qml`) setting up the application window with navigation, instantiating the Python data model, and including a button for adding new entries.

```QML
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import Finance

ApplicationWindow {
    id: appWindow
    visible: true
    width: 640
    height: 480
    title: qsTr("Finance Manager")

    FinanceModel { id: finance_model }

    header: TabBar {
        id: tabBar
        currentIndex: stackLayout.currentIndex
        TabButton { text: qsTr("Expenses") }
        TabButton { text: qsTr("Charts") }
    }

    StackLayout {
        id: stackLayout
        currentIndex: tabBar.currentIndex
        anchors.fill: parent

        FinanceView { model: finance_model }
        FinancePieChart { model: finance_model }
    }

    footer: ToolBar {
        ToolButton {
            text: qsTr("Add Expense")
            onClicked: addDialog.open()
        }
    }

    AddDialog {
        id: addDialog
        onFinished: (item, category, cost, date) => {
            if (item && category && cost && date) {
                finance_model.append(item, category, parseFloat(cost), date);
                finance_model.getCategoryData(); // Refresh chart data
            }
        }
    }
}
```

--------------------------------

### PySide6 Key Modules and Classes for MIME Type Browser

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/mimetypesbrowser/README.md

Overview of essential PySide6 modules and classes used in the MIME Types Browser Example, detailing their roles and functionalities.

```APIDOC
QtCore:
  - QMimeDatabase: Core class for querying the system's database of MIME types.
  - QMimeType: Represents an individual MIME type and provides access to its properties (name, comment, aliases, suffixes, parent types, icon names, etc.).
  - QStandardItemModel: Used as the base for the custom MimeTypeModel to store and manage the hierarchical MIME type data.
  - QStandardItem: Tree items within the QStandardItemModel, each representing a MIME type.
  - QModelIndex: Used for interacting with items in the model and view.
  - Qt: Provides enums for item data roles (e.g., Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.UserRole) and item flags.
  - QDir: Used in the "Detect File Type" feature.
  - QFileInfo: Used in the "Detect File Type" feature.

QtWidgets:
  - QApplication: Manages the application's event loop.
  - QMainWindow (custom MainWindow class): The main application window.
  - QTreeView: Displays the hierarchical tree of MIME types from the custom model.
  - QTextEdit: Displays detailed information about the currently selected MIME type (as HTML).
  - QSplitter: Used to arrange the QTreeView and QTextEdit panes, allowing resizing.
  - QAction: For menu bar actions like "Detect File Type...", "Find...", "Exit".
  - QFileDialog: Allows the user to select a file for MIME type detection.
  - QInputDialog: Prompts the user for text when using the "Find..." feature.
  - QMessageBox: Used to display informational messages (e.g., if a file's MIME type cannot be determined).

QtGui:
  - QKeySequence: Used for defining standard keyboard shortcuts for menu actions.
```

--------------------------------

### LocationDialog Class: QSettings Path Configuration

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/settingseditor/README.md

A dialog allowing users to configure QSettings format, scope, organization, and application names, displaying relevant file paths.

```APIDOC
LocationDialog(QDialog):
  Description:
    - A dialog that allows the user to specify the QSettings.Format (Native or INI), QSettings.Scope (User or System), organization name, and application name when opening application-specific settings.
    - It also displays a table of file paths where QSettings would look for settings based on the chosen parameters, indicating if they are read-write or read-only fallbacks.
```

--------------------------------

### Execute PySide6 QML Object List Model Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick/models/objectlistmodel/README.md

This command runs the Python script that initializes a PySide6 application, demonstrating how a Python list of DataObject instances can be used as a model for a QML ListView, displaying colored rectangles with labels.

```bash
python objectlistmodel.py
```

--------------------------------

### PySide6 Text-to-Speech Playback Control

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Outlines the methods used for controlling speech playback, including pausing, resuming, and stopping the synthesis.

```APIDOC
MainWindow:
  pause_speaking() slot:
    - Connected to _ui.pauseButton clicked signal
    - Calls self._speech.pause()

  resume_speaking() slot:
    - _ui.resumeButton clicked signal is directly connected to self._speech.resume()

  stop_speaking() slot:
    - Connected to _ui.stopButton clicked signal
    - Calls self._speech.stop()
```

--------------------------------

### PySide6 Text-to-Speech Speak Function

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Explains how the 'Speak' button initiates text-to-speech synthesis by retrieving text from a plain text edit and calling the `say` method of the `QTextToSpeech` instance.

```APIDOC
MainWindow:
  speak_text() slot:
    - Connected to _ui.speakButton clicked signal
    - Retrieves text from _ui.plainTextEdit.toPlainText()
    - Initiates speech synthesis by calling self._speech.say(text_to_speak)
```

--------------------------------

### API Documentation for NumPy (External Dependency)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/datavisualization/surface_numpy/README.md

Details the NumPy functions and usage within the example for data generation.

```APIDOC
numpy:
  np.zeros: To initialize the NumPy array for Y-values.
  Mathematical functions (e.g., math.sqrt, math.sin): Used in conjunction with NumPy array population, even if filled via loops rather than vectorized operations, demonstrating NumPy's role in array storage.
```

--------------------------------

### PySide6 QtMultimedia UI Control Population and Settings Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

This section describes how the application populates UI controls with supported media formats, resolutions, and quality settings. It also details the apply_settings() function, which configures QMediaRecorder and QCamera based on user selections, and update_formats_and_codecs() for dynamic codec updates.

```APIDOC
UI Control Population:
  - QMediaFormat: Supported video formats/codecs
  - QCameraDevice.videoFormats(): Resolutions/frame rates
  - QAudioInput.device().minimumSampleRate()/maximumSampleRate(): Audio sample rates
  - QMediaRecorder.Quality: Quality settings

apply_settings():
  Purpose: Applies selected media settings to recording and camera devices.
  Applies to:
    - QMediaRecorder: media format, quality, audio sample rate, video resolution, frame rate
    - QCamera: camera format

update_formats_and_codecs():
  Purpose: Dynamically updates available codecs based on the selected container format.
```

--------------------------------

### CMake Configuration for QtExampleStyle QML Module

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/demos/colorpaletteclient/QtExampleStyle/CMakeLists.txt

This CMakeLists.txt file configures the 'qtexamplestyle' Qt QML module. It defines project settings, enables AUTOMOC, sets installation directories, finds required Qt components (Core, Gui, Quick, QuickControls2), registers QML files as a singleton and a module, links necessary libraries, and specifies installation rules for the module and its 'qmldir' file. It also includes a workaround for a specific Qt bug on Unix systems.

```CMake
# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

cmake_minimum_required(VERSION 3.16)
project(qtexamplestyle LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)

if(NOT DEFINED INSTALL_EXAMPLESDIR)
    set(INSTALL_EXAMPLESDIR "examples")
endif()

set(INSTALL_EXAMPLEDIR "${INSTALL_EXAMPLESDIR}/quickcontrols/colorpaletteclient/QtExampleStyle")

find_package(Qt6 REQUIRED COMPONENTS Core Gui Quick QuickControls2)

set_source_files_properties(UIStyle.qml
    PROPERTIES
        QT_QML_SINGLETON_TYPE TRUE
)

qt_policy(SET QTP0001 NEW)
qt_add_qml_module(qtexamplestyle
    URI QtExampleStyle
    PLUGIN_TARGET qtexamplestyle
    QML_FILES
        Button.qml
        Popup.qml
        UIStyle.qml
        TextField.qml
)

target_link_libraries(qtexamplestyle PUBLIC
    Qt6::Core
    Qt6::Gui
    Qt6::Quick
    Qt6::QuickControls2
)

if(UNIX AND NOT APPLE AND CMAKE_CROSSCOMPILING)
    find_package(Qt6 REQUIRED COMPONENTS QuickTemplates2)

    # Work around QTBUG-86533
    target_link_libraries(qtexamplestyle PRIVATE Qt6::QuickTemplates2)
endif()

install(TARGETS qtexamplestyle
    RUNTIME DESTINATION "${INSTALL_EXAMPLEDIR}"
    BUNDLE DESTINATION "${INSTALL_EXAMPLEDIR}"
    LIBRARY DESTINATION "${INSTALL_EXAMPLEDIR}"
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/qmldir
    DESTINATION "${INSTALL_EXAMPLEDIR}"
)
```

--------------------------------

### PySide6 QtSerialBus Modbus Client API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/serialbus/modbus/modbusclient/README.md

Overview of key PySide6 modules and classes used in the Modbus client example, detailing their purpose and relevant enums for Modbus communication and UI development.

```APIDOC
PySide6.QtSerialBus:
  QModbusClient: Abstract base class for Modbus client devices.
  QModbusTcpClient: For Modbus TCP communication.
  QModbusRtuSerialClient: For Modbus RTU communication over a serial line.
  QModbusDataUnit: Represents a block of Modbus registers/coils for read/write operations (specifies register type, start address, and values).
  QModbusReply: Represents the result of a Modbus request; emits a 'finished' signal upon completion.
  Enums:
    QModbusDevice.Error
    QModbusDevice.State
    QModbusDevice.ConnectionParameter
    QModbusDataUnit.RegisterType

PySide6.QtWidgets:
  QApplication
  QMainWindow: Custom MainWindow class.
  QDialog: Custom SettingsDialog class.
  Controls:
    QComboBox: For server type, register type for writing.
    QLineEdit: For server address/port, serial port.
    QSpinBox: For Modbus server address, register start address, number of values.
    QPushButton
    QStatusBar
    QMessageBox
  QListWidget: Used as ui.readValue to display read register values.
  QTableView: Used as ui.writeValueTable with WriteRegisterModel.

PySide6.QtGui:
  QStandardItemModel
  QStandardItem: Used for ui.writeSize ComboBox model.

PySide6.QtCore:
  QAbstractTableModel: Custom WriteRegisterModel class.
  Slot
  Signal
  QUrl
  QLoggingCategory: For enabling Modbus debug messages.
```

--------------------------------

### PySide6 and QML API Components for Windowing and Screen Management

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick/window/README.md

Overview of key Python (PySide6) modules, QML imports, and QML types used for window management and screen information retrieval in Qt Quick applications, along with details on the Qt Resource System.

```APIDOC
Python (main.py) Modules:
  PySide6.QtGui.QGuiApplication: Main application object for GUI applications.
  PySide6.QtQml.QQmlComponent: Used to instantiate QML components.
  PySide6.QtQml.QQmlEngine: Provides the environment for loading and running QML.
  PySide6.QtQuick.QQuickWindow: Base class for QML windows, used for setDefaultAlphaBuffer.
  PySide6.QtQuickControls2.QQuickStyle: For applying platform-specific styles (e.g., "Fusion" on Windows).
  rc_window: Generated Python module from window.qrc, bundles QML files.
  shared_rc: Another generated Python module, likely for shared resources like images.
```

```APIDOC
QML Imports (within .qml files):
  import QtQuick: Provides fundamental types (QtObject, Window, Screen, Rectangle, Text, Timer, SystemPalette, Image, MouseArea, Item, etc.).
  import QtQuick.Controls: Provides standard UI controls (Label, Button, CheckBox).
  import shared: Custom module for shared resources (e.g., Images.qtLogo).
```

```APIDOC
QML Types Utilized:
  QtObject: Used as the root controller in window.qml to manage window instances.
  Window (from QtQuick.Window): The fundamental QML type for creating top-level windows. Used for the control window, the test window, and the splash screen.
  Screen: Provides access to properties of the display screen (e.g., Screen.width or Window.screen attached property).
  (Qt.application).screens: A QML global property (referring to QGuiApplication::screens()) that provides a list of all available Screen objects.
  Layouts & Views: Column, Grid, Repeater (in AllScreens.qml).
  Controls: Label, Button, CheckBox.
  Visuals: Rectangle, Image, Text.
  Timer: Used in Splash.qml to control its duration.
  SystemPalette: To access system theme colors.
```

```APIDOC
Qt Resource System (.qrc):
  window.qrc: Bundles QML files (window.qml, Splash.qml, CurrentScreen.qml, AllScreens.qml) into the application binary.
  Images: Accessed from a shared resource module (like Images.qtLogo).
```

--------------------------------

### PySide6 Key Modules and Classes API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/audio/README.md

Detailed API documentation for essential PySide6 modules and classes used in real-time audio processing and charting, including their purpose and core functionalities.

```APIDOC
QtCharts:
  QChartView: The widget used for displaying the chart.
  QChart: The main object representing the chart.
  QLineSeries: Used to represent and draw the audio waveform.
  QValueAxis: Used for defining the properties of the X and Y axes (e.g., range, title, label format).
QtMultimedia:
  QAudioSource: The class responsible for capturing audio from an input device.
  QMediaDevices: Used to query available audio input devices.
  QAudioFormat: Defines the parameters for the audio stream (sample rate, channel count, sample format like UInt8).
QtWidgets:
  QApplication: Manages the application's event loop.
  QMainWindow: Serves as the main window hosting the chart view.
  QMessageBox: Used to display a warning if no audio input devices are found.
QtCore:
  QIODevice: The QAudioSource.start() method returns a QIODevice (or a derived class instance) from which raw audio data is read.
  QByteArray: The format in which raw audio data is read from the QIODevice.
  QPointF: Represents data points (sample index, audio level) for the QLineSeries.
  Slot: Decorator for methods connected to signals (like readyRead).
```

--------------------------------

### MainWindow Class (Main Application Window) API

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/address_book/README.md

Documentation for the `MainWindow` class, the main application window hosting `AddressWidget` and managing menus/actions.

```APIDOC
Class: MainWindow
Inherits: QMainWindow
File: address_book.py

Description: The top-level application window that integrates AddressWidget and provides file and tool menus.

Components:
  - AddressWidget: Set as the central widget.
  - Menus: "File" (Open, Save As, Exit) and "Tools" (Add Entry, Edit Entry, Remove Entry).
  - QAction instances for menu items.

Slots:
  update_actions(selection: QItemSelection):
    Description: Enables or disables "Edit Entry" and "Remove Entry" actions based on whether any contact is currently selected in the AddressWidget.
    Parameters:
      selection: QItemSelection - The current item selection from AddressWidget.
    Returns: None
```

--------------------------------

### PySide6 QtMultimedia API Reference for Camera Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/camera/README.md

Overview of key PySide6 modules and classes used in the camera application, detailing their purpose and functionality within the QtMultimedia framework and other essential Qt modules.

```APIDOC
QtMultimedia:
  QCamera: Represents the camera device.
  QCameraDevice: Represents a specific camera hardware device.
  QMediaDevices: For enumerating available camera and audio input devices.
  QMediaCaptureSession: Manages the overall capture workflow, linking the camera, viewfinder, image capture, and video recorder.
  QImageCapture: For configuring and capturing still images.
  QMediaRecorder: For configuring and recording video and audio.
  QVideoWidget: For displaying the live camera viewfinder (used in .ui file via promotion).
  QMediaFormat: For configuring video/audio encoding formats and container formats for recording.
  QAudioInput: For capturing audio to be included in video recordings.
  QMediaMetaData: For reading and writing metadata associated with media files.
QtWidgets:
  QApplication
  QMainWindow (custom Camera class)
  QDialog (custom ImageSettings, VideoSettings, MetaDataDialog classes)
  QMessageBox: For error display.
  QMenu
  QAction
  QActionGroup
  UI controls: QTabWidget (for switching between image/video capture modes in UI), QPushButton, QComboBox, QSlider, QLabel, QStackedWidget (for switching between viewfinder and image preview).
QtGui:
  QPixmap
  QImage: For handling and displaying captured images.
  QKeySequence: For keyboard shortcuts.
  QIcon: For button/action icons.
QtCore:
  Slot
  Signal
  QUrl: Used by QMediaRecorder for output location.
  QStandardPaths: Used implicitly for determining save locations if not fully qualified.
  QDir: For path manipulation.
  QTimer: Used for temporarily displaying captured images.
  QCameraPermission
  QMicrophonePermission: For handling device permissions.
```

--------------------------------

### PySide6 Window Class API

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/flowlayout/README.md

API documentation for the `Window` class, demonstrating the usage of `FlowLayout` by adding various `QPushButton` widgets.

```APIDOC
Window(QWidget):
  __init__():
    description: Initializes the Window, creates a FlowLayout instance, adds QPushButton widgets to it, and sets the FlowLayout as the window's layout.
```

--------------------------------

### PySide6 WidgetGallery Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/widgetsgallery/README.md

Detailed API documentation for the `WidgetGallery` class, a `QDialog` subclass, outlining its structure, key methods for creating widget groups, handling style changes, managing progress, and displaying system information.

```APIDOC
WidgetGallery Class (subclass of QDialog):
  Purpose: Main dialog organizing different categories of widgets.

  Methods/Components:
    Style Selection:
      Component: QComboBox
      Functionality: Allows users to select and apply different Qt application styles dynamically.
      API Call: QApplication.setStyle(QStyleFactory.create(style_name))

    Widget Showcase (organized into groups):
      create_buttons_groupbox():
        Purpose: Displays various button types.
        Widgets: QPushButton (default, toggle, flat), QToolButton (with popup menu), QCommandLinkButton, QRadioButton (in a group), QCheckBox (tri-state).

      create_simple_inputwidgets_groupbox():
        Purpose: Features common input widgets.
        Widgets: QLineEdit (configured for password input), QSpinBox, QDateTimeEdit, QSlider (horizontal), QScrollBar (horizontal), QDial.

      create_itemview_tabwidget():
        Purpose: A QTabWidget showcasing different item views.
        Tabs:
          QTreeView:
            Model: QFileSystemModel (displays local file system).
          QTableWidget:
            Size: 10x10.
          QListView (list mode):
            Model: QStandardItemModel (items with text and icons).
          QListView (IconMode):
            Model: QStandardItemModel (same as above).

      create_text_toolbox():
        Purpose: A QToolBox displaying different text widgets.
        Widgets:
          QTextEdit: Initialized with pre-formatted rich text (HTML).
          QPlainTextEdit: Initialized with plain text.
          QTextBrowser (_systeminfo_textbrowser): Displays system information.

    create_progress_bar():
      Component: QProgressBar
      Animation: Value animated using QTimer, calls advance_progressbar() periodically.

    Dynamic Information and Help:
      update_systeminfo():
        Purpose: Updates _systeminfo_textbrowser with Python version, Qt build, OS, screen configurations (DPI, device pixel ratio).
        Trigger: When window is shown or screen changes.

      help_on_current_widget():
        Purpose: Triggered by F1, identifies widget under mouse, opens Qt documentation in web browser.
        API Calls: QApplication.widgetAt(QCursor.pos()), QDesktopServices.openUrl().

    Widget Disabling:
      Component: Global "Disable widgets" QCheckBox
      Functionality: Toggles enabled state of all main widget groups.

    Main Layout:
      Layout Type: QGridLayout
      Arrangement: Arranges group boxes, progress bar, and QDialogButtonBox (with Help and Close buttons).

Application Entry Point (main.py):
  Standard PySide6 QApplication setup.
  Instantiates and shows the WidgetGallery dialog.
  Includes setup for resource files (import rc_widgetsgallery).
```

--------------------------------

### PySide6 Window Class Usage Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/layouts/borderlayout/README.md

A demonstration class showing how to use the custom BorderLayout. It creates an instance of BorderLayout, adds various widgets (QTextBrowser, QLabel) to different positions, and sets the BorderLayout as its main layout.

```APIDOC
Window Class (subclass of QWidget):
  Initialization:
    - Creates an instance of BorderLayout.
    - Adds a QTextBrowser to Position.Center.
    - Adds QLabel widgets (styled with frames) to Position.North, Position.South, Position.West, and Position.East.
    - Sets the BorderLayout instance as the layout for the Window.
```

--------------------------------

### Interactive Program Startup Notice for GPL Software

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/LICENSES/GPL-2.0-only.txt

This snippet shows a sample short notice to be displayed by an interactive program when it starts, informing users about the software's copyright, lack of warranty, and redistribution conditions, with prompts for more details.

```Text
Gnomovision version 69, Copyright (C) year name of author
Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
```

--------------------------------

### Expected Output of Default Property Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced3-Default-properties/README.md

This snippet shows the console output produced by running the PySide6 QML example. It confirms that the `guests` list is correctly populated even with the simplified QML syntax, and the underlying Python objects are accessible.

```text
Bob Jones is having a birthday!
He is inviting:
    Leo Hodges
    Jack Smith
    Anne Brown
```

--------------------------------

### Chart Creation and Layout Management

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/pointconfiguration/doc/pointconfiguration.rst

Sets up the `QChart` and `QChartView`, adds the `QLineSeries` to the chart, and arranges all UI components (chart view and controls) within the `QMainWindow` using layouts. It also includes logic to select an initial point upon application startup.

```python
self.chart = QChart()
self.chart.addSeries(self.series)
self.chart_view = QChartView(self.chart)
# Layout setup
main_layout = QHBoxLayout()
main_layout.addWidget(self.chart_view)
# Add controls to layout
controls_layout = QVBoxLayout()
controls_layout.addWidget(self.color_combo)
# ... more layout
main_layout.addLayout(controls_layout)
central_widget = QWidget()
central_widget.setLayout(main_layout)
self.setCentralWidget(central_widget)
# Select initial point
if self.series.count() > 0:
    self.handlePointClicked(self.series.at(0))
```

--------------------------------

### PySide6 Modules and Classes for CAN Bus GUI

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/serialbus/can/README.md

This section outlines the core PySide6 modules and classes utilized in the CAN bus communication example, detailing their purpose and role in GUI development and CAN bus interaction.

```APIDOC
PySide6.QtSerialBus:
  QCanBus:
    Description: The entry point to access CAN bus functionality, list available plugins, and discover devices.
  QCanBusDevice:
    Description: Represents a connection to a specific CAN interface, used for sending/receiving frames and configuring parameters.
  QCanBusFrame:
    Description: Represents a single CAN frame, including its ID, payload, type (data, remote, error), and flags (e.g., extended format, flexible data rate, bitrate switch).
  QCanBusDeviceInfo:
    Description: Provides information about an available CAN interface (name, description, capabilities).

PySide6.QtWidgets:
  QApplication:
    Description: Manages the application event loop.
  QMainWindow (custom MainWindow class):
    Description: The main application window.
  QDialog (custom ConnectDialog, CanBusDeviceInfoDialog classes):
    Description: For user interaction to set up connections and view device information.
  QGroupBox (custom SendFrameBox, CanBusDeviceInfoBox classes):
    Description: For organizing UI elements related to sending frames and displaying device info.
  QTableView (custom ReceivedFramesView class):
    Description: Displays received CAN frames.
  Input Controls:
    Description: QLineEdit, QComboBox, QCheckBox, QSpinBox, QPushButton.
  QMessageBox:
    Description: For displaying error messages.
  UI loading:
    Description: Uses compiled UI files (e.g., ui_mainwindow.py from mainwindow.ui).

PySide6.QtCore:
  QAbstractTableModel (custom ReceivedFramesModel class):
    Description: Manages the data for received CAN frames.
  Slot:
    Description: PySide6 decorator for defining slots.
  Signal:
    Description: PySide6 class for defining signals.
  Qt:
    Description: Provides enums like ItemDataRole, AlignmentFlag.
  QTimer:
    Description: Used for periodically updating the CAN bus status.
  QByteArray:
    Description: For CAN frame payloads.
  QSettings:
    Description: Used by ConnectDialog to save and restore connection configurations.

Other Python Modules:
  re:
    Description: Used in sendframebox.py for input validation.
```

--------------------------------

### MainWindow Class API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/multimedia/player/README.md

Detailed API documentation for the `MainWindow` class, outlining its constructor, methods, and their functionalities within a PySide6 media player application.

```APIDOC
MainWindow(QMainWindow):
  __init__():
    - Initializes QMediaPlayer (_player) and QAudioOutput (_audio_output).
    - Sets _player's audio output to _audio_output.
    - Creates QVideoWidget (_video_widget) as central widget; sets _player's video output.
    - Sets up QToolBar and QAction instances (Open, Play, Pause, Previous, Next, Stop) with icons/shortcuts.
    - Creates QSlider (_volume_slider) for volume control (0-100), adds to toolbar.
    - Connects signals:
      - _player.playbackStateChanged -> self.update_buttons
      - _player.errorOccurred -> self._player_error
      - "Open" action.triggered -> self.open
      - "Play" action.triggered -> self._player.play
      - "Pause" action.triggered -> self._player.pause
      - "Stop" action.triggered -> self._ensure_stopped
      - "Previous" action.triggered -> self.previous_clicked
      - "Next" action.triggered -> self.next_clicked
      - _volume_slider.valueChanged -> self.setVolume
    - Initializes _playlist (list[QUrl]) and _playlist_index.

  open():
    - Calls _ensure_stopped().
    - Uses QFileDialog to select media files (filtered by QMediaFormat.Decode).
    - Appends selected QUrls to _playlist, updates _playlist_index.
    - Sets _player.setSource(url) and _player.play().

  _ensure_stopped():
    - Calls _player.stop() if player is not in stopped state.

  update_buttons(state: QMediaPlayer.PlaybackState):
    - Enables/disables Play, Pause, Stop, Next, Previous actions based on `state` and playlist.

  previous_clicked():
    - If current position < 5s and previous track exists: loads/plays previous.
    - Else: seeks current track to position 0.

  next_clicked():
    - If next track exists: loads/plays next.

  setVolume(value: int):
    - Parameters:
      - value: int (0-100) - Slider value.
    - Converts `value` to linear volume (0.0-1.0) using QAudio.convertVolume.
    - Sets _audio_output.setVolume(converted_volume).

  _player_error():
    - Prints error string to sys.stderr.
    - Displays error string in status bar.

  closeEvent(event: QCloseEvent):
    - Calls _ensure_stopped() on window close.
```

--------------------------------

### PySide6 Modules and Classes for Threaded OpenGL

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/opengl/threadedqopenglwidget/README.md

Overview of essential PySide6 modules and classes used in the threaded QOpenGLWidget example, detailing their roles in managing OpenGL contexts, rendering, threading, and GUI integration. Includes external dependencies like PyOpenGL and NumPy.

```APIDOC
QtOpenGLWidgets:
  QOpenGLWidget (subclassed as GLWidget):
    Description: The widget responsible for displaying OpenGL content. Its context is moved between threads.

QtGui:
  QOpenGLContext:
    Description: Represents an OpenGL context. Crucially, it can be moved between threads (moveToThread).
  QOpenGLFunctions (used as a base class for Renderer):
    Description: Provides access to OpenGL functions for the current context.
  QSurfaceFormat:
    Description: To configure default OpenGL context properties (e.g., depth buffer size).
  QMatrix4x4:
    Description: For 3D transformations.
  QVector3D:
    Description: For 3D transformations and geometry.

QtOpenGL:
  QOpenGLShaderProgram:
    Description: For managing GLSL shader programs.
  QOpenGLShader:
    Description: For managing GLSL shader programs.
  QOpenGLBuffer:
    Description: For Vertex Buffer Objects (VBOs).
  QOpenGLVertexArrayObject (VAO):
    Description: For managing vertex attribute state (though VAO usage is minimal in the Renderer's direct GL calls, it's created).

QtWidgets:
  QApplication:
    Description: Manages the application event loop.
  QMainWindow (custom MainWindow in the example, though it's actually a QWidget):
    Description: A window that hosts multiple GLWidget instances.
  QWidget:
    Description: Base for MainWindow.
  QMessageBox:
    Description: For error reporting (e.g., PyOpenGL missing).

QtCore:
  QThread:
    Description: The base class for creating worker threads. The Renderer object is moved to a QThread.
  QObject (base for the Renderer class):
    Description: Base class for the Renderer object.
  Signal:
    Description: For communication and event handling between objects, including cross-thread.
  Slot:
    Description: For communication and event handling between objects, including cross-thread.
  QMutex:
    Description: For synchronizing access to resources and context grabbing between threads.
  QMutexLocker:
    Description: For synchronizing access to resources and context grabbing between threads.
  QWaitCondition:
    Description: For synchronizing access to resources and context grabbing between threads.
  QElapsedTimer:
    Description: Used by the Renderer to time operations or manage animation.
  Qt:
    Description: General Qt namespace.
  QSize:
    Description: For size definitions.
  QMetaObject:
    Description: For meta-object system operations.

External Dependencies:
  PyOpenGL:
    Description: Used for some OpenGL constants (e.g., GL.GL_FLOAT) and the glDrawArrays call in the Renderer.
  numpy:
    Description: Used by the Renderer to prepare vertex data for the VBO.
```

--------------------------------

### QML Module Imports for Qt Quick 3D Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/intro/README.md

These are the standard QML module imports required in `main.qml` to access the core functionalities of Qt Quick for UI elements and Qt Quick 3D for 3D scene rendering.

```APIDOC
import QtQuick
import QtQuick3D
```

--------------------------------

### Collect Shiboken Shared Libraries for Windows Deployment (CMake)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgetbinding/CMakeLists.txt

This snippet compiles a list of Shiboken shared libraries that need to be installed alongside the main application. It iterates through the provided library paths, replaces '.lib' extensions with '.dll' for Windows compatibility, and appends them to a list for later installation, simplifying deployment for users.

```CMake
foreach(library_path ${shiboken_shared_libraries})
    string(REGEX REPLACE ".lib$" ".dll" library_path ${library_path})
    file(TO_CMAKE_PATH ${library_path} library_path)
    list(APPEND windows_shiboken_shared_libraries "${library_path}")
endforeach()
```

--------------------------------

### Run PySide6 Image Viewer Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/imageviewer/README.md

This command executes the main Python script for the PySide6 image viewer. It can be run without arguments to open an empty viewer, or with an optional image path to load an image directly upon startup.

```bash
python main.py
```

```bash
python main.py path/to/your/image.jpg
```

--------------------------------

### PySide6 QtWidgets Module API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/chartthemes/README.md

Essential UI components from the `QtWidgets` module used for building the application's main window, controls, and layout.

```APIDOC
QtWidgets:
  QApplication: Manages the application's event loop.
  QMainWindow: Serves as the main application window.
  QWidget: Base class for UI elements; the custom `ThemeWidget` class inherits from this.
  QComboBox: Used for selecting the desired chart theme, animation style, and legend alignment.
  QCheckBox: Used for toggling the anti-aliasing render hint.
  QLabel: For descriptive labels in the UI.
  QGridLayout: Used by the `ThemeWidget` (via `themewidget.ui`) to arrange the multiple chart views and control widgets.
  Ui_ThemeWidgetForm: The Python class generated from `themewidget.ui`, providing access to UI elements.
```

--------------------------------

### PySide6 Main Application Structure

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/rhi/simplerhiwidget/README.md

Defines the main `Widget` class that hosts the `ExampleRhiWidget` within a `QVBoxLayout`, and the application's entry point. It ensures proper resource cleanup for the RHI widget upon application closure.

```APIDOC
class Widget(QWidget):
  # Constructor:
  __init__(parent: QWidget = None) -> None:
    # Initializes a QVBoxLayout.
    # Creates an instance of ExampleRhiWidget.
    # Adds the ExampleRhiWidget to the layout.

  closeEvent(event: QCloseEvent) -> None:
    # Overrides the close event to ensure ExampleRhiWidget.releaseResources() is called
    # for proper RHI resource cleanup before the widget closes.
    # Calls the base class's closeEvent.

def main() -> None:
  # Initializes QApplication.
  # Creates and shows the main Widget instance.
  # Starts the QApplication event loop, which manages the application's execution.
```

--------------------------------

### build_machine Method API Reference (PySide6 QStateMachine)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/statemachine/rogue/README.md

Documents the `build_machine` method within `MainWindow`, which configures and starts a `QStateMachine` to manage game states, transitions based on player input, and application termination.

```APIDOC
build_machine():
  - Creates QStateMachine instance ('machine').
  States:
    - input_state (Custom(machine, self)):
      - Main state for player input.
      - Custom subclass of QState; onEntry prints MainWindow.status to console.
      - assignProperty(self, 'status', 'Move the rogue with 2, 4, 6, and 8') on entry.
    - quit_state (QState(machine)):
      - Entered when 'Q' is pressed.
      - assignProperty(self, 'status', 'Really quit(y/n)?') on entry.
    - _final_state (QFinalState(machine)):
      - When entered, state machine finishes and application quits.
  Transitions:
    - Movement:
      - movement_transition (MovementTransition(self)):
        - Subclasses QEventTransition; eventTest checks KeyPress for 2, 4, 6, 8.
        - onTransition calls self.window.move_player() with corresponding direction.
        - input_state.addTransition(movement_transition) (no target state, input_state remains active).
    - Quitting Process:
      - quit_key_transition (QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_Q)):
        - Listens for 'Q' key press.
        - setTargetState(quit_state).
        - input_state.addTransition(quit_key_transition).
      - yes_transition (QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_Y)):
        - Listens for 'Y' key.
        - setTargetState(_final_state).
        - quit_state.addTransition(yes_transition).
      - no_transition (QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_N)):
        - Listens for 'N' key.
        - setTargetState(input_state).
        - quit_state.addTransition(no_transition).
  Initialization and Start:
    - machine.setInitialState(input_state).
    - machine.finished.connect(QApplication.instance().quit).
    - machine.start().
```

--------------------------------

### APIDOC: QML Finance Entries View (FinanceView.qml)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/tutorials/finance_manager/README.md

Documentation for the QML component responsible for displaying finance entries. It details how data from the `finance_model` is presented in a sectioned list.

```APIDOC
FinanceView.qml (QML Component)
  Base Component: ListView

  Data Source: finance_model (Python FinanceModel instance)

  Features:
    Sectioning:
      property: "month" (uses MonthRole from FinanceModel)
      Description: Groups entries by month (e.g., "Month YYYY").
    Delegate: FinanceDelegate.qml (custom delegate for rendering each item)
```

--------------------------------

### Building CMake-Generated Solution with MSBuild

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/scriptableapplication/doc/scriptableapplication.rst

Command to build a Visual Studio solution file (.sln) generated by CMake using MSBuild, specifically targeting the Release configuration.

```bash
MSBuild scriptableapplication.sln "/p:Configuration=Release"
```

--------------------------------

### PySide6 Core Modules and Classes for Screenshot Application

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/desktop/screenshot/README.md

Overview of key PySide6 modules and classes utilized in the screenshot application, detailing their purpose and specific functionalities like managing application events, UI elements, image handling, and timing.

```APIDOC
PySide6.QtWidgets:
  - QApplication: Manages the application event loop.
  - QWidget (custom main class Screenshot): The main application window.
  - QCheckBox ("Hide This Window"): Option to hide the application window during capture.
  - QLabel (screenshot_label): To display the captured screenshot preview.
  - QPushButton ("New Screenshot", "Save Screenshot", "Quit"): For user actions.
  - QSpinBox (delay_spinbox): For setting the capture delay in seconds.
  - Layout classes (QGridLayout, QHBoxLayout, QVBoxLayout): For arranging UI elements.
  - QFileDialog: For the "Save As" dialog when saving the screenshot.
  - QMessageBox: For displaying error messages (e.g., if saving fails).
  - QGroupBox: To group option controls.

PySide6.QtGui:
  - QScreen: Represents a system screen and provides the grabWindow() method for capturing.
  - QPixmap: Stores the captured image data.
  - QGuiApplication: Global GUI application object, used for QGuiApplication.primaryScreen() and QGuiApplication.beep().
  - QImageWriter: To query supported image formats for saving.

PySide6.QtCore:
  - QTimer: Used for delayed capture via QTimer.singleShot().
  - Slot: For defining slot methods.
  - Qt: For enums like Qt.AlignmentFlag, Qt.AspectRatioMode, Qt.Key.
  - QDir, QRect, QPoint, QStandardPaths: Utility classes for file paths, geometry, and standard directories.
```

--------------------------------

### PySide6.QtGui Module API

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/graphs/3d/minimalsurfacegraph/README.md

API reference for the `PySide6.QtGui` module, containing fundamental GUI classes.

```APIDOC
PySide6.QtGui:
  QGuiApplication:
    Description: The application class used. (Note: For a purely QWidget-based application using Q3DSurfaceWidgetItem, QApplication from QtWidgets would be more standard).
  QVector3D:
    Description: Used to define the coordinates (x, y_height, z) of each QSurfaceDataItem.
```

--------------------------------

### PySide6 Elastic Nodes API Documentation

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/graphicsview/elasticnodes/README.md

Detailed API documentation for the Node, Edge, and GraphWidget classes used in the Elastic Nodes example, outlining their properties, methods, and interactions within the PySide6 Graphics View Framework.

```APIDOC
Node Class (subclass of QGraphicsItem):
  Appearance:
    - Drawn as circles with a radial gradient.
    - Appearance changes slightly when selected (simulating a "sunken" state).
  Physics-Based Movement:
    calculate_forces():
      - Implements core physics logic.
      - Repulsion: Nodes exert repulsive force on each other (stronger for closer nodes).
      - Attraction (Edges): Edges act like springs, pulling connected nodes. Strength proportional to distance and influenced by connection count.
      - Sum of forces determines a target new position (_new_pos).
      - Boundary constraints keep nodes within the visible scene area.
    advance():
      - Called periodically by the simulation timer.
      - If _new_pos differs from current, setPos() is called to move the node.
      - Returns True if movement occurred.
  Interactivity:
    - Movable by mouse (ItemIsMovable) and selectable.
    - Dragging a node triggers physics simulation to re-settle.
  Connectivity:
    - Maintains a list of Edge items connected to it (using weakref).
  itemChange():
    - When position changes, notifies connected edges to update geometry (edge.adjust()).
    - Signals GraphWidget that an item moved, potentially restarting the physics simulation timer.

Edge Class (subclass of QGraphicsItem):
  Appearance:
    - Drawn as black lines with arrowheads at both ends, connecting two nodes.
  Dynamic Adjustment:
    adjust():
      - Recalculates its start and end points based on the current positions of its source and destination nodes.
      - Points are slightly offset from nodes' centers to connect to the periphery.
      - This method is called when connected nodes move.
  Connectivity:
    - Stores weakref references to its sourceNode and destNode.

GraphWidget Class (subclass of QGraphicsView):
  Scene Setup:
    - Initializes a QGraphicsScene and sets properties (e.g., NoIndex, scene rectangle).
    - Populates the scene with a predefined set of Nodes and Edges.
  Physics Simulation Loop:
    - Uses a QTimer (managed via startTimer and killTimer in timerEvent) to drive the simulation.
    timerEvent():
      1. Calls calculate_forces() on all Node items.
      2. Calls advance() on all Node items.
      3. If no nodes moved in the advance() step (layout stable), the timer is stopped.
    item_moved():
      - Slot connected to signals from nodes (implicitly via itemChange).
      - If a node is moved by the user, this restarts the simulation timer.
  User Interaction:
    keyPressEvent():
      - Allows moving a central node with arrow keys.
      - Zooms with '+' and '-' keys.
      - Randomizes all node positions with Space or Enter.
    wheelEvent():
      - Implements zooming with the mouse wheel.
  Custom Background:
    drawBackground():
      - Draws a gradient background with subtle shadow effects and instructional text.
  View Optimizations:
    - Uses CacheBackground.
    - Enables antialiasing.
    - Sets appropriate transformation/resize anchors.
```

--------------------------------

### SettingsTree Class: Displaying and Editing QSettings

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/corelib/settingseditor/README.md

A QTreeWidget subclass that visualizes QSettings data, supporting recursive loading, in-place editing, and optional auto-refresh.

```APIDOC
SettingsTree(QTreeWidget):
  Description:
    - Displays settings from a QSettings object in a tree.
    - Columns: "Setting" (key/group name), "Type" (data type name), and "Value".

  Methods:
    refresh():
      - Recursively iterates through settings.childGroups() and settings.childKeys() to populate the tree.
    update_child_items():
      - Helper method for recursive population.
      - Groups are represented as expandable parent items, and keys as child items.
      - Stores full key path and QVariant value in QTreeWidgetItem data roles for editing and type identification.
      - Displays the type of the value (e.g., "bool", "QString", "QColor") in the "Type" column.

  Editing:
    - Uses a custom VariantDelegate for in-place editing of values in the "Value" column.
    - update_setting(full_key, new_value): Called when an item is changed to write the new value back to QSettings using settings.setValue().

  Auto-Refresh:
    - If enabled, uses a QTimer to periodically call refresh() (unless an editor is active).

  Fallbacks:
    - Allows toggling settings.setFallbacksEnabled().
```

--------------------------------

### Execute PySide6 QML Grouped Properties Example

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/qml/tutorials/extending-qml-advanced/advanced4-Grouped-properties/README.md

This command executes the main Python script for the PySide6 QML example, which processes grouped properties defined in QML and prints relevant information to the console.

```bash
python main.py
```

--------------------------------

### PySide6 Text-to-Speech State Management

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/speech/hello_speak/README.md

Details the `state_changed` slot, which updates the application's status bar and enables/disables playback control buttons based on the `QTextToSpeech` instance's current state.

```APIDOC
MainWindow:
  state_changed(state: QTextToSpeech.State) slot:
    - Connected to self._speech.stateChanged signal
    - Updates messages in the _ui.statusbar based on the TTS state (Speaking, Ready, Paused, BackendError)
    - Enables or disables the "Pause", "Resume", and "Stop" buttons according to the current state (e.g., "Pause" enabled only when speaking; "Resume" only when paused)
```

--------------------------------

### PySide6 QSortFilterProxyModel Core API Usage

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/basicfiltermodel/README.md

This section outlines the key PySide6 classes and methods used in the example for implementing data sorting and filtering with `QSortFilterProxyModel`. It covers the source model, proxy model, views, and regular expression handling.

```APIDOC
QStandardItemModel:
  - Purpose: Used as the underlying source model for storing data.

QSortFilterProxyModel:
  - Purpose: Central class for demonstrating sorting and filtering.
  - Methods:
    - setSourceModel(source_model: QAbstractItemModel): Links the proxy model to the source model.
    - setDynamicSortFilter(dynamic: bool): Ensures automatic updates on filter/source changes.
    - setFilterRegularExpression(pattern: str | QRegularExpression): Sets the filter pattern.
    - setFilterKeyColumn(column: int): Specifies the column to apply the filter to.
    - setSortCaseSensitivity(sensitivity: Qt.CaseSensitivity): Controls case sensitivity for sorting.

QTreeView:
  - Purpose: Used to display both the source and proxy models.
  - Methods:
    - setSortingEnabled(enabled: bool): Enables user sorting by clicking column headers (when connected to a proxy model).

QRegularExpression:
  - Purpose: Used for defining filter patterns, with options for case sensitivity and converting wildcard/fixed string patterns.
  - Static Methods:
    - wildcardToRegularExpression(pattern: str): Converts a wildcard pattern to a regular expression.
    - escape(pattern: str): Escapes special characters in a string for literal matching.

Qt.CaseSensitivity:
  - Values: Qt.CaseInsensitive, Qt.CaseSensitive (used with setSortCaseSensitivity)

UI Widgets:
  - QLineEdit: For filter pattern input.
  - QComboBox: For filter syntax and column selection.
  - QCheckBox: For case sensitivity controls.
  - QLabel: For text labels.
  - QGroupBox: For grouping UI elements.

Layouts:
  - QVBoxLayout
  - QHBoxLayout
  - QGridLayout

Signals and Slots:
  - textChanged (QLineEdit)
  - currentIndexChanged (QComboBox)
  - toggled (QCheckBox)
  - Purpose: Connecting UI control changes to slots that update QSortFilterProxyModel parameters.
```

--------------------------------

### Configure QML 3D Scene Environment

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick3d/intro/README.md

Sets the background color and mode for the 3D scene within a QML `View3D` element, providing a visual base for the 3D content.

```QML
environment: SceneEnvironment {
    clearColor: "skyblue"
    backgroundMode: SceneEnvironment.Color
}
```

--------------------------------

### Create and Populate Python List with DataObject Instances (PySide6)

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/quick/models/objectlistmodel/README.md

Illustrates how to create a standard Python list (`dataList`) and populate it with instances of the `DataObject` class, which will serve as the data model for QML.

```python
dataList = [DataObject("Item 1", "red"),
            DataObject("Item 2", "green"),
            DataObject("Item 3", "blue"),
            DataObject("Item 4", "yellow")]
```

--------------------------------

### PySide6 QtGui and QtCore Modules API Reference

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/charts/chartthemes/README.md

Key classes and enums from `QtGui` and `QtCore` modules for rendering hints, color manipulation, event handling, and data structures.

```APIDOC
QtGui:
  QPainter: Its `RenderHint.Antialiasing` is used to enable or disable anti-aliasing for charts.
  QPalette: Used to adjust the application window's background and text colors to complement the selected chart theme.
  QColor: Used to adjust the application window's background and text colors to complement the selected chart theme.
QtCore:
  Slot: While not explicitly used as a decorator in `main.py` for `update_ui`, the connections in the `.ui` file effectively make `update_ui` a slot.
  Qt: Namespace for enums like `Qt.AlignmentFlag` (used for legend alignment).
  QPointF: Used for generating random data points for the charts.
```

--------------------------------

### Install Compiled Libraries and Dependencies to Source Directory

Source: https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/samplebinding/CMakeLists.txt

This section handles the installation of the compiled bindings library, any sample libraries, and the collected Shiboken shared libraries. It places all these necessary files directly into the current source directory, ensuring that the Python interpreter can successfully import the required modules without additional configuration.

```CMake
install(TARGETS ${bindings_library} ${sample_library}
        LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        )
install(FILES ${windows_shiboken_shared_libraries} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
```