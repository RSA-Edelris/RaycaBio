
# ── Segment the SSE trace ─────────────────────────────────────────────────────
def make_segments(res_ids, sse, px, py, depth):
    """Return list of dicts: {type, indices, px, py, depth_mean}"""
    segs = []
    i = 0
    n = len(sse)
    while i < n:
        t = sse[i]
        j = i
        while j < n and sse[j] == t:
            j += 1
        idx = list(range(i, j))
        segs.append(dict(type=t, idx=idx,
                         px=px[idx], py=py[idx],
                         depth=depth[idx].mean()))
        i = j
    return segs

segments = make_segments(res_ids, sse, px, py, depth)
print(f"Total segments: {len(segments)}")
print("Type distribution:", {t: sum(1 for s in segments if s['type']==t)
                              for t in 'abc'})
