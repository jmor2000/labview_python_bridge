# labview_python_bridge
Connects labview with python applications asynchronously via multi-processing data queues.

![alt text](docs/images/banner.png)

## How does it work?
### Code basic
This code utlises to native libraries in python and labview to provide bi-directional data communication.
- Python - native [multiprocessing library](https://docs.python.org/3/library/multiprocessing.html)
- Labview - native [python functions](https://www.ni.com/docs/en-US/bundle/labview-api-ref/page/menus/categories/computer/python-node-mnu.html)

The 'Your-Python-App' deploys a 'Global Queue Service' to run in parrallel to itself on startup.
This 'Global Queue Service' hosts two data queues (In & Out) which can be accessed using the python "Lbv_Global_Que" class
'Your-Labview-App' connects to the 'Global Queue Service' and accesses the data queses by creating and interactive with "Lbv_Global_Que" class object.

![alt text](docs/images/diagram_code_basic.png)



## Requirements
Labview

[LabVIEW and Python Compatibility](https://www.ni.com/en/support/documentation/supplemental/18/installing-python-for-calling-python-code.html)


Python


> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.
