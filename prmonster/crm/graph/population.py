from seaborn import lineplot
import matplotlib.pyplot as plt
from prmonster.crm import repos_over_days, Connection

OUTPUT_FILE = 'data/repos_over_days.png'
CONN = Connection()

def plot_repos_over_days():
    data = repos_over_days()

    x, y = zip(*data)
    lineplot(x=x, y=y)
    plt.savefig(OUTPUT_FILE)

if __name__ == '__main__':
    # result = CONN.execute("ALTER TABLE repos ADD COLUMN created TIMESTAMP")
    plot_repos_over_days()
