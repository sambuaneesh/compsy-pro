# System Specs Snapshot

Last captured: `2026-04-24T09:43:48+05:30` (Asia/Kolkata)

## Host / OS

- Hostname: `Bor`
- OS: `Ubuntu 22.04.5 LTS (Jammy Jellyfish)`
- Kernel: `Linux 6.8.0-107-generic`
- Architecture: `x86_64`

## CPU

- Model: `AMD Ryzen 9 7950X3D 16-Core Processor`
- Cores / Threads: `16 / 32`
- Sockets: `1`
- Base min MHz: `400`
- Max MHz: `5858`
- Caches:
- L1d: `512 KiB (16 instances)`
- L1i: `512 KiB (16 instances)`
- L2: `16 MiB (16 instances)`
- L3: `128 MiB (2 instances)`
- Virtualization: `AMD-V`

## Memory

- RAM (total): `30 GiB`
- RAM (used at capture): `10 GiB`
- RAM (available at capture): `19 GiB`
- Swap: `2.0 GiB` (used: `0`)

## GPU

- NVIDIA:
- Model: `NVIDIA GeForce RTX 5060 Ti`
- Driver: `580.126.09`
- CUDA: `13.0`
- VRAM: `16311 MiB`
- AMD iGPU/secondary display adapter also present (`Advanced Micro Devices, Inc. [AMD/ATI] Device 164e`)

## Storage

- Root disk: `/dev/nvme0n1` (`465.8G`)
- `/` partition: `/dev/nvme0n1p2` ext4 (`457G`, ~`51%` used at capture)
- EFI: `/dev/nvme0n1p1` vfat (`512M`)
- Home disk: `/dev/nvme1n1` (`1.8T`)
- `/home` partition: `/dev/nvme1n1p1` ext4 (`1.8T`, ~`20%` used at capture)

## Network Interfaces (at capture)

- Ethernet: `enp6s0` (`UP`, IPv4 `10.2.36.243/24`)
- Wireless interface present: `wlxa842a1408444` (`DOWN`)
- Tailscale: `tailscale0` (IPv4 `100.122.80.98/32`)
- Virtual/container bridges present: `virbr0`, `docker0`, `br-b797158973ac`
- Ethernet controller: `Realtek RTL8125 2.5GbE`

## Toolchain / Runtime Versions

- Python: `3.8.5`
- Node.js: `v20.20.0`
- npm: `10.8.2`
- Git: `2.34.1`
- Docker Engine: `28.2.2`
- GCC: `11.4.0`
- Java (OpenJDK): `11.0.30`
- Not installed (in PATH at capture): `go`, `rustc`, `pnpm`
- Docker Compose plugin: not available via `docker compose`

## Notes

- This is a point-in-time snapshot. Re-run capture periodically to keep it current.
- This file is intended as the baseline inventory for future setup and debugging tasks.
