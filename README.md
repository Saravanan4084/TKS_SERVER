## <img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/03c9a69e-f501-47a6-871e-5ed86a057432" /> Link : https://discord.gg/X4GEUPDcg
🚀 MODIFIED Bombsquad-Ballistica-Modded-Server

Modded server scripts to host a Ballistica (BombSquad) server.  
Running on BS 1.7.41 (API 9).

## 📦 Prerequisites

- Basic knowledge of Linux
- A VPS (e.g. [Amazon Web Services](https://aws.amazon.com/), [Microsoft Azure](https://portal.azure.com/))
- Any Linux distribution  
  - Recommended: **Ubuntu 22+**
- **Python 3.13**
- At least **1 GB RAM** (2 GB recommended)
- Open ports on your firewall for your BombSquad server port (default `43210`)

---

## 🛠️ Getting Started

This assumes you are on Ubuntu or an Ubuntu-based distribution.

### 1. Install `software-properties-common`

```bash
sudo apt install software-properties-common -y
```

### 2. Add Python Deadsnakes PPA

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

### 3. Install Python 3.13 and tools

```bash
sudo apt install python3.13 python3.13-dev python3.13-venv python3-pip python3-psutil -y
```

### 4. Update installed and existing packages

```bash
sudo apt update && sudo apt upgrade -y
```

### 5. (Optional but recommended) Create a tmux session

```bash
tmux new -s 43210
```

### 6. Download server files

```bash
git clone https://github.com/Saravanan4084/TKS_SERVER.git
cd TKS_SERVER
```

If you are using your own fork, replace the URL with your GitHub repository link.

### 7. Edit `config.yaml`

In the repo root, open `config.yaml` and change:

- Server name
- Port
- Admin accounts
- Playlist
- Team name, etc.

### 8. Make the server files executable

```bash
chmod 777 bombsquad_server
chmod 777 dist/bombsquad_headless
chmod 777 dist/bombsquad_headless_aarch64
```

### 9. Start the server

```bash
python3 ./bombsquad_server
```

If ports are open and configured correctly, you can connect to your server now.

---

## ⚙️ More Configuration

### Server Settings

Open:

```text
dist/ba_root/mods/setting.json
```

in your preferred editor and customize values for:

- `HostName` – server name
- `discordbot` – Discord bot token and channel IDs
- `textonmap` – text shown on map (top/bottom watermarks, owner line, center messages)
- `playlists` – playlist IDs used by the server
- AFK remover, leaderboard, night mode, whitelist, etc.

### Adding Yourself as Owner

1. Open:

   ```text
   dist/ba_root/mods/playersdata/roles.json
   ```

2. Find the **owner** role and add your PB‑ID in the owner id list.
3. Restart your server.

---

### Managing Players

Open:

```text
dist/ba_root/mods/playersdata/profiles.json
```

Here you can:

- Ban players
- Mute players
- Disable their kick votes
- Adjust other profile-related settings

---

## ✨ Features

### 🎮 Core Gameplay & Admin

- **Rank system**  
  - Tracks player stats and ranks; top players are shown on the map and in leaderboards.

- **Chat commands (normal & admin)**  
  - Rich set of commands for players and admins:
    - Normal: `/me`, `/stats`, `/coins`, `/shop`, `/tag`, `/save`, `/chatlist`, `/comp`, etc.
    - Admin: `kick`, `ban`, `unban`, `maxplayers`, `playlist`, `slowmo`, `mute`, `unmute`, and many more.

- **V2 Account with cloud console**  
  - Integration with Ballistica V2 account system (where available).

- **Ping checking**  
  - `/ping` to check your own ping  
  - `/ping all` to show ping for all players.

- **Hide / show player IDs**  
  - `/hideid` and `/showid` to hide or show player specs from clients.

- **Easy role management**  
  - Create many roles; assign different commands/tags to roles.  
  - Role system driven by `roles.json` and management commands.

- **Rejoin cooldown**  
  - Prevent players from rapidly rejoining.

- **Leaderboard**  
  - Top 3 rank player names on the screen (shimmer effect, top right).

- **Restrict kick vote starters**  
  - Limit which players are allowed to start kickvotes.

- **Owner join priority**  
  - Server owners can join even when full (based on stored IP/device info).

- **Auto-kick fake accounts**  
  - Detect and remove unsigned / not-master-verified accounts.

- **Auto public queue control**  
  - Automatically enable/disable public queue when server is full.

- **Auto night mode**  
  - Time-based night mode with optional fireflies.

- **Transparent kick vote**  
  - Shows who started a kick vote and against whom.

- **Kickvote message style**  
  - Choose to show kickvote messages as screen messages or chat messages.

- **IP and device tracking**  
  - Track player IP address and device UUID for banning and management.

---

### 💬 Chat & Voting Quality of Life

- **Team chat**  
  - Start message with `,` (comma) to send only to teammates.

- **In‑game popup chat**  
  - Start message with `.` (dot) to send as in‑game popup message.

- **Custom voting system**  
  - Type `end` in chat to start end vote.  
  - Also supports `sm`, `nv`, `dv` votes.

---

### 💰 Coin System & Shop

- Full **coin economy** (`tools/coins.py`):
  - Earn coins, bank score, convert score to coins.
  - Daily claim (`/claim`), transfer (`/transfer`), wallet (`/coins`).
  - Shop (`/shop`) for:
    - Temporary visual **effects** (e.g. spark, glow, rainbow ice, etc.)
    - **Tag pass** (`/shop buy tagpass`) to set a custom tag for 1 day.

- Effects & tags integrate with:
  - `spazmod/spaz_effects.py` – visual effects around players.
  - `chathandle` commands – to show prices & descriptions.

---

### 🤖 Discord Integration

- Integrated **Discord bot** (`features/discord_bot.py`):
  - Live **stats channel** (players, current/next game, CPU/RAM, top players).
  - Live **chat mirror**: in‑game chat mirrored to a logs channel.
  - **Game info channel**: per‑team and lobby embeds updating every few seconds.
  - **Logs channel**: server logs and text logs pushed automatically.
  - **Complaint system**:
    - In‑game `/comp` sends a rich embed to a complaints channel.
    - Discord staff buttons: “Complaint Accepted”, “Complaint Complete”.
    - Auto thread creation per complaint.

- **Remote admin from Discord**:
  - `c?` commands in your Discord command channel mapped to in‑game admin actions:
    - `c?kick`, `c?ban`, `c?sm`, `c?pause`, `c?recents`, `c?nv`, etc.
  - `c?say <name> <msg>` to send game chat messages from Discord.
  - `c?chatlist <pb-id> [days]` to inspect recent chat for a PB‑ID from log file.

- **Discord ACL**:
  - Allowed Discord user IDs are stored in `allowed_users.json`.
  - `c?adduser`, `c?removeuser`, `c?userlist` for managing who can run bot commands.

- **Role commands** (`r?` prefix):
  - `r?addrole`, `r?rmrole`, `r?crole`, `r?list` to manage BombSquad roles from Discord.

---

### 🌐 Website / API Integration

- **Ballistica web stats support**  
  - `ballistica_web` section in `setting.json` links this server to an external web stats panel:
    - `discord_link`
    - `enable`
    - `server_password`
---

### 🎨 Visual & Gameplay Enhancements

- **Text on map** (`features/text_on_map.py`):
  - Top center shimmering title (configurable in `setting.json`).
  - Bottom left watermarks and custom owner line.
  - Center rotating highlight messages (tips or info).
  - Season reset countdown and restart message.

- **Custom player effects & tags** (`spazmod/spaz_effects.py`, `spazmod/tag.py`):
  - Rainbow, glow, ice, metal, slime, orbiting heads, pets, etc.
  - Rank‑based auto effects for top players.
  - Custom tags above player heads with shimmer/animations.
  - HP display and rank indicators.

- **Many new mini‑games and maps**  
  - Extra games in `dist/ba_root/mods/games/` and maps in `dist/ba_root/mods/maps/`.

- **Colorful bomb explosions**  
  - Visual tweaks for explosions.

- **Floater & other fun features**  
  - Additional fun/cheat/admin utilities in `fun.py`, `cheats.py`, `NewCmds.py`.

- **Auto stats reset**  
  - Automatically resets season stats after configured days.

- **AFK / idle removal**  
  - Auto kick idle players in game and optionally in lobby.

- **Auto server update checks**  
  - Server can auto‑check for new versions.

- **All settings in one place**  
  - Most behavior is controlled via `setting.json`, no coding required.

- **Custom characters & character chooser**  
  - Support for external character packs and a character chooser at join.

- **Account age restrictions**  
  - Block very new accounts from chatting or joining if you want.

- **Auto team balance**  
  - Team balancing for dual‑team modes.

- **ElPatron powerups integration**  
  - Extended powerup system, fully configurable.

- **Coop auto-switch**  
  - Auto switch to coop playlist when players drop below a threshold.

- **On‑the‑fly playlist change**  
  - `/playlist teams`, `/playlist coop`, `/playlist 34532` to change playlist in-game.

- Many other small quality‑of‑life improvements – explore and tweak to your style.

---

## 🤖 Discord Bot Commands (Full List)

### `c?` commands (run in the configured command channel)

Core bot / ACL:

- `c?help` – Show all Discord bot commands and usage.
- `c?adduser <discord_id>` – Add a Discord user to the allowed list.
- `c?removeuser <discord_id>` – Remove a Discord user from the allowed list.
- `c?userlist` – Show all allowed Discord users.

Remote server control / info:

- `c?say <name> <message>` – Send a chat message into the game as `<name>`.
- `c?chatlist <pb-id> [days]` – Show a player’s recent chat from server logs.
- `c?sm` – Toggle slow motion in the server.
- `c?pause` – Pause or resume the current game.
- `c?kick <player/args>` – Kick a player.
- `c?ban <player/args>` – Ban a player.
- `c?unban <player/args>` – Unban a player (mapped to in‑game `unban`).
- `c?mute` / `c?mutechat` – Mute chat.
- `c?unmute` / `c?unmutechat` – Unmute chat.
- `c?nv` – Toggle night vision / night mode.
- `c?recents` – Show recent players.
- `c?restart` / `c?quit` – Restart or quit the server (mapped to in‑game commands).
- `c?end` / `c?next` – End current game / go to next.
- `c?maxplayers` / `c?max` – Change max players (via management module).
- `c?playlist` – Change playlist (same as `/playlist` in-game).

Player control / effects (mapped to in‑game admin commands):

- `c?hug`, `c?hugall` – Make one/all players hug.
- `c?control`, `c?exchange` – Swap/control other players.
- `c?icy` – Freeze players.
- `c?spaz`, `c?cc` – Apply spaz effect to a player.
- `c?spazall`, `c?ccall` – Apply spaz effect to all players.
- `c?box`, `c?boxall` – Put one/all players in a box.
- `c?kickall` – Kick all players.

Tag / role / ACL management:

- `c?customeffect <args>` – Set custom effect (mapped to `customeffect`).
- `c?removeeffect <args>` – Remove custom effect.
- `c?customtag <args>` – Set custom tag for a player.
- `c?changetag <args>` – Change tag for a player.
- `c?addcmd <role> <command>` – Attach a command to a role.
- `c?addrole <role> <pbid>` – Add role to a PB‑ID (when mapped).
- `c?rm` / `c?remove` – Remove a player from game (management `remove`).
- `c?acl` – Show ACL / role command overview.
- `c?pme` – Show stats for a specific player (mapped to `pme`).

> Note: Many `c?` commands are thin wrappers that call the same admin functions
> as the in-game chat commands. The exact argument formats follow the in‑game ones.

### `r?` role commands (run in role command channel)

- `r?help` – Show help for role commands.
- `r?addrole <role> <pbid>` – Add a role to a PB‑ID.
- `r?rmrole <role> <pbid>` / `r?removerole` / `r?delrole` – Remove a role.
- `r?crole <role> <pbid>` / `r?changerole` – Make this the only role for a PB‑ID.
- `r?list` / `r?listroles` / `r?show` – List all players with roles.

---

## 🧩 Command Modules Overview

All command modules live in:

```text
dist/ba_root/mods/chathandle/chatcommands/commands/
```

### `normal_commands.py` (public/player commands)

Commands:

- `me` / `stats` / `score` / `rank` / `myself`  
  Show your stats (score, games, kills, deaths, etc.).
- `list` / `l`  
  List players with client ID and player index.
- `uniqeid` / `id` / `pb-id` / `pb` / `accountid`  
  Show your account PB‑ID or someone else’s by index.
- `ping`, `ping all`  
  Show your ping or all players’ ping.
- `efflist`  
  Show all available visual effects.
- `cmdlist`  
  Show all available player commands.
- `help`  
  General help for normal commands.
- `pme`  
  Show stats for a specific player (by client ID).

Coin & wallet:

- `coins` / `wallet`  
  Show your coin balance and current active effect.
- `claim`  
  Claim your daily coin reward.
- `convert`  
  Convert banked score to coins.
- `transfer`  
  Transfer coins to another player.
- `shop`  
  Show the coin shop with available effects and tag pass.
- `coinhelp`  
  Help for the coin system and commands.

Tags & friends:

- `tag`  
  Use your tag pass to set a custom tag.
- `save`  
  Save a player as friend.
- `savelist`  
  Show your saved friends.
- `rmsave`  
  Remove a saved friend.
- `setmsg`  
  Set your custom join message.
- `sap`  
  Show available playlists.

Logs & complaints:

- `chatlist`  
  Show recent chats for a specific PB‑ID.
- `comp`  
  Send a complaint report (connected to Discord complaints channel).

### `management.py` (admin / owner commands)

Server / players:

- `recents`  
  Show recent players.
- `banlist`  
  Show banned players.
- `info` / `i`  
  Show detailed info about a player.
- `maxplayers` / `max`  
  Change the party max players.
- `playlist` / `p`  
  Change active playlist.
- `kick` / `k`  
  Kick a player.
- `ban` / `b`  
  Ban a player.
- `unban`  
  Unban a player.
- `unkick`  
  Remove a player from the kick‑ban list.
- `kickvote`  
  Start a default kick vote.
- `end` / `next` / `e`  
  End current game / go to next.
- `quit` / `restart` / `r`  
  Quit or restart server.
- `party`  
  Toggle party visibility (public / private).

Chat & visibility:

- `mute` / `mutechat`  
  Mute chat.
- `unmute` / `unmutechat`  
  Unmute chat.
- `showid` / `hideid`  
  Show or hide player IDs / specs.
- `lm`  
  Show last messages.

Gameplay / environment:

- `slowmo` / `slow` / `sm`  
  Toggle slow motion.
- `nv` / `night`  
  Night mode.
- `dv` / `day`  
  Day mode.
- `pause` / `pausegame`  
  Pause / unpause the game.
- `tint`  
  Adjust tint.
- `cameramode` / `camera_mode` / `rotate_camera`  
  Change/rotate camera mode.

Roles & ACL:

- `createrole`  
  Create a role.
- `addrole` / `removerole`  
  Assign/remove role to/from PB‑ID.
- `addcommand` / `addcmd` / `removecommand` / `removecmd`  
  Attach/remove commands to/from roles.
- `getroles`  
  List roles.
- `acl` / `admincmdlist` / `vipcmdlist` / `vcl`  
  Show ACL and admin/vip command lists.
- `spectators`  
  Manage spectators (whitelist / lobby handling).
- `lobbytime`  
  Set lobby idle time.
- `givecoins`  
  Give coins to player.

Fun / control:

- `hug`, `hugall`  
  Make players hug each other.
- `control`, `exchange`  
  Swap control between players.
- `icy`  
  Freeze player(s).
- `spaz`, `spazall`, `cc`, `ccall`  
  Apply spaz effects.
- `zombie`, `zombieall`  
  Turn players into zombies.
- `tex`, `texall`  
  Apply textures/effects.
- `playsound`, `ooh`  
  Play sound effects.
- `floater`  
  Float players (floater feature).
- `healer`, `rmhealer`  
  Add/remove healer.
- `attack`  
  Special attack utility.

Bomb / powerup tuning:

- `dbc`, `d_bomb_count`, `default_bomb_count`  
  Default bomb count controls.
- `dbt`, `d_bomb_type`, `default_bomb_type`  
  Default bomb type controls.

### `fun.py` (fun cosmetic commands)

Commands:

- `speed`  
  Change game/player speed factor.
- `fly`  
  Toggle flying for a specific player or all.
- `invisible` / `inv`  
  Make players invisible.
- `headless` / `hl`  
  Make players headless.
- `creepy` / `creep`  
  Apply creepy look/effects.
- `celebrate` / `celeb`  
  Celebration effects.
- `spaz`  
  Spaz effect.
- `floater` / `flo`  
  Enable floater controls for a client.

### `cheats.py` (admin-only cheat/power commands)

Commands:

- `kill` / `die`  
  Kill a player or everyone.
- `heal` / `heath`  
  Heal player(s).
- `curse` / `cur`  
  Apply curse powerup.
- `sleep`  
  Knock out players.
- `superpunch` / `sp`  
  Super punches.
- `gloves` / `punch`  
  Give boxing gloves.
- `shield` / `protect`  
  Give shield.
- `freeze` / `ice`  
  Freeze players.
- `unfreeze` / `thaw`  
  Unfreeze players.
- `godmode` / `gm`  
  God mode (high survivability).

### `NewCmds.py` (extra utility/fun/admin commands)

Commands:

- `hug`, `hugall`  
  Same as management, but implemented with extra logic.
- `control`, `exchange`  
  Swap control.
- `icy`  
  Freeze players.
- `spaz`, `spazall`, `cc`, `ccall`  
  Spaz effects.
- `box`, `boxall`  
  Box players.
- `kickall`  
  Kick all players.
- `tex`, `texall`  
  Texture / visual effects.
- `zombie`, `zombieall`  
  Zombie mode.
- `say`  
  Server chat from commands.
- `acl`, `admincmdlist`, `vipcmdlist`, `vcl`  
  ACL and admin/vip command listing.
- `ooh`  
  Play “ooh” sound.
- `zm` / `zoommessage`  
  Zoomed‑in text messages.
- `playsound`  
  Play custom sound.
- `prot` / `protect`  
  Protect players.
- `pme`  
  Print stats for a player by client ID.

