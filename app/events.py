class Event:
    def __init__(self, line):
        (date_time, content) = line.strip().split('  ')
        (date, time) = date_time.split(' ')
        self.date = date
        self.time = time

        timeparts = time.split(':')
        self.timestamp_millis = int((int(timeparts[0])*3600 +
                          int(timeparts[1])*60 +
                          float(timeparts[2])) * 1000)
        self.values = content.split(',')
        
        # Base event values, shared by all events.
        self.EVENT_TYPE = self.values[0]
        self.srcGUID = self.values[1]
        self.srcName = self.values[2].strip('"')
        self.tarIsPlayer = self.values[3][-3] == '5'
        self.tarGUID = self.values[4]
        self.tarName = self.values[5].strip('"')
        self.tarIsPlayer = self.values[6][-3] == '5'

        # for isPlayer definition check unitFlags: https://wow.gamepedia.com/UnitFlag
        # Specific values as properties so that it doesn't crash when the values are absent

    
    @property
    def spellID(self):
        return int(self.values[7])


    @property
    def spellName(self):
        return self.values[8].strip('"')

    @property
    def amount(self):
        return int(self.values[10])


    @property
    def overkill(self):
        return int(self.values[11])
