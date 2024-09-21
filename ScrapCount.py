from myModule import getScrapCount
search = ['Users data_pushed','profiles_pushed','UserTimeTaken','FollowingTimeTaken']
UserCount = getScrapCount(search)[0]
ProfileCount = getScrapCount(search)[1]
UserTimeTaken = getScrapCount(search)[2]
ProfileTimeTaken = getScrapCount(search)[3]

print(f'User DataPushed Count: {UserCount}')
print(f'Profiles Pushed Count: {ProfileCount}')

search = ['FollowingTimeTaken','UserTimeTaken']
scrapCount = getScrapCount(search, stats=True)
print(f'FollowingScriptTimeTaken: {UserTimeTaken}')
print(f'UserScriptTimeTaken: {ProfileTimeTaken}')
input('Press Enter to exit')