
# Find the SSH/docker run part of dispatch
idx = dsrc.find('docker run')
if idx < 0:
    idx = dsrc.find('_ssh(')
print(dsrc[max(0,idx-200):idx+2000])
