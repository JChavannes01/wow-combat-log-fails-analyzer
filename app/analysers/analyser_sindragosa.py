from .analyser_base import BaseAnalyser
from events import Event


class Explosion:
    def __init__(self, srcName, stacks, time, timestamp):
        self.stacks = stacks
        self.srcName = srcName
        self.time = time
        self.ts = timestamp

        self.targets = []
        self.numTargets = 0
        self.numTargetsUM = 0
        self.numTargetsNoUM = 0
        self.numKills = 0

    def addTarget(self, target, targetDied, targetHasUM):
        self.numTargets += 1
        self.targets.append((target, targetDied, targetHasUM))

        if targetDied:
            self.numKills += 1

        if targetHasUM:
            self.numTargetsUM += 1
        else:
            self.numTargetsNoUM += 1

    def pprint(self, indentLevel=0):
        lines = []
        indent = ' '*4
        lvl = indentLevel

        def addLine(line):
            lines.append(indent*lvl + line + '\n')

        addLine(f"Explosion from {self.srcName} at {self.time}:")
        lvl += 1
        addLine(
            f"Stacks {self.stacks}, Targets: {self.numTargets}, Kills: {self.numKills}")
        addLine('')
        tarTemplate = "{:12}  {:5}  {}"
        addLine(tarTemplate.format('Target', "Died?", 'Had UM?'))
        addLine("-"*28)
        for t in self.targets:
            addLine(tarTemplate.format(
                t[0], ['No', 'Yes'][t[1]], 'Yes' if t[2] else 'No'))

        lines.append('\n')

        return lines


class SindragosaAnalyser(BaseAnalyser):
    FAIL_EXPLOSIONS = 1

    def __init__(self):
        self.UM_targets = dict()
        self.instability_stacks = dict()
        self.lastPlayerLosingStacks = ("", 0)  # player, stacks
        self.explosions = []
        self.currentExplosion = None

    def _parseEvent(self, event: Event):
        # Save current explosion if needed.
        if (self.currentExplosion != None and event.timestamp_millis > self.currentExplosion.ts+200):
            self.explosions.append(self.currentExplosion)
            self.currentExplosion = None

        super()._parseEvent(event)

    def onSpellAuraApplied(self, event: Event):
        if (event.spellName == 'Unchained Magic'):
            self.UM_targets[event.tarName] = event.timestamp_millis
        elif (event.spellName == 'Instability'):
            self.instability_stacks[event.tarName] = 1

    def onSpellAuraAppliedDose(self, event: Event):
        if (event.spellName == "Instability"):
            self.instability_stacks[event.tarName] += 1

    def onSpellAuraRemoved(self, event: Event):
        if (event.spellName == 'Unchained Magic' and event.tarName in self.UM_targets):
            del self.UM_targets[event.tarName]
        elif (event.spellName == 'Instability'):
            self.lastPlayerLosingStacks = (
                event.tarName, self.instability_stacks[event.tarName])
            self.instability_stacks[event.tarName] = 0
            if self.currentExplosion is not None:
                # A new person exploded during the small grace period, save the old explosion.
                self.explosions.append(self.currentExplosion)
                self.currentExplosion = None

    def onSpellDamage(self, event: Event):
        if (event.spellName == "Backlash" and event.tarIsPlayer):
            # Who exploded ??
            if self.currentExplosion == None:
                self.currentExplosion = Explosion(
                    *self.lastPlayerLosingStacks, event.time, event.timestamp_millis)

            target = event.tarName
            self.currentExplosion.addTarget(
                target, event.overkill > 0, target in self.UM_targets)

    def getFails(self, failType, minStacks=0, minTargets=1, requireDeaths=False, hideAllUM=False):
        if failType == SindragosaAnalyser.FAIL_EXPLOSIONS:
            # Add lines with settings and get the explosion details.
            lines = []

            # Add header with settings.
            lines.append('-'*49 + '\n')
            lines.append('|' + ' '*47 + '|\n')
            lines.append('| List of explosions for the following settings |\n')
            lines.append('|' + ' '*47 + '|\n')
            lines.append('-'*49 + '\n')
            lines.append(f'| Minimum Instability stacks: {minStacks:2}' + ' '*15 + ' |\n')
            lines.append(f'| Minimum number of targets: {minTargets:2}' + ' '*16 + ' |\n')
            lines.append(f'| Require deaths? {("Yes" if requireDeaths else "No"):3}' + ' '*26 + ' |\n')
            lines.append(f'| Hide UM only explosions? {("Yes" if hideAllUM else "No"):3}' + ' '*17 + ' |\n')
            lines.append('-'*49 + '\n')

            lines.append('\n')
            filtered_expl = self.getExplosionsFiltered(
                minStacks, minTargets, requireDeaths, hideAllUM)

            # Add player totals
            totals = dict()
            for e in filtered_expl:
                totals[e.srcName] = totals.get(e.srcName, 0) + 1

            totals_sorted = sorted(
                totals.items(), key=lambda t: t[1], reverse=True)

            lines.append("Instability explosions per player:\n")
            for (name, num) in totals_sorted:
                lines.append(f"{name:12}: {num}\n")

            # Add all the explosion details
            for expl in filtered_expl:
                lines.append('\n')
                lines.extend(expl.pprint())

            return lines
        else:
            raise ValueError(f"Unknown failtype: {failType}")

    def getExplosionsFiltered(self, minStacks, minTargets, requireDeaths, hideAllUM):
        def matches(expl: Explosion):
            if requireDeaths and (sum([t[1] for t in expl.targets]) == 0):
                return False
            if hideAllUM and expl.numTargetsNoUM == 0:
                return False
            return (expl.stacks >= minStacks) and (expl.numTargets >= minTargets)

        return [e for e in self.explosions if matches(e)]
