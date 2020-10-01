from events import Event
from analysers import SindragosaAnalyser, LadyAnalyser

INFILE = 'data/WoWCombatLog.txt'

OUTFILE_SINDRAGOSA = 'out/sindra_explosions.txt'
OUTFILE_LADY = 'out/lady_spirits.txt'


def read_log(fp):
    with open(fp, 'r') as f:
        events = [Event(line) for line in f.readlines()]

    return events


if __name__ == "__main__":
    events = read_log(INFILE)

    sind = SindragosaAnalyser()
    sind.parseEvents(events)

    outLines = sind.getFails(SindragosaAnalyser.FAIL_EXPLOSIONS,
                             minStacks=4,
                             minTargets=1,
                             requireDeaths=False,
                             hideAllUM=True)
    with open(OUTFILE_SINDRAGOSA, 'w') as out:
        out.writelines(outLines)

    print(f'Output written to "{OUTFILE_SINDRAGOSA}"')

    # LADY
    events = read_log('data/lady.txt')

    lady = LadyAnalyser()
    lady.parseEvents(events)

    outLines = lady.getFails(LadyAnalyser.FAIL_SPIRITS,
                             minTargets=1,
                             requireDeaths=False)

    with open(OUTFILE_LADY, 'w') as out:
        out.writelines(outLines)

    print(f'Output written to "{OUTFILE_LADY}"')
