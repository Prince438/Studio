import json, sys
t0, t1, fps, per = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 6
n = int(round((t1 - t0) * fps)) + 1
ts = [round(t0 + k / fps, 4) for k in range(n)]
pairs = [(ts[i], ts[i + 1] if i + 1 < len(ts) else None) for i in range(0, len(ts), 2)]
for i in range(0, len(pairs), per):
    acts = []
    for a, c in pairs[i:i + per]:
        acts.append({'name': 'javascript_tool', 'input': {'action': 'javascript_exec', 'text': f'await PAIR({a},{"null" if c is None else c})'}})
        acts.append({'name': 'computer', 'input': {'action': 'screenshot', 'scale': 0.1}})
        acts.append({'name': 'computer', 'input': {'action': 'screenshot', 'scale': 1}})
    print(json.dumps(acts)); print()
