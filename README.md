# labview_python_bridge
Connects labview with python applications asynchronously via multi-processing data queues.

![alt text](docs/images/banner.png)

## How does it work?
### Code basic
This method utlises native libraries in python and labview to provide bi-directional data communication.
- Python - native [multiprocessing library](https://docs.python.org/3/library/multiprocessing.html)
- Labview - native [python functions](https://www.ni.com/docs/en-US/bundle/labview-api-ref/page/menus/categories/computer/python-node-mnu.html)

**Topology**
'Your-Python-App' 
- deploys a 'Global Queue Service' to run in parrallel to itself on startup.
- listens to the 'data in' queue for data to process, and sends data back via the 'data out' queue.

'Global Queue Service'
- hosts two data queues (In & Out) which can be accessed using the python "Lbv_Global_Que" class.
- requirements to connect are IP Address, Network Port, Password (Auth), defined in 'Your-Python-App'.

'Your-Labview-App'
- connects to the 'Global Queue Service' and accesses the data queses by creating and interactive with "Lbv_Global_Que" class object.
- sends data yo python via the 'data in' queue, and listens to the 'data out' queue for data sent back.

> [!NOTE]
> 'Global Queue Service' can be access via a local network, as such 'Your-Python-App' doesn't need to run on the same computer as your 'Your-Labview-App' if you don't want it to.

![alt text](docs/images/diagram_code_basic.png)

## Requirements
Labview

[LabVIEW and Python Compatibility](https://www.ni.com/en/support/documentation/supplemental/18/installing-python-for-calling-python-code.html)


Python


> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.
