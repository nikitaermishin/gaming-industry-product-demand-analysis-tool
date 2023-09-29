import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime

def PrepareResults(google_result, yandex_result, steam_result, app_name):
    start_date = yandex_result['start_date'].min()

    max_value = max(max(yandex_result['absolute_pop']), max(steam_result['Players']))

    google_res = google_result[app_name].reset_index()
    google_res = google_res[google_res['date'] >= start_date]
    
    google_res[app_name] = google_res[app_name].apply(lambda x: x * max_value / max(google_res[app_name]))

    steam_res = steam_result[steam_result['DateTime'] >= start_date.strftime('%Y-%m-%d')].iloc[::7, :]

    return (google_res, yandex_result, steam_res, app_name)

def PlotGoogleResult(google_trends_result):
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    def to_date(timestamp):
        return timestamp.strftime("%Y-%m-%d")

    fig, ax = plt.subplots(1,1)
    num=0
    for column in google_trends_result.reset_index().drop('date', axis=1):
        num+=1
        ax.plot(google_trends_result.reset_index()['date'].apply(to_date), google_trends_result[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=15))
    plt.xticks(rotation=60)
    plt.legend(loc=0, ncol=2)
    
    plt.title("Application popularity comparison via Google Trends", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel("Time")
    plt.ylabel("Relative popularity")
    plt.show()

def PlotYandexResult(app1_result, app2_result, app3_result, labels):
    def to_date(timestamp):
        return timestamp.strftime("%Y-%m-%d")

    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    fig, ax = plt.subplots(1,1)
    ax.plot(app1_result['start_date'].apply(to_date), app1_result['absolute_pop'], marker='', color=palette(1), linewidth=1, alpha=0.9, label=labels[0])
    ax.plot(app2_result['start_date'].apply(to_date), app2_result['absolute_pop'], marker='', color=palette(2), linewidth=1, alpha=0.9, label=labels[1])
    ax.plot(app3_result['start_date'].apply(to_date), app3_result['absolute_pop'], marker='', color=palette(3), linewidth=1, alpha=0.9, label=labels[2])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    plt.xticks(rotation=60)

    plt.yscale("log")
    plt.legend(loc=0, ncol=1)
    
    plt.title("Application popularity comparison via Yandex Wordstat", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel("Time")
    plt.ylabel("Absolute popularity")
    plt.show()

def PlotSteamResult(app1_result, app2_result, app3_result, labels, start_date='2019-01-01', freq=7):
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    def truncate(str):
        return str[:10]

    app1_data = app1_result[app1_result['DateTime'] > start_date].iloc[::freq, :]
    app2_data = app2_result[app2_result['DateTime'] > start_date].iloc[::freq, :]
    app3_data = app3_result[app3_result['DateTime'] > start_date].iloc[::freq, :]

    fig, ax = plt.subplots(1,1)
    ax.plot(app1_data['DateTime'].apply(truncate), app1_data['Players'], marker='', color=palette(1), linewidth=1, alpha=0.9, label=labels[0])
    ax.plot(app2_data['DateTime'].apply(truncate), app2_data['Players'], marker='', color=palette(2), linewidth=1, alpha=0.9, label=labels[1])
    ax.plot(app3_data['DateTime'].apply(truncate), app3_data['Players'], marker='', color=palette(3), linewidth=1, alpha=0.9, label=labels[2])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=15))
    plt.xticks(rotation=60)

    plt.legend(loc=0, ncol=2)
    
    plt.title("Application popularity comparison via SteamDB", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel("Time")
    plt.ylabel("Users count")
    plt.show()

def PlotAppPop(google_app_result, yandex_app_result, steam_app_result, app_name):
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set2')

    fig, ax = plt.subplots(1,1)
    ax.plot(google_app_result['date'], google_app_result[app_name], marker='', color=palette(1), linewidth=1, alpha=0.9, label='Google Trends')
    ax.plot(yandex_app_result['start_date'], yandex_app_result['absolute_pop'], marker='', color=palette(2), linewidth=1, alpha=0.9, label='Yandex Wordstat')
    ax.plot(steam_app_result['DateTime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')), steam_app_result['Players'], marker='', color=palette(3), linewidth=1, alpha=0.9, label='Steam Users')

    labels = [item.strftime("%Y-%m-%d") for item in google_app_result['date']]
    ax.set_xticklabels(labels)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    plt.xticks(rotation=60)

    plt.legend(loc=0, ncol=1)
    
    plt.title(f"Popularity comparison for {app_name}", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel("Time")
    plt.ylabel("Popularity")
    plt.show()