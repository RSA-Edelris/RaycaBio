
# Check structure of all_cpds
m0 = all_cpds[0]
print("Props on first mol:", list(m0.GetPropsAsDict().keys()))
print("Total all_cpds:", len(all_cpds))

# Identify actives vs designed by checking name or props
for m in all_cpds[:3]:
    print(m.GetProp('_Name'), m.GetPropsAsDict())
