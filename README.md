# 🌪️ NetStorm Pro - Advanced Network Testing Suite

![NetStorm Pro Banner](./img/netstorm_banner.png)
![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-CC--BY--NC--4.0-lightgrey.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-brightgreen.svg)
![Version](https://img.shields.io/badge/Version-3.0.0-purple.svg)

**NetStorm Pro** is an advanced multi-protocol network testing suite designed for security professionals and system administrators. It offers comprehensive network analysis and stress testing capabilities with support for multiple targets and attack methods.

## 🚀 Key Features

### ⚡ Multi-Protocol Support
- **UDP Flood**: High-speed UDP packet flooding
- **TCP SYN Flood**: Half-open connection attacks
- **HTTP Flood**: HTTP request flooding
- **DNS Amplification**: DNS amplification attack simulation
- **Mixed Attacks**: Intelligent combination of multiple methods

### 🎯 Advanced Target Management
- Single and multiple target support
- Load targets from text files
- Automatic target validation
- Custom ports per target

### 📊 Real-Time Monitoring
- Live statistics during execution
- Visual progress bar
- Real-time performance metrics
- Detailed post-execution reports

### 🔧 Technical Features
- High-performance multi-threaded architecture
- Dynamic payload system
- Elegant error handling
- Colored terminal interface

## 📦 Installation

### System Requirements
- Python 3.6 or higher
- Operating System: Linux, Windows, or macOS
- Appropriate network permissions

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/CHICO-CP/netstorm-pro.git
cd netstorm-pro

# Run directly
python3 netstorm_pro.py --help
```

# 🛠️ Basic Usage

### Comprehensive Help

```bash
python3 netstorm_pro.py --help
```

### Single Target Attack

```bash
# Basic UDP Flood
python3 netstorm_pro.py -t 192.168.1.1 -p 80 -d 60 -th 20 -m udp_flood

# Advanced HTTP Flood
python3 netstorm_pro.py -t example.com -p 443 -d 120 -th 50 -m http_flood

# Mixed Attack
python3 netstorm_pro.py -t target.com -p 53 -d 300 -th 100 -m mixed
```

### Multi-Target Attacks

```bash
# From targets file
python3 netstorm_pro.py -f targets.txt -p 80 -d 180 -th 30 -m tcp_syn
```

# 📁 Targets File Format

Create a targets.txt file with the following format:

```
# Comments with #
192.168.1.1
example.com
10.0.0.5:8080
google.com:443
target-domain.com:21
```

## 🎯 Available Attack Methods

| Method | Description | Use Cases |
|--------|-------------|-----------|
| `udp_flood` | High-speed UDP flooding | Bandwidth testing |
| `tcp_syn` | TCP half-open connection flood | Web server testing |
| `http_flood` | HTTP request flooding | Web application testing |
| `dns_amp` | DNS amplification simulation | DNS server testing |
| `mixed` | Multiple method combination | Comprehensive resilience testing |

## 📊 Statistics and Metrics

NetStorm Pro provides real-time metrics during execution:

· 📦 **Packets Sent**: Total packet counter  
· 🚨 **Errors**: Connection/sending failures  
· 🧵 **Active Threads**: Running thread count  
· ⏱️ **Elapsed/Remaining Time**: Precise time control  
· 📈 **Packets/Second**: Performance metric  

# 🔒 Security Considerations

### ⚠️ LEGAL WARNING

```
NetStorm Pro is designed EXCLUSIVELY for:
✓ Authorized security testing
✓ Controlled laboratory environments
✓ Evaluation of own systems
✓ Research and education

UNAUTHORIZED USE IS ILLEGAL AND ETHICALLY WRONG.
The developer is not responsible for misuse of this tool.
```

## 🔒 Best Practices

· ✅ **Use only on own networks or with explicit authorization**  
· ✅ **Perform tests in controlled environments**  
· ✅ **Document all tests performed**  
· ✅ **Respect acceptable use policies**  

# 🐛 Troubleshooting

### Common Errors

```bash
# Error: Cannot resolve hostname
❌ Check DNS connectivity and target name

# Error: Permission denied
❌ Run with appropriate system permissions

# Error: Invalid port
✅ Use ports in range 1-65535
```

## ⚡ Performance Optimization

· **Adjust thread count according to hardware**  
· **Use mixed for complex stress tests**  
· **Monitor system resource usage**  

## 🤝 Contributing

Contributions are welcome. Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support and Contact

· **GitHub**: [github.com/CHICO-CP](https://github.com/CHICO-CP)  
· **Telegram**: [@Gh0stDeveloper](https://t.me/Gh0stDeveloper)  
· **Telegram Channel**: [Ghost Developer](https://t.me/GhostDeve)  
· **Discord**: [Join our community](https://discord.gg/SHjF9qw9)  
· **Developer**: Ghost Developer  

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the `LICENSE` file for details.

---

**⚠️ IMPORTANT NOTE**: This tool should be used only for educational and testing purposes in controlled environments. Malicious use is strictly prohibited.

**🔐 Responsible Security • 🎓 Continuous Education • 🔧 Professional Development**