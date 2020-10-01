from events import Event
from constants import EventTypes as types

class BaseAnalyser:

    def __init__(self):
        pass

    def parseEvents(self, events: [Event]):
        for event in events:
            self._parseEvent(event)

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

    def createLogHeader(self, width, description, settings):
        #TODO: Create dynamic header implementation, see sindra analyser.
        raise NotImplementedError('Todo: Create the nice header')


    