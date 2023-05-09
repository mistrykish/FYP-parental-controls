import sqlite3
import matplotlib.pyplot as plt


def show_graphs():
    conn = sqlite3.connect(
        r'C:\Users\kisha\AppData\Local\Google\Chrome\User Data\Default\History')
    c = conn.cursor()

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Graph 1: Total visits per keyword
    keywords = ['youtube', 'google', 'stackoverflow']

    query = f"SELECT SUM(visit_count) as total_visits FROM urls WHERE visit_count > 0 AND (url LIKE ? OR title LIKE ?)"
    for _ in range(len(keywords) - 1):
        query += f" OR (url LIKE ? OR title LIKE ?)"

    c.execute(query, tuple(
        f'%{keyword}%' for keyword in keywords for _ in range(2)))

    total_visits = [row[0] for row in c.fetchall()]

    axs[0, 0].bar(keywords, total_visits)
    axs[0, 0].set_xlabel('Keywords')
    axs[0, 0].set_ylabel('Total Visits')
    axs[0, 0].set_title('Total visits per keyword')

    # Graph 2: Top 10 most visited sites
    c.execute(
        "SELECT url, visit_count FROM urls WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 10")
    rows = c.fetchall()
    urls = [row[0] for row in rows]
    visit_counts = [row[1] for row in rows]

    axs[0, 1].barh(urls, visit_counts)
    axs[0, 1].set_xlabel('Visit Count')
    axs[0, 1].set_ylabel('URLs')
    axs[0, 1].set_title('Top 10 most visited sites')

    # Graph 3: Visits per day of the week
    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']
    visits_per_day = []

    for i in range(1, 8):
        c.execute("SELECT COUNT(*) FROM urls WHERE visit_count > 0 AND strftime('%w', datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')) = ?", (str(i),))
        visits_per_day.append(c.fetchone()[0])

    axs[1, 0].bar(days, visits_per_day)
    axs[1, 0].set_xlabel('Day of the Week')
    axs[1, 0].set_ylabel('Total Visits')
    axs[1, 0].set_title('Visits per day of the week')

    # Remove the bottom right subplot
    axs[1, 1].axis('off')

    plt.tight_layout()
    plt.show()
