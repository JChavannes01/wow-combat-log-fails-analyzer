from events import Event
from constants import EventTypes as types

class BaseAnalyser:

    def __init__(self):
        pass

    def parseEvents(self, events: [Event]):
        for event in events:
            self._parseEvent(event)

        self.onFinish()

    def _parseEvent(self, event: Event):
        if (event.EVENT_TYPE == types.SPELL_AURA_APPLIED):
            self.onSpellAuraApplied(event)
        elif (event.EVENT_TYPE == types.SPELL_AURA_REMOVED):
            self.onSpellAuraRemoved(event)
        elif (event.EVENT_TYPE == types.SPELL_AURA_APPLIED_DOSE):
            self.onSpellAuraAppliedDose(event)
        elif (event.EVENT_TYPE == types.SPELL_DAMAGE):
            self.onSpellDamage(event)
        elif (event.EVENT_TYPE == types.SWING_MISSED):
            self.onSwingMissed(event)
        elif (event.EVENT_TYPE == types.SWING_DAMAGE):
            self.onSwingDamage(event)

    def onFinish(self):
        pass

    def onSpellAuraApplied(self, event: Event):
        pass

    def onSpellAuraAppliedDose(self, event: Event):
        pass

    def onSpellAuraRemoved(self, event: Event):
        pass

    def onSpellDamage(self, event: Event):
        pass

    def onSwingDamage(self, event: Event):
        pass

    def onSwingMissed(self, event: Event):
        pass

    def getFails(self, *args, **kwargs):
        raise NotImplementedError('Method not implemented in subclass')

    def createLogHeader(self, minWidth, title, settings):
        maxContentWidth = len(title)
        for s in settings:
            maxContentWidth = max(maxContentWidth, len(s))

        # Compensate for padding
        width = max(minWidth, maxContentWidth+4)
        
        lines = []
        lines.append('-'*width + '\n')
        lines.append('|' + ' '*(width - 2) + '|\n')
        lines.append(f'| {title:{width-4}} |\n')
        lines.append('|' + ' '*(width - 2) + '|\n')
        lines.append('-'*width + '\n')

        for s in settings:
            lines.append(f'| {s:{width-4}} |\n')
        
        lines.append('-'*width + '\n')
        
        return lines


    