<h1 align="center"><img src="./data/themes/logo.ico" width="32" align="center" /> PERT Maker: Build PERT Diagrams with Ease</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.10" src="https://img.shields.io/badge/Python-3.10-blue" />
  </a>
  <a href="https://www.qt.io/">
    <img alt="Qt 6" src="https://img.shields.io/badge/Qt-6.2.3-brightgreen" />
  </a>
  <a href="https://github.com/Synell/PERT-Maker/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows" src="https://img.shields.io/badge/Platforms-Windows-yellow" />
</p>

----------------------------------------------------------------------

PERT Maker is a simple tool to create PERT diagrams. It is written in Python and uses the Qt framework.


## Requirements

### Windows

- Windows 7 or later
- VC++ 2015 Redistributable


### Source Code
- Python 3.10 or later
  - PyQt6 (`pip install PyQt6`)
  - datetime (`pip install datetime`)
  - requests (`pip install requests`)


## Installation

### Windows

<a href="https://github.com/Synell/PERT-Maker/releases/latest">
  <img alt="Release: Latest" src="https://img.shields.io/badge/Release-Latest-00B4BE?style=for-the-badge" target="_blank" />
</a>

- Download the latest release from the [releases page](https://github.com/Synell/PERT-Maker/releases) and extract it to a folder of your choice.


## Customization

### Language

- You can customize the language of the app by adding a new file into the `/data/lang/` folder. The language must be a valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) code. If the language is not supported, the app will default to English. Then, you can change the language in the settings menu.

  *See [this file](https://github.com/Synell/PERT-Maker/blob/main/data/lang/english.json) for an example.*

### Theme

- You can customize the theme of the app by adding new files into the `/data/themes/` folder. The theme must be contain valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) codes and valid [QSS](https://doc.qt.io/qt-6/stylesheet-reference.html) codes. If the theme is not supported, the app will default to the default theme. Then, you can change the theme in the settings menu.

  *See [this file](https://github.com/Synell/PERT-Maker/blob/main/data/themes/neutron.json) and [this folder](https://github.com/Synell/PERT-Maker/tree/main/data/themes/neutron) for an example.*


## Usage

### Creating a PERT Diagram

By default, a new PERT diagram is created when you start the app. You can create a new PERT diagram by clicking on the "New" button in the "File" toolbar.

<img alt="Default interface when opening the app" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmQMNStpD5p4D6paAA3PhMt8rpJhkfRR5kZnXEArZSlxPP2k7UeXsRUl_FzH_pTHReMsRR3NHvZGSRwYxUuZl6LZAp0ufg" />

To start making a PERT diagram, you need to add some nodes. You can add a node by right-clicking on the canvas. There, you can edit the properties of the node in the "Properties" tab.

<img alt="Creating a node" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSC1LMO9GkXR2YNidRLwjNVZbEnkB5OGhSiNw3qk3UIAybniz-2JJCUyzJan8INZxb5n-ivIul_ybaYslIRMDggXkgJEQ" />

To select a node, you can left-click on it. To delete a node, you need to select it and press the "Delete" key on your keyboard.

*Nodes can be moved by left-clicking on them and dragging them to the desired position.*

<br/>

To connect two nodes, you need to select the first node and then right-click on the second node. There, you can edit the properties of the connection in the "Properties" tab.

*You can link existing nodes by right-clicking on an existing node as you second node.*

<img alt="Connect a node" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmQGYA_PMQ8YM-_V6scrlk2oo5Vc8TJV7H0P8wCkxUdMz76GJn1HqmTS354_XwzkiHD-_p-FAbXHv1HX9Wp8-gr3umatMw" />

<br/>

Nodes have properties that can be edited in the "Properties" tab. You can edit the properties of a node by selecting it. You can edit the display name, the minimum time to do the task and the maximum time to do the task.

<img alt="Node properties" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSoW1gZtZdPw7mvnEUgHxGFKMxI_zbYqPpFsU_CFesP79cDtn2ztmLJaA0uMz6pS2t3Vrk0OFc51SV7KL3QhIx4h-I1" />

If the node is pointing to another node, you can edit the display name of the connection and the time to do the task.

<br/>

Let's say you have this PERT diagram:

<img alt="Apps tab with an app installed" src="https://drive.google.com/u/0/uc?id=1KXyBOgzz5TLCnXRZ8BddpA8xLxbU9rCw" />

Let's focus on the "Generation" tab:

<img alt="Generation tab" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSYpOV0CqdvUHgCU5Q0gcAzMTLLlYqp3qXeZfIoMlAUKbvYU2nDEs2PCsrkN3g40CA5jrp3SRvTsow-XL10LohY-EV7jA" />

You can see that we have 3 buttons.

*Note that each toggle switch next to a button has the function to, when activated, enable or disable the live refresh of the corresponding button so you don't have to manually press the button. It can be useful if you want to see the result of a change in real time but it can quickly take a lot of resources if you have a lot of nodes.*

#### Refresh Connection View

Before clicking on the "Refresh Connection View" button, the connections are not displayed in the "Connection View" tab.

<img alt="Refresh connection view tab" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmRSToxp0BIP0gK5P91Wjsx8XV4oJZD5yvNkNFs0fR4JDzItSuytQcphmmlciguopHpmTL_ilpcLUTg3y5PKQkTSTbbu" />

After clicking on the "Refresh Connection View" button, the connections are displayed as a table in the "Connection View" tab.

<img alt="Refresh connection view tab with values" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSKyaHGRt20x-a89WQLi7TYpOa9UkiFkaLFGp2CTY9IQXbC26EArE0oKKIwq1WuEFLawP3QNv91R7tIHBUomgPT4FEIVg" />

#### Generate Min and Max Times

Before clicking on the "Generate Min and Max Times" button, the minimum and maximum times are not set on our PERT diagram. You could set them manually, but it's a lot of work. So, we can use the "Generate Min and Max Times" button to automatically set the minimum and maximum times.

<img alt="PERT diagrams with min and max values" src="https://drive.google.com/u/0/uc?id=1fFJ2zov3SUyBvWOtxU_UURi6x1wfcq_4" />

After clicking on the "Generate Min and Max Times" button, the minimum and maximum times are set on our PERT diagram.

#### Generate Critical Path

Before clicking on the "Generate Critical Path" button, the critical path is not displayed in the "Critical Path" tab.

<img alt="Generation critical path tab" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmTPpX8oNmwqy4p85AujQuzbuFqs87PFvwwXV21mmBxlrloM0Uc-pIognceHYX2swenMpYBHLHHwduH0Lf8HdkfkfkMu" />

After clicking on the "Generate Critical Path" button, the critical path is displayed as a table in the "Critical Path" tab.

<img alt="Generation critical path tab with values" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSQz4BcK0fP2GxW7bwlM7Ez2zuxFfkycILnbtN8gxk0lRrYMTGJ-L7-_pBK6PgBR37n0ELVypEZmOtVJfzRGBSaF-Yf" />

<br/>

The last toggle switch, as its name suggests, allows you to use the node names instead of the node IDs in the "Connection View" and "Critical Path" tabs.

*Note that the diagram will not look the same after checking this toggle switch.*

<img alt="PERT diagram with node names instead of path names" src="https://drive.google.com/u/0/uc?id=1qKbrbROttYOwRL-QzojXRzasmNixla9Y" />

<br/>


### Exporting the PERT diagram

You can export the PERT diagram as an image or as a vectorial image (SVG) by clicking on the "Export" button, then on the "Image" button, in the "File" tab.

<img alt="PERT diagram with node names instead of path names" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSJr_xhMwDgP4OYPkTERQg7LOsB2ZJE8MVEHU60bskFhCebgmfAUGM3YJEozjiql07hdyBcdTFSYZ1pEXbLWLy86VMG" />

There, you can choose the file location, the file name, the background color and the foreground color.

<img alt="PERT diagram with node names instead of path names" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmRMehVydSaZr-ifBg7KUQpJkQc36IBcszT_RnawKm1Rj6LuENXwSG6cHbE6wMYvZnmWVkqrFZv-xgDNt6c1VFHT5_3Azg" />


### Generate a PERT diagram from a CSV file

You can generate a PERT diagram from a CSV file by clicking on the "Import" button, then on the "Table" button, in the "File" tab.

<img alt="Generate a PERT diagram from a table" src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmTVOk_aMsZhr-IBaYhFvyAyYXPgRkYpOQs7pquMxZtlIuH6d1AQH6fKwkRDZUCGHgRMy6Fmjo_v5TFxjW_mHbPEywVt" />

There, you can choose the file to load or set manually the data.


### Exporting the PERT diagram as a CSV file

You can export the PERT diagram as a CSV file by clicking on the "Export" button, then on the "Table" button, in the "File" tab.
