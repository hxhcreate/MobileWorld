<h1 align="center">Mobile World</h1>

<p align="center">
  <strong>Benchmarking Autonomous Mobile Agents in Agent-User Interactive, and MCP-Augmented Environments</strong>
</p>

<p align="center">
  <a href="https://tongyi-mai.github.io/MobileWorld/"><img src="https://img.shields.io/badge/Project-Website-blue" alt="Project Website"></a>
  <a href="https://arxiv.org/abs/2512.19432"><img src="https://img.shields.io/badge/arXiv-Paper-red" alt="arXiv Paper"></a>
  <a href="https://github.com/Tongyi-MAI/MobileWorld"><img src="https://img.shields.io/badge/GitHub-Repo-green" alt="GitHub"></a>
  <a href="#citation"><img src="https://img.shields.io/badge/Cite-BibTeX-orange" alt="Citation"></a>
</p>

<p align="left">
  <b>Mobile World</b> is a challenging mobile-use benchmark designed to reflect real-world scenarios. It comprises <b>201 tasks</b> across <b>20 applications</b>, featuring long-horizon, cross-app tasks, and novel task categories including agent–user interaction and MCP-augmented tasks.
</p>

---

## News

- **[2025-12-23]** Docker image `ghcr.io/Tongyi-MAI/mobile_world:latest` available
- **[2025-12-23]** Initial release of Mobile World benchmark

---

## Installation & Prerequisites

### System Requirements

- **Docker** with privileged container support
- **KVM** (Kernel-based Virtual Machine) for Android emulator acceleration
- **Python 3.12+**
- **Linux** host system (or Windows with WSL2 + KVM enabled), MacOS support is in progress.

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Tongyi-MAI/MobileWorld.git
cd MobileWorld

# Install dependencies with uv
uv sync
```

### Environment Configuration

Create a `.env` file from `.env.example` in the project root with your OpenAI-compatible API key and other required parameters. Refer to [MCP Setup](docs/mcp_setup.md) for setting up MCP servers.

---

## Quick Start

### 1. Check Environment & Pull Docker Image

```bash
sudo mw env check
```

This command verifies Docker, KVM support, and prompts to pull the latest `mobile_world` Docker image if needed.

### 2. Launch Docker Containers

```bash
sudo mw env run --count 5 --launch-interval 20
```

This launches 5 containerized Android environments with:
- `--count 5`: Number of parallel containers
- `--launch-interval 20`: Wait 20 seconds between container launches

### 3. Run Evaluation

```bash
sudo mw eval \
    --agent_type qwen3vl \
    --task ALL \
    --max_round 50 \
    --model_name Qwen3-VL-235B-A22B \
    --llm_base_url [openai_compatible_url] \
    --step_wait_time 3 \
    --log_file_root traj_logs/qwen3_vl_logs \
    --enable_mcp
```

Parameters:
- `--agent_type`: Agent implementation to use (e.g., `qwen3vl`)
- `--task ALL`: Run all benchmark tasks
- `--max_round 50`: Maximum steps per task
- `--model_name`: VLM model to use
- `--llm_base_url`: OpenAI-compatible API endpoint
- `--step_wait_time`: Wait time between actions (seconds)
- `--log_file_root`: Directory for trajectory logs
- `--enable_mcp`: Enable MCP server for external tools, if not set, the MCP-augmented tasks will be skipped.

### 4. View Results

```bash
mw logs view --log_dir traj_logs/qwen3_vl_logs
```

Opens an interactive web-based visualization at `http://localhost:7860` to explore task trajectories and results.

---

## Available Commands

Mobile World provides a comprehensive CLI (`mw` or `mobile-world`) with the following commands:

| Command | Description |
|---------|-------------|
| `mw env check` | Check prerequisites (Docker, KVM) and pull latest image |
| `mw env run` | Launch Docker container(s) with Android emulators |
| `mw env list` | List running Mobile World containers |
| `mw env rm` | Remove/destroy containers |
| `mw env info` | Get detailed info about a container |
| `mw env restart` | Restart the server in a container |
| `mw env exec` | Open a shell in a container |
| `mw eval` | Run benchmark evaluation suite |
| `mw test` | Run a single ad-hoc task for testing |
| `mw info task` | Display available tasks |
| `mw info agent` | Display available agents |
| `mw info app` | Display available apps |
| `mw info mcp` | Display available MCP tools |
| `mw logs view` | Launch interactive log viewer |
| `mw logs results` | Print results summary table |
| `mw logs export` | Export logs as static HTML site |
| `mw device` | View live Android device screen |
| `mw server` | Start the backend API server |

Use `mw <command> --help` for detailed options.

---

## Documentation

For detailed documentation, see the `docs/` directory:

| Document | Description |
|----------|-------------|
| [Development Guide](docs/development.md) | Dev mode, debugging, container management workflows |
| [MCP Setup](docs/mcp_setup.md) | Configure MCP servers for external tool integration |
| [Windows Setup](docs/setup_for_windows.md) | WSL2 and KVM setup instructions for Windows |
| [AVD Configuration](docs/configure_avd.md) | Customize and save Android Virtual Device snapshots |

---

## Acknowledgements

We thank [Android World](https://github.com/google-research/android_world) and [Android-Lab](https://github.com/THUDM/Android-Lab) for their open source contributions.

---

## Citation

If you find Mobile World useful in your research, please cite our paper:

```bibtex
@article{mobileworld2025,
  title={MobileWorld: Benchmarking Autonomous Mobile Agents in Agent-User Interactive, and MCP-Augmented Environments},
  author={Quyu Kong and Xu Zhang and Zhenyu Yang and Nolan Gao and Chen Liu and Panrong Tong and Chenglin Cai and Hanzhang Zhou and Jianan Zhang and Liangyu Chen and Zhidan Liu and Steven Hoi and Yue Wang},
  journal={arXiv preprint arXiv:2512.19432},
  year={2025}
}
```

---

## Contact

For questions, issues, or collaboration inquiries:

- **GitHub Issues**: [Open an issue](https://github.com/Tongyi-MAI/MobileWorld/issues)
- **WeChat Group**: Scan to join our discussion group

<p align="center">
  <img src="site/assets/wechat_qr.png" alt="WeChat Group QR Code" width="200">
</p>
