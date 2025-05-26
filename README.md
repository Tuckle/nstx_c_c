# 💳 Mini Payment-Link Challenge

Welcome 👋  
This repo contains a deliberately **buggy** in-memory implementation of a payment-link
service (`service.py`) plus a small test-suite (`tests`).  
**All tests are red on purpose.** Your task is to make them green without
changing the test-code.

---

## 📜 Background

A payment link can move through these states:

CREATED ──► PAID ──► REFUNDED

└────► EXPIRED (if TTL lapses before payment)