
# Find returned_files population
idx = dsrc.find('returned_files')
print(dsrc[max(0,idx-500):idx+2000])
