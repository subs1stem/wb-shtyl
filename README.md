# wb-shtyl

Module for integrating the Shtyl UPS into the Wiren Board controller.

## 🛠 Installation

* **Step 1:** Clone the repository:

```bash
git clone https://github.com/subs1stem/wb-shtyl.git /opt/wb-shtyl
```

* **Step 2:** Run the installation script:

```bash
# Make the install.sh script executable
chmod +x /opt/wb-shtyl/install.sh

# Run the installation script
/opt/wb-shtyl/install.sh
```

* **Step 3:** Configure the .env file:

```bash
nano /opt/wb-shtyl/.env
```

* **Step 4:** Start service:

```bash
systemctl start wb-shtyl.service
```
