<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="22308000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="ex1_call_collect.vi" Type="VI" URL="../ex1_call_collect.vi"/>
		<Item Name="ex2_producer.vi" Type="VI" URL="../ex2_producer.vi"/>
		<Item Name="ex2_consumer.vi" Type="VI" URL="../ex2_consumer.vi"/>
		<Item Name="ex3_producer_consumer.vi" Type="VI" URL="../ex3_producer_consumer.vi"/>
		<Item Name="py_msg.ctl" Type="VI" URL="../py_msg.ctl"/>
		<Item Name="pythonq.lvlib" Type="Library" URL="../pylabview/pythonq.lvlib"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Application Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Application Directory.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
			</Item>
			<Item Name="PythonVersionsEnum.ctl" Type="VI" URL="/C/Program Files (x86)/National Instruments/LabVIEW 2022/examples/Connectivity/Python/support/PythonVersionsEnum.ctl"/>
			<Item Name="ToPythonVersionString.vi" Type="VI" URL="/C/Program Files (x86)/National Instruments/LabVIEW 2022/examples/Connectivity/Python/support/ToPythonVersionString.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
