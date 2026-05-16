# Commands and Troubleshooting

Use this reference for Flatpak user operations, permission overrides, downgrade/bisect workflows, uninstall cleanup, rebuilds from published sources, and common debugging commands.

## Contents

- Repository Setup
- User vs System Installs
- Installing and Running
- Permissions and Overrides
- Updates, Downgrades, and Bisecting
- Uninstalling and Cleanup
- Rebuild from Published Sources
- Slow Connection Checks
- Debugging Installed Apps
- Offline and USB Distribution

## Repository Setup

Add Flathub user-wide:

```bash
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Add Flathub system-wide:

```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Flathub Beta:

```bash
flatpak remote-add --if-not-exists --user flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo
```

List remotes:

```bash
flatpak remotes --columns=name,url,options
```

## User vs System Installs

- Per-user installs do not need administrator privileges and live under the user's Flatpak installation.
- System-wide installs are available to all users and may require administrator privileges.
- Many commands accept `--user` or `--system`. Match the location of the remote and installed ref.

## Installing and Running

```bash
flatpak search <name>
flatpak install flathub <app-id>
flatpak install --user flathub <app-id>
flatpak run <app-id>
flatpak info <app-id>
flatpak list --app
```

Install a specific branch or architecture using an identifier triple:

```bash
flatpak install flathub <app-id>/<arch>/<branch>
```

## Permissions and Overrides

Show static permissions:

```bash
flatpak info --show-permissions <app-id>
```

Show overrides:

```bash
flatpak override --show <app-id>
```

Add an override:

```bash
flatpak override --user --filesystem=xdg-download:ro <app-id>
```

Reset overrides:

```bash
flatpak override --user --reset <app-id>
```

Portal permissions:

```bash
flatpak permission-show <app-id>
flatpak permission-reset <app-id>
```

When advising users, prefer narrower grants and explain the security tradeoff.

## Updates, Downgrades, and Bisecting

Update:

```bash
flatpak update
flatpak update <app-id>
```

Show history:

```bash
flatpak remote-info --log flathub <app-id>
```

Deploy an older commit:

```bash
flatpak update --commit=<commit> <app-id>
```

Prevent automatic updates for a ref:

```bash
flatpak mask <app-id>
flatpak mask --remove <app-id>
flatpak mask --list
```

For regression bisects, use the Flathub docs workflow: identify commits from `remote-info --log`, deploy candidate commits, test, and narrow the bad range.

## Uninstalling and Cleanup

Uninstall an app:

```bash
flatpak uninstall <app-id>
```

Remove app data only when the user explicitly wants it:

```bash
flatpak uninstall --delete-data <app-id>
```

Remove unused runtimes and extensions:

```bash
flatpak uninstall --unused
```

Remove a remote:

```bash
flatpak remote-delete <remote-name>
```

## Rebuild from Published Sources

When a user wants to rebuild a Flathub app from published sources:

1. Find the app's Flathub repository or source location.
2. Clone the Flathub manifest repository.
3. Install the matching runtime and SDK from Flathub.
4. Build with `org.flatpak.Builder` or `flatpak-builder`.
5. Install locally and test with `flatpak run`.

Use current Flathub docs for app-specific source discovery details, because source locations and repository layouts can change.

## Slow Connection Checks

For slow Flathub downloads:

- Confirm whether the issue affects all apps or one ref.
- Check the user's region, ISP, DNS, proxy/VPN, and whether IPv6 is involved.
- Try again later before assuming a packaging issue.
- Collect `flatpak -v` output and remote URL details when reporting.

## Debugging Installed Apps

Install debug material:

```bash
flatpak install --include-sdk --include-debug <app-id>
```

Open a debug shell:

```bash
flatpak run --command=sh --devel --filesystem=$(pwd) <app-id>
```

Open a build tree shell:

```bash
flatpak-builder --run build-dir <manifest> sh
```

GDB:

```bash
gdb /app/bin/<binary>
(gdb) run
(gdb) bt full
(gdb) thread apply all backtrace
```

Coredump:

```bash
coredumpctl list
flatpak-coredumpctl -m <pid> <app-id>
```

Other tools:

```bash
valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all /app/bin/<binary>
strace -e trace=openat,read -o strace.log -f /app/bin/<binary>
```

Audit D-Bus:

```bash
flatpak run --log-session-bus <app-id>
flatpak run --log-system-bus <app-id>
```

Enter another shell in the same sandbox:

```bash
flatpak ps
flatpak enter <instance-id> /bin/bash
```

## Offline and USB Distribution

Use `flatpak create-usb` for offline transfer when collection IDs and remote metadata are suitable:

```bash
flatpak list --app
flatpak remotes --columns=name,collection
flatpak create-usb <mountpoint> <app-id>
```

On newer setups, `flatpak install` may use sideload repositories automatically. Otherwise use:

```bash
flatpak install --sideload-repo=<path> <remote> <app-id>
```
