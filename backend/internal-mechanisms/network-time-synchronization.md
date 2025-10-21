---
description: >-
  This page explains how the Demos network leverages NTP efficiently to sync the
  timestamp across the network.
icon: watch
---

# Network Time Synchronization

As Demos network is strongly based on correct communication between nodes, the protocol's way to synchronize timestamps and to have a reliable network timestamp is crucial. The `calibrateTime.ts` library provides essential functionality for time synchronization and correction in the Demos network. Here's an overview of its key components and functions:

### NTP Server Configuration

The library defines a primary NTP (Network Time Protocol) server and a list of fallback servers to ensure reliable time synchronization.

### Time Calibration:

The main function getTimestampCorrection() calculates the time difference between the local system and the NTP server, storing this correction in shared state.

### Network Timestamp Retrieval

The getNetworkTimestamp() function provides a corrected network timestamp by applying the stored correction to the current local time.

### Time Delta Calculation

The getMeasuredTimeDelta() function performs the actual time synchronization by:

* Fetching the NTP time
* Calculating the round-trip time
* Adjusting for network latency
* Computing the difference between the adjusted NTP time and local time

### NTP Time Fetching

The library includes functions to fetch time from the primary NTP server (getNtpTime()) and fallback servers (getFallbackNtpTime()) if the primary server fails.

### Example



### Summary

This library ensures that all nodes in the Demos network can maintain synchronized time, which is critical for proper communication and consensus mechanisms. By using NTP servers and accounting for network latency, it provides a robust solution for time synchronization across the distributed network.

