PrivacyEraser Dual-Mode GUI SpecificationDocument Version: 1.0
Date: 2025-10-09
Target Framework: CustomTkinter 5.2.0
Language: Python 3.12+1. Overview1.1 Design Goals

Dual Mode Support: Easy Mode (Wizard) ↔ Advanced Mode (Sidebar)
Seamless Transition: Mode switching without data loss
Debug Panel: Collapsible debug console at bottom (toggleable in Settings)
Settings Persistence: Save user preferences (mode, debug, theme)
1.2 UI ModesEasy Mode (Default for New Users)

Target Users: Beginners, casual users
Style: Wizard-style step flow (Concept 3)
Steps:

Select Browsers
Choose Options
Review & Execute


Navigation: Back/Next buttons, progress indicator
Advanced Mode (Power Users)

Target Users: Experienced users, IT professionals
Style: Sidebar navigation with detail panel (Concept 2)
Layout: Sidebar (browsers list) + Main panel (options + actions)
Features: Quick presets, bulk actions, real-time stats
2. Application Architecture2.1 Window Structure┌─────────────────────────────────────────────────────────────────┐
│ HEADER BAR                                                      │
│ ├─ App Title (left)                                            │
│ └─ Top Actions (right): [Settings] [Mode Toggle]               │
├─────────────────────────────────────────────────────────────────┤
│ CONTENT AREA (Mode-dependent)                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Easy Mode: Wizard Flow (Progress Bar + Step Content)       │ │
│ │ OR                                                           │ │
│ │ Advanced Mode: Sidebar + Main Panel                         │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ DEBUG PANEL (Collapsible, controlled by Settings)              │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Variables Section: [Refresh]                                │ │
│ │ Console Section: [Clear]                                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘2.2 Application Statespythonclass AppState:
    # UI Mode
    ui_mode: Literal["easy", "advanced"] = "easy"
    
    # Debug
    debug_enabled: bool = False
    debug_panel_visible: bool = False
    
    # Theme
    appearance_mode: Literal["light", "dark", "system"] = "system"
    
    # Wizard State (Easy Mode)
    wizard_step: int = 0  # 0=Select Browsers, 1=Choose Options, 2=Review
    wizard_selected_browsers: list[str] = []
    
    # Browser Selection (Both Modes)
    active_browser: str | None = None
    active_cleaner_options: list[CleanerOption] = []
    selected_option_ids: set[str] = set()
    
    # Scan Results
    scanned_programs: list[dict] = []3. Component Specifications3.1 Header BarCustomTkinter Widgets:

CTkFrame (height: 60px, bg: gradient or solid)
CTkLabel (title text)
CTkButton (Settings icon button)
CTkSwitch or CTkSegmentedButton (Mode toggle)
Layout:
pythonheader_frame = ctk.CTkFrame(app, height=60, corner_radius=0)
header_frame.pack(fill="x", side="top")

# Left: Title
title_label = ctk.CTkLabel(
    header_frame, 
    text="🛡️ PrivacyEraser",
    font=("Segoe UI", 24, "bold")
)
title_label.pack(side="left", padx=20)

# Right: Actions
actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
actions_frame.pack(side="right", padx=20)

settings_btn = ctk.CTkButton(
    actions_frame,
    text="⚙️ Settings",
    width=100,
    command=open_settings_dialog
)
settings_btn.pack(side="left", padx=5)

mode_toggle = ctk.CTkSegmentedButton(
    actions_frame,
    values=["Easy Mode", "Advanced Mode"],
    command=on_mode_change
)
mode_toggle.pack(side="left", padx=5)Behavior:

Mode toggle updates AppState.ui_mode
Settings button opens modal dialog
Title acts as home button (reset to step 0 in Easy Mode)
3.2 Easy Mode (Wizard)3.2.1 Progress BarCustomTkinter Widgets:

CTkFrame for progress bar container
CTkLabel for step circles and labels
CTkCanvas or custom drawing for connection lines
Layout:
pythonprogress_frame = ctk.CTkFrame(content_area, height=100)
progress_frame.pack(fill="x", pady=20)

steps = [
    {"label": "Select Browsers", "icon": "1️⃣"},
    {"label": "Choose Options", "icon": "2️⃣"},
    {"label": "Review & Clean", "icon": "3️⃣"}
]

for i, step in enumerate(steps):
    step_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
    step_frame.pack(side="left", expand=True)
    
    # Circle
    circle = ctk.CTkLabel(
        step_frame,
        text=step["icon"],
        width=50,
        height=50,
        corner_radius=25,
        fg_color="gray" if i > wizard_step else "blue"
    )
    circle.pack()
    
    # Label
    label = ctk.CTkLabel(step_frame, text=step["label"])
    label.pack()States:

completed (green checkmark ✓)
active (blue, current step number)
pending (gray, future step number)
3.2.2 Step 0: Select BrowsersCustomTkinter Widgets:

CTkScrollableFrame for browser grid
CTkFrame for each browser card
CTkCheckBox for selection
Layout:
pythonstep0_frame = ctk.CTkScrollableFrame(content_area)
step0_frame.pack(fill="both", expand=True)

# Title
title = ctk.CTkLabel(
    step0_frame,
    text="Which browsers would you like to clean?",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=20)

# Browser grid (3 columns)
grid_frame = ctk.CTkFrame(step0_frame, fg_color="transparent")
grid_frame.pack(fill="both", expand=True, padx=40)

for i, browser in enumerate(scanned_programs):
    col = i % 3
    row = i // 3
    
    browser_card = ctk.CTkFrame(
        grid_frame,
        width=200,
        height=180,
        corner_radius=12,
        border_width=2,
        border_color="gray"
    )
    browser_card.grid(row=row, column=col, padx=10, pady=10)
    
    # Icon
    icon_label = ctk.CTkLabel(
        browser_card,
        text=browser["icon"],  # e.g., "C" for Chrome
        font=("Segoe UI", 48),
        width=60,
        height=60,
        corner_radius=10,
        fg_color=browser["color"]
    )
    icon_label.pack(pady=(20, 10))
    
    # Name
    name_label = ctk.CTkLabel(
        browser_card,
        text=browser["name"],
        font=("Segoe UI", 14, "bold")
    )
    name_label.pack()
    
    # Status badge
    status_label = ctk.CTkLabel(
        browser_card,
        text=browser["status"],  # "Installed" / "Not Found"
        font=("Segoe UI", 10),
        fg_color="green" if browser["present"] else "gray",
        corner_radius=10
    )
    status_label.pack(pady=5)
    
    # Checkbox
    checkbox = ctk.CTkCheckBox(
        browser_card,
        text="Select",
        command=lambda b=browser: toggle_browser_selection(b)
    )
    checkbox.pack(pady=10)Behavior:

Clicking card toggles checkbox
Disabled cards for "Not Found" browsers
Selected browsers stored in AppState.wizard_selected_browsers
3.2.3 Step 1: Choose OptionsCustomTkinter Widgets:

CTkScrollableFrame for options list
CTkFrame for each option card
CTkCheckBox for selection
Layout:
pythonstep1_frame = ctk.CTkScrollableFrame(content_area)
step1_frame.pack(fill="both", expand=True)

# Title
title = ctk.CTkLabel(
    step1_frame,
    text="What would you like to clean?",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=20)

subtitle = ctk.CTkLabel(
    step1_frame,
    text=f"Options for: {', '.join(wizard_selected_browsers)}",
    font=("Segoe UI", 12),
    text_color="gray"
)
subtitle.pack()

# Options list
for option in active_cleaner_options:
    option_card = ctk.CTkFrame(
        step1_frame,
        corner_radius=12,
        border_width=2,
        border_color="gray"
    )
    option_card.pack(fill="x", padx=40, pady=10)
    
    # Checkbox
    checkbox = ctk.CTkCheckBox(
        option_card,
        text="",
        width=24,
        height=24
    )
    checkbox.pack(side="left", padx=20)
    
    # Icon
    icon_label = ctk.CTkLabel(
        option_card,
        text=option["icon"],  # e.g., "🗂️" for cache
        font=("Segoe UI", 32),
        width=56,
        height=56,
        corner_radius=10,
        fg_color="blue"
    )
    icon_label.pack(side="left", padx=10)
    
    # Details
    details_frame = ctk.CTkFrame(option_card, fg_color="transparent")
    details_frame.pack(side="left", fill="both", expand=True, padx=10)
    
    title_label = ctk.CTkLabel(
        details_frame,
        text=option["label"],
        font=("Segoe UI", 14, "bold"),
        anchor="w"
    )
    title_label.pack(anchor="w")
    
    desc_label = ctk.CTkLabel(
        details_frame,
        text=option["description"],
        font=("Segoe UI", 11),
        text_color="gray",
        anchor="w"
    )
    desc_label.pack(anchor="w")
    
    # Size
    size_label = ctk.CTkLabel(
        option_card,
        text=option.get("size", "N/A"),
        font=("Segoe UI", 18, "bold"),
        text_color="blue"
    )
    size_label.pack(side="right", padx=20)Warning Banner (for dangerous options):
pythonif option["warning"]:
    warning_frame = ctk.CTkFrame(
        step1_frame,
        fg_color="#FEF3C7",  # Yellow background
        corner_radius=8
    )
    warning_frame.pack(fill="x", padx=40, pady=(0, 10))
    
    warning_label = ctk.CTkLabel(
        warning_frame,
        text=f"⚠️ {option['warning']}",
        text_color="#92400E",
        font=("Segoe UI", 11)
    )
    warning_label.pack(padx=16, pady=12)3.2.4 Step 2: Review & CleanCustomTkinter Widgets:

CTkScrollableFrame for summary
CTkLabel for statistics
CTkTextbox for item preview (read-only)
CTkProgressBar during cleaning
Layout:
pythonstep2_frame = ctk.CTkScrollableFrame(content_area)
step2_frame.pack(fill="both", expand=True)

# Title
title = ctk.CTkLabel(
    step2_frame,
    text="Review your selections",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=20)

# Summary cards
summary_grid = ctk.CTkFrame(step2_frame, fg_color="transparent")
summary_grid.pack(fill="x", padx=40, pady=20)

summary_data = [
    {"label": "Browsers", "value": str(len(wizard_selected_browsers))},
    {"label": "Options", "value": str(len(selected_option_ids))},
    {"label": "Total Size", "value": calculate_total_size()},
]

for i, data in enumerate(summary_data):
    card = ctk.CTkFrame(summary_grid, corner_radius=12)
    card.grid(row=0, column=i, padx=10, sticky="ew")
    summary_grid.columnconfigure(i, weight=1)
    
    label = ctk.CTkLabel(
        card,
        text=data["label"],
        font=("Segoe UI", 12),
        text_color="gray"
    )
    label.pack(pady=(10, 0))
    
    value = ctk.CTkLabel(
        card,
        text=data["value"],
        font=("Segoe UI", 24, "bold")
    )
    value.pack(pady=(0, 10))

# Selected items list
items_frame = ctk.CTkFrame(step2_frame, corner_radius=12)
items_frame.pack(fill="both", expand=True, padx=40, pady=20)

items_title = ctk.CTkLabel(
    items_frame,
    text="What will be cleaned:",
    font=("Segoe UI", 14, "bold")
)
items_title.pack(anchor="w", padx=20, pady=(10, 5))

items_textbox = ctk.CTkTextbox(
    items_frame,
    height=200,
    wrap="word",
    state="disabled"
)
items_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Populate preview
preview_text = generate_preview_text()
items_textbox.configure(state="normal")
items_textbox.insert("1.0", preview_text)
items_textbox.configure(state="disabled")3.2.5 Wizard NavigationCustomTkinter Widgets:

CTkFrame for footer
CTkButton for Back/Next/Finish
Layout:
pythonwizard_footer = ctk.CTkFrame(content_area, height=80, corner_radius=0)
wizard_footer.pack(fill="x", side="bottom")

# Back button (left)
back_btn = ctk.CTkButton(
    wizard_footer,
    text="← Back",
    width=120,
    command=wizard_previous_step,
    state="disabled" if wizard_step == 0 else "normal"
)
back_btn.pack(side="left", padx=20, pady=20)

# Right buttons container
right_frame = ctk.CTkFrame(wizard_footer, fg_color="transparent")
right_frame.pack(side="right", padx=20, pady=20)

# Skip button (optional, for step 1)
if wizard_step == 1:
    skip_btn = ctk.CTkButton(
        right_frame,
        text="Skip",
        width=100,
        fg_color="gray",
        command=wizard_skip_step
    )
    skip_btn.pack(side="left", padx=5)

# Next/Finish button
next_text = "Finish & Clean" if wizard_step == 2 else "Next →"
next_btn = ctk.CTkButton(
    right_frame,
    text=next_text,
    width=140,
    command=wizard_next_step,
    fg_color="green" if wizard_step == 2 else "blue"
)
next_btn.pack(side="left", padx=5)3.3 Advanced Mode (Sidebar)3.3.1 Sidebar (Browser List)CustomTkinter Widgets:

CTkFrame for sidebar (width: 300px, fixed)
CTkScrollableFrame for browser list
CTkEntry for search box
Layout:
pythonsidebar = ctk.CTkFrame(content_area, width=300, corner_radius=0)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)  # Fixed width

# Header
sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent", height=80)
sidebar_header.pack(fill="x", pady=10)

title = ctk.CTkLabel(
    sidebar_header,
    text="🛡️ Browsers",
    font=("Segoe UI", 18, "bold")
)
title.pack(padx=20, pady=(10, 5))

# Search box
search_entry = ctk.CTkEntry(
    sidebar,
    placeholder_text="🔍 Search browsers...",
    height=35
)
search_entry.pack(fill="x", padx=15, pady=(0, 10))

# Scan button
scan_btn = ctk.CTkButton(
    sidebar,
    text="🔄 Scan Programs",
    height=35,
    command=run_scan
)
scan_btn.pack(fill="x", padx=15, pady=5)

# Browser list
browser_list = ctk.CTkScrollableFrame(sidebar)
browser_list.pack(fill="both", expand=True, padx=10, pady=10)

for browser in scanned_programs:
    browser_item = ctk.CTkFrame(
        browser_list,
        corner_radius=8,
        border_width=2,
        border_color="transparent"
    )
    browser_item.pack(fill="x", pady=5)
    
    # Make clickable
    browser_item.bind("<Button-1>", lambda e, b=browser: select_browser(b))
    
    # Icon
    icon = ctk.CTkLabel(
        browser_item,
        text=browser["icon"],
        font=("Segoe UI", 24),
        width=40,
        height=40,
        corner_radius=8,
        fg_color=browser["color"]
    )
    icon.pack(side="left", padx=10, pady=10)
    
    # Info
    info_frame = ctk.CTkFrame(browser_item, fg_color="transparent")
    info_frame.pack(side="left", fill="x", expand=True, pady=10)
    
    name_label = ctk.CTkLabel(
        info_frame,
        text=browser["name"],
        font=("Segoe UI", 12, "bold"),
        anchor="w"
    )
    name_label.pack(anchor="w")
    
    # Status badges
    status_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    status_frame.pack(anchor="w")
    
    if browser["present"] == "yes":
        status_badge = ctk.CTkLabel(
            status_frame,
            text="Installed",
            font=("Segoe UI", 9),
            fg_color="green",
            corner_radius=8,
            padx=6,
            pady=2
        )
        status_badge.pack(side="left", padx=(0, 5))
    
    if browser["running"] == "yes":
        running_badge = ctk.CTkLabel(
            status_frame,
            text="● Running",
            font=("Segoe UI", 9),
            fg_color="orange",
            corner_radius=8,
            padx=6,
            pady=2
        )
        running_badge.pack(side="left")
    
    # Stats (on new line)
    stats_label = ctk.CTkLabel(
        info_frame,
        text=f"📁 {browser.get('cache_size', 'N/A')}  🍪 {browser.get('cookies', 'N/A')}",
        font=("Segoe UI", 9),
        text_color="gray",
        anchor="w"
    )
    stats_label.pack(anchor="w")Active State:
pythondef select_browser(browser):
    # Update active state
    AppState.active_browser = browser["name"]
    
    # Update border color of selected item
    for item in browser_list.winfo_children():
        if item.cget("border_color") == "blue":
            item.configure(border_color="transparent")
    
    # Highlight selected
    selected_item.configure(border_color="blue", border_width=3)
    
    # Load cleaner options in main panel
    load_cleaner_options_for_browser(browser)3.3.2 Main PanelCustomTkinter Widgets:

CTkFrame for main panel (flex, fills remaining space)
CTkScrollableFrame for content
Layout:
pythonmain_panel = ctk.CTkFrame(content_area, corner_radius=0)
main_panel.pack(side="right", fill="both", expand=True)

# Header
main_header = ctk.CTkFrame(main_panel, height=80, corner_radius=0)
main_header.pack(fill="x")

# Title
header_title = ctk.CTkLabel(
    main_header,
    text=f"{active_browser}",
    font=("Segoe UI", 22, "bold")
)
header_title.pack(side="left", padx=30, pady=20)

# User Data Path (subtitle)
path_label = ctk.CTkLabel(
    main_header,
    text=f"📁 {user_data_path}",
    font=("Segoe UI", 10),
    text_color="gray"
)
path_label.place(x=30, y=50)

# Action buttons (right)
actions_frame = ctk.CTkFrame(main_header, fg_color="transparent")
actions_frame.pack(side="right", padx=30, pady=20)

refresh_btn = ctk.CTkButton(
    actions_frame,
    text="🔄 Refresh",
    width=100,
    fg_color="gray",
    command=refresh_browser_data
)
refresh_btn.pack(side="left", padx=5)

preview_btn = ctk.CTkButton(
    actions_frame,
    text="👁️ Preview All",
    width=120,
    command=preview_all_selected
)
preview_btn.pack(side="left", padx=5)

clean_btn = ctk.CTkButton(
    actions_frame,
    text="🧹 Clean Selected",
    width=140,
    fg_color="green",
    command=clean_selected
)
clean_btn.pack(side="left", padx=5)

# Content area
main_content = ctk.CTkScrollableFrame(main_panel)
main_content.pack(fill="both", expand=True, padx=20, pady=20)

# Quick Presets Section
presets_section = ctk.CTkFrame(main_content, corner_radius=12)
presets_section.pack(fill="x", pady=(0, 20))

presets_title = ctk.CTkLabel(
    presets_section,
    text="⚡ Quick Presets",
    font=("Segoe UI", 14, "bold")
)
presets_title.pack(anchor="w", padx=20, pady=(15, 10))

presets_frame = ctk.CTkFrame(presets_section, fg_color="transparent")
presets_frame.pack(fill="x", padx=20, pady=(0, 15))

presets = [
    {"label": "🍪 Cookies Only", "options": ["cookies"]},
    {"label": "🚀 Quick Clean", "options": ["cache", "cookies"]},
    {"label": "🔒 Security Clean", "options": ["cookies", "passwords", "session"]},
    {"label": "💥 Full Clean", "options": ["cache", "cookies", "history", "session"]},
]

for preset in presets:
    preset_btn = ctk.CTkButton(
        presets_frame,
        text=preset["label"],
        width=160,
        height=35,
        fg_color="transparent",
        border_width=2,
        border_color="gray",
        command=lambda p=preset: apply_preset(p)
    )
    preset_btn.pack(side="left", padx=5)

# Cleaner Options Section
options_section = ctk.CTkFrame(main_content, corner_radius=12)
options_section.pack(fill="both", expand=True)

options_title = ctk.CTkLabel(
    options_section,
    text="🎯 Cleaning Options",
    font=("Segoe UI", 16, "bold")
)
options_title.pack(anchor="w", padx=20, pady=(20, 15))

# Select All / Clear All
bulk_frame = ctk.CTkFrame(options_section, fg_color="transparent")
bulk_frame.pack(anchor="w", padx=20, pady=(0, 10))

select_all_btn = ctk.CTkButton(
    bulk_frame,
    text="✓ Select All",
    width=100,
    height=30,
    fg_color="transparent",
    border_width=1,
    command=select_all_options
)
select_all_btn.pack(side="left", padx=5)

clear_all_btn = ctk.CTkButton(
    bulk_frame,
    text="✗ Clear All",
    width=100,
    height=30,
    fg_color="transparent",
    border_width=1,
    command=clear_all_options
)
clear_all_btn.pack(side="left", padx=5)

# Option cards
for option in active_cleaner_options:
    option_card = ctk.CTkFrame(
        options_section,
        corner_radius=12,
        border_width=2,
        border_color="#E9ECEF"
    )
    option_card.pack(fill="x", padx=20, pady=8)
    
    # Hover effect
    option_card.bind("<Enter>", lambda e: e.widget.configure(border_color="blue"))
    option_card.bind("<Leave>", lambda e: e.widget.configure(border_color="#E9ECEF"))
    
    # Checkbox
    checkbox = ctk.CTkCheckBox(
        option_card,
        text="",
        width=20,
        height=20,
        command=lambda opt=option: toggle_option(opt)
    )
    checkbox.pack(side="left", padx=20, pady=15)
    
    # Details
    details_frame = ctk.CTkFrame(option_card, fg_color="transparent")
    details_frame.pack(side="left", fill="both", expand=True, pady=15)
    
    title_label = ctk.CTkLabel(
        details_frame,
        text=option["label"],
        font=("Segoe UI", 14, "bold"),
        anchor="w"
    )
    title_label.pack(anchor="w")
    
    desc_label = ctk.CTkLabel(
        details_frame,
        text=option["description"],
        font=("Segoe UI", 11),
        text_color="gray",
        anchor="w"
    )
    desc_label.pack(anchor="w")
    
    # Stats (secondary line)
    stats_text = f"{option.get('file_count', 'N/A')} files • Last cleaned: {option.get('last_cleaned', 'Never')}"
    stats_label = ctk.CTkLabel(
        details_frame,
        text=stats_text,
        font=("Segoe UI", 9),
        text_color="gray",
        anchor="w"
    )
    stats_label.pack(anchor="w", pady=(4, 0))
    
    # Size
    size_label = ctk.CTkLabel(
        option_card,
        text=option.get("size", "N/A"),
        font=("Segoe UI", 18, "bold"),
        text_color="blue"
    )
    size_label.pack(side="right", padx=20, pady=15)Warning Section (for dangerous options):
python# Insert before dangerous options
warning_banner = ctk.CTkFrame(
    options_section,
    fg_color="#FEF3C7",
    corner_radius=12
)
warning_banner.pack(fill="x", padx=20, pady=10)

warning_content = ctk.CTkFrame(warning_banner, fg_color="transparent")
warning_content.pack(padx=16, pady=12)

warning_icon = ctk.CTkLabel(
    warning_content,
    text="⚠️",
    font=("Segoe UI", 24)
)
warning_icon.pack(side="left", padx=(0, 12))

warning_text_frame = ctk.CTkFrame(warning_content, fg_color="transparent")
warning_text_frame.pack(side="left", fill="x", expand=True)

warning_title = ctk.CTkLabel(
    warning_text_frame,
    text="Destructive Options Below",
    font=("Segoe UI", 12, "bold"),
    text_color="#92400E",
    anchor="w"
)
warning_title.pack(anchor="w")

warning_desc = ctk.CTkLabel(
    warning_text_frame,
    text="The following options will delete sensitive data that cannot be recovered.",
    font=("Segoe UI", 10),
    text_color="#92400E",
    anchor="w"
)
warning_desc.pack(anchor="w")3.4 Settings DialogCustomTkinter Widgets:

CTkToplevel for modal window
CTkTabview for categorized settings
CTkSwitch for toggles
CTkSegmentedButton for mode selection
Layout:
pythonsettings_window = ctk.CTkToplevel(app)
settings_window.title("⚙️ Settings")
settings_window.geometry("600x500")
settings_window.transient(app)  # Modal
settings_window.grab_set()

# Tab view
tabview = ctk.CTkTabview(settings_window)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

# --- General Tab ---
general_tab = tabview.add("General")

# UI Mode
mode_frame = ctk.CTkFrame(general_tab, fg_color="transparent")
mode_frame.pack(fill="x", pady=15)

mode_label = ctk.CTkLabel(
    mode_frame,
    text="User Interface Mode",
    font=("Segoe UI", 14, "bold")
)
mode_label.pack(anchor="w", pady=(0, 8))

mode_desc = ctk.CTkLabel(
    mode_frame,
    text="Choose between Easy Mode (wizard) or Advanced Mode (sidebar)",
    font=("Segoe UI", 10),
    text_color="gray"
)
mode_desc.pack(anchor="w")

mode_selector = ctk.CTkSegmentedButton(
    mode_frame,
    values=["Easy Mode", "Advanced Mode"],
    command=on_settings_mode_change
)
mode_selector.pack(anchor="w", pady=10)
mode_selector.set("Easy Mode" if AppState.ui_mode == "easy" else "Advanced Mode")

# Theme
theme_frame = ctk.CTkFrame(general_tab, fg_color="transparent")
theme_frame.pack(fill="x", pady=15)

theme_label = ctk.CTkLabel(
    theme_frame,
    text="Appearance Theme",
    font=("Segoe UI", 14, "bold")
)
theme_label.pack(anchor="w", pady=(0, 8))

theme_selector = ctk.CTkSegmentedButton(
    theme_frame,
    values=["Light", "Dark", "System"],
    command=on_theme_change
)
theme_selector.pack(anchor="w", pady=10)
theme_selector.set(AppState.appearance_mode.capitalize())

# Auto-scan on startup
autoscan_switch = ctk.CTkSwitch(
    general_tab,
    text="Automatically scan for browsers on startup",
    command=toggle_autoscan
)
autoscan_switch.pack(anchor="w", pady=15)

# --- Debug Tab ---
debug_tab = tabview.add("Debug")

debug_label = ctk.CTkLabel(
    debug_tab,
    text="Debug Settings",
    font=("Segoe UI", 14, "bold")
)
debug_label.pack(anchor="w", pady=(0, 8))

debug_desc = ctk.CTkLabel(
    debug_tab,
    text="Enable debug mode to view logs and variables at the bottom of the app",
    font=("Segoe UI", 10),
    text_color="gray",
    wraplength=500
)
debug_desc.pack(anchor="w", pady=(0, 15))

debug_switch = ctk.CTkSwitch(
    debug_tab,
    text="Enable Debug Panel",
    command=toggle_debug_mode
)
debug_switch.pack(anchor="w", pady=10)
debug_switch.select() if AppState.debug_enabled else debug_switch.deselect()

# Log level
log_level_frame = ctk.CTkFrame(debug_tab, fg_color="transparent")
log_level_frame.pack(fill="x", pady=15)

log_level_label = ctk.CTkLabel(
    log_level_frame,
    text="Log Level",
    font=("Segoe UI", 12, "bold")
)
log_level_label.pack(anchor="w", pady=(0, 8))

log_level_selector = ctk.CTkSegmentedButton(
    log_level_frame,
    values=["DEBUG", "INFO", "WARNING", "ERROR"],
    command=on_log_level_change
)
log_level_selector.pack(anchor="w", pady=10)
log_level_selector.set("INFO")

# --- Advanced Tab ---
advanced_tab = tabview.add("Advanced")

# CleanerML directory
cleanerml_frame = ctk.CTkFrame(advanced_tab, fg_color="transparent")
cleanerml_frame.pack(fill="x", pady=15)

cleanerml_label = ctk.CTkLabel(
    cleanerml_frame,
    text="CleanerML Directory",
    font=("Segoe UI", 12, "bold")
)
cleanerml_label.pack(anchor="w", pady=(0, 8))

cleanerml_path_frame = ctk.CTkFrame(cleanerml_frame, fg_color="transparent")
cleanerml_path_frame.pack(fill="x")

cleanerml_entry = ctk.CTkEntry(
    cleanerml_path_frame,
    width=400,
    placeholder_text="bleachbit/cleaners"
)
cleanerml_entry.pack(side="left", padx=(0, 10))

cleanerml_btn = ctk.CTkButton(
    cleanerml_path_frame,
    text="Browse",
    width=80,
    command=browse_cleanerml_dir
)
cleanerml_btn.pack(side="left")

# Footer buttons
footer_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
footer_frame.pack(fill="x", padx=20, pady=(0, 20))

reset_btn = ctk.CTkButton(
    footer_frame,
    text="Reset to Defaults",
    width=140,
    fg_color="gray",
    command=reset_settings
)
reset_btn.pack(side="left")

button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
button_frame.pack(side="right")

cancel_btn = ctk.CTkButton(
    button_frame,
    text="Cancel",
    width=100,
    fg_color="gray",
    command=settings_window.destroy
)
cancel_btn.pack(side="left", padx=5)

save_btn = ctk.CTkButton(
    button_frame,
    text="Save",
    width=100,
    command=save_settings
)
save_btn.pack(side="left", padx=5)3.5 Debug PanelCustomTkinter Widgets:

CTkFrame for container (collapsible)
CTkTabview for Variables/Console tabs
CTkTextbox for console output
CTkLabel for variables
Layout:
pythondebug_panel = ctk.CTkFrame(app, height=300, corner_radius=0)
# Only pack if debug_enabled
if AppState.debug_enabled:
    debug_panel.pack(fill="both", side="bottom")

# Tab view
debug_tabs = ctk.CTkTabview(debug_panel)
debug_tabs.pack(fill="both", expand=True, padx=10, pady=10)

# --- Variables Tab ---
variables_tab = debug_tabs.add("Variables")

variables_frame = ctk.CTkScrollableFrame(variables_tab)
variables_frame.pack(fill="both", expand=True)

# Refresh button
refresh_btn = ctk.CTkButton(
    variables_tab,
    text="🔄 Refresh",
    width=100,
    height=30,
    command=refresh_variables
)
refresh_btn.place(relx=1.0, x=-110, y=10, anchor="ne")

# Variables display
variables_data = _collect_variables()
for key, value in variables_data:
    var_row = ctk.CTkFrame(variables_frame, fg_color="transparent")
    var_row.pack(fill="x", pady=5)
    
    key_label = ctk.CTkLabel(
        var_row,
        text=f"{key}:",
        font=("Segoe UI", 11, "bold"),
        width=150,
        anchor="w"
    )
    key_label.pack(side="left")
    
    value_label = ctk.CTkLabel(
        var_row,
        text=value,
        font=("Segoe UI", 11),
        anchor="w"
    )
    value_label.pack(side="left", fill="x", expand=True)

# --- Console Tab ---
console_tab = debug_tabs.add("Console")

# Console textbox
console_textbox = ctk.CTkTextbox(
    console_tab,
    wrap="word",
    state="disabled",
    font=("Consolas", 10)
)
console_textbox.pack(fill="both", expand=True, padx=10, pady=(10, 10))

# Clear button
clear_btn = ctk.CTkButton(
    console_tab,
    text="🗑️ Clear",
    width=100,
    height=30,
    command=clear_console
)
clear_btn.place(relx=1.0, x=-110, y=10, anchor="ne")

# Wire to loguru
def append_console(text: str):
    console_textbox.configure(state="normal")
    console_textbox.insert("end", text)
    console_textbox.see("end")
    console_textbox.configure(state="disabled")

logger.add(
    lambda msg: append_console(str(msg)),
    level="INFO",
    format="[ {time:HH:mm:ss} ] {level}: {message}",
)Toggle Visibility:
pythondef toggle_debug_panel():
    if AppState.debug_panel_visible:
        debug_panel.pack_forget()
        AppState.debug_panel_visible = False
    else:
        debug_panel.pack(fill="both", side="bottom")
        AppState.debug_panel_visible = True4. State Management4.1 Settings PersistenceStorage: SQLite database (privacy_eraser.db)Schema:
sqlCREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);Keys:

ui_mode: "easy" or "advanced"
appearance_mode: "light", "dark", or "system"
debug_enabled: "true" or "false"
autoscan_on_startup: "true" or "false"
log_level: "DEBUG", "INFO", "WARNING", or "ERROR"
cleanerml_directory: file path
Implementation:
pythonimport sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".privacy_eraser" / "settings.db"

def init_settings_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_setting(key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    conn.close()

def load_setting(key: str, default: str = "") -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def load_app_state():
    AppState.ui_mode = load_setting("ui_mode", "easy")
    AppState.appearance_mode = load_setting("appearance_mode", "system")
    AppState.debug_enabled = load_setting("debug_enabled", "false") == "true"
    # Apply theme
    ctk.set_appearance_mode(AppState.appearance_mode)4.2 Mode SwitchingTransition Logic:
pythondef switch_ui_mode(new_mode: Literal["easy", "advanced"]):
    # Save current selections
    previous_mode = AppState.ui_mode
    AppState.ui_mode = new_mode
    
    # Persist to DB
    save_setting("ui_mode", new_mode)
    
    # Destroy old content
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Build new UI
    if new_mode == "easy":
        build_wizard_ui()
    else:
        build_advanced_ui()
    
    # Restore selections if possible
    restore_selections_after_mode_switch()
    
    logger.info(f"Switched from {previous_mode} to {new_mode} mode")Preserve State Across Modes:

Selected browsers → Both modes
Selected cleaner options → Both modes
Active browser → Advanced mode only (set to first in Easy mode)
5. Event Flow5.1 Application Startup1. Load settings from DB
   ├─ ui_mode
   ├─ appearance_mode
   ├─ debug_enabled
   └─ autoscan_on_startup

2. Apply theme (ctk.set_appearance_mode)

3. Build main window
   ├─ Header bar
   ├─ Content area (mode-dependent)
   └─ Debug panel (if enabled)

4. If autoscan_on_startup:
   └─ run_scan()

5. Show window5.2 Scan Programs (Both Modes)User clicks "Scan Programs"
   ↓
run_scan()
   ├─ Logger: "Starting scan..."
   ├─ Execute: collect_programs(probes)
   ├─ Update: AppState.scanned_programs
   ├─ Logger: f"Found {len(programs)} browsers"
   └─ UI Update:
       ├─ Easy Mode: Populate Step 0 grid
       └─ Advanced Mode: Populate sidebar list5.3 Preview (Both Modes)User clicks "Preview" or "Preview All"
   ↓
preview_selected_options()
   ├─ For each selected option:
   │   ├─ option.preview() → list of file paths
   │   └─ Logger: Log first 50 items, then "... and N more"
   └─ UI Update:
       ├─ Easy Mode: Update Step 2 textbox
       └─ Advanced Mode: Show preview in dialog or console5.4 Clean (Both Modes)User clicks "Clean" or "Finish & Clean"
   ↓
Confirm dialog: "Are you sure?"
   ↓ (Yes)
execute_clean()
   ├─ For each selected option:
   │   ├─ option.execute() → (count, bytes_deleted)
   │   └─ Logger: f"Deleted {count} items, {bytes_deleted} bytes"
   ├─ Aggregate stats
   └─ UI Update:
       ├─ Show success message
       └─ Reset selections (optional)5.5 Wizard Navigation (Easy Mode)User clicks "Next"
   ↓
wizard_next_step()
   ├─ Validate current step
   │   ├─ Step 0: At least 1 browser selected
   │   └─ Step 1: At least 1 option selected
   ├─ Increment wizard_step
   ├─ Update progress bar
   ├─ Hide current step content
   ├─ Show next step content
   └─ Update footer buttons6. CustomTkinter Widget Mapping6.1 Core Widgets UsedComponentWidgetNotesMain WindowCTk()Root windowContainersCTkFrameSections, cards, panelsScrollable AreasCTkScrollableFrameLists, optionsButtonsCTkButtonActions, navigationLabelsCTkLabelText, titlesCheckboxesCTkCheckBoxOption selectionText InputCTkEntrySearch, settingsMultiline TextCTkTextboxConsole, previewTabsCTkTabviewSettings, debugSwitchesCTkSwitchToggle settingsSegmented ButtonCTkSegmentedButtonMode, theme selectorProgress BarCTkProgressBarLoading indicatorModalCTkToplevelSettings dialog6.2 Color PaletteLight Mode:
pythonCOLORS_LIGHT = {
    "primary": "#667eea",
    "primary_hover": "#5568d3",
    "success": "#10b981",
    "success_hover": "#059669",
    "warning": "#fbbf24",
    "danger": "#ef4444",
    "gray": "#6c757d",
    "gray_light": "#f8f9fa",
    "border": "#e9ecef",
    "text": "#212529",
    "text_secondary": "#6c757d",
}Dark Mode:
pythonCOLORS_DARK = {
    "primary": "#667eea",
    "primary_hover": "#5568d3",
    "success": "#10b981",
    "success_hover": "#059669",
    "warning": "#fbbf24",
    "danger": "#ef4444",
    "gray": "#94a3b8",
    "gray_light": "#1e293b",
    "border": "#334155",
    "text": "#f8f9fa",
    "text_secondary": "#94a3b8",
}7. Implementation PlanPhase 1: Core Infrastructure (Priority: High)

 Existing: Basic GUI with single mode
 Settings database (SQLite schema + CRUD)
 AppState class with mode management
 Mode switching logic (destroy/rebuild UI)
 Theme application from settings
Phase 2: Easy Mode (Wizard) (Priority: High)

 Progress bar component
 Step 0: Browser selection grid
 Step 1: Options selection list
 Step 2: Review summary
 Navigation footer (Back/Next/Finish)
 Wizard state management
Phase 3: Advanced Mode (Sidebar) (Priority: High)

 Sidebar browser list
 Search functionality
 Main panel header
 Quick presets section
 Options section with cards
 Bulk actions (Select All/Clear All)
Phase 4: Settings Dialog (Priority: Medium)

 Modal window (CTkToplevel)
 General tab (mode, theme, autoscan)
 Debug tab (debug toggle, log level)
 Advanced tab (CleanerML path)
 Save/Cancel/Reset buttons
Phase 5: Debug Panel (Priority: Medium)

 Collapsible panel at bottom
 Variables tab with refresh
 Console tab with clear
 Loguru integration
 Toggle from settings
Phase 6: Polish & Testing (Priority: Low)

 Hover effects
 Transitions/animations
 Keyboard shortcuts
 Tooltips
 Error handling dialogs
 Icon assets
8. File Structuresrc/privacy_eraser/
├── __main__.py           # Entry point
├── gui.py                # Main GUI orchestration (REFACTOR)
├── gui_easy_mode.py      # NEW: Wizard UI components
├── gui_advanced_mode.py  # NEW: Sidebar UI components
├── gui_settings.py       # NEW: Settings dialog
├── gui_debug.py          # NEW: Debug panel
├── gui_widgets.py        # NEW: Reusable custom widgets
├── app_state.py          # NEW: Application state management
├── settings_db.py        # NEW: Settings persistence
├── cleaning.py           # Existing: CleanerOption, DeleteAction
├── detect_windows.py     # Existing: Browser detection
└── cleanerml_loader.py   # Existing: CleanerML parsingKey Refactoring Goals

Separate UI modes into different modules (no more 80% duplication)
Extract common widgets (browser cards, option cards)
Centralized state management (AppState singleton)
Settings persistence layer (SQLite wrapper)

7. Implementation Plan
Phase 1: Core Infrastructure (Priority: High)

 Existing: Basic GUI with single mode
 Settings database (SQLite schema + CRUD)
 AppState class with mode management
 Mode switching logic (destroy/rebuild UI)
 Theme application from settings

Phase 2: Easy Mode (Wizard) (Priority: High)

 Progress bar component
 Step 0: Browser selection grid
 Step 1: Options selection list
 Step 2: Review summary
 Navigation footer (Back/Next/Finish)
 Wizard state management

Phase 3: Advanced Mode (Sidebar) (Priority: High)

 Sidebar browser list
 Search functionality
 Main panel header
 Quick presets section
 Options section with cards
 Bulk actions (Select All/Clear All)

Phase 4: Settings Dialog (Priority: Medium)

 Modal window (CTkToplevel)
 General tab (mode, theme, autoscan)
 Debug tab (debug toggle, log level)
 Advanced tab (CleanerML path)
 Save/Cancel/Reset buttons

Phase 5: Debug Panel (Priority: Medium)

 Collapsible panel at bottom
 Variables tab with refresh
 Console tab with clear
 Loguru integration
 Toggle from settings

Phase 6: Polish & Testing (Priority: Low)

 Hover effects
 Transitions/animations
 Keyboard shortcuts
 Tooltips
 Error handling dialogs
 Icon assets


8. File Structure
src/privacy_eraser/
├── __main__.py           # Entry point
├── gui.py                # Main GUI orchestration (REFACTOR)
├── gui_easy_mode.py      # NEW: Wizard UI components
├── gui_advanced_mode.py  # NEW: Sidebar UI components
├── gui_settings.py       # NEW: Settings dialog
├── gui_debug.py          # NEW: Debug panel
├── gui_widgets.py        # NEW: Reusable custom widgets
├── app_state.py          # NEW: Application state management
├── settings_db.py        # NEW: Settings persistence
├── cleaning.py           # Existing: CleanerOption, DeleteAction
├── detect_windows.py     # Existing: Browser detection
└── cleanerml_loader.py   # Existing: CleanerML parsing
Key Refactoring Goals

Separate UI modes into different modules (no more 80% duplication)
Extract common widgets (browser cards, option cards)
Centralized state management (AppState singleton)
Settings persistence layer (SQLite wrapper)


9. API Examples
9.1 Mode Switching
pythonfrom privacy_eraser.app_state import AppState
from privacy_eraser.gui import switch_ui_mode

# Switch to Advanced Mode
switch_ui_mode("advanced")

# Current mode
print(AppState.ui_mode)  # "advanced"
9.2 Settings Management
pythonfrom privacy_eraser.settings_db import save_setting, load_setting

# Save debug mode
save_setting("debug_enabled", "true")

# Load on startup
debug_enabled = load_setting("debug_enabled", "false") == "true"
9.3 Wizard Navigation
pythonfrom privacy_eraser.gui_easy_mode import wizard_next_step, wizard_previous_step

# Move to next step
if wizard_step == 0 and len(selected_browsers) > 0:
    wizard_next_step()

# Go back
wizard_previous_step()
9.4 Debug Panel Toggle
pythonfrom privacy_eraser.gui_debug import toggle_debug_panel
from privacy_eraser.settings_db import save_setting

# Toggle visibility
toggle_debug_panel()

# Persist setting
save_setting("debug_enabled", str(AppState.debug_enabled).lower())

10. Testing Strategy
10.1 Manual Testing Checklist
Mode Switching:

 Switch Easy → Advanced preserves selections
 Switch Advanced → Easy preserves selections
 Mode persists after restart
 No UI glitches during transition

Easy Mode:

 All 3 steps display correctly
 Progress bar updates
 Browser cards clickable
 Option cards clickable
 Review summary accurate
 Clean executes successfully

Advanced Mode:

 Sidebar list populates
 Search filters correctly
 Browser selection highlights
 Quick presets apply correctly
 Bulk actions work (Select All/Clear All)
 Clean executes successfully

Settings:

 Dialog opens/closes
 All settings save to DB
 Theme changes apply immediately
 Debug toggle shows/hides panel
 Reset to defaults works

Debug Panel:

 Variables display correctly
 Refresh updates variables
 Console streams logs
 Clear empties console
 Panel collapses/expands

10.2 Automated Testing (Future)
python# Unit tests for state management
def test_mode_switching():
    AppState.ui_mode = "easy"
    switch_ui_mode("advanced")
    assert AppState.ui_mode == "advanced"

# Settings persistence
def test_settings_persistence():
    save_setting("ui_mode", "advanced")
    assert load_setting("ui_mode") == "advanced"

11. Performance Considerations
11.1 Lazy Loading

Load CleanerML only when browser selected
Defer size calculation until preview
Render visible items only in scrollable lists

11.2 Async Operations (Future)
pythonimport threading

def run_scan_async():
    thread = threading.Thread(target=run_scan)
    thread.start()
    show_loading_spinner()
11.3 Memory Management

Destroy old UI components when switching modes
Clear console after N lines (configurable)
Limit preview to 1000 items max


12. Accessibility
12.1 Keyboard Navigation

Tab order: logical flow through controls
Enter: Activate focused button
Space: Toggle focused checkbox
Escape: Close dialogs

12.2 Screen Reader Support

All buttons have descriptive labels
Status announcements for important actions
Alt text for icons

12.3 High Contrast Mode

Detect Windows high contrast settings
Override colors with high-contrast palette
Increase border widths for visibility


Appendix A: UI Mode Comparison
FeatureEasy ModeAdvanced ModeLayoutWizard (3 steps)Sidebar + Main PanelNavigationBack/Next buttonsClick sidebar itemsBrowser SelectionGrid of cards (Step 0)List in sidebarOption SelectionList of cards (Step 1)Inline checkboxesQuick Presets❌✅ (top of main panel)Bulk Actions✅ (Step 1 header)✅ (options header)PreviewAutomatic (Step 2)Manual buttonStatsSummary cards (Step 2)Per-option displayBest ForBeginners, guided flowPower users, quick access

End of Specification Document