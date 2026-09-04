
# Find where output files are handled in dispatch source
idx = dsrc.find('output.json')
print(dsrc[max(0,idx-200):idx+1000])
