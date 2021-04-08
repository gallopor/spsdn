import os, sys, time
import pandas as pd
import traceback
from cntmap import TRAFFIC_COUNTER, PORT_COUNTER_MAP


class TestCenter():

    def __init__(self, insdir, licsvr=None):
        '''
        Load STC Native API
        '''
        os.environ['STC_PRIVATE_INSTALL_DIR'] = insdir
        # Add STC Python library to the system path
        sys.path.append(os.path.join(insdir, 'API', 'Python'))

        from StcPython import StcPython
        try:
            self.hStc = StcPython()
            self.hStc.config('AutomationOptions', LogLevel="ERROR")
            # Setup license server
            if licsvr is not None:
                licmgr = self.hStc.get('system1', 'children-licenseservermanager')
                self.hStc.create('LicenseServer', under=licmgr, server=licsvr)
        except:
            raise BaseException('Failed to load STC library.')

    def cfgLoad(self, cfgfile, offline=False):
        '''
        Load STC XML Configuration file
        '''
        try:
            self.hStc.perform('LoadFromXml', filename=cfgfile)
            self.hPorts = self.hStc.get('project1', 'children-port').split()
            if not offline:
                self.hStc.perform('AttachPorts', AutoConnect='True', PortList=self.hPorts)

            self.hDevices = self.hStc.get('project1', 'children-emulateddevice').split()
            self.hStreams = dict()
            for hp in self.hPorts:
                self.hStreams[hp] = self.hStc.get(hp, 'children-streamblock').split()
            
            self.dsGenerator = self.hStc.subscribe(Parent='Project1', ConfigType='Generator', ResultType='GeneratorPortResults')
            self.dsAnalyzer = self.hStc.subscribe(Parent='Project1', ConfigType='Analyzer', ResultType='AnalyzerPortResults')

            self.dsPceLsp = self.hStc.subscribe(Parent='Project1', ConfigType='PceLspConfig', ResultType='PcepLspResults')
        except:
            raise BaseException('Failed to load STC configuration file.')

    def getObjs(self, type, obj_name='*'):
        dict={}
        dict['ObjectList']=''
        ret=self.__hStc.perform('GetObjects', classname=type)
        #print ret
        dict.update(ret)
        if name=='*':
            return dict['ObjectList'].split()

        retList=[]	
        for object in dict['ObjectList'].split():
            name1=stc.get(object,'name').upper().strip()
            print('name=<%s> name1=<%s> ' %(name,name1))
            if name.upper().strip()==name1:
                retList.append(object)	
        return retList	

    def deviceStart(self, names=None):
        ''' Start Devices '''
        try:
            hdevs = self.hStc.get('project1', 'children-emulateddevice').split()
            if names is None:
                self.hStc.perform('deviceStart', DeviceList=hdevs)
                print('stc.perform deviceStart ALL')
            else:
                hdev_selected = list()
                for hd in hdevs:
                    dn = self.hStc.get(hd, 'name').lower()
                    if dn in [n.lower() for n in names if isinstance(n, str)]:
                        hdev_selected.append(hd)
                if len(hdev_selected):
                    self.hStc.perform('deviceStart', DeviceList=hdev_selected)
                    print('stc.perform deviceStart DeviceList=%s' % hdev_selected)
                else:
                    raise BaseException('No device found with the names(%s)' % names)
        except:
            errMsg = traceback.format_exc()
            raise BaseException(errMsg)

    def deviceStop(self, names=None):
        ''' Stop Devices '''
        try:
            hdevs = self.hStc.get('project1', 'children-emulateddevice').split()
            if names is None:
                self.hStc.perform('deviceStop', DeviceList=hdevs)
                print('stc.perform deviceStop ALL')
            else:
                hdev_selected = list()
                for hd in hdevs:
                    dn = self.hStc.get(hd, 'name').lower()
                    if dn in [n.lower() for n in names if isinstance(n, str)]:
                        hdev_selected.append(hd)
                if len(hdev_selected):
                    self.hStc.perform('deviceStop', DeviceList=hdev_selected)
                    print('stc.perform deviceStop DeviceList=%s' % hdev_selected)
                else:
                    raise BaseException('No device found with the names(%s)' % names)
        except:
            errMsg = traceback.format_exc()
            raise BaseException(errMsg)

    def trafficStart(self, names=None):
        ''' Start Traffic '''
        try:
            hstream_selected = list()
            for hp in self.hStreams.keys():
                if names is None:
                    hstream_selected.extend(self.hStreams[hp])
                else:
                    for hs in self.hStreams[hp]:
                        sn = self.hStc.get(hs, 'name').lower()
                        if sn in names:
                            hstream_selected.extend(hs)
            if len(hstream_selected):
                print('stc.perform StreamBlockStart StreamBlockList=%s' % hstream_selected)
                self.hStc.perform('StreamBlockStart', StreamBlockList=hstream_selected)
            else:
                print('No streamblock found')
                raise BaseException('No streamblock found with the names(%s)' % names)
        except:
            errMsg = traceback.format_exc()
            raise BaseException(errMsg)

    def trafficStop(self, names=None):
        ''' Stop Traffic '''
        try:
            hstream_selected = list()
            for hp in self.hStreams.keys():
                if names is None:
                    hstream_selected.append(self.hStreams[hp])
                else:
                    for hs in self.hStreams[hp]:
                        sn = self.hStc.get(hs, 'name').lower()
                        if sn in names:
                            hstream_selected = hstream_selected + hs
            if len(hstream_selected):
                self.hStc.perform('StreamBlockStop', StreamBlockList=hstream_selected)
                print('stc.perform StreamBlockStop StreamBlockList=%s' % hstream_selected)
            else:
                raise BaseException('No streamblock found with the names(%s)' % names)
        except:
            errMsg = traceback.format_exc()
            raise BaseException(errMsg)

    def getResults(self, output=True):
        rst = dict()
        for hp in self.hPorts:
            anaRst = self.hStc.get('%s.Analyzer.AnalyzerPortResults' % hp)
            # anaRst = self.hStc.get(hAnalyzerRst)

            hGen = self.hStc.get(hp, 'Children-Generator')
            hGenRst = self.hStc.get(hGen, 'Children-GeneratorPortResults')
            genRst = self.hStc.get(hGenRst)

            stat = dict()
            for counter in TRAFFIC_COUNTER:
                lc = counter.lower()
                if lc.startswith('tx'):
                    stat[counter] = genRst[PORT_COUNTER_MAP[lc]]
                elif lc.startswith('rx'):
                    stat[counter] = anaRst[PORT_COUNTER_MAP[lc]]
                else:
                    pass
            rst[hp] = stat

        if output:
            df_rst = pd.DataFrame.from_dict(rst, orient='index', columns=TRAFFIC_COUNTER)
            print(df_rst)
        return rst

    def ClearTrafficStats(self):
        '''
        清除流量统计计数

        '''
        try:
            print('+++++Enter ClearTrafficStats+++++') 
            stc=self.__hStc
            portList=[]
            for port in stc.get('project1','children-port').split():
                portList.append(port)
            print("stc.perform('ResultsClearAll',PortList=%s,ExecuteSynchronous='True')" %portList)
            stc.perform('ResultsClearAll',PortList=portList,ExecuteSynchronous='True')
            print('-----Exit ClearTrafficStats-----')
        except:
            errMsg=traceback.format_exc()
            raise BaseException(errMsg)

    def cleanup(self):
        self.hStc.perform("ChassisDisconnectAll")
        self.hStc.perform("ResetConfigCommand")

    def captureStart(self):
        pass

    def captureStop(self):
        pass


if __name__ == "__main__":
    stc_install_dir = 'C:/Program Files/Spirent Communications/Spirent TestCenter 5.09/Spirent TestCenter Application'
    stc = TestCenter(insdir=stc_install_dir, licsvr='10.61.43.250')
    stc.cfgLoad(cfgfile='./conf/basic_traffic.xml')

    stc.trafficStart()
    time.sleep(5)
    stc.trafficStop()

    analyzer = stc.hStc.get('port1', 'children-analyzer')
    ret = stc.hStc.get(analyzer)
    print(ret)
