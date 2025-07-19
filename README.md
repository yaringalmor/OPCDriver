# OPC UA Driver

A Python-based OPC UA client for connecting to Siemens WinCC Panel RT servers and managing variables.

## 🚀 **Features**

- ✅ **OPC UA Client** - Connect to Siemens WinCC Panel RT servers
- ✅ **Variable Management** - Read, write, and export variables
- ✅ **Context Manager** - Automatic connection cleanup
- ✅ **JSON Export/Import** - Save and load variable configurations
- ✅ **Random Value Generation** - Test with randomized variable values
- ✅ **Command Line Interface** - Easy to use CLI with arguments

## 📋 **Prerequisites**

```bash
pip install opcua
```

## 🔧 **Installation**

1. **Clone or download the script**
2. **Install dependencies:**
   ```bash
   pip install opcua
   ```

## 📖 **Usage**

### **Command Line Interface**

#### **Basic Connection:**
```bash
python opcdriver.py --server_address localhost --server_port 4870
```

#### **Custom Server Configuration:**
```bash
python opcdriver.py --server_address 192.168.1.100 --server_port 4840 --objects_node_name "Custom Panel"
```

#### **Available Arguments:**
- `--server_address`: OPC server address (default: localhost)
- `--server_port`: OPC server port (default: 4870)
- `--protocol`: OPC protocol (default: opc.tcp)
- `--objects_node_name`: OPC objects node name (default: WinCC Panel RT)

### **Programmatic Usage**

```python
from opcdriver import OCUDriver

# Using context manager (recommended)
with OCUDriver("opc.tcp://localhost:4870", "WinCC Panel RT") as driver:
    # Get all variables
    variables = driver.get_variables()
    print(f"Found {len(variables)} variables")
    
    # Export variables to JSON
    driver.export_variables("variables.json")
    
    # Load variables from JSON
    driver.load_variables("variables.json")
```

## 🔍 **Core Functionality**

### **OCUDriver Class**

#### **Initialization:**
```python
driver = OCUDriver(server_url, objects_node_name='WinCC Panel RT')
```

#### **Context Manager:**
```python
with OCUDriver(server_url, objects_node_name) as driver:
    # Your code here
    # Automatically disconnects when exiting
```

#### **Methods:**

| Method | Description | Usage |
|--------|-------------|-------|
| `get_variables()` | Get all variables from server | `variables = driver.get_variables()` |
| `export_variables(path)` | Export variables to JSON file | `driver.export_variables("vars.json")` |
| `load_variables(path)` | Load variables from JSON file | `driver.load_variables("vars.json")` |
| `disconnect()` | Manually disconnect | `driver.disconnect()` |

### **Random Value Generation**

The script includes a `random_values()` function that:
- Copies the original JSON file to `tnuva_copy.json`
- Randomly adjusts numeric values by ±10
- Toggles boolean values randomly
- Excludes diagnostic and system variables

## 📊 **Variable Structure**

Variables are represented as dictionaries:
```json
{
    "name": "VariableName",
    "node_id": "ns=1;i=123",
    "value": 42.5
}
```

## 🔧 **Configuration**

### **Server Configuration:**
- **Default Protocol:** `opc.tcp`
- **Default Port:** `4870`
- **Default Objects Node:** `WinCC Panel RT`
- **Variable Path:** `WinCC Panel RT/Tags`

### **Excluded Variables:**
The following variables are automatically excluded from operations:
- `@DiagnosticsIndicatorTag`
- `Tag_ScreenNumber`

## 📁 **File Structure**

```
opc/
├── opcdriver.py          # Main OPC driver script
├── README.md             # This documentation
├── tnuva.json           # Exported variables (generated)
└── tnuva_copy.json      # Modified variables (generated)
```

## 🛠️ **Examples**

### **Example 1: Basic Variable Export**
```bash
python opcdriver.py --server_address localhost --server_port 4870
```

**Output:**
```json
[
    {
        "name": "Temperature",
        "node_id": "ns=1;i=123",
        "value": 23.5
    },
    {
        "name": "Pressure",
        "node_id": "ns=1;i=124",
        "value": 101.3
    }
]
```

### **Example 2: Custom Server Configuration**
```bash
python opcdriver.py --server_address 192.168.1.100 --server_port 4840 --objects_node_name "Production Panel"
```

### **Example 3: Programmatic Usage**
```python
from opcdriver import OCUDriver

# Connect and export variables
with OCUDriver("opc.tcp://localhost:4870") as driver:
    variables = driver.get_variables()
    driver.export_variables("my_variables.json")
    
    # Load and modify variables
    driver.load_variables("modified_variables.json")
```

## 🔒 **Security Considerations**

### **Authentication:**
- Currently supports unsecured connections
- For production, implement proper authentication
- Consider using certificates for enhanced security

### **Network Security:**
- Ensure OPC UA server is properly configured
- Use firewalls to restrict access
- Monitor network traffic

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **Connection Failed:**
   ```
   Error: Error connecting to the server: [Errno 111] Connection refused
   Solution: Check server address, port, and ensure OPC UA server is running
   ```

2. **Authentication Failed:**
   ```
   Error: Access denied
   Solution: Check server credentials and permissions
   ```

3. **Variable Not Found:**
   ```
   Error: Node not found
   Solution: Verify objects_node_name and variable paths
   ```

### **Diagnostic Commands:**
```bash
# Test network connectivity
ping <server_address>

# Test port connectivity
telnet <server_address> <server_port>

# Check if OPC UA server is running
nmap -p <server_port> <server_address>
```

## 📊 **Output Examples**

### **Variable Export:**
```json
[
    {
        "name": "SystemStatus",
        "node_id": "ns=1;i=85",
        "value": "Running"
    },
    {
        "name": "Temperature",
        "node_id": "ns=1;i=123",
        "value": 23.5
    },
    {
        "name": "Pressure",
        "node_id": "ns=1;i=124",
        "value": 101.3
    }
]
```

### **Random Value Generation:**
```json
[
    {
        "name": "Temperature",
        "value": 28.7
    },
    {
        "name": "Pressure",
        "value": 95.2
    },
    {
        "name": "Status",
        "value": false
    }
]
```

## 🔗 **Integration Examples**

### **Python Script Integration:**
```python
from opcdriver import OCUDriver
import json

def monitor_variables(server_url, objects_node_name):
    with OCUDriver(server_url, objects_node_name) as driver:
        variables = driver.get_variables()
        
        for var in variables:
            print(f"{var['name']}: {var['value']}")
        
        return variables

# Usage
variables = monitor_variables("opc.tcp://localhost:4870", "WinCC Panel RT")
```

### **Batch Processing:**
```python
from opcdriver import OCUDriver
import time

def continuous_monitoring(server_url, interval=5):
    while True:
        try:
            with OCUDriver(server_url) as driver:
                variables = driver.get_variables()
                print(f"Timestamp: {time.time()}")
                for var in variables:
                    print(f"  {var['name']}: {var['value']}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)
```

## 📚 **Additional Resources**

- [OPC UA Foundation](https://opcfoundation.org/)
- [Siemens WinCC Documentation](https://support.industry.siemens.com/)
- [asyncua Documentation](https://asyncua.readthedocs.io/)

## 🤝 **Support**

For issues and questions:
1. Check the troubleshooting section
2. Verify server connectivity
3. Test with different server configurations
4. Check OPC UA server logs

## 📄 **License**

This project is provided as-is for educational and development purposes.

## 🔄 **Version History**

- **v1.0**: Initial implementation with basic OPC UA client
- **v1.1**: Added context manager for automatic cleanup
- **v1.2**: Added random value generation for testing
- **v1.3**: Improved error handling and documentation 