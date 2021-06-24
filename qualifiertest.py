from qualifier import make_table

print(make_table([['James','Director'],['John','Composer']],['name','position'],False))
print(make_table([['James'],['John']],['name'],False))
print(make_table([['Lemon',183285,'Owner'],
                  ['Sabastiaan',183285.1,'Owner'],
                  ['KutieKatej',15000,'Admin'],
                  ['Jake','MoreThanU','Helper'],
                  ['Joe',-12,'Idk Tbh']],['User','Messages','role'],True))