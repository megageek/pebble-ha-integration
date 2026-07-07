# Pebble Watch

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

**✨ Develop in the cloud:** Want to contribute or customize this integration? Open it directly in GitHub Codespaces - no local setup required!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/megageek/pebble-ha-integration?quickstart=1)

Home Assistant integration for a custom Pebble watchface. It works over Home
Assistant's own WebSocket API - the watch's phone bridge connects in and:

- **pulls** up to 10 numbered "channels" of data to show on the watchface, fed
  by your automations via a single service call
- **pushes** battery, activity, sleep, heart rate, and device info back to Home
  Assistant, which appear automatically as sensors

See [`HA_INTEGRATION_SPEC.md`](HA_INTEGRATION_SPEC.md) for the full wire
protocol if you're working on the watch/phone side.

## ✨ Features

- **Zero-config setup**: no host, credentials, or API key - just add the
  integration. The phone authenticates with a Home Assistant long-lived access
  token you already have, entirely outside this integration's control
- **Dashboard channels**: call `pebble_ha_integration.set_channel` from any
  automation to push a value, label, color, or unit to one of the watch's 10
  channels - no static entity-to-channel mapping to configure
- **Automatic status sensors**: battery, steps, activity, sleep, heart rate,
  connectivity, and watch color/model/firmware appear the first time your
  watch actually reports them - nothing is pre-created for hardware or
  permissions you don't have
- **Respects on-watch privacy settings**: if you turn off a measure group
  (e.g. heart rate) in the watchface's own settings, the matching Home
  Assistant entity is disabled automatically

**This integration sets up the following platforms, populated dynamically as
your watch reports in:**

| Platform        | Entities                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------ |
| `sensor`        | Battery %, Steps, Active Time, Distance, Active/Resting Calories, Sleep, Heart Rate, Color |
| `binary_sensor` | Charging, Connected                                                                        |

## 🚀 Quick Start

### Step 1: Install the Integration

**Prerequisites:** This integration requires [HACS](https://hacs.xyz/) (Home Assistant Community Store) to be installed.

Click the button below to open the integration directly in HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=megageek&repository=pebble-ha-integration&category=integration)

Then:

1. Click "Download" to install the integration
2. **Restart Home Assistant** (required after installation)

> [!NOTE]
> The My Home Assistant redirect will first take you to a landing page. Click the button there to open your Home Assistant instance.

<details>
<summary><strong>Manual Installation (Advanced)</strong></summary>

If you prefer not to use HACS:

1. Download the `custom_components/pebble_ha_integration/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

</details>

### Step 2: Add the Integration

**Important:** You must have installed the integration first (see Step 1) and restarted Home Assistant!

Click the button below to open the configuration dialog:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=pebble_ha_integration)

There's nothing to fill in - click **Submit** to create the integration. Only
one instance is needed; the phone brings its own Home Assistant long-lived
access token when it connects, so there are no credentials to enter here.

Alternatively:

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "Pebble Watch" and click **Submit**

### Step 3: Point the Watch at Home Assistant

On the phone running the Pebble watchface app, configure the watchface's Clay
settings with your Home Assistant URL and a
[long-lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile).
Once the watch connects, it registers its status and starts receiving channel
updates automatically - no further setup is needed on the Home Assistant side.

### Step 4: Feed the Dashboard Channels

Call the `pebble_ha_integration.set_channel` service from an automation
whenever you want a channel's value to change:

```yaml
action: pebble_ha_integration.set_channel
data:
  channel: 1
  value: "{{ states('sensor.outdoor_temperature') }}"
  label: "Temp"
  kind: numeric
  unit: "°C"
```

See [Custom Services](#custom-services) below for every available field.

## Available Entities

Entities appear the first time the watch actually reports that measure - if
your watch has no heart rate sensor, or the user hasn't granted Health
permission, that sensor simply never shows up (it won't linger as
"unavailable"). Find them in **Settings** → **Devices & Services** → **Pebble
Watch** → click on the device.

### Sensors

- **Battery**: current battery percentage
- **Steps**, **Active Time**, **Distance**, **Active Calories**, **Resting Calories**: today's cumulative activity totals, reset at local midnight on the watch
- **Sleep**, **Restful Sleep**: today's cumulative sleep totals
- **Heart Rate**: most recent background heart-rate sample (can be up to ~15 minutes stale - the watch doesn't spend extra battery to keep it fresher)
- **Color** (Diagnostic): the watch's case color, reported once at app startup

### Binary Sensors

- **Charging** (Diagnostic): whether the watch is currently charging
- **Connected** (Diagnostic): whether the watch app is connected to the phone

### Entity availability vs. disabled

- If a measure is temporarily unreported (e.g. a momentary gap), an
  already-created entity goes `unavailable` rather than disappearing.
- If you turn a measure group off in the watchface's own Clay settings, the
  matching entity is disabled in the entity registry instead - re-enable it in
  **Settings** → **Devices & Services** → **Entities** if you turn the measure
  back on and want the entity restored.

## Custom Services

### `pebble_ha_integration.set_channel`

Push a value to one of the watch's 10 dashboard channels. This is the primary
way automations drive the watchface - call it whenever the value you want
displayed changes.

| Field                                      | Required | Description                                                                                     |
| ------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------- |
| `channel`                                  | Yes      | Channel number on the watchface (1-10)                                                          |
| `value`                                    | Yes      | String for a text channel, or a whole number for numeric/binary (no floats - scale into `unit`) |
| `label`                                    | No       | Short label (max 7 characters); only needs resending when it changes                            |
| `kind`                                     | No       | `text` (default), `numeric`, or `binary`; sticky - only resend when it changes                  |
| `unit`                                     | No       | Suffix appended after a numeric value, e.g. `"%"` or `" kcal"`                                  |
| `min` / `max`                              | No       | Range for a numeric channel; only takes effect when both are sent together                      |
| `style`                                    | No       | `raw` (default) or `bar`, once `min`/`max` are set                                              |
| `on_color` / `off_color`                   | No       | Status-dot color when the user displays this channel as a dot                                   |
| `hide_when`                                | No       | `none` (default), `on`, or `off` - hide the status dot except when it needs attention           |
| `bg_color` / `value_color` / `label_color` | No       | Background/value/label colors for this channel's normal display                                 |

Color fields accept: `red`, `orange`, `yellow`, `green`, `blue`, `purple`, `white`, `gray`.

**Example - a numeric channel with a progress bar:**

```yaml
action: pebble_ha_integration.set_channel
data:
  channel: 2
  value: "{{ states('sensor.living_room_humidity') | int }}"
  label: "Humid"
  kind: numeric
  unit: "%"
  min: 0
  max: 100
  style: bar
```

**Example - a status-dot channel:**

```yaml
action: pebble_ha_integration.set_channel
data:
  channel: 3
  value: "{{ 'on' if is_state('binary_sensor.front_door', 'on') else 'off' }}"
  label: "Door"
  on_color: red
  off_color: green
  hide_when: "off"
```

## Troubleshooting

### No entities appear after setup

Entities are created lazily, the first time the watch actually sends a status
report - they won't exist until the watch has connected at least once. Confirm
the watch/phone bridge is configured with the correct Home Assistant URL and a
valid long-lived access token, then check the debug log (below) for incoming
`pebble_dashboard/report_status` commands.

### A channel isn't updating on the watch

- Confirm the automation is actually calling `pebble_ha_integration.set_channel`
  (check **Settings** → **Automations & Scenes** → trace, or **Developer Tools**
  → **Actions**).
- Only one watch/phone connection is served at a time per subscription - if the
  phone reconnected, it re-subscribes and receives the current state
  immediately, so a stuck value usually means the automation itself isn't firing.

### Enable Debug Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.pebble_ha_integration: debug
```

This logs every `set_channel` call and every status report received from the
watch, which is the fastest way to confirm data is flowing in both directions.

### Diagnostics

Download diagnostics from **Settings** → **Devices & Services** → **Pebble
Watch** → 3 dots → **Download diagnostics** to see the current channel state,
which status measures are being reported, and how many watch/phone connections
are currently subscribed.

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

You have two options to set up a development environment — expand below for full details.

<details>
<summary><strong>Development Setup</strong></summary>

Both options provide the same fully-configured environment with Home Assistant, Python 3.14, Node.js LTS, and all necessary tools.

### Option 1: GitHub Codespaces (Recommended) ☁️

Develop directly in your browser without installing anything locally!

1. Click the green **"Code"** button in this repository
2. Switch to the **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. **Wait for setup** (2-3 minutes first time) — everything installs automatically
5. **Review and commit** your changes in the Source Control panel (`Ctrl+Shift+G`)

> [!TIP]
> Codespaces gives you **60 hours/month free** for personal accounts. When you start Home Assistant (`script/develop`), port 8123 forwards automatically.

### Option 2: Local Development with VS Code 💻

#### Prerequisites

You'll need these installed locally:

- **A Docker-compatible container engine** — see options by platform:

  | Option                                                                                                                   | 🍎 macOS | 🐧 Linux | 🪟 Windows | Notes                                                                                                                                                                                                                                     |
  | ------------------------------------------------------------------------------------------------------------------------ | :------: | :------: | :--------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | [Docker Desktop](https://www.docker.com/products/docker-desktop/)                                                        |    ✅    |    ✅    |     ✅     | **Easiest starting point for all platforms.** GUI-based, well-documented, one installer. Uses WSL2 as default backend on Windows (Hyper-V also available). Installation requires admin rights; daily use does not. Free for personal use. |
  | [OrbStack](https://orbstack.dev/) ⭐                                                                                     |    ✅    |    —     |     —      | **Recommended for macOS** once Docker Desktop feels slow. Starts in ~2s, much lighter on RAM/CPU, full Docker API compatibility. Free for personal use.                                                                                   |
  | [Docker CE](https://docs.docker.com/engine/install/) (native) ⭐                                                         |    —     |    ✅    |     —      | **Recommended for Linux.** Install directly via your package manager — no VM, no GUI, no overhead. Free.                                                                                                                                  |
  | [WSL2](https://learn.microsoft.com/windows/wsl/install) + [Docker CE](https://docs.docker.com/engine/install/ubuntu/) ⭐ |    —     |    —     |     ✅     | **Recommended for Windows** once you're comfortable with WSL2. Docker runs natively inside WSL2 — no GUI overhead. Requires one-time WSL2 setup. Free.                                                                                    |
  | [Rancher Desktop](https://rancherdesktop.io/)                                                                            |    ✅    |    ✅    |     ✅     | Open source by SUSE. GUI-based, uses WSL2 on Windows. Good alternative to Docker Desktop. Free.                                                                                                                                           |
  | [Colima](https://github.com/abiosoft/colima)                                                                             |    ✅    |    ✅    |     —      | CLI-only, very lightweight. Good for terminal-focused workflows. Free.                                                                                                                                                                    |

- **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Git** — macOS and Linux usually have it already; see below if not, or to get a newer version:
  - **🍎 macOS:** The system Git (`xcode-select --install`) works fine. Recommended: `brew install git` ([Homebrew](https://brew.sh/)) for a current version.
  - **🐧 Linux:** Usually pre-installed. If not: `sudo apt install git` (or your distro's equivalent).
  - **🪟 Windows + WSL2 ⭐:** Install Git _inside WSL2_ with `sudo apt install git`. Git on Windows itself is not needed — VS Code clones and operates entirely within WSL2.
  - **🪟 Windows + Docker Desktop:** Install via `winget install Git.Git` or download [Git for Windows](https://git-scm.com/download/win).
- **Hardware** — the devcontainer runs a full Home Assistant instance including Python tooling:

  |          | Minimum    | Recommended                           |
  | -------- | ---------- | ------------------------------------- |
  | **RAM**  | 8 GB       | 16 GB or more                         |
  | **CPU**  | 4 cores    | 8 cores or more                       |
  | **Disk** | 10 GB free | 20 GB free (SSD strongly recommended) |

> [!TIP]
> **Not sure which Docker option to pick?** Start with [Docker Desktop](https://www.docker.com/products/docker-desktop/) — it works on all platforms, has a GUI, and needs no extra setup. The ⭐ options are faster alternatives once you're comfortable. macOS and Linux offer the best devcontainer experience — containers run with no extra VM layer and file I/O is fast. Windows works well too; this integration uses named container volumes (files live inside WSL2, not on the Windows drive) to keep performance acceptable.

> [!NOTE]
> **New to Dev Containers?** See the [VS Code Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers#_system-requirements) for system requirements and how to install the extension. **Once the extension is installed, you're done** — this repository already ships a complete devcontainer configuration. You don't need to follow the rest of the VS Code guide; the setup steps below are all that's needed.

#### Setup Steps

1. **Clone in a Dev Container:**

   **🍎 macOS / 🐧 Linux:** Clone the repository and open the folder in VS Code → click **"Reopen in Container"** when prompted (or `F1` → **"Dev Containers: Reopen in Container"**).

   **🪟 Windows:** In VS Code, press `F1` → **"Dev Containers: Clone Repository in Named Container Volume..."** and enter the repository URL. This keeps files inside WSL2 for best I/O performance.

2. Wait for the container to build (2-3 minutes first time)

3. **Review and commit** changes in Source Control (`Ctrl+Shift+G`)

4. **Start developing**:

   ```bash
   script/develop  # Home Assistant runs at http://localhost:8123
   ```

> [!NOTE]
> Both Codespaces and local DevContainer provide the exact same experience. The only difference is where the container runs (GitHub's cloud vs. your machine).

</details>

---

## 🤖 AI-Assisted Development

> [!NOTE]
> **Transparency Notice:** This integration was developed with assistance from AI coding agents (GitHub Copilot, Claude, and others). While the codebase follows Home Assistant Core standards, AI-generated code may not be reviewed or tested to the same extent as manually written code. AI tools were used to generate boilerplate code, implement standard integration features (config flow, coordinator, entities), ensure code quality and type safety, and write documentation. If you encounter unexpected behavior, please [open an issue](../../issues) on GitHub.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [@megageek][user_profile]**

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/megageek/pebble-ha-integration.svg?style=for-the-badge
[commits]: https://github.com/megageek/pebble-ha-integration/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/megageek/pebble-ha-integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40megageek-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/megageek/pebble-ha-integration.svg?style=for-the-badge
[releases]: https://github.com/megageek/pebble-ha-integration/releases
[user_profile]: https://github.com/megageek
