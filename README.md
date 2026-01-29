# Multi-Router Configuration Demo Application

## Project Overview
This project presents a Multi-Router Configuration Demo Application designed to demonstrate the principles of Software Defined Networking (SDN) and network automation using OpenDaylight (ODL) and NETCONF/YANG technologies.
The application provides a graphical user interface (GUI) that allows users to visualize a network topology, select routers, and simulate configuration tasks without manually accessing router command-line interfaces.
The system is implemented using Python for backend logic and integrates network visualization tools to display router connectivity and topology structure.
Although implemented as a demo application, the project serves as a proof of concept for a scalable SDN-based network management system capable of automating multi-router configuration in real-world deployments.

## Technologies Used
- Python
- OpenDaylight
- NETCONF/YANG
- Electron.js (if applicable)
- GNS3 / VyOS

## Project Limitations and Demo Application Justification
**Incomplete Full Implementation
The original goal of this project was to develop a fully functional multi-router configuration application using OpenDaylight (ODL) as the SDN controller and NETCONF/YANG for real-time router configuration. However, the full implementation could not be completed within the available project timeframe due to the following technical constraints:
Complexity of OpenDaylight setup and stability:
OpenDaylight requires precise configuration of services, features, and YANG models. During development, the controller experienced stability issues, including delayed responses and inconsistent NETCONF session handling.

**NETCONF integration challenges:
Establishing and maintaining reliable NETCONF connections between OpenDaylight and multiple virtual routers proved difficult. Some routers intermittently failed to respond to configuration RPCs, which affected automation consistency.

**Time constraints:
Significant time was spent troubleshooting controller–router communication rather than implementing higher-level application features such as dynamic topology updates, advanced routing protocol configuration, and full CRUD operations.

***Demo Application Decision
Due to the challenges above, the project was scaled down to a demo application to ensure the core concept and technical understanding were still clearly demonstrated. The demo application focuses on:
Demonstrating NETCONF-based communication logic
Visualizing a static network topology
Providing a GUI-based interface for router selection and basic configuration simulation
Showing how OpenDaylight would be used in a production-ready system
This approach allowed the project to remain aligned with its original objectives while ensuring a working, testable, and presentable solution.

***Educational Value
Despite being a demo, the application successfully demonstrates:
Understanding of Software Defined Networking (SDN)
Practical use of NETCONF/YANG concepts
Integration of Python backend logic with a GUI frontend
Network automation design principles
The demo application therefore serves as a proof of concept for a larger, fully deployable system that can be completed with additional time and resources.


## Application Screenshots



