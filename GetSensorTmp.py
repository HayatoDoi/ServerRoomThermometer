import os
class GetSensorTmp():
    def __init__(self, sensorID):
        self.sensorID = sensorID
        self.sensorFile = '/sys/bus/w1/devices/{0}/w1_slave'.format(self.sensorID)
        if os.path.isfile(self.sensorFile) == False :
            raise IOError('sensor is not found.')
    def get(self):
        with open(self.sensorFile, 'r') as sensorFile:
            sensorData = sensorFile.read()
        sensorDataSplit = sensorData.split('=')
        tmpStr = sensorDataSplit[-1].replace('\n','')

        if tmpStr == '85000':
            raise IOError('can not get sensor data.')
        tmp = round(float(tmpStr) / 1000, 2)
        return  '{0:.2f}'.format(tmp)
