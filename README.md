<h1 align="center"><img src="./data/icons/PERTMaker.svg" width="32" align="center" /> PERT Maker: Build PERT Charts with Ease</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-blue" />
  </a>
  <a href="https://doc.qt.io/qtforpython/index.html">
    <img alt="PySide 6" src="https://img.shields.io/badge/PySide-6.4.1-brightgreen" />
  </a>
  <a href="https://github.com/Synell/PERT-Maker/blob/master/LICENSE">
    <img alt="License: LGPL" src="https://img.shields.io/badge/License-LGPL-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows" src="https://img.shields.io/badge/Platforms-Windows-yellow" />
</p>

----------------------------------------------------------------------

PERT Maker is a simple tool to create <a href="https://en.wikipedia.org/wiki/Program_evaluation_and_review_technique">PERT charts</a>. It is written in Python and uses the PySide framework.


## Requirements

### Windows

- Windows 7 or later
- VC++ 2015 Redistributable


### Source Code
- Python 3.11 or later
  - Dependencies (use `pip install -r requirements.txt` in the project root folder to install them)


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

### Creating a PERT Chart

By default, a new PERT chart is created when you start the app. You can create a new PERT chart by clicking on the "New" button in the "File" toolbar.

<img alt="Default interface when opening the app" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/interface.png" />

To start making a PERT chart, you need to add some nodes. You can add a node by right-clicking on the canvas. There, you can edit the properties of the node in the "Properties" tab.

<img alt="Creating a node" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/create_node.png" />

To select a node, you can left-click on it. To delete a node, you need to select it and press the "Delete" key on your keyboard.

*Nodes can be moved by left-clicking on them and dragging them to the desired position.*

<br/>

To connect two nodes, you need to select the first node and then right-click on the second node. There, you can edit the properties of the connection in the "Properties" tab.

*You can link existing nodes by right-clicking on an existing node as you second node.*

<img alt="Connect a node" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/connect_node.png" />

<br/>

Nodes have properties that can be edited in the "Properties" tab. You can edit the properties of a node by selecting it. You can edit the display name, the minimum time to do the task and the maximum time to do the task.

<img alt="Node properties" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/node_properties.png" />

If the node is pointing to another node, you can edit the display name of the connection and the time to do the task.

<br/>

Let's say you have this PERT chart:

<img alt="PERT chart example" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/example.svg" />

Let's focus on the "Generation" tab:

<img alt="Generation tab" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/generation_view.png" />

You can see that we have 3 buttons.

*Note that each toggle switch next to a button has the function to, when activated, enable or disable the live refresh of the corresponding button so you don't have to manually press the button. It can be useful if you want to see the result of a change in real time but it can quickly take a lot of resources if you have a lot of nodes.*

#### Refresh Connection View

Before clicking on the "Refresh Connection View" button, the connections are not displayed in the "Connection View" tab.

<img alt="Refresh connection view tab" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/connection_view.png" />

After clicking on the "Refresh Connection View" button, the connections are displayed as a table in the "Connection View" tab.

<img alt="Refresh connection view tab with values" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/connection_view_full.png" />

#### Generate Min and Max Times

Before clicking on the "Generate Min and Max Times" button, the minimum and maximum times are not set on our PERT chart. You could set them manually, but it's a lot of work. So, we can use the "Generate Min and Max Times" button to automatically set the minimum and maximum times.

<img alt="PERT charts with min and max values" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/example_min_max.svg" />

After clicking on the "Generate Min and Max Times" button, the minimum and maximum times are set on our PERT chart.

#### Generate Critical Path

Before clicking on the "Generate Critical Path" button, the critical path is not displayed in the "Critical Path" tab.

<img alt="Generate critical path tab" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/critical_path_view.png" />

After clicking on the "Generate Critical Path" button, the critical path is displayed as a table in the "Critical Path" tab.

<img alt="Generate critical path tab with values" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/critical_path_view_full.png" />

<br/>

The last toggle switch, as its name suggests, allows you to use the node names instead of the node IDs in the "Connection View" and "Critical Path" tabs.

*Note that the chart will not look the same after checking this toggle switch.*

<img alt="PERT chart with node names instead of path names" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/example_node_names.svg" />

<br/>


### Exporting the PERT Chart

You can export the PERT chart as an image or as a vectorial image (SVG) by clicking on the "Export" button, then on the "Image" button, in the "File" tab.

<img alt="Export menu" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/export_image.png" />

There, you can choose the file location, the file name, the background color and the foreground color.

<img alt="Color picker menu" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/color_panel.png" />


### Generate a PERT Chart from a CSV file

You can generate a PERT chart from a CSV file by clicking on the "Import" button, then on the "Table" button, in the "File" tab.

<img alt="Generate a PERT chart from a table" src="https://raw.githubusercontent.com/Synell/Assets/main/PERTMaker/readme/import_table.png" />

There, you can choose the file to load or set manually the data.


### Exporting the PERT Chart as a CSV file

You can export the PERT chart as a CSV file by clicking on the "Export" button, then on the "Table" button, in the "File" tab.
