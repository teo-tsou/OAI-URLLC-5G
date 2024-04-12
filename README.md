# OAI 5G URLLC Network Evaluation

![Alt text](/figures/setup.png)

## Overview
This repository provides comprehensive instructions and necessary files for evaluating an end-to-end Ultra-Reliable Low-Latency Communication (URLLC) 5G Network using OpenairInterface (OAI). URLLC is a key component of 5G networks, offering highly reliable and low-latency communication ideal for critical applications such as autonomous driving, industrial IoT, and remote surgery.

We offer a complete suite of OAI Core deployment files, incorporating various User Plane Function (UPF) implementations, including SPGWU, VPP, and eBPF.
In addition, this project guides you through system optimizations and RAN configurations that are essential for enabling URLLC capabilities in your 5G network setup.

## Prerequisites

### System
- Laptop/Desktop/Server for OAI CN5G and OAI gNB
    - Operating System: [Ubuntu 22.04 LTS](https://releases.ubuntu.com/22.04/ubuntu-22.04.1-desktop-amd64.iso)
    - CPU: 16 cores, 11th Gen Intel Core i7-11700K
    - RAM: 32 GB
- Laptop/Desktop/Server for UE
    - Operating System: Microsoft Windows 10 x64 / Ubuntu 20.04 LTS
    - CPU: 4 cores x86_64
    - RAM: 8 GB
    - Windows driver for Quectel MUST be equal or higher than version **2.2.4**
    - The Ubuntu driver can be found under quectel-ue directory
- [USRP B210](https://www.ettus.com/all-products/ub210-kit/), [USRP N300](https://www.ettus.com/all-products/USRP-N300/) or [USRP X300](https://www.ettus.com/all-products/x300-kit/)
    - Please identify the network interface(s) on which the USRP is connected and update the gNB configuration file. We are using N310 with 2x2 MIMO configuration.
- Quectel RM500Q
    - Module, M.2 to USB adapter, antennas, and SIM card
    - Firmware version of Quectel MUST be equal or higher than **RM500QGLABR11A06M4G**
    - Ideally with MIMO 2x2

### Docker Installation

Update:
```
sudo apt-get update
```
Install Docker:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
Enable & start Docker with the following commands:
```
sudo systemctl enable docker
```

```
sudo systemctl start docker
```

### Docker Compose Installation:

Download Docker Compose from its official GitHub repository
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.0.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Apply executable permissions to the binary:
```
sudo chmod +x /usr/local/bin/docker-compose
```

## System Optimizations

- You need to install Real-Time Ubuntu kernels from [here](https://www.acontis.com/en/building-a-real-time-linux-kernel-in-ubuntu-preemptrt.html) to enable real-time perfomance
- Enable Performance Mode on CPU cores: `cpupower idle-set -D 0`
- Use a new UHD version (4.6.0 and newer)
- Install the XG FPGA image flavor for 10 Gbps speeds. More info on [Ettus](https://kb.ettus.com/USRP_Host_Performance_Tuning_Tips_and_Tricks) website.
- Increase Ethernet Ring Buffers: `sudo ethtool -G <ifname> rx 4096 tx 4096`
- Disable hyper-threading in the BIOS (This step is optional)
- Optional: Disable KPTI Protections for Spectre/Meltdown for more performance. **This is a security risk.** Add `mitigations=off nosmt` in your grub config and update grub.
- Enable Governor CPU and adjust network buffers:
```
for ((i=0;i<$(nproc);i++)); do sudo cpufreq-set -c $i -r -g performance; done
sudo sysctl -w net.core.wmem_max=62500000
sudo sysctl -w net.core.rmem_max=62500000
sudo sysctl -w net.core.wmem_default=62500000
sudo sysctl -w net.core.rmem_default=62500000
sudo ethtool -G enp1s0f0 tx 4096 rx 4096
```

- Adjust Ethernet MTU

  -  This applies to Ethernet connected USRPs (N2xx, N3xx, X3xx, E320).

  - For 1 Gigabit connections, the MTU should be set to 1500.

  - For 10 Gigabit connections, the MTU should be set to 9000.

  - It is important to set the value and not leave it is automatic

## UPF Solutions Evaluation


Each UPF deployment has one folder for the core network configuration (i.e. spgwu, vpp, p4) and one folder for the respective UERANSIM deployment (i.e. UERASNIM-spgwu, UERASNIM-vpp, UERASNIM-p4). You can manually deploy everything by using the docker-compose -f command. However, we have generated scripts for deploying and destroying each deployment more easily. To isolate our focus only on the UPF perfomance we 

### SPGWU-UPF

The OpenAirInterface's 'oai-spgwu-tiny' is an enhanced version of the Serving and Packet Data Network Gateway User plane (SPGW-U), a key component in 4G/LTE networks for routing and forwarding user data. Initially designed for 4G/LTE based on 3GPP standards, it has been updated to also support 5G networks.

![Alt text](/figures/spgwu_arch.png)

To Deploy this setup you have to execute the following commands on your host machine:

* Deploy the 5G Core Network based on SPGWU:
```
sudo bash scripts/deploy-spgwu-based-core.sh
```
* Deploy 5G RAN based on UERANSIM:
```
sudo bash scripts/deploy-ueransim-spgwu.sh
```

When both commands are executed, your SPGWU-based deployment should be working properly. 

- You may check the status of your containers with:
```
sudo docker ps -a
```
- You may check the logs of each core network function by executing the following command (generates .txt log files):
```
sudo bash scripts/generate-logs-spgwu.sh
```
- You can destroy the whole architecture by executing the following commands:
```
sudo bash scripts/destroy-spgwu-based-core.sh
```
```
sudo bash scripts/destroy-spgwu-ueransim.sh
```


### VPP-UPF: 

Vector Packet Processing (VPP) is a high-speed, high-efficiency packet processing framework that enhances data plane performance in networks. Unlike traditional methods, VPP uses vector processing to handle multiple packets simultaneously, leveraging modern CPUs' SIMD capabilities for parallel processing. This results in high throughput and low latency, often outperforming specialized hardware. VPP incorporates the Data Plane Development Kit (DPDK) for direct NIC access, bypassing the OS network stack, and distributing workloads across multiple CPU cores for scalability. VPP is particularly beneficial in 5G networks, where it's used for User Plane Function solutions, handling high-speed data with low response times.

![Alt text](/figures/vpp_arch.png)

To Deploy this setup you have to execute the following commands on your host machine:

* Deploy the 5G Core Network based on VPP:
```
sudo bash scripts/deploy-vpp-based-core.sh
```
* Deploy 5G RAN based on UERANSIM:
```
sudo bash scripts/deploy-ueransim-vpp.sh
```

When both commands are executed, your VPP-based deployment should be working properly. 

- You may check the status of your containers with:
```
sudo docker ps -a
```
- You may check the logs of each core network function by executing the following command (generates .txt log files):
```
bash scripts/generate-logs-vpp.sh
```
- You can destroy the whole architecture by executing the following commands:
```
sudo bash scripts/destroy-vpp-based-core.sh
```
```
sudo bash scripts/destroy-vpp-ueransim.sh
```
### EBPF-UPF:

eBPF (Extended Berkeley Packet Filter) is a powerful technology that allows code to run in the kernel space within a safe, restricted environment. It has evolved significantly since its origins as a packet filtering mechanism. eBPF UPF offers further capabilities including security, networking, and performance monitoring because it's highly efficient and flexible. Note that we're using the generic EBPF version which doesn't offload the processing to the net cards. The performance could vary from machine to machine.

![Alt text](/figures/ebpf_arch.png)

 To Deploy this setup you have to execute the following commands on your host machine:

* Deploy the 5G Core Network based on EBPF:
```
sudo bash scripts/deploy-ebpf-based-core.sh
```
* Deploy 5G RAN based on UERANSIM:
```
sudo bash scripts/deploy-ueransim-ebpf.sh
```

When both commands are executed, your EBPF-based deployment should be working properly. 

- You may check the status of your containers with:
```
sudo docker ps -a
```
- You may check the logs of each core network function by executing the following command (generates .txt log files):
```
bash scripts/generate-logs-ebpf.sh
```
- You can destroy the whole architecture by executing the following commands:
```
sudo bash scripts/destroy-ebpf-based-core.sh
```
```
sudo bash scripts/destroy-ebpf-ueransim.sh

```

Among these UPFs for URLLC, it is recommended to either utilize VPP or URLLC in your setup!

## RAN Configurations

Before heading to the configurations let's first install the OAI RAN with E2 capabilities:

Install and deploy the OAI 5G SA gNB as follows

## <a name='BuildOAIgNB'></a>5.1 Build OAI gNB

```bash
# Get openairinterface5g source code
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git ~/openairinterface5g
cd ~/openairinterface5g
git checkout develop

# Install OAI dependencies
cd ~/openairinterface5g/cmake_targets
./build_oai -I

# Build OAI gNB
cd ~/openairinterface5g
source oaienv
cd cmake_targets
./build_oai -w USRP --ninja --gNB -c --build-e2
```

* All the important modifications are gathered in the table below:

![Alt text](/figures/table.png)

The configuration files can be found under the ran_confs directory of the repo. All confs are specifically for 2X2 MIMO N310 USRP:

- For the default 5ms TDD cycle duration:  `gnb-78-2x2-106prb-5ms-tdd.conf`
- For the 2.5ms TDD cycle duration: ` gnb-78-2x2-106prb-2.5ms-tdd.conf`
- For the 2ms TDD cycle duration: ` gnb-78-2x2-106prb-2ms-tdd.conf`



**For 2.5ms TDD**



```
     referenceSubcarrierSpacing                                    = 1;
     dl_UL_TransmissionPeriodicity                                 = 5;
     nrofDownlinkSlots                                             = 3;
     nrofDownlinkSymbols                                           = 6;
     nrofUplinkSlots                                               = 1;
     nrofUplinkSymbols                                             = 4;
```


**For 2ms TDD**

```
     referenceSubcarrierSpacing                                    = 1;
     dl_UL_TransmissionPeriodicity                                 = 4;
     nrofDownlinkSlots                                             = 2;
     nrofDownlinkSymbols                                           = 6;
     nrofUplinkSlots                                               = 1;
     nrofUplinkSymbols                                             = 4;
```

- Make sure you have this in the MACRLC section of the configuration file for the UL max frame inactivity :

`ulsch_max_frame_inactivity=0;`

This guarantees UL is scheduled in every TDD period with the minimal UL allocation (5 PRBs by default, mcs 9). You might want to increase this minimal allocation to something like :

```
min_grant_prb = 20;
min_grant_mcs = 16;
```

 - Also modify the `sl_ahead` in the RU section: should be 5 for 2.5 ms and 4 for 2ms


   Before running the softmodems ensure the following:

* The MCC, MNC, TAC (tracking_area_code) and S-NSSAI (SST and SD) parameters should be the same as the values seen in the core configuration files.
* To configure the connection between the core and the gNB, you need to set the correct AMF parameters (amf_ip_address) to the address of the AMF and the correct network interfaces (NETWORK_INTERFACES).
* The selected frequency band and configuration should be supported by the UE, we used TDD band 78 with the QUECTEL UE.


**For N300 USRP:**
`sudo ./nr-softmodem -O gnb-78-2x2-106prb-2ms-tdd.conf --sa --usrp-tx-thread-config 1`

- To reduce the number of LDPC decoder iterations, which will make the LDPC decoder take less time add this as a running argument in the command: `--L1s.[0].max_ldpc_iterations 4`
- To experiment with the various UL MAX MCS: `--MACRLCs.[0].ul_max_mcs 6`.



## (Optional) XApp Measurements

- To collect various measurements from MAC, RLC, and PDCP layers you can use our xapp (which can be found in xapp directory), which collects the following metrics and stores them to CSV files for further preprocessing:


**MAC Layer Metrics** 

The following metrics are collected from the MAC layer:

- **Timestamp**: The time at which the metrics were collected.
- **RNTI**: Radio Network Temporary Identifier.
- **CQI**: Channel Quality Indicator.
- **PUSCH SNR**: Signal-to-Noise Ratio on the Physical Uplink Shared Channel.
- **UL BLER**: Uplink Block Error Rate.
- **DL BLER**: Downlink Block Error Rate.
- **UL MCS1**: Uplink Modulation and Coding Scheme 1.
- **UL MCS2**: Uplink Modulation and Coding Scheme 2.
- **DL MCS1**: Downlink Modulation and Coding Scheme 1.
- **DL MCS2**: Downlink Modulation and Coding Scheme 2.
- **UL Throughput**: Uplink Throughput.
- **DL Throughput**: Downlink Throughput.

**RLC Layer Metrics**

Metrics gathered from the RLC layer include:

- **Timestamp**: The time at which the metrics were collected.
- **TXPDU WT MS**: Transmission PDU Wait Time in Milliseconds.
- **TXBUF OCC Bytes**: Transmission Buffer Occupancy in Bytes.
- **RXBUF OCC Bytes**: Reception Buffer Occupancy in Bytes.
- **TXPDU RETX PKTS**: Transmission PDU Retransmitted Packets.
- **RXPDU DUP PKTS**: Received PDU Duplicate Packets.
- **TXPDU DD PKTS**: Transmission PDU Discarded Packets.
- **RXPDU DD PKTS**: Received PDU Discarded Packets.
- **TXPDU Segmented**: Transmission PDU Segmented.
- **RXPDU Status PKTS**: Received PDU Status Packets.
- **TXSDU PKTS**: Transmission SDU Packets.
- **RXSDU PKTS**: Received SDU Packets.

**PDCP Layer Metrics**

From the PDCP layer, the `xapp` collects:

- **Timestamp**: The time at which the metrics were collected.
- **RXPDU OO PKTS**: Received PDU Out Of Order Packets.
- **RXPDU OO Bytes**: Received PDU Out Of Order Bytes.
- **RXPDU DD PKTS**: Received PDU Discarded Packets.
- **RXPDU DD Bytes**: Received PDU Discarded Bytes.
- **RXPDU RO Count**: Received PDU Reordering Count.
- **TXPDU PKTS**: Transmission PDU Packets.
- **TXPDU Bytes**: Transmission PDU Bytes.
- **RXPDU PKTS**: Received PDU Packets.
- **RXPDU Bytes**: Received PDU Bytes.
- **TXSDU PKTS**: Transmission SDU Packets.
- **TXSDU Bytes**: Transmission SDU Bytes.
- **RXSDU PKTS**: Received SDU Packets.
- **RXSDU Bytes**: Received SDU Bytes.

To run this xapp you need to install FlexRIC. Please refer to this [tutorial](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair2/E2AP/README.md)

## (Optional) One-Way Latency Measurements

One-latency measurements are very important in order to evaluate URLLC systems. We're taking one-way latency measurements via the [owamp tool](https://github.com/perfsonar/owamp). We have prepared an install script in the scripts directory referred to as owamp-install.sh . You can install it on the external-network/core side and on the UE to get the one-way measurements.

