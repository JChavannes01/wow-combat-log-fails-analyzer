from .analyser_base import BaseAnalyser
from events import Event


class Explosion:
    def __init__(self, time):
        self.srcName = "Unknown"
        self.time = time

        self.targets = []
        self.numTargets = 0
        self.numKills = 0

    def addTarget(self, target, targetDied):
        self.numTargets += 1
        self.targets.append((target, targetDied))

        if targetDied:
            self.numKills += 1

    def pprint(self, indentLevel=0):
        lines = []
        indent = ' '*4
        lvl = indentLevel

        def addLine(line):
            lines.append(indent*lvl + line + '\n')

        addLine(f"Explosion from {self.srcName} at {self.time}:")
        lvl += 1
        addLine(f"Targets: {self.numTargets}, Kills: {self.numKills}")
        addLine('')
        tarTemplate = "{:12}  {:5}"
        addLine(tarTemplate.format('Target', "Died?"))
        addLine("-"*19)
        for t in self.targets:
            addLine(tarTemplate.format(t[0], ['No', 'Yes'][t[1]]))

        lines.append('\n')

        return lines


class LadyAnalyser(BaseAnalyser):
    FAIL_SPIRITS = 1

    def __init__(self):
        self.spirits_taken = dict()
        self.explosions = []
        self.currentExplosion = None
        self.explosionsPerPerson = dict()

    def _parseEvent(self, event: Event):
        # Save current explosion if needed.
        if (self.currentExplosion != None and event.time != self.currentExplosion.time):
            self.explosions.append(self.currentExplosion)
            self.currentExplosion = None

        super()._parseEvent(event)

    def onSpellDamage(self, event: Event):
        if (event.spellName == "Vengeful Blast" and event.tarIsPlayer):
            if self.currentExplosion is None:
                self.currentExplosion = Explosion(event.time)

            self.currentExplosion.addTarget(event.tarName, event.overkill > 0)

    def onSwingDamage(self, event: Event):
        if self.currentExplosion is None:
            self.currentExplosion = Explosion(event.time)
        if (event.srcName == "Vengeful Shade" and self.currentExplosion.time == event.time):
            self.currentExplosion.srcName = event.tarName

    def onSwingMissed(self, event: Event):
        if (event.srcName == "Vengeful Shade" and self.currentExplosion.time == event.time):
            self.currentExplosion.srcName = event.tarName

    def getFails(self, failType, minTargets=1, requireDeaths=False):
        if failType == LadyAnalyser.FAIL_SPIRITS:
            # Add lines with settings and get the explosion details.
            lines = []

            lines.append('-'*49 + '\n')
            lines.append('|' + ' '*47 + '|\n')
            lines.append('| List of spirits for the following settings    |\n')
            lines.append('|' + ' '*47 + '|\n')
            lines.append('-'*49 + '\n')
            lines.append(
                f'| Minimum number of targets: {minTargets:2}' + ' '*16 + ' |\n')
            lines.append(
                f'| Require deaths?: {("Yes" if requireDeaths else "No"):3}' + ' '*25 + ' |\n')
            lines.append('-'*49 + '\n')

            lines.append('\n')

            filtered_expl = self.getExplosionsFiltered(
                minTargets, requireDeaths)

            totals = dict()
            for e in filtered_expl:
                totals[e.srcName] = totals.get(e.srcName, 0) + 1

            totals_sorted = sorted(totals.items(), key=lambda t: t[1])

            lines.append("Spirits triggered per player:\n")
            for (name, num) in totals_sorted:
                lines.append(f"{name:12}: {num}\n")

            for expl in filtered_expl:
                lines.append('\n')
                lines.extend(expl.pprint())

            return lines
        else:
            raise ValueError(f"Unknown failtype: {failType}")

    def getExplosionsFiltered(self, minTargets, requireDeaths):
        def matches(expl: Explosion):
            if requireDeaths and (sum([t[1] for t in expl.targets]) == 0):
                return False
            return (expl.numTargets >= minTargets)

        return [e for e in self.explosions if matches(e)]
